# tecno_utils.py

import logging
import re
from typing import Optional, List
from rapidfuzz import fuzz

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, TECNO_MOBILE_PATTERN_COLOR, MINIMUM_PRICE_FOR_BRAND,
    IGNORING_MODEL_FOR_TECNO_MOBILE
)

logger = logging.getLogger(__name__)


def find_best_tecno_model(user_input: str) -> Optional[str]:
    """
    Ищет модель Tecno Mobile, перебирая все алиасы и отбрасывая кандидатов,
    если в пользовательском вводе встречается хотя бы один игнорируемый термин для этой модели.

    Возвращает название модели или None, если совпадений не найдено.
    """
    brand_data = PRODUCT_LIBRARY.get("Tecno Mobile", {})
    if not brand_data:
        logger.warning("[find_best_tecno_model] Нет 'Tecno Mobile' в PRODUCT_LIBRARY.")
        return None

    user_input_lower = user_input.lower()
    found_entries = []  # Список кортежей (model_name, alias)
    score_threshold = 95  # Пороговое значение для совпадения

    # Перебираем модели в PRODUCT_LIBRARY для Tecno Mobile
    for model_name, model_info in brand_data.items():
        aliases = model_info.get("aliases", [])
        for alias in aliases:
            alias_lower = alias.lower()
            # Используем fuzz.partial_ratio для оценки совпадения
            score = fuzz.partial_ratio(alias_lower, user_input_lower)
            if score >= score_threshold:
                # Перед добавлением кандидата проверяем игнорируемые слова для данной модели
                ignoring_words = IGNORING_MODEL_FOR_TECNO_MOBILE.get(model_name, [])
                should_ignore = False
                for word in ignoring_words:
                    ignore_pattern = re.compile(
                        rf'(?<![A-Za-z0-9+]){re.escape(word)}(?![A-Za-z0-9+])',
                        re.IGNORECASE
                    )
                    if ignore_pattern.search(user_input_lower):
                        logger.debug(
                            f"[find_best_tecno_model] Пропускаем модель '{model_name}', найдено игнорируемое слово '{word}'"
                        )
                        should_ignore = True
                        break
                if not should_ignore:
                    logger.debug(
                        f"[find_best_tecno_model] Совпадение alias='{alias}' (score={score}) -> модель='{model_name}'"
                    )
                    found_entries.append((model_name, alias))

    if not found_entries:
        logger.info("[find_best_tecno_model] Ничего не найдено среди Tecno Mobile-моделей.")
        return None

    # Выбираем кандидата, у которого алиас наибольшей длины
    best_model, best_alias = max(found_entries, key=lambda x: len(x[1]))
    logger.info(
        f"[find_best_tecno_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_tecno_product(cleaned_line: str, top_level_model: str) -> dict:
    """
    Парсит дополнительные атрибуты для «Tecno Mobile».
    Возвращает словарь извлечённых атрибутов.
    """
    extracted_attributes = {}

    # Если модели нет в PRODUCT_LIBRARY, завершаем
    brand_data = PRODUCT_LIBRARY.get("Tecno Mobile", {})
    if top_level_model not in brand_data:
        logger.warning(f"[parse_tecno_product] Модель '{top_level_model}' нет в 'Tecno Mobile'.")
        return {}

    attributes = brand_data[top_level_model]["attributes"]

    # 0) Парсим паттерн RAM/SSD вида "x/a" или "x / a"
    ram_ssd_pattern = re.compile(r'\b(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\b')
    match = ram_ssd_pattern.search(cleaned_line)
    if match:
        ram_value = match.group(1)
        ssd_value = match.group(2)
        extracted_attributes["RAM"] = ram_value
        extracted_attributes["SSD"] = ssd_value
        logger.debug(
            f"[Tecno Mobile Parser] Найден паттерн RAM/SSD: '{match.group(0)}', RAM='{ram_value}', SSD='{ssd_value}'"
        )
        # Удаляем найденный паттерн из строки и очищаем её
        cleaned_line = cleaned_line.replace(match.group(0), '')
        cleaned_line = re.sub(r'\s+', ' ', cleaned_line).strip()



    # 1) Перебираем атрибуты и ищем алиасы (если атрибут уже определён, пропускаем его)
    for attr_name, attr_info in attributes.items():
        if attr_name in extracted_attributes:
            continue  # Значение уже установлено паттерном, не перезаписываем
        attr_aliases = attr_info["aliases"]
        found_aliases = []
        for value, aliases in attr_aliases.items():
            sorted_aliases = sorted(aliases, key=len, reverse=True)
            for alias in sorted_aliases:
                pattern = re.compile(
                    rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                    re.IGNORECASE
                )
                if pattern.search(cleaned_line):
                    found_aliases.append((alias, value))
        if found_aliases:
            best_alias, best_value = max(found_aliases, key=lambda x: len(x[0]))
            extracted_attributes[attr_name] = best_value
            logger.debug(
                f"[parse_tecno_product] Для attr='{attr_name}' выбрали value='{best_value}' (alias='{best_alias}', len={len(best_alias)})"
            )
        else:
            logger.debug(f"[parse_tecno_product] Для attr='{attr_name}' ничего не найдено в строке.")

    if "+ 5G" in extracted_attributes and "Wi-Fi" not in extracted_attributes:
        extracted_attributes["Wi-Fi"] = "Wi-Fi"
        logger.debug(
            "[parse_tecno_product] 'Cellular' обнаружен, но 'Wi-Fi' отсутствует => добавляем 'Wi-Fi' автоматически."
        )

    # 2) Дополнительный блок для парсинга цвета
    sub_model = extracted_attributes.get("model")
    if sub_model and top_level_model in TECNO_MOBILE_PATTERN_COLOR :
        model_color_info = TECNO_MOBILE_PATTERN_COLOR[top_level_model]
        if sub_model in model_color_info :
            # Получаем маппинг: канонический цвет -> список возможных алиасов
            color_aliases_map = model_color_info[sub_model].get("color", {})
            found_colors = []
            for canonical_color, aliases in color_aliases_map.items() :
                for alias in aliases :
                    pattern = re.compile(
                        rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                        re.IGNORECASE
                    )
                    if pattern.search(cleaned_line) :
                        found_colors.append((alias, canonical_color))
                        # Если для данного цвета найдено совпадение по хотя бы одному алиасу,
                        # можно выйти из внутреннего цикла.
                        break
            if found_colors :
                # Выбираем совпадение с самым длинным алиасом (приоритет длинных совпадений)
                best_alias, best_color = max(found_colors, key=lambda x : len(x[0]))
                extracted_attributes["color"] = best_color
                logger.debug(
                    f"[Tecno Mobile Parser] Для 'color' выбрали '{best_color}' (найден алиас '{best_alias}', len={len(best_alias)})"
                )
            else :
                logger.debug(
                    f"[Tecno Mobile Parser] По TECNO_MOBILE_PATTERN_COLOR для модели '{top_level_model}' и подмодели '{sub_model}' не найдено совпадений для цвета."
                )
        else :
            logger.debug(
                f"[Tecno Mobile Parser] Для модели '{top_level_model}' отсутствует подмодель '{sub_model}' в TECNO_MOBILE_PATTERN_COLOR."
            )
    else :
        logger.debug(
            f"[Tecno Mobile Parser] Не найдены данные по цвету: либо sub-model='{sub_model}' отсутствует, либо '{top_level_model}' нет в TECNO_MOBILE_PATTERN_COLOR."
        )

    logger.debug(f"[parse_tecno_product] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes



def handle_tecno_product(
        line: str,
        cleaned_line: str,
        model: str,
        countries: list,
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Формирует итоговое название товара с учётом распознанных атрибутов и сохраняет результат.
    Возвращает True, если товар добавлен, иначе False.
    """
    from utils import add_or_update_product, apply_special_rules_iphone

    extracted_attributes = parse_tecno_product(cleaned_line, model)
    has_special_alias = ("final_product_name" in extracted_attributes)

    if not has_special_alias :
        required_attrs_mapping = {
            "tecno mobile" : {"model", "RAM", "SSD", "color"},
        }
        required_attrs = required_attrs_mapping.get(model.lower(), set())
        if not required_attrs :
            logger.info(
                f"[handle_tecno_product] Модель '{model}' не найдена в required_attrs_mapping => return False"
            )
            return False

        recognized_keys = set(extracted_attributes.keys())
        logger.info(
            f"[handle_tecno_product] Распознано {len(recognized_keys)} атр.: {recognized_keys} для модели='{model}'"
        )
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs :
            logger.info(
                f"[handle_tecno_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False
        logger.info(
            f"[handle_tecno_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # Формирование итогового названия товара
    final_product_name = None

    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
    else :
        if model.lower().startswith("tecno mobile") :
            # 1. База с моделью
            if "model" in extracted_attributes and extracted_attributes["model"].strip() :
                model_attr = extracted_attributes["model"].strip()
                product_base = f" {model_attr}"
            else :
                product_base = model.strip()
            final_product_name = product_base

            # 2. Добавляем RAM/SSD
            if "RAM" in extracted_attributes and "SSD" in extracted_attributes :
                final_product_name += f" {extracted_attributes['RAM']}/{extracted_attributes['SSD']}"
            elif "RAM" in extracted_attributes :
                final_product_name += f" {extracted_attributes['RAM']}"
            elif "SSD" in extracted_attributes :
                final_product_name += f" {extracted_attributes['SSD']}"

            # 3. Добавляем цвет
            if "color" in extracted_attributes :
                final_product_name += f" {extracted_attributes['color']}"

            # 4. Удаляем дубли 'Pad'
            final_product_name = re.sub(
                r'(?i)\bpad(?:\s+pad)+\b',
                'Pad',
                final_product_name
            )
            # 5. Сжимаем пробелы
            final_product_name = re.sub(r'\s+', ' ', final_product_name).strip()

    if final_product_name is None :
        final_product_name = "Unknown Tecno Mobile"

    logger.info(f"[Tecno Mobile Parser] Итоговое наименование товара: '{final_product_name}'")

    # Если страна не указана, подставляем пустую строку
    brand = "Tecno Mobile"
    if brand == "Tecno Mobile" and not countries :
        logger.debug("[Tecno Mobile Parser] Не указана страна => ''")
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

    logger.debug("[Tecno Mobile Parser] Товар успешно обработан => True")
    return True


def handle_complex_tecno(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки товаров Tecno Mobile:
      1) Определяем лучшую модель с учётом игнорируемых слов.
      2) Парсим атрибуты, формируем итоговое название и сохраняем товар.
    """
    best_model = find_best_tecno_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_tecno] Не нашли модель Tecno Mobile для '{cleaned_line}'")
        return False

    brand = "Tecno Mobile"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_tecno] Цена товара ({price}) ниже минимальной ({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_tecno] Лучшая модель Tecno Mobile: '{best_model}'")

    result = handle_tecno_product(
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
