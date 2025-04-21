# playstation_utils.py

import logging
import re
from typing import Optional, List
from rapidfuzz import fuzz

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, MINIMUM_PRICE_FOR_BRAND,
    IGNORING_MODEL_FOR_PLAYSTATION
)

logger = logging.getLogger(__name__)


def find_best_playstation_model(user_input: str) -> Optional[str]:
    """
    Ищет модель PlayStation, перебирая все алиасы и отбрасывая кандидатов,
    если в пользовательском вводе встречается хотя бы один игнорируемый термин для этой модели.

    Возвращает название модели или None, если совпадений не найдено.
    """
    brand_data = PRODUCT_LIBRARY.get("PlayStation", {})
    if not brand_data:
        logger.warning("[find_best_playstation_model] Нет 'PlayStation' в PRODUCT_LIBRARY.")
        return None

    user_input_lower = user_input.lower()
    found_entries = []  # Список кортежей (model_name, alias)
    score_threshold = 95  # Пороговое значение для совпадения

    # Перебираем модели в PRODUCT_LIBRARY для PlayStation
    for model_name, model_info in brand_data.items():
        aliases = model_info.get("aliases", [])
        for alias in aliases:
            alias_lower = alias.lower()
            # Используем fuzz.partial_ratio для оценки совпадения
            score = fuzz.partial_ratio(alias_lower, user_input_lower)
            if score >= score_threshold:
                # Перед добавлением кандидата проверяем игнорируемые слова для данной модели
                ignoring_words = IGNORING_MODEL_FOR_PLAYSTATION.get(model_name, [])
                should_ignore = False
                for word in ignoring_words:
                    ignore_pattern = re.compile(
                        rf'(?<![A-Za-z0-9+]){re.escape(word)}(?![A-Za-z0-9+])',
                        re.IGNORECASE
                    )
                    if ignore_pattern.search(user_input_lower):
                        logger.debug(
                            f"[find_best_playstation_model] Пропускаем модель '{model_name}', найдено игнорируемое слово '{word}'"
                        )
                        should_ignore = True
                        break
                if not should_ignore:
                    logger.debug(
                        f"[find_best_playstation_model] Совпадение alias='{alias}' (score={score}) -> модель='{model_name}'"
                    )
                    found_entries.append((model_name, alias))

    if not found_entries:
        logger.info("[find_best_playstation_model] Ничего не найдено среди PlayStation-моделей.")
        return None

    # Выбираем кандидата, у которого алиас наибольшей длины
    best_model, best_alias = max(found_entries, key=lambda x: len(x[1]))
    logger.info(
        f"[find_best_playstation_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_playstation_product(cleaned_line: str, top_level_model: str) -> dict:
    """
    Парсит дополнительные атрибуты для «PlayStation».
    Возвращает словарь извлечённых атрибутов.
    """
    extracted_attributes = {}

    # Если модели нет в PRODUCT_LIBRARY, завершаем
    brand_data = PRODUCT_LIBRARY.get("PlayStation", {})
    if top_level_model not in brand_data:
        logger.warning(f"[parse_playstation_product] Модель '{top_level_model}' нет в 'PlayStation'.")
        return {}

    attributes = brand_data[top_level_model]["attributes"]


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
                f"[parse_playstation_product] Для attr='{attr_name}' выбрали value='{best_value}' (alias='{best_alias}', len={len(best_alias)})"
            )
        else:
            logger.debug(f"[parse_playstation_product] Для attr='{attr_name}' ничего не найдено в строке.")

    # Блок 1: Если найдены атрибуты 'console' и 'version', устанавливаем 'number' равным 5.
    if "console" in extracted_attributes and "version" in extracted_attributes :
        extracted_attributes["number"] = 5
        logger.debug("[parse_playstation_product] Обнаружены 'console' и 'version'; установлено number = 5")

    # Блок 2: Если известны 'console' и 'number', но отсутствуют 'version' и 'drive', устанавливаем version=FAT, drive=Disk.
    if ("console" in extracted_attributes and "number" in extracted_attributes and
            "version" not in extracted_attributes and "drive" not in extracted_attributes) :
        extracted_attributes["version"] = "FAT"
        extracted_attributes["drive"] = "Disk"
        logger.debug(
            "[parse_playstation_product] Обнаружены 'console' и 'number', но отсутствуют 'version' и 'drive'; установлено version=FAT, drive=Disk")

    logger.debug(f"[parse_playstation_product] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_playstation_product(
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

    extracted_attributes = parse_playstation_product(cleaned_line, model)
    has_special_alias = ("final_product_name" in extracted_attributes)

    if not has_special_alias :
        required_attrs_mapping = {
            "консоли playstation" : {"console", "number", "version"},
            "контроллеры playstation" : {"dualsense", "consoles", "colors"},
            "playstation vr" : {"vr"},
            "аксессуары playstation" : {"acs", "coloracs"},
        }
        required_attrs = required_attrs_mapping.get(model.lower(), set())

        # Блок 1: Если acs равен "PlayStation Portal", атрибут coloracs не требуется.
        if (model.lower() == "аксессуары playstation" and
                extracted_attributes.get("acs", "").strip().lower() == "playstation portal".lower()) :
            required_attrs.discard("coloracs")
            logger.debug("[handle_playstation_product] Для 'PlayStation Portal' не требуется атрибут coloracs")
            if "coloracs" in extracted_attributes :
                del extracted_attributes["coloracs"]
                logger.debug(
                    "[handle_playstation_product] Найденный атрибут 'coloracs' удалён для 'PlayStation Portal'")

        # Блок 2: Если acs равен одному из заданных наушников, то для coloracs допускаются только "White", "Black" или "Camouflage".
        if (model.lower() == "аксессуары playstation" and
                extracted_attributes.get("acs", "").strip() in {"Наушники Sony Pulse 3D", "Наушники Sony Elite",
                                                                "Наушники Sony Explore"}) :
            allowed_coloracs = {"White", "Black", "Camouflage"}
            if "coloracs" in extracted_attributes :
                if extracted_attributes["coloracs"] not in allowed_coloracs :
                    logger.debug(
                        f"[handle_playstation_product] Значение 'coloracs' ('{extracted_attributes['coloracs']}') недопустимо для '{extracted_attributes.get('acs')}', удаляем его.")
                    del extracted_attributes["coloracs"]
            if "coloracs" not in extracted_attributes :
                extracted_attributes["coloracs"] = "White"
                logger.debug(
                    "[handle_playstation_product] Для заданного 'acs' не найден атрибут 'coloracs', установлено значение 'White'")

        if not required_attrs :
            logger.info(
                f"[handle_playstation_product] Модель '{model}' не найдена в required_attrs_mapping => return False"
            )
            return False

        recognized_keys = set(extracted_attributes.keys())
        logger.info(
            f"[handle_playstation_product] Распознано {len(recognized_keys)} атр.: {recognized_keys} для модели='{model}'"
        )
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs :
            logger.info(
                f"[handle_playstation_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False
        logger.info(
            f"[handle_playstation_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # Формирование итогового названия товара
    final_product_name = None


    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Xiaomi Parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        if model.lower().startswith("консоли playstation") :
            # Собираем название продукта без использования исходного model
            parts = []

            # Добавляем версию, если она есть
            if "console" in extracted_attributes :
                parts.append(extracted_attributes["console"])

            # Добавляем цвет, если он есть
            if "number" in extracted_attributes :
                parts.append(extracted_attributes["number"])

            # Добавляем версию, если она есть
            if "version" in extracted_attributes :
                parts.append(extracted_attributes["version"])

            # Добавляем цвет, если он есть
            if "drive" in extracted_attributes :
                parts.append(extracted_attributes["drive"])

            # Собираем финальное название, разделяя части пробелами
            final_product_name = " ".join(str(part) for part in parts)

        elif model.lower().startswith("контроллеры playstation") :
            # Собираем название продукта без использования исходного model
            parts = []

            # Добавляем версию, если она есть
            if "dualsense" in extracted_attributes :
                parts.append(extracted_attributes["dualsense"])

            # Добавляем цвет, если он есть
            if "consoles" in extracted_attributes :
                parts.append(extracted_attributes["consoles"])

            # Добавляем версию, если она есть
            if "colors" in extracted_attributes :
                parts.append(extracted_attributes["colors"])

            # Собираем финальное название, разделяя части пробелами
            final_product_name = " ".join(str(part) for part in parts)

        elif model.lower().startswith("playstation vr") :
            # Собираем название продукта без использования исходного model
            parts = []

            # Добавляем версию, если она есть
            if "vr" in extracted_attributes :
                parts.append(extracted_attributes["vr"])

            # Добавляем цвет, если он есть
            if "game" in extracted_attributes :
                parts.append(extracted_attributes["game"])

            # Собираем финальное название, разделяя части пробелами
            final_product_name = " ".join(str(part) for part in parts)

        elif model.lower().startswith("аксессуары playstation") :
            # Собираем название продукта без использования исходного model
            parts = []

            # Добавляем версию, если она есть
            if "acs" in extracted_attributes :
                parts.append(extracted_attributes["acs"])

            # Добавляем цвет, если он есть
            if "coloracs" in extracted_attributes :
                parts.append(extracted_attributes["coloracs"])

            # Собираем финальное название, разделяя части пробелами
            final_product_name = " ".join(str(part) for part in parts)

    if final_product_name is None :
        final_product_name = "Unknown PlayStation"

    logger.info(f"[PlayStation Parser] Итоговое наименование товара: '{final_product_name}'")

    # Если страна не указана, подставляем пустую строку
    brand = "PlayStation"
    if brand == "PlayStation" and not countries :
        logger.debug("[PlayStation Parser] Не указана страна => ''")
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

    logger.debug("[PlayStation Parser] Товар успешно обработан => True")
    return True


def handle_complex_playstation(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки товаров PlayStation:
      1) Определяем лучшую модель с учётом игнорируемых слов.
      2) Парсим атрибуты, формируем итоговое название и сохраняем товар.
    """
    best_model = find_best_playstation_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_playstation] Не нашли модель PlayStation для '{cleaned_line}'")
        return False

    brand = "PlayStation"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_playstation] Цена товара ({price}) ниже минимальной ({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    # Проверка, была ли цена извлечена из CFI-кода
    price_str = str(price)
    cfi_pattern = re.compile(r'CFI[- ]?([A-Za-z0-9]+)', re.IGNORECASE)
    cfi_matches = cfi_pattern.findall(line)
    for match in cfi_matches:
        if price_str in match:
            logger.info(
                f"[handle_complex_playstation] Цена {price} найдена в CFI-коде '{match}'. Товар пропущен."
            )
            return False

    logger.info(f"[handle_complex_playstation] Лучшая модель PlayStation: '{best_model}'")

    result = handle_playstation_product(
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
