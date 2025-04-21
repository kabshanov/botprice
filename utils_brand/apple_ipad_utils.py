# apple_ipad_utils.py

import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, IPAD_YEAR_RELEASE_PATTERN_CHIP,
    IGNORING_IPAD_NO_CHIP, GLASS_IPAD_STANDARD, MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)

def find_best_apple_ipad_model(user_input: str) -> Optional[str] :
    """
    Ищет модель ipad
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Apple iPad", {})
    if not brand_data :
        logger.warning("[find_best_apple_ipad_model] Нет 'Apple ipad' в PRODUCT_LIBRARY.")
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
                    f"[find_best_apple_ipad_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_apple_ipad_model] Ничего не найдено среди ipad-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_apple_ipad_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_ipad_product(cleaned_line: str, model: str) -> dict:
    """
    Парсит дополнительные атрибуты (diagonal, chip, RAM, SSD, color)
    для «Apple iPad».

    Параметры:
    ----------
    cleaned_line: str
        Очищенная строка (без цены и артикулов).
    model: str
        Модель (например, "iPad Pro").

    Возвращает:
    ----------
    dict
        Словарь извлечённых атрибутов.
        Если обнаружен специальный алиас, добавляется "final_product_name".
        Если атрибутов меньше заданного минимума и нет специального алиаса, возвращается пустой словарь {}.

    Дополнительная логика:
    ----------------------
    - Для всех атрибутов ищем алиасы.
    - Для attr='diagonal' в обычном iPad алиас "10" матчим только \b10(?!\.)\b,
      а алиас "10.2" ищем как простой фрагмент "10.2" без границ слова.
    - Если для "diagonal" не найдено ни одного алиаса, просто пропускаем (никакого fallback).
    """

    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Apple iPad", {})
    if model not in brand_data:
        logger.warning(f"[parse_ipad_product] Модель '{model}' нет в Apple iPad.")
        return {}

    attributes = brand_data[model]["attributes"]

    # Проходим по всем атрибутам, определённым для модели
    for attr_name, attr_info in attributes.items():
        attr_aliases = attr_info["aliases"]
        found_aliases = []

        for value, aliases_list in attr_aliases.items():
            for alias in aliases_list:

                # --- Особая логика для обычного iPad (model='iPad') и атрибута 'diagonal' ---
                if model.lower() == "ipad" and attr_name.lower() == "diagonal":
                    if alias == "10":
                        # Шаблон, запрещающий '10' перед точкой => \b10(?!\.)\b
                        pattern_str = r"\b10(?!\.)\b"
                        pattern = re.compile(pattern_str, re.IGNORECASE)
                    elif alias == "10.2":
                        # Для "10.2" убираем \b, чтобы '.' не ломала границу слова
                        pattern_str = re.escape(alias)  # => "10\.2"
                        pattern = re.compile(pattern_str, re.IGNORECASE)
                    else:
                        # Обычный случай для прочих алиасов
                        pattern_str = rf"\b{re.escape(alias)}\b"
                        pattern = re.compile(pattern_str, re.IGNORECASE)

                else:
                    # Общий путь для всего остального
                    pattern_str = rf"\b{re.escape(alias)}\b"
                    pattern = re.compile(pattern_str, re.IGNORECASE)

                # Ищем все совпадения данного alias в cleaned_line
                for match in pattern.finditer(cleaned_line):
                    found_aliases.append((match.start(), alias, value))

        # Выбираем alias, который встречается раньше в тексте
        if found_aliases:
            best = min(found_aliases, key=lambda x: x[0])
            extracted_attributes[attr_name] = best[2]
            logger.debug(
                f"[ipad parser] Для attr='{attr_name}' выбрано alias='{best[1]}' "
                f"(позиция {best[0]}) -> значение='{best[2]}'"
            )
        else:
            logger.debug(f"[ipad parser] Для attr='{attr_name}' ничего не найдено => пропускаем.")

    # --- Дополнительная логика ---
    # Если "Cellular" есть, а "Wi-Fi" нет — добавляем "Wi-Fi"
    if "Cellular" in extracted_attributes and "Wi-Fi" not in extracted_attributes:
        extracted_attributes["Wi-Fi"] = "Wi-Fi"
        logger.debug(
            "[ipad parser] 'Cellular' обнаружен, но 'Wi-Fi' отсутствует => добавляем 'Wi-Fi' автоматически."
        )

    # Пример логики проставления чипа по году (если у вас в IPAD_YEAR_RELEASE_PATTERN_CHIP есть данные)
    if model in IPAD_YEAR_RELEASE_PATTERN_CHIP:
        year_chip_map = IPAD_YEAR_RELEASE_PATTERN_CHIP[model]  # например, {"2024": "M2"}
        match_year = re.search(r"\b(20\d{2})\b", cleaned_line)
        if match_year:
            found_year = match_year.group(1)
            if found_year in year_chip_map and "chip" not in extracted_attributes:
                chip_value = year_chip_map[found_year]
                extracted_attributes["chip"] = chip_value
                logger.debug(
                    f"[ipad parser] Обнаружен год {found_year} для модели '{model}' => chip='{chip_value}'"
                )

    # Пример проверки IGNORING_IPAD_NO_CHIP
    if model in IGNORING_IPAD_NO_CHIP:
        diagonal_set = IGNORING_IPAD_NO_CHIP[model]  # напр. {"11”, "13”"}
        current_diagonal = extracted_attributes.get("diagonal")
        if current_diagonal in diagonal_set and "chip" not in extracted_attributes:
            logger.info(
                f"[ipad parser] Модель '{model}' и diagonal='{current_diagonal}' => Требуется chip, "
                f"а он не найден => пропускаем (return {{}})"
            )
            return {}

    # Пример проверки GLASS_IPAD_STANDARD
    if (
        model in GLASS_IPAD_STANDARD
        and "chip" in extracted_attributes
        and "SSD" in extracted_attributes
        and extracted_attributes["SSD"] in ["1TB", "2TB"]
    ):
        glass_map = GLASS_IPAD_STANDARD[model]
        chip_value = extracted_attributes["chip"]

        if chip_value in glass_map:
            ssd_value = extracted_attributes["SSD"]
            if ssd_value in glass_map[chip_value]:
                if "glass" not in extracted_attributes:
                    standard_glass = glass_map[chip_value][ssd_value]
                    extracted_attributes["glass"] = standard_glass
                    logger.debug(
                        f"[ipad parser] model='{model}', chip='{chip_value}', SSD='{ssd_value}': "
                        f"'glass' не найден => устанавливаем '{standard_glass}' из GLASS_IPAD_STANDARD."
                    )

    logger.debug(f"[ipad parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes



def handle_ipad_product(
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
    «Склейка» итогового названия для Apple iPad с учётом распознанных атрибутов
    и сохранение результата в USER_DATA.
    Возвращает True, если товар добавлен, иначе False (для обработки как простой).
    """
    from utils import add_or_update_product, apply_special_rules_iphone

    # 1. Парсим дополнительные атрибуты (diagonal, chip, RAM, SSD, color)
    extracted_attributes = parse_ipad_product(cleaned_line, model)

    # 2. Проверяем, есть ли специальный алиас (final_product_name)
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 3. Если нет специального алиаса => проверяем набор атрибутов
    if not has_special_alias:

        # теперь переходим к конкретным "обязательным" атрибутам для каждой модели.

        # (НОВЫЙ КОММЕНТАРИЙ) Для каждой модели, в которой нет "спец.алиаса", укажем
        # точный набор требуемых атрибутов:
        required_attrs_mapping = {
            "ipad": {"diagonal", "SSD", "color", "Wi-Fi"},
            "ipad mini": {"diagonal", "SSD", "color", "Wi-Fi"},
            "ipad air" : {"diagonal", "SSD", "color", "Wi-Fi"},
            "ipad pro" : {"diagonal", "SSD", "color", "Wi-Fi"}
        }

        # (НОВЫЙ КОММЕНТАРИЙ) Берём "обязательные" атрибуты из словаря (по model.lower())
        required_attrs = required_attrs_mapping.get(model.lower())
        if required_attrs is None:
            # Если модель не найдена в нашем словаре => считаем, что
            # мы не можем проверить корректность. Логируем и возвращаем False
            logger.info(
                f"[handle_mac_product] Модель '{model}' не найдена в required_attrs_mapping => return False"
            )
            return False

        # Смотрим, что именно распознали
        attr_count = len(extracted_attributes)
        recognized_keys = set(extracted_attributes.keys())  # напр. {"chip", "ssd", "color", ...}
        logger.info(
            f"[handle_ipad_product] Распознано {attr_count} атр.: {recognized_keys} для модели='{model}'"
        )

        # (НОВЫЙ КОММЕНТАРИЙ) Проверяем, не пропущены ли какие-то обязательные атрибуты
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            # Если есть пропущенные, логируем и возвращаем False
            logger.info(
                f"[handle_ipad_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        # Если дошли сюда, значит все обязательные атрибуты присутствуют
        logger.info(
            f"[handle_ipad_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # 4. Формируем final_product_name
    #   Если есть алиас, используем extracted_attributes["final_product_name"]
    #   Иначе формируем вручную.

    final_product_name = None  # (НОВЫЙ КОД) Инициализация

    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[ipad parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        # Старая логика
        if model.lower() in ["ipad", "ipad mini"] :
            final_product_name = f"{model}"
            for attr in ["diagonal", "SSD", "color", "Wi-Fi", "Cellular"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower() in ["ipad air"] :
            final_product_name = f"{model}"
            for attr in ["diagonal", "chip", "SSD", "color", "Wi-Fi", "Cellular"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower() in ["ipad pro"] :
            final_product_name = f"{model}"
            for attr in ["diagonal", "chip", "SSD", "color", "Wi-Fi", "Cellular", "glass"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

    # Если до сих пор переменная осталась None — значит ни один из if/elif не выполнился
    if final_product_name is None :
        final_product_name = "Unknown iPad"

    logger.info(f"[ipad parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5. Если страна не указана => ставим "США"
    brand = "Apple iPad"
    if brand == "Apple iPad" and not countries:
        logger.debug("[iPad parser] Не указана страна => 'США'")
        countries = ["США"]

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

    logger.debug("[iPad parser] Успешно => True")
    return True


def handle_complex_apple_ipad(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки iPad:
      1) find_best_apple_ipad_model — чтобы не «застревать» на коротких алиас
         а собрать все совпадения и выбрать лучший (например, 'pro max').
      2) handle_ipad_product — парсит атрибуты, формирует название, сохраняет.
    """
    best_model = find_best_apple_ipad_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_apple_ipad] Не нашли модель ipad для '{cleaned_line}'")
        return False

    brand = "Apple iPad"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_apple_ipad] Лучшая модель ipad: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_ipad_product(
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