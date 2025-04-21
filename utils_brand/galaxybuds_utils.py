# samsung_galaxy_utils.py
import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, MINIMUM_PRICE_FOR_BRAND, IGNORING_SAMSUNG_GALAXY_RECOGNITION
)

logger = logging.getLogger(__name__)


def find_best_galaxybuds_model(user_input: str) -> Optional[str] :
    """
    Ищет модель samsung_galaxy accessories
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Galaxy Buds", {})
    if not brand_data :
        logger.warning("[find_best_galaxybuds_model] Нет 'Galaxy Buds' в PRODUCT_LIBRARY.")
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
                    f"[find_best_galaxybuds_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_galaxybuds_model] Ничего не найдено среди Galaxy Buds-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_galaxybuds_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_galaxybuds_product(cleaned_line: str, top_level_model: str) -> dict:
    """
    Парсит дополнительные атрибуты
    для «Galaxy Buds.

    dict
        Словарь извлечённых атрибутов.
        Если обнаружен специальный алиас, добавляется "final_product_name".
        Если атрибутов меньше заданного минимума и нет специального алиса,
        возвращается пустой словарь {}.
    """

    extracted_attributes = {}

    # В PRODUCT_LIBRARY, ключом является "Galaxy Buds"
    #  -> внутри: {"Galaxy S": { "attributes": {...}}, "Galaxy A": {...}, etc.}
    # Аргумент top_level_model может быть, напр., "Galaxy S"
    brand_data = PRODUCT_LIBRARY.get("Galaxy Buds", {})
    if top_level_model not in brand_data:
        logger.warning(
            f"[parse_galaxybuds_product] Модель '{top_level_model}' нет в 'Galaxy Buds'."
        )
        return {}

    attributes = brand_data[top_level_model]["attributes"]


    # 1) Старая логика: перебираем attr_name, attr_info
    for attr_name, attr_info in attributes.items():
        attr_aliases = attr_info["aliases"]

        found_aliases = []
        for value, aliases in attr_aliases.items():
            # Сортируем алиасы по длине в порядке убывания
            sorted_aliases = sorted(aliases, key=len, reverse=True)
            for alias in sorted_aliases:
                # Вместо \b...\b используем lookbehind/lookahead,
                # чтобы '+' считался частью "слова".
                # (?<![A-Za-z0-9+]) <alias> (?![A-Za-z0-9+])
                pattern = re.compile(
                    rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                    re.IGNORECASE
                )
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
            logger.debug(
                f"[accessories parser] Для attr='{attr_name}' ничего не найдено в строке."
            )


    logger.debug(f"[ipad parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_galaxybuds_product(
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
    extracted_attributes = parse_galaxybuds_product(cleaned_line, model)

    # --- Проверяем исключающие слова ---
    for word in IGNORING_SAMSUNG_GALAXY_RECOGNITION :
        if re.search(rf'\b{re.escape(word)}\b', cleaned_line, re.IGNORECASE) :
            logger.info(f"[airpods parser] Найдено слово-исключение '{word}' => return False")
            return False
        if word in extracted_attributes.values() :
            logger.info(f"[airpods parser] Слово-исключение '{word}' в атрибутах => return False")
            return False

    # 2. Проверяем, есть ли специальный алиас (final_product_name)
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 3. Если нет специального алиаса => проверяем набор атрибутов
    if not has_special_alias:

        # теперь переходим к конкретным "обязательным" атрибутам для каждой модели.

        # (НОВЫЙ КОММЕНТАРИЙ) Для каждой модели, в которой нет "спец.алиаса", укажем
        # точный набор требуемых атрибутов:
        required_attrs_mapping = {
            "наушники galaxy buds" : {"model", "color"},
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
            f"[handle_galaxybuds_product] Распознано {attr_count} атр.: {recognized_keys} для модели='{model}'"
        )

        # (НОВЫЙ КОММЕНТАРИЙ) Проверяем, не пропущены ли какие-то обязательные атрибуты
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            # Если есть пропущенные, логируем и возвращаем False
            logger.info(
                f"[handle_galaxybuds_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        # Если дошли сюда, значит все обязательные атрибуты присутствуют
        logger.info(
            f"[handle_galaxybuds_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # 4. Формируем final_product_name
    #   Если есть алиас, используем extracted_attributes["final_product_name"]
    #   Иначе формируем вручную.

    final_product_name = None  # (НОВЫЙ КОД) Инициализация

    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Galaxy Buds parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        if model.lower().startswith("наушники galaxy buds") :
            # Создаем список частей названия
            parts = []

            # Разбиваем исходную модель на части, исключая первое слово
            model_parts = model.split()
            if model_parts[0].lower() == "наушники" :
                parts.extend(model_parts[1 :])  # Пропускаем первое слово
            else :
                parts.extend(model_parts)

            # Добавляем атрибуты
            if "model" in extracted_attributes :
                parts.append(extracted_attributes["model"])
            if "color" in extracted_attributes :
                parts.append(extracted_attributes["color"])

            # Собираем финальное название
            final_product_name = ' '.join(parts)

            # Фильтрем оставшиеся вхождения (на случай если были в атрибутах)
            final_product_name = final_product_name.replace("наушники", "").strip()
            final_product_name = ' '.join(final_product_name.split())


    # Если до сих пор переменная осталась None — значит ни один из if/elif не выполнился
    if final_product_name is None :
        final_product_name = "Unknown Galaxy Buds"

    logger.info(f"[Galaxy Buds parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5. Если страна не указана => ставим ""
    brand = "Galaxy Buds"
    if brand == "Galaxy Buds" and not countries:
        logger.debug("[Galaxy Buds parser] Не указана страна => ''")
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

    logger.debug("[Galaxy Buds parser] Успешно => True")
    return True


def handle_complex_galaxybuds(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки Galaxy Buds:
      1) find_best_galaxybuds_model — чтобы не «застревать» на коротких алиас
         а собрать все совпадения и выбрать лучший.
      2) handle_galaxybuds_product — парсит атрибуты, формирует название, сохраняет.
    """
    best_model = find_best_galaxybuds_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_galaxybuds] Не нашли модель Galaxy Buds для '{cleaned_line}'")
        return False

    brand = "Galaxy Buds"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_galaxybuds] Лучшая модель Galaxy Buds: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_galaxybuds_product(
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