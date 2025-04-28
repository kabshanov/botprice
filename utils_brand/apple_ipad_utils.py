# apple_ipad_utils.py
# -*- coding: utf-8 -*-
"""
Модуль для разбора и формирования итоговых названий товаров Apple iPad.
Содержит:
  • поиск наилучшей модели по алиасам;
  • извлечение атрибутов (диагональ, чип, SSD, цвет, …);
  • «склейку» финального имени с учётом правил Wi‑Fi / Cellular;
  • сохранение результата в USER_DATA.

Все комментарии из исходной версии сохранены, добавлены новые — помечены
(НОВЫЙ КОММЕНТАРИЙ) для удобного diff‑а.
"""

import logging
import re
from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY,
    USER_DATA,
    IPAD_YEAR_RELEASE_PATTERN_CHIP,
    IGNORING_IPAD_NO_CHIP,
    GLASS_IPAD_STANDARD,
    MINIMUM_PRICE_FOR_BRAND,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 1.  Поиск модели
# ---------------------------------------------------------------------------

def find_best_apple_ipad_model(user_input: str) -> Optional[str]:
    """Возвращает название модели iPad, чей алиас самый длинный.

    Если совпадений нет — None.
    """

    brand_data = PRODUCT_LIBRARY.get("Apple iPad", {})
    if not brand_data:
        logger.warning("[find_best_apple_ipad_model] Нет 'Apple iPad' в PRODUCT_LIBRARY.")
        return None

    user_input_lower = user_input.lower()
    found_entries: list[tuple[str, str]] = []  # (model_name, alias)

    # Идём по моделям и собираем все совпадения
    for model_name, model_info in brand_data.items():
        aliases = model_info.get("aliases", [])
        for alias in aliases:
            alias_lower = alias.lower()
            pattern = re.compile(rf"\b{re.escape(alias_lower)}\b", re.IGNORECASE)
            if pattern.search(user_input_lower):
                logger.debug(
                    f"[find_best_apple_ipad_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries:
        logger.info("[find_best_apple_ipad_model] Ничего не найдено среди iPad‑моделей.")
        return None

    # Выбираем запись с самым длинным алиасом (более специфичная)
    best_model, best_alias = max(found_entries, key=lambda x: len(x[1]))
    logger.info(
        f"[find_best_apple_ipad_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


# ---------------------------------------------------------------------------
# 2.  Парсинг строки и извлечение атрибутов
# ---------------------------------------------------------------------------

def parse_ipad_product(cleaned_line: str, model: str) -> dict:
    """Извлекает атрибуты для Apple iPad.

    Возвращает словарь атрибутов или {{}} если собрать не удалось.
    """

    extracted_attributes: dict[str, str] = {}

    brand_data = PRODUCT_LIBRARY.get("Apple iPad", {})
    if model not in brand_data:
        logger.warning(f"[parse_ipad_product] Модель '{model}' нет в Apple iPad.")
        return {}

    attributes = brand_data[model]["attributes"]

    # 2.1  Проходим по атрибутам из PRODUCT_LIBRARY
    for attr_name, attr_info in attributes.items():
        attr_aliases = attr_info["aliases"]
        found_aliases: list[tuple[int, str, str]] = []  # (pos, alias, canonical_value)

        for value, aliases_list in attr_aliases.items():
            for alias in aliases_list:

                # --- Особая логика для обычного iPad, attr='diagonal' ---
                if model.lower() == "ipad" and attr_name.lower() == "diagonal":
                    if alias == "10":
                        pattern = re.compile(r"\b10(?!\.)\b", re.IGNORECASE)
                    elif alias == "10.2":
                        pattern = re.compile(re.escape(alias), re.IGNORECASE)
                    else:
                        pattern = re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
                else:
                    pattern = re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)

                for match in pattern.finditer(cleaned_line):
                    found_aliases.append((match.start(), alias, value))

        if found_aliases:
            best = min(found_aliases, key=lambda x: x[0])  # alias, встретившийся раньше
            extracted_attributes[attr_name] = best[2]
            logger.debug(
                f"[ipad parser] Для attr='{attr_name}' выбрано alias='{best[1]}' "
                f"(позиция {best[0]}) -> значение='{best[2]}'"
            )
        else:
            logger.debug(
                f"[ipad parser] Для attr='{attr_name}' ничего не найдено => пропускаем."
            )

    # 2.2  Авто‑добавление Wi‑Fi, если есть Cellular
    if "Cellular" in extracted_attributes and "Wi-Fi" not in extracted_attributes:
        extracted_attributes["Wi-Fi"] = "Wi-Fi"
        logger.debug(
            "[ipad parser] 'Cellular' обнаружен, но 'Wi‑Fi' отсутствует => добавляем 'Wi‑Fi'."
        )

    # 2.3  Подстановка чипа по году (если задано в IPAD_YEAR_RELEASE_PATTERN_CHIP)
    if model in IPAD_YEAR_RELEASE_PATTERN_CHIP:
        year_chip_map = IPAD_YEAR_RELEASE_PATTERN_CHIP[model]
        m_year = re.search(r"\b(20\d{2})\b", cleaned_line)
        if m_year:
            found_year = m_year.group(1)
            if found_year in year_chip_map and "chip" not in extracted_attributes:
                extracted_attributes["chip"] = year_chip_map[found_year]
                logger.debug(
                    f"[ipad parser] Год {found_year} => chip='{year_chip_map[found_year]}'"
                )

    # 2.4  Отбрасываем, если нужен chip, а его нет
    if model in IGNORING_IPAD_NO_CHIP:
        diag_set = IGNORING_IPAD_NO_CHIP[model]
        if extracted_attributes.get("diagonal") in diag_set and "chip" not in extracted_attributes:
            logger.info(
                "[ipad parser] Требуется chip, а он не найден => пропускаем товар."
            )
            return {}

    # 2.5  Стекло по умолчанию
    if (
        model in GLASS_IPAD_STANDARD
        and "chip" in extracted_attributes
        and extracted_attributes.get("SSD") in {"1TB", "2TB"}
        and "glass" not in extracted_attributes
    ):
        standard_glass = GLASS_IPAD_STANDARD[model][extracted_attributes["chip"]][
            extracted_attributes["SSD"]
        ]
        extracted_attributes["glass"] = standard_glass
        logger.debug(
            f"[ipad parser] Добавлено стекло по умолчанию: '{standard_glass}'."
        )

    logger.debug(f"[ipad parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


# ---------------------------------------------------------------------------
# 3.  Склейка итогового названия и сохранение
# ---------------------------------------------------------------------------

def handle_ipad_product(
    line: str,
    cleaned_line: str,
    model: str,
    countries: list,
    price: int,
    supplier: str,
    comment: str,
    user_id: int,
) -> bool:
    """Формирует final_product_name, применяет правила и добавляет товар."""

    from utils import add_or_update_product, apply_special_rules_iphone

    # 1) Извлекаем атрибуты
    extracted_attributes = parse_ipad_product(cleaned_line, model)

    # 2) Спец‑алиас?
    has_special_alias = "final_product_name" in extracted_attributes

    # 3) Валидация обязательных атрибутов (если алиаса нет)
    if not has_special_alias:
        required_map = {
            "ipad": {"diagonal", "SSD", "color", "Wi-Fi"},
            "ipad mini": {"diagonal", "SSD", "color", "Wi-Fi"},
            "ipad air": {"diagonal", "SSD", "color", "Wi-Fi"},
            "ipad pro": {"diagonal", "SSD", "color", "Wi-Fi"},
        }
        required_attrs = required_map.get(model.lower())
        if required_attrs is None:
            logger.info(
                f"[handle_ipad_product] Модель '{model}' не описана в required_map => False"
            )
            return False

        missing = required_attrs - set(extracted_attributes)
        logger.info(
            f"[handle_ipad_product] Распознано {len(extracted_attributes)} атр. ({set(extracted_attributes)})"
        )
        if missing:
            logger.info(
                f"[handle_ipad_product] Не хватает атрибутов {missing} => False"
            )
            return False

    # ─────────────────────────────────────────────────────────
    # 3a  Копия для названия (Wi‑Fi убираем при наличии Cellular)
    attrs_for_title = extracted_attributes.copy()
    if "Cellular" in attrs_for_title:
        attrs_for_title.pop("Wi-Fi", None)

    # -------------------------------------------------------------------
    # 4) Формируем final_product_name
    # -------------------------------------------------------------------
    if has_special_alias:
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(
            f"[ipad parser] Используем специальное итоговое название: '{final_product_name}'"
        )
    else:
        final_product_name = model  # базовая часть
        if model.lower() in {"ipad", "ipad mini"}:
            order = ["diagonal", "SSD", "color", "Wi-Fi", "Cellular"]
        elif model.lower() == "ipad air":
            order = ["diagonal", "chip", "SSD", "color", "Wi-Fi", "Cellular"]
        elif model.lower() == "ipad pro":
            order = [
                "diagonal",
                "chip",
                "SSD",
                "color",
                "Wi-Fi",
                "Cellular",
                "glass",
            ]
        else:
            order = []

        for attr in order:
            if attr in attrs_for_title:
                final_product_name += f" {attrs_for_title[attr]}"

    logger.info(
        f"[ipad parser] Итоговое наименование сложного товара: '{final_product_name}'"
    )

    # 5) Страна по умолчанию
    brand = "Apple iPad"
    if brand == "Apple iPad" and not countries:
        logger.debug("[iPad parser] Страна не указана => 'США'")
        countries = ["США"]

    # 6) Применяем спец‑правила и сохраняем
    if countries:
        for country in countries:
            selected_variant = apply_special_rules_iphone(
                model_group=model,
                country=country,
                variant=final_product_name,
                product_library=PRODUCT_LIBRARY,
                brand=brand,
            )
            add_or_update_product(
                USER_DATA,
                user_id,
                line,
                [country],
                selected_variant,
                model,
                price,
                supplier,
                comment,
                brand,
            )
    else:
        selected_variant = apply_special_rules_iphone(
            model_group=model,
            country="",
            variant=final_product_name,
            product_library=PRODUCT_LIBRARY,
            brand=brand,
        )
        add_or_update_product(
            USER_DATA,
            user_id,
            line,
            [],
            selected_variant,
            model,
            price,
            supplier,
            comment,
            brand,
        )

    logger.debug("[iPad parser] Успешно => True")
    return True


# ---------------------------------------------------------------------------
# 4.  Точка входа для комплекса iPad
# ---------------------------------------------------------------------------

def handle_complex_apple_ipad(
    line: str,
    cleaned_line: str,
    countries: List[str],
    price: int,
    supplier: str,
    comment: str,
    user_id: int,
) -> bool:
    """Главная функция для iPad‑товаров."""

    best_model = find_best_apple_ipad_model(cleaned_line)
    if not best_model:
        logger.info(
            f"[handle_complex_apple_ipad] Модель iPad не найдена для '{cleaned_line}'"
        )
        return False

    brand = "Apple iPad"
    if brand in MINIMUM_PRICE_FOR_BRAND:
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price:
            logger.info(
                f"[handle_complex_apple_ipad] Цена {price} < минимальной {min_price} => пропуск."
            )
            return False

    logger.info(f"[handle_complex_apple_ipad] Лучшая модель ipad: '{best_model}'")

    # Дальнейшая обработка
    return handle_ipad_product(
        line=line,
        cleaned_line=cleaned_line,
        model=best_model,
        countries=countries,
        price=price,
        supplier=supplier,
        comment=comment,
        user_id=user_id,
    )
