# apple_iphone_utils.py

import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, IGNORING_APPLE_IPHONE_RECOGNITION, MINIMUM_PRICE_FOR_BRAND
)

from utils import add_or_update_product, apply_special_rules_iphone

logger = logging.getLogger(__name__)


def find_best_apple_iphone_model(user_input: str) -> Optional[str] :
    """
    Ищет модель iPhone (например, 'iPhone 16 Pro Max'),
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Apple iPhone", {})
    if not brand_data :
        logger.warning("[find_best_apple_iphone_model] Нет 'Apple iPhone' в PRODUCT_LIBRARY.")
        return None

    user_input_lower = user_input.lower()
    found_entries = []  # Будем складывать (model_name, alias)

    # Идём по моделям: "iPhone 16", "iPhone 16 Plus", "iPhone 16 Pro", "iPhone 16 Pro Max"...
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
                    f"[find_best_apple_iphone_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_apple_iphone_model] Ничего не найдено среди iPhone-моделей.")
        return None

    # Выберем запись, у которой alias длиннее (чтобы '16 Pro Max' победил '16')
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_apple_iphone_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_apple_iphone_product(cleaned_line: str, model: str) -> dict :
    """
    Парсит дополнительные атрибуты (SSD, color) для «Apple iPhone».
    Если атрибутов < 2, возвращает пустой словарь.
    """
    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Apple iPhone", {})
    if model not in brand_data :
        logger.warning(f"[parse_apple_iphone_product] Модель '{model}' нет в Apple iPhone.")
        return {}

    attributes = brand_data[model]["attributes"]

    for attr_name, attr_info in attributes.items() :
        attr_aliases = attr_info["aliases"]

        found_aliases = []
        for value, val_aliases in attr_aliases.items() :
            # Сортируем val_aliases по длине, чтобы более длинный alias
            # имел приоритет, если нужно
            sorted_aliases = sorted(val_aliases, key=len, reverse=True)
            for alias in sorted_aliases :
                pattern = re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
                if pattern.search(cleaned_line) :
                    found_aliases.append((alias, value))
                    # НЕ прерываемся: ищем вдруг более длинный.

        if found_aliases :
            # берём alias, у которого alias длиннее
            best_alias, best_value = max(found_aliases, key=lambda x : len(x[0]))
            extracted_attributes[attr_name] = best_value
            logger.debug(
                f"[parse_apple_iphone_product] Для attr='{attr_name}' выбрали value='{best_value}' "
                f"(alias='{best_alias}')"
            )
        else :
            logger.debug(f"[parse_apple_iphone_product] Для attr='{attr_name}' нет совпадений.")


    # Проверяем, встречаются ли они в cleaned_line. Если да — возвращаем {}.
    for ignore_word in IGNORING_APPLE_IPHONE_RECOGNITION:
        # Используем \b, чтобы не совпадать по подстрокам вроде "WifiHotspot"
        pattern = re.compile(rf"\b{re.escape(ignore_word.lower())}\b", re.IGNORECASE)
        if pattern.search(cleaned_line.lower()):
            logger.debug(f"[parse_apple_iphone_product] Найдено слово-исключение '{ignore_word}' => возвращаем {{}}.")
            return {}


    # Минимальное количество атрибутов
    if len(extracted_attributes) < 2 :
        # (НОВЫЙ КОММЕНТАРИЙ) Выводим более детальную инфу о найденных и пропущенных атрибутах
        found_attrs = list(extracted_attributes.keys())
        missing_attrs = []
        for required_attr in ["SSD", "color"] :
            if required_attr not in extracted_attributes :
                missing_attrs.append(required_attr)

        logger.debug(
            f"[parse_apple_iphone_product] Найдено только {len(extracted_attributes)} атрибут(ов): {found_attrs}. "
            f"Недостаточно -> отсутствуют: {missing_attrs} -> возвращаем {{}}."
        )
        return {}

    logger.debug(f"[parse_apple_iphone_product] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_apple_iphone_product(
        line: str,
        cleaned_line: str,
        model: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    «Склейка» итогового названия для Apple iPhone (SSD + color),
    сохранение результата в USER_DATA.
    """
    # Парсим атрибуты
    extracted_attributes = parse_apple_iphone_product(cleaned_line, model)

    # Проверка «final_product_name»
    if "final_product_name" in extracted_attributes :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[handle_apple_iphone_product] Используем спецназвание='{final_product_name}'")
    else :
        if len(extracted_attributes) < 2 :
            logger.info(
                f"[handle_apple_iphone_product] Недостаточно атрибутов ({len(extracted_attributes)}) для '{model}'."
                " Товар не сохраняем."
            )
            return False

        # Формируем название типа: "iPhone 16 Pro Max 512 Desert"
        # После обновления название будет без слова "iPhone", например: "16 Pro Max 512 Desert"
        final_product_name = f"{model.replace('iPhone', '').strip()}"
        for attr in ["SSD", "color"] :
            if attr in extracted_attributes :
                final_product_name += f" {extracted_attributes[attr]}"

    logger.info(f"[handle_apple_iphone_product] Итоговое название: '{final_product_name}'")

    # Сохраняем (через add_or_update_product)
    if countries :
        for country in countries :
            updated_variant = apply_special_rules_iphone(
                model_group=model,
                country=country,
                variant=final_product_name,
                product_library=PRODUCT_LIBRARY,
                brand="Apple iPhone"
            )
            add_or_update_product(
                USER_DATA,
                user_id,
                line,
                [country],
                updated_variant,
                model,
                price,
                supplier,
                comment,
                brand="Apple iPhone"
            )
    else :
        updated_variant = apply_special_rules_iphone(
            model_group=model,
            country="",
            variant=final_product_name,
            product_library=PRODUCT_LIBRARY,
            brand="Apple iPhone"
        )
        add_or_update_product(
            USER_DATA,
            user_id,
            line,
            [],
            updated_variant,
            model,
            price,
            supplier,
            comment,
            brand="Apple iPhone"
        )

    logger.debug("[handle_apple_iphone_product] Успешно обработано как сложный товар.")
    return True


def handle_complex_apple_iphone(
    line: str,
    cleaned_line: str,
    countries: List[str],
    price: int,
    supplier: str,
    comment: str,
    user_id: int
) -> bool:
    """
    Точка входа для обработки iPhone:
      1) Сначала проверяем количество числовых паттернов (если их 3 и более, выходим).
      2) find_best_apple_iphone_model — чтобы не «застревать» на '16',
         а собрать все совпадения и выбрать лучший (например, '16 pro max').
      3) handle_apple_iphone_product — парсит SSD+color, формирует название, сохраняет.
    """
    # --- НОВЫЙ БЛОК: проверка паттерна 'число/число' ---
    if re.search(r'\b\d+/\d+\b', cleaned_line):
        logger.info(
            f"[handle_complex_apple_iphone] Обнаружен паттерн 'число/число' в '{cleaned_line}'. Исключаем из обработки."
        )
        return False

    # проверка количества числовых паттернов ---
    numeric_patterns = re.findall(r'\b\d+\b', cleaned_line)
    if len(numeric_patterns) > 2:
        logger.info(
            f"[handle_complex_apple_iphone] Обнаружено {len(numeric_patterns)} "
            f"числовых паттернов в '{cleaned_line}'. Исключаем из обработки."
        )
        return False

    best_model = find_best_apple_iphone_model(cleaned_line)
    if not best_model:
        logger.info(f"[handle_complex_apple_iphone] Не нашли модель iPhone для '{cleaned_line}'")
        return False

    brand = "Apple iPhone"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_apple_iphone] Лучшая модель iPhone: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_apple_iphone_product(
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
