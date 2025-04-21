# gopro_utils.py

import logging
import re
from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)


def find_best_gopro_model(user_input: str) -> Optional[str] :
    """
    Ищет модель Steam Deck, перебирая все алиасы и отбрасывая кандидатов,
    если в пользовательском вводе встречается хотя бы один игнорируемый термин для этой модели.

    Возвращает название модели или None, если совпадений не найдено.
    """
    brand_data = PRODUCT_LIBRARY.get("GoPro", {})
    if not brand_data :
        logger.warning("[find_best_gopro_model] Нет 'GoPro' в PRODUCT_LIBRARY.")
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
        logger.info("[find_best_gopro_model] Ничего не найдено среди GoPro-моделей.")
        return None

    # Выбираем кандидата, у которого алиас наибольшей длины
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_gopro_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_gopro_product(cleaned_line: str, top_level_model: str, line: str) -> dict:
    """
    Парсит дополнительные атрибуты для «GoPro».
    Возвращает словарь извлечённых атрибутов.
    """
    extracted_attributes = {}

    # Если модели нет в PRODUCT_LIBRARY, завершаем
    brand_data = PRODUCT_LIBRARY.get("GoPro", {})
    if top_level_model not in brand_data :
        logger.warning(f"[parse_gopro_product] Модель '{top_level_model}' нет в 'GoPro'.")
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
                f"[parse_gopro_product] Для attr='{attr_name}' выбрали value='{best_value}' (alias='{best_alias}', len={len(best_alias)})"
            )
        else :
            logger.debug(f"[parse_gopro_product] Для attr='{attr_name}' ничего не найдено в строке.")

    logger.debug(f"[parse_gopro_product] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes



def handle_gopro_product(
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

    extracted_attributes = parse_gopro_product(cleaned_line, model, line)
    has_special_alias = ("final_product_name" in extracted_attributes)

    if not has_special_alias :
        required_attrs_mapping = {
            "экшн-камера gopro": {"console", "version", "number"},
        }
        required_attrs = required_attrs_mapping.get(model.lower(), set())


        recognized_keys = set(extracted_attributes.keys())
        logger.info(
            f"[handle_gopro_product] Распознано {len(recognized_keys)} атр.: {recognized_keys} для модели='{model}'"
        )

        missing_attrs = required_attrs - recognized_keys
        if missing_attrs :
            logger.info(
                f"[handle_gopro_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        logger.info(
            f"[handle_gopro_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

        # Формирование итогового названия товара
    final_product_name = None


    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Parser GoPro] Используем специальное итоговое название: '{final_product_name}'")
    else :
        if model.lower().startswith("экшн-камера gopro") :
            # Собираем название продукта без использования исходного model
            parts = []

            # Добавляем версию, если она есть
            if "console" in extracted_attributes :
                parts.append(extracted_attributes["console"])

            # Добавляем цвет, если он есть
            if "version" in extracted_attributes :
                parts.append(extracted_attributes["version"])

            # Добавляем цвет, если он есть
            if "number" in extracted_attributes :
                parts.append(extracted_attributes["number"])

            if "add" in extracted_attributes :
                parts.append(extracted_attributes["add"])

            # Собираем финальное название, разделяя части пробелами
            final_product_name = " ".join(parts)

    if final_product_name is None :
        final_product_name = "Unknown GoPro"

    logger.info(f"[Parser GoPro] Итоговое наименование товара: '{final_product_name}'")

    # Если страна не указана, подставляем пустую строку
    brand = "GoPro"
    if brand == "GoPro" and not countries :
        logger.debug("[Parser GoPro] Не указана страна => ''")
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

    logger.debug("[Parser GoPro] Товар успешно обработан => True")
    return True


def handle_complex_gopro(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки товаров GoPro:
      1) Определяем лучшую модель с учётом игнорируемых слов.
      2) Парсим атрибуты, формируем итоговое название и сохраняем товар.
    """
    best_model = find_best_gopro_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_gopro] Не нашли модель GoPro для '{cleaned_line}'")
        return False

    brand = "GoPro"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_gopro] Цена товара ({price}) ниже минимальной ({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_gopro] Лучшая модель GoPro: '{best_model}'")

    result = handle_gopro_product(
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
