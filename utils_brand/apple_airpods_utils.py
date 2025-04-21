# apple_airpods_utils.py

import logging
import re
from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA,
    AIRPODS_MAX_YEAR_RELEASE_PATTERN_COLOR,
    AIRPODS_MAX_YEAR_RELEASE_PATTERN_PRICE,
    AIRPODS_CASE, IGNORING_APPLE_AIRPODS_RECOGNITION, MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)


def find_best_apple_airpods_model(user_input: str) -> Optional[str]:
    """
    Ищет модель AirPods ...
    (ваш код без изменений)
    """
    brand_data = PRODUCT_LIBRARY.get("Apple Airpods", {})
    if not brand_data:
        logger.warning("[find_best_apple_airpods_model] Нет 'Apple airpods' в PRODUCT_LIBRARY.")
        return None

    user_input_lower = user_input.lower()
    found_entries = []
    for model_name, model_info in brand_data.items():
        aliases = model_info.get("aliases", [])
        for alias in aliases:
            alias_lower = alias.lower()
            pattern = re.compile(rf"\b{re.escape(alias_lower)}\b", re.IGNORECASE)
            if pattern.search(user_input_lower):
                logger.debug(f"[find_best_apple_airpods_model] Совпадение alias='{alias}' -> модель='{model_name}'")
                found_entries.append((model_name, alias))

    if not found_entries:
        logger.info("[find_best_apple_airpods_model] Ничего не найдено среди airpods-моделей.")
        return None

    best_model, best_alias = max(found_entries, key=lambda x: len(x[1]))
    logger.info(f"[find_best_apple_airpods_model] Лучшая модель='{best_model}' (alias='{best_alias}')")
    return best_model


def parse_airpods_product(cleaned_line: str, model: str) -> dict:
    """
    Парсит дополнительные атрибуты для «Apple airpods».
    (Без изменений, кроме логгера)
    """
    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Apple Airpods", {})
    if model not in brand_data:
        logger.warning(f"[parse_airpods_product] Модель '{model}' нет в Apple Airpods.")
        return {}

    attributes = brand_data[model]["attributes"]
    for attr_name, attr_info in attributes.items():
        attr_aliases = attr_info["aliases"]
        found_aliases = []
        for value, aliases in attr_aliases.items():
            sorted_aliases = sorted(aliases, key=len, reverse=True)
            for alias in sorted_aliases:
                pattern = re.compile(rf'\b{re.escape(alias)}\b', re.IGNORECASE)
                if pattern.search(cleaned_line):
                    found_aliases.append((alias, value))

        if found_aliases:
            best_alias, best_value = max(found_aliases, key=lambda x: len(x[0]))
            extracted_attributes[attr_name] = best_value
            logger.debug(f"[airpods parser] attr='{attr_name}' => '{best_value}' (alias='{best_alias}')")
        else:
            logger.debug(f"[airpods parser] Для attr='{attr_name}' ничего не найдено.")

    logger.debug(f"[airpods parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_airpods_product(
    line: str,
    cleaned_line: str,
    model: str,
    countries: List[str],
    price: int,
    supplier: str,
    comment: str,
    user_id: int
) -> bool:
    """
    «Склейка» итогового названия для Apple AirPods с учётом распознанных атрибутов
    и сохранение результата в USER_DATA.
    Возвращает True, если товар добавлен, иначе False.
    """
    from utils import add_or_update_product, apply_special_rules_iphone

    # 1) Парсим атрибуты
    extracted_attributes = parse_airpods_product(cleaned_line, model)

    # --- Проверяем исключающие слова ---
    for word in IGNORING_APPLE_AIRPODS_RECOGNITION:
        if re.search(rf'\b{re.escape(word)}\b', cleaned_line, re.IGNORECASE):
            logger.info(f"[airpods parser] Найдено слово-исключение '{word}' => return False")
            return False
        if word in extracted_attributes.values():
            logger.info(f"[airpods parser] Слово-исключение '{word}' в атрибутах => return False")
            return False

    # 2) Проверяем, есть ли спец. алиас
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 3) Проверяем «обязательные» атрибуты, если нет спец. алиаса
    if not has_special_alias:
        required_attrs_mapping = {
            "airpods max": {"color"},
            "airpods" : {"version"}
        }

        required_attrs = required_attrs_mapping.get(model.lower(), set())
        if required_attrs is None:
            logger.info(f"[handle_airpods_product] Модель '{model}' не найдена => return False")
            return False

        recognized_keys = set(extracted_attributes.keys())
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            logger.info(
                f"[handle_airpods_product] Для '{model}' не хватает атрибутов {missing_attrs} => return False"
            )
            return False

    # === НОВЫЙ БЛОК: Если обнаружили 'version' среди атрибутов, проверяем словарь AIRPODS_CASE
    #                 и пытаемся определить атрибут 'case'.
    version_val = extracted_attributes.get("version")
    if version_val and (model.lower() == "airpods"):
        # см. есть ли эта версия в словаре
        if version_val in AIRPODS_CASE:
            case_map = AIRPODS_CASE[version_val]
            found_case = None

            # Идём по словарю вида {"case MagSafe": ["MagSafe"], ...}
            for case_name, aliases in case_map.items():
                # если в cleaned_line найдём один из aliases => это будет наш case
                for alias in aliases:
                    pattern = re.compile(rf"\b{re.escape(alias.lower())}\b", re.IGNORECASE)
                    if pattern.search(cleaned_line.lower()):
                        found_case = case_name
                        logger.info(f"[handle_airpods_product] Нашли паттерн '{alias}' => '{case_name}'")
                        break
                if found_case:
                    break

            # Исключение для AirPods version="3": если мы ничего не нашли => "case Lightning"
            if (not found_case) and (version_val == "3"):
                found_case = "case Lightning"
                logger.info("[handle_airpods_product] AirPods 3, не нашли паттерн => 'case Lightning' по умолчанию")

            if found_case:
                extracted_attributes["case"] = found_case

    # === НОВЫЙ БЛОК: Если model == "AirPods Max" => проставляем years=2024 при двух условиях ===
    model_lower = model.lower()
    if model_lower == "airpods max":
        # 1) Если нет 'years', но color ∈ AIRPODS_MAX_YEAR_RELEASE_PATTERN_COLOR => years=2024
        if "years" not in extracted_attributes:
            color_val = extracted_attributes.get("color")  # Может быть "Midnight", "Purple" и т.п.
            if color_val in AIRPODS_MAX_YEAR_RELEASE_PATTERN_COLOR:
                extracted_attributes["years"] = AIRPODS_MAX_YEAR_RELEASE_PATTERN_COLOR[color_val]
                logger.info(f"[airpods parser] Устанавили years={extracted_attributes['years']} по цвету={color_val}")

        # 2) Если всё ещё нет 'years' и price > 53000 => years=2024
        if "years" not in extracted_attributes:
            if price > AIRPODS_MAX_YEAR_RELEASE_PATTERN_PRICE:
                extracted_attributes["years"] = "2024"
                logger.info(
                    f"[airpods parser] Устанавили years=2024, т.к. цена {price} > {AIRPODS_MAX_YEAR_RELEASE_PATTERN_PRICE}"
                )

    # 4) Сформируем final_product_name
    final_product_name = None
    if has_special_alias:
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[airpods parser] Спец. алиас => {final_product_name}")
    else:
        if model_lower == "airpods max":
            final_product_name = f"{model}"
            # Склеим color + years
            for attr in ["color", "years"]:
                if attr in extracted_attributes:
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model_lower == "airpods":
            final_product_name = f"{model}"
            # Склеим color + years
            for attr in ["version", "ANC", "case"]:
                if attr in extracted_attributes:
                    final_product_name += f" {extracted_attributes[attr]}"

    # Если до сих пор None
    if final_product_name is None:
        final_product_name = "Unknown airpods"

    logger.info(f"[airpods parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5) Если страна не указана => countries=[""]
    brand = "Apple Airpods"
    if brand == "Apple Airpods" and not countries:
        logger.debug("[airpods parser] Не указана страна => ''")
        countries = [""]

    # 6) Сохраняем
    selected_variant = None
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

    logger.debug("[airpods parser] Успешно => True")
    return True


def handle_complex_apple_airpods(
    line: str,
    cleaned_line: str,
    countries: List[str],
    price: int,
    supplier: str,
    comment: str,
    user_id: int
) -> bool:
    """
    Точка входа для обработки airpods:
    1) find_best_apple_airpods_model
    2) handle_airpods_product
    """
    best_model = find_best_apple_airpods_model(cleaned_line)
    if not best_model:
        logger.info(f"[handle_complex_apple_airpods] Не нашли модель airpods для '{cleaned_line}'")
        return False

    brand = "Apple Airpods"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_apple_airpods] Лучшая модель airpods: '{best_model}'")
    result = handle_airpods_product(
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
