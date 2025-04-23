# dji_osmo_utils.py

import logging
import re
from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)


def find_best_dji_osmo_model(user_input: str) -> Optional[str] :
    """
    Ищет модель DJI Osmo, перебирая все алиасы и отбрасывая кандидатов,
    если в пользовательском вводе встречается хотя бы один игнорируемый термин для этой модели.

    Возвращает название модели или None, если совпадений не найдено.
    """
    brand_data = PRODUCT_LIBRARY.get("DJI Osmo", {})
    if not brand_data :
        logger.warning("[find_best_dji_osmo_model] Нет 'DJI Osmo' в PRODUCT_LIBRARY.")
        return None

    user_input_lower = user_input.lower()
    found_entries = []  # Список кортежей (model_name, alias)

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
                    f"[find_best_dyson_cleaner_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_dji_osmo_model] Ничего не найдено среди DJI Osmo-моделей.")
        return None

    # Выбираем кандидата, у которого алиас наибольшей длины
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_dji_osmo_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_dji_osmo_product(cleaned_line: str, top_level_model: str, line: str) -> dict:
    """
    Парсит дополнительные атрибуты для «DJI Osmo».
    Возвращает словарь извлечённых атрибутов.
    """
    extracted_attributes = {}

    # Если модели нет в PRODUCT_LIBRARY, завершаем
    brand_data = PRODUCT_LIBRARY.get("DJI Osmo", {})
    if top_level_model not in brand_data :
        logger.warning(f"[parse_dji_osmo_product] Модель '{top_level_model}' нет в 'Nothing Ear'.")
        return {}

    attributes = brand_data[top_level_model]["attributes"]

    # 1) Перебираем атрибуты и ищем алиасы (если атрибут уже определён, пропускаем его)
    for attr_name, attr_info in attributes.items() :
        if attr_name in extracted_attributes :
            continue  # Значение уже установлено паттерном, не перезаписываем
        attr_aliases = attr_info["aliases"]
        found_aliases = []
        for value, aliases in attr_aliases.items() :
            sorted_aliases = sorted(aliases, key=len, reverse=True)
            for alias in sorted_aliases :
                pattern = re.compile(
                    rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                    re.IGNORECASE
                )
                if pattern.search(cleaned_line) :
                    found_aliases.append((alias, value))
        if found_aliases :
            best_alias, best_value = max(found_aliases, key=lambda x : len(x[0]))
            extracted_attributes[attr_name] = best_value
            logger.debug(
                f"[parse_dji_osmo_product] Для attr='{attr_name}' выбрали value='{best_value}' (alias='{best_alias}', len={len(best_alias)})"
            )
        else :
            logger.debug(f"[parse_dji_osmo_product] Для attr='{attr_name}' ничего не найдено в строке.")

    logger.debug(f"[parse_dji_osmo_product] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes



def handle_dji_osmo_product(
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
    Формирует итоговое название товара с учётом распознанных атрибутов и сохраняет результат.
    Возвращает True, если товар добавлен, иначе False.
    """
    from utils import add_or_update_product, apply_special_rules_iphone

    extracted_attributes = parse_dji_osmo_product(cleaned_line, model, line)
    has_special_alias = ("final_product_name" in extracted_attributes)

    if not has_special_alias :
        required_attrs_mapping = {
            "экшн-камера dji osmo": {"console", "version"},
            "стабилизаторы dji osmo" : {"console"}
        }
        required_attrs = required_attrs_mapping.get(model.lower(), set())


        recognized_keys = set(extracted_attributes.keys())
        logger.info(
            f"[handle_dji_osmo_product] Распознано {len(recognized_keys)} атр.: {recognized_keys} для модели='{model}'"
        )

        missing_attrs = required_attrs - recognized_keys
        if missing_attrs :
            logger.info(
                f"[handle_dji_osmo_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        logger.info(
            f"[handle_dji_osmo_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

        # Формирование итогового названия товара
    final_product_name = None


    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Parser DJI Osmo] Используем специальное итоговое название: '{final_product_name}'")
    else :
        if model.lower().startswith("экшн-камера dji osmo") :
            # Собираем название продукта без использования исходного model
            parts = []

            # Добавляем версию, если она есть
            if "console" in extracted_attributes :
                parts.append(extracted_attributes["console"])

            # Добавляем цвет, если он есть
            if "version" in extracted_attributes :
                parts.append(extracted_attributes["version"])

            if "add" in extracted_attributes :
                parts.append(extracted_attributes["add"])

            # Собираем финальное название, разделяя части пробелами
            final_product_name = " ".join(parts)

        elif model.lower().startswith("стабилизаторы dji osmo") :
            # Собираем название продукта без использования исходного model
            parts = []

            # Добавляем версию, если она есть
            if "console" in extracted_attributes :
                parts.append(extracted_attributes["console"])

            # Собираем финальное название, разделяя части пробелами
            final_product_name = " ".join(parts)

    if final_product_name is None :
        final_product_name = "Unknown DJI Osmo"

    logger.info(f"[Parser DJI Osmo] Итоговое наименование товара: '{final_product_name}'")

    # Если страна не указана, подставляем пустую строку
    brand = "DJI Osmo"
    if brand == "DJI Osmo" and not countries :
        logger.debug("[Parser DJI Osmo] Не указана страна => ''")
        countries = [""]

    # Сохраняем товар (через apply_special_rules_iphone и add_or_update_product)
    if countries :
        for country in countries :
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
    else :
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

    logger.debug("[Parser DJI Osmo] Товар успешно обработан => True")
    return True


def handle_complex_dji_osmo(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки товаров DJI Osmo:
      1) Определяем лучшую модель с учётом игнорируемых слов.
      2) Парсим атрибуты, формируем итоговое название и сохраняем товар.
    """
    best_model = find_best_dji_osmo_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_dji_osmo] Не нашли модель DJI Osmo для '{cleaned_line}'")
        return False

    brand = "DJI Osmo"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dji_osmo] Цена товара ({price}) ниже минимальной ({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_dji_osmo] Лучшая модель DJI Osmo: '{best_model}'")

    result = handle_dji_osmo_product(
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
