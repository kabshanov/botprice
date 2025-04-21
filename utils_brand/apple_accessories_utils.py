# apple_accessories_utils.py

import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)

def find_best_apple_accessories_model(user_input: str) -> Optional[str] :
    """
    Ищет модель Apple accessories
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Apple Аксессуары", {})
    if not brand_data :
        logger.warning("[find_best_apple_accessories_model] Нет 'Apple accessories' в PRODUCT_LIBRARY.")
        return None

    user_input_lower = user_input.lower()
    found_entries = []  # Будем складывать (model_name, alias)

    # Идём по моделям:
    for model_name, model_info in brand_data.items() :
        aliases = model_info.get("aliases", [])
        for alias in aliases :
            # Regex по \balias\b (IGNORECASE),
            # alias_lower, user_input_lower
            alias_lower = alias.lower()
            pattern = re.compile(rf"\b{re.escape(alias_lower)}\b", re.IGNORECASE)
            if pattern.search(user_input_lower) :
                # Нашли совпадение
                logger.debug(
                    f"[find_best_apple_accessories_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_apple_accessories_model] Ничего не найдено среди Apple accessories-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_apple_accessories_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_apple_accessories_product(cleaned_line: str, model: str) -> dict:
    """
    Парсит дополнительные атрибуты
    для «Apple Аксессуары».

    dict
        Словарь извлечённых атрибутов.
        Если обнаружен специальный алиас, добавляется "final_product_name".
        Если атрибутов меньше заданного минимума и нет специального алиаса, возвращается пустой словарь {}.

    """

    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Apple Аксессуары", {})
    if model not in brand_data:
        logger.warning(f"[parse_apple_accessories_product] Модель '{model}' нет в Apple Аксессуары.")
        return {}

    attributes = brand_data[model]["attributes"]

    for attr_name, attr_info in attributes.items():
        attr_aliases = attr_info["aliases"]

        found_aliases = []
        for value, aliases in attr_aliases.items():
            # Сортируем алиасы по длине в порядке убывания
            sorted_aliases = sorted(aliases, key=len, reverse=True)
            for alias in sorted_aliases:
                pattern = re.compile(rf'\b{re.escape(alias)}\b', re.IGNORECASE)
                if pattern.search(cleaned_line):
                    found_aliases.append((alias, value))
                    # НЕ прерываемся: ищем вдруг более длинный.

        if found_aliases:
            # Выбираем алиас с наибольшей длиной
            best_alias, best_value = max(found_aliases, key=lambda x: len(x[0]))
            extracted_attributes[attr_name] = best_value
            logger.debug(
                f"[accessories parser] Для attr='{attr_name}' выбрали value='{best_value}' "
                f"(alias='{best_alias}', len={len(best_alias)})"
            )
        else:
            logger.debug(f"[accessories parser] Для attr='{attr_name}' ничего не найдено в строке.")

    # (НОВЫЙ БЛОК) Если "diagonal" есть, а iPad нет => искусственно добавляем iPad.
    if "diagonal" in extracted_attributes and "iPad" not in extracted_attributes:
        extracted_attributes["iPad"] = "iPad Pro"
        logger.debug(
            "[accessories parser] 'diagonal' обнаружен, но 'iPad' отсутствует => добавляем 'iPad Pro' автоматически."
        )


    logger.debug(f"[ipad parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_apple_accessories_product(
    line: str,
    cleaned_line: str,
    model: str,
    countries: list,
    price: int,
    supplier: str,
    comment: str,
    user_id: int
) -> bool:
    """
    «Склейка» итогового названия для Apple Аксессуары с учётом распознанных атрибутов
    и сохранение результата в USER_DATA.
    Возвращает True, если товар добавлен, иначе False (для обработки как простой).
    """
    from utils import add_or_update_product, apply_special_rules_iphone

    # 1. Парсим дополнительные атрибуты (diagonal, chip, RAM, SSD, color)
    extracted_attributes = parse_apple_accessories_product(cleaned_line, model)

    # 2. Проверяем, есть ли специальный алиас (final_product_name)
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 3. Если нет специального алиаса => проверяем набор атрибутов
    if not has_special_alias:

        # теперь переходим к конкретным "обязательным" атрибутам для каждой модели.

        # (НОВЫЙ КОММЕНТАРИЙ) Для каждой модели, в которой нет "спец.алиаса", укажем
        # точный набор требуемых атрибутов:
        required_attrs_mapping = {
            "magic keyboard": set(),
            "magic mouse": {"color"},
            "magic trackpad" : {"color"},
            "pencil": set(),
            "airtag" : set(),
            "charger" : set(),
            "apple tv 4k": {"SSD"},
            "наборы для airpods": {"version", "Pack"}
        }

        # (НОВЫЙ КОММЕНТАРИЙ) Берём "обязательные" атрибуты из словаря (по model.lower())
        required_attrs = required_attrs_mapping.get(model.lower(), set())
        if required_attrs is None:
            # Если модель не найдена в нашем словаре => считаем, что
            # мы не можем проверить корректность. Логируем и возвращаем False
            logger.info(
                f"[handle_mac_product] Модель '{model}' не найдена в required_attrs_mapping => return False"
            )
            return False

        # Смотрим, что именно распознали
        attr_count = len(extracted_attributes)
        recognized_keys = set(extracted_attributes.keys())
        logger.info(
            f"[handle_apple_accessories_product] Распознано {attr_count} атр.: {recognized_keys} для модели='{model}'"
        )

        # (НОВЫЙ КОММЕНТАРИЙ) Проверяем, не пропущены ли какие-то обязательные атрибуты
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            # Если есть пропущенные, логируем и возвращаем False
            logger.info(
                f"[handle_apple_accessories_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        # Если дошли сюда, значит все обязательные атрибуты присутствуют
        logger.info(
            f"[handle_apple_accessories_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # 4. Формируем final_product_name
    #   Если есть алиас, используем extracted_attributes["final_product_name"]
    #   Иначе формируем вручную.

    final_product_name = None  # (НОВЫЙ КОД) Инициализация

    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[apple accessories parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        # Старая логика
        if model.lower() == "magic keyboard" :
            final_product_name = model  # Используем оригинальное название модели
            attributes = []

            # Сначала добавляем цвет, если присутствует
            color = extracted_attributes.get("color")
            if color :
                attributes.append(color)

            # Если присутствует "iPad", добавляем "for" перед ним
            if "iPad" in extracted_attributes :
                if color :
                    attributes.append("for")  # Добавляем "for" только если цвет уже добавлен
                attributes.append(extracted_attributes["iPad"])

            # Добавляем диагональ, если присутствует
            diagonal = extracted_attributes.get("diagonal")
            if diagonal :
                attributes.append(diagonal)

            # Обработка "Numeric Keypad" и "Touch ID"
            numeric_keypad = extracted_attributes.get("Numeric Keypad")
            touch_id = extracted_attributes.get("Touch ID")

            if numeric_keypad and touch_id :
                # Если оба атрибута присутствуют, соединяем их "и"
                combined_attrs = f"{numeric_keypad} и {touch_id}"
                attributes.append(combined_attrs)
            else :
                # Если присутствует только один из них, добавляем его
                if numeric_keypad :
                    attributes.append(numeric_keypad)
                if touch_id :
                    attributes.append(touch_id)

            # Формируем окончательное название, соединяя все части через пробел
            if attributes :
                final_product_name += " " + " ".join(attributes)

        elif model.lower() == "magic mouse" :
            final_product_name = f"{model}"
            for attr in ["color", "USB"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower() == "magic trackpad" :
            final_product_name = f"{model}"
            for attr in ["color"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower() == "pencil" :
            final_product_name = f"{model}"
            for attr in ["version", "USB"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower() == "airtag" :
            final_product_name = f"{model}"
            for attr in ["Pack"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower() == "charger" :
            attributes = [extracted_attributes[attr] for attr in ["version"] if attr in extracted_attributes]
            final_product_name = " ".join(attributes)

        elif model.lower() == "apple tv 4k" :
            final_product_name = f"{model}"
            for attr in ["SSD"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower() == "наборы для airpods" :
            product_base = model.lower().replace("наборы для ", "").capitalize()
            final_product_name = f"{product_base}"
            for attr in ["version", "Pack"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

    # Если до сих пор переменная осталась None — значит ни один из if/elif не выполнился
    if final_product_name is None :
        final_product_name = "Unknown apple accessories"

    logger.info(f"[apple accessories parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5. Если страна не указана => ставим ""
    brand = "Apple Аксессуары"
    if brand == "Apple Аксессуары" and not countries:
        logger.debug("[apple accessories parser] Не указана страна => ''")
        countries = [""]

    # 6. Применяем apply_special_rules_iphone и сохраняем
    if countries:
        for country in countries:
            selected_variant = apply_special_rules_iphone(
                model_group=model,
                country=country,
                variant=final_product_name,
                product_library=PRODUCT_LIBRARY,
                brand=brand
            )
            add_or_update_product(
                USER_DATA, user_id,
                line, [country],
                selected_variant, model,
                price, supplier, comment, brand
            )
    else:
        selected_variant = apply_special_rules_iphone(
            model_group=model,
            country="",
            variant=final_product_name,
            product_library=PRODUCT_LIBRARY,
            brand=brand
        )
        add_or_update_product(
            USER_DATA, user_id,
            line, [],
            selected_variant, model,
            price, supplier, comment, brand
        )

    logger.debug("[apple accessories parser] Успешно => True")
    return True


def handle_complex_apple_accessories(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки apple accessories:
      1) find_best_apple_accessories_model — чтобы не «застревать» на коротких алиас
         а собрать все совпадения и выбрать лучший.
      2) handle_apple_accessories_product — парсит атрибуты, формирует название, сохраняет.
    """
    best_model = find_best_apple_accessories_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_apple_accessories] Не нашли модель apple accessories для '{cleaned_line}'")
        return False

    brand = "Apple Аксессуары"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False
    logger.info(f"[handle_complex_apple_accessories] Лучшая модель apple accessories: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_apple_accessories_product(
        line=line,
        cleaned_line=cleaned_line,
        model=best_model,
        countries=countries,
        price=price,
        supplier=supplier,
        comment=comment,
        user_id=user_id
    )
    return result