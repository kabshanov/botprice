# apple_mac_utils.py

import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, IGNORING_APPLE_MAC_RECOGNITION,
    SPECIAL_ALIASES_FOR_FINAL_PRODUCT_NAME_APPLE_MAC, MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)

def find_best_apple_mac_model(user_input: str) -> Optional[str] :
    """
    Ищет модель Mac
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Apple Mac", {})
    if not brand_data :
        logger.warning("[find_best_apple_Mac_model] Нет 'Apple Mac' в PRODUCT_LIBRARY.")
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
                    f"[find_best_apple_Mac_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_apple_Mac_model] Ничего не найдено среди Mac-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_apple_Mac_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_mac_product(cleaned_line: str, model: str) -> dict:
    """
    Парсит дополнительные атрибуты (diagonal, chip, RAM, SSD, color)
    для «Apple Mac».

    Параметры:
    ----------
    cleaned_line: str
        Очищенная строка (без цены и артикулов).
    model: str
        Модель (например, "MacBook Pro").

    Возвращает:
    ----------
    dict
        Словарь извлечённых атрибутов. Например:
        {
            "diagonal": "14”",
            "chip": "M4 Max",
            "RAM": "128",
            "SSD": "1TB",
            "color": "Silver"
        }
        Если обнаружен специальный алиас, добавляется "final_product_name".
        Если атрибутов меньше заданного минимума и нет специального алиаса, возвращается пустой словарь {}.

    Дополнительная логика:
    ----------------------
    - Сортируем алиасы по длине (убывание), чтобы длинные алиасы проверялись раньше коротких.
    - Если находим совпадение, добавляем его в список найденных для данного attr_name,
      а затем выбираем «самую длинную» подстроку.
    - Если обнаружен специальный алиас, устанавливаем итоговое название из словаря и возвращаем извлечённые атрибуты.
    - Если распознано меньше необходимого количества атрибутов и нет специального алиаса, возвращаем {}.
    """


    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Apple Mac", {})
    if model not in brand_data :
        logger.warning(f"[parse_Mac_product] Модель '{model}' нет в Apple Mac.")
        return {}

    attributes = brand_data[model]["attributes"]

    for attr_name, attr_info in attributes.items() :
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
                f"[MAC parser] Для attr='{attr_name}' выбрали value='{best_value}' "
                f"(alias='{best_alias}', len={len(best_alias)})"
            )
        else:
            logger.debug(f"[MAC parser] Для attr='{attr_name}' ничего не найдено в строке.")

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Новый блок: проверяем, есть ли спец. алиас для итогового названия
    for alias, full_product_names in SPECIAL_ALIASES_FOR_FINAL_PRODUCT_NAME_APPLE_MAC.items():
        pattern = re.compile(rf'\b{re.escape(alias)}\b', re.IGNORECASE)
        if pattern.search(cleaned_line):
            # Если найден специальный алиас, устанавливаем итоговое название напрямую
            extracted_attributes["final_product_name"] = full_product_names[0]
            logger.debug(
                f"[MAC parser] Найден специальный алиас '{alias}'. "
                f"Устанавливаем итоговое название '{full_product_names[0]}'."
            )
            # Не выходим, просто продолжаем —
            # вдруг ещё есть атрибуты, которые пригодятся (хотя они не влияют на финальную строку)
            break
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    logger.debug(f"[MAC parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_mac_product(
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
    «Склейка» итогового названия для Apple Mac с учётом распознанных атрибутов
    и сохранение результата в USER_DATA.
    Возвращает True, если товар добавлен, иначе False (для обработки как простой).
    """
    from utils import add_or_update_product, apply_special_rules_iphone

    # 1. Парсим дополнительные атрибуты (diagonal, chip, RAM, SSD, color)
    extracted_attributes = parse_mac_product(cleaned_line, model)

    # --- Проверяем исключающие слова ---
    for word in IGNORING_APPLE_MAC_RECOGNITION:
        if re.search(rf'\b{re.escape(word)}\b', cleaned_line, re.IGNORECASE):
            logger.info(f"[MAC parser] Найдено слово-исключение '{word}' => return False")
            return False
        if word in extracted_attributes.values():
            logger.info(f"[MAC parser] Слово-исключение '{word}' в атрибутах => return False")
            return False

    # 2. Проверяем, есть ли специальный алиас (final_product_name)
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 3. Если нет специального алиаса => проверяем min_required_attributes
    if not has_special_alias:
        min_attributes_mapping = {
            "mac mini": 3,
            "mac studio": 3,
            "mac pro": 3,
            "apple 5k retina display": 1,
            "pro display xdr": 1
        }
        # Используем model.lower() для поиска в словаре
        # По умолчанию пусть будет 5
        min_required_attributes = min_attributes_mapping.get(model.lower(), 5)

        attr_count = len(extracted_attributes)
        if attr_count < min_required_attributes:
            logger.info(
                f"[handle_mac_product] Атр-тов={attr_count} < {min_required_attributes}, "
                f"model='{model}', нет спец.алиаса => return False"
            )
            return False

    # 4. Формируем final_product_name
    #   Если есть алиас, используем extracted_attributes["final_product_name"]
    #   Иначе формируем вручную.
    if has_special_alias:
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[MAC parser] Используем специальное итоговое название: '{final_product_name}'")
    else:
        # Старая логика
        if model.lower() in ["mac mini", "mac studio", "mac pro"]:
            final_product_name = f"{model}"
            for attr in ["chip", "RAM", "SSD"]:
                if attr in extracted_attributes:
                    if attr == "chip":
                        final_product_name += f" ({extracted_attributes[attr]}"
                    elif attr == "RAM":
                        final_product_name += f" {extracted_attributes[attr]}"
                    elif attr == "SSD":
                        final_product_name += f"/{extracted_attributes[attr]})"
        elif model.lower() in ["apple 5k retina display", "pro display xdr"]:
            final_product_name = f"{model}"
            if "diagonal" in extracted_attributes :
                final_product_name += f" {extracted_attributes['diagonal']}"
            logger.info(f"[MAC parser] Формируем итоговое название для Apple Display: '{final_product_name}'")

        else:
            final_product_name = f"{model}"
            for attr in ["diagonal", "custom", "chip", "RAM", "SSD", "color", "glass"]:
                if attr in extracted_attributes:
                    if attr == "diagonal":
                        final_product_name += f" {extracted_attributes[attr]}"
                    elif attr == "custom":
                        final_product_name += f" {extracted_attributes[attr]}"
                    elif attr == "chip":
                        final_product_name += f" ({extracted_attributes[attr]}"
                    elif attr == "RAM":
                        final_product_name += f" {extracted_attributes[attr]}"
                    elif attr == "SSD":
                        final_product_name += f"/{extracted_attributes[attr]}"
                    elif attr == "color":
                        final_product_name += f") {extracted_attributes[attr]}"

    logger.info(f"[MAC parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5. Если страна не указана => ставим "США"
    brand = "Apple Mac"
    if brand == "Apple Mac" and not countries:
        logger.debug("[MAC parser] Не указана страна => 'США'")
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

    logger.debug("[MAC parser] Успешно => True")
    return True


def handle_complex_apple_mac(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки Mac:
      1) find_best_apple_mac_model — чтобы не «застревать» на коротких алиас
         а собрать все совпадения и выбрать лучший (например, 'pro max').
      2) handle_mac_product — парсит атрибуты, формирует название, сохраняет.
    """
    best_model = find_best_apple_mac_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_apple_mac] Не нашли модель Mac для '{cleaned_line}'")
        return False

    brand = "Apple Mac"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_apple_mac] Лучшая модель Mac: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_mac_product(
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