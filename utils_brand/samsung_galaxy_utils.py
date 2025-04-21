# samsung_galaxy_utils.py
import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, GALAXY_S_PATTERN_COLOR, MINIMUM_PRICE_FOR_BRAND, IGNORING_SAMSUNG_GALAXY_RECOGNITION
)

logger = logging.getLogger(__name__)


def find_best_samsung_galaxy_model(user_input: str) -> Optional[str] :
    """
    Ищет модель samsung_galaxy accessories
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Samsung Galaxy", {})
    if not brand_data :
        logger.warning("[find_best_samsung_galaxy_model] Нет 'Samsung Galaxy' в PRODUCT_LIBRARY.")
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
                    f"[find_best_samsung_galaxy_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_samsung_galaxy_model] Ничего не найдено среди Samsung Galaxy-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_samsung_galaxy_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_samsung_galaxy_product(cleaned_line: str, top_level_model: str) -> dict:
    """
    Парсит дополнительные атрибуты
    для «Samsung Galaxy.

    dict
        Словарь извлечённых атрибутов.
        Если обнаружен специальный алиас, добавляется "final_product_name".
        Если атрибутов меньше заданного минимума и нет специального алиса,
        возвращается пустой словарь {}.
    """

    extracted_attributes = {}

    # В PRODUCT_LIBRARY, ключом является "Samsung Galaxy"
    #  -> внутри: {"Galaxy S": { "attributes": {...}}, "Galaxy A": {...}, etc.}
    # Аргумент top_level_model может быть, напр., "Galaxy S"
    brand_data = PRODUCT_LIBRARY.get("Samsung Galaxy", {})
    if top_level_model not in brand_data:
        logger.warning(
            f"[parse_samsung_galaxy_product] Модель '{top_level_model}' нет в 'Samsung Galaxy'."
        )
        return {}

    attributes = brand_data[top_level_model]["attributes"]

    # 0) Новое правило: если в строке встречается паттерн вида "x/a" или "x / a",
    # где x – значение для RAM, а a – значение для SSD, извлекаем их
    ram_ssd_pattern = re.compile(r'\b(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\b')
    match = ram_ssd_pattern.search(cleaned_line)
    if match :
        ram_value = match.group(1)
        ssd_value = match.group(2)
        extracted_attributes["RAM"] = ram_value
        extracted_attributes["SSD"] = ssd_value
        logger.debug(
            f"[Xiaomi Parser] Найден паттерн RAM/SSD: '{match.group(0)}', "
            f"RAM='{ram_value}', SSD='{ssd_value}'"
        )
        # Удаляем найденный паттерн из строки, чтобы он не мешал дальнейшему поиску
        cleaned_line = cleaned_line.replace(match.group(0), '')

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

    # 2) ДОПОЛНИТЕЛЬНЫЙ БЛОК:
    #    Если внутри extracted_attributes["model"] мы нашли sub-model, типа "S24" или "S24+",
    #    попробуем получить цвет из GALAXY_S_PATTERN_COLOR[sub_model]["color"].

    sub_model = extracted_attributes.get("model")  # напр. "S24"
    if sub_model and sub_model in GALAXY_S_PATTERN_COLOR:
        color_map = GALAXY_S_PATTERN_COLOR[sub_model].get("color", {})

        found_color_aliases = []
        for color_value, color_aliases in color_map.items():
            sorted_aliases = sorted(color_aliases, key=len, reverse=True)
            for alias in sorted_aliases:
                pattern = re.compile(
                    rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                    re.IGNORECASE
                )
                if pattern.search(cleaned_line):
                    found_color_aliases.append((alias, color_value))
                    # ищем вдруг более длинный

        if found_color_aliases:
            best_alias, best_color_value = max(found_color_aliases, key=lambda x: len(x[0]))
            extracted_attributes["color"] = best_color_value
            logger.debug(
                f"[samsung galaxy parser] Для 'color' выбрали '{best_color_value}' "
                f"(alias='{best_alias}', len={len(best_alias)})"
            )
        else:
            logger.debug(
                f"[samsung galaxy parser] По GALAXY_S_PATTERN_COLOR для sub-model '{sub_model}' не нашли color."
            )
    else:
        logger.debug(
            f"[samsung galaxy parser] sub-model='{sub_model}' нет в GALAXY_S_PATTERN_COLOR или sub-model не найден."
        )

    logger.debug(f"[ipad parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_samsung_galaxy_product(
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
    extracted_attributes = parse_samsung_galaxy_product(cleaned_line, model)

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
            "galaxy a": {"model", "RAM", "SSD", "color"},
            "galaxy m" : {"model", "RAM", "SSD", "color"},
            "galaxy s" : {"model", "RAM", "SSD", "color"},
            "galaxy watch" : {"model", "case_size", "color"},
            "galaxy buds" : {"model", "color"},
            "galaxy tab" : {"model", "diagonal", "RAM", "SSD", "color"}
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
            f"[handle_samsung_galaxy_product] Распознано {attr_count} атр.: {recognized_keys} для модели='{model}'"
        )

        # (НОВЫЙ КОММЕНТАРИЙ) Проверяем, не пропущены ли какие-то обязательные атрибуты
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            # Если есть пропущенные, логируем и возвращаем False
            logger.info(
                f"[handle_samsung_galaxy_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        # Если дошли сюда, значит все обязательные атрибуты присутствуют
        logger.info(
            f"[handle_samsung_galaxy_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # 4. Формируем final_product_name
    #   Если есть алиас, используем extracted_attributes["final_product_name"]
    #   Иначе формируем вручную.

    final_product_name = None  # (НОВЫЙ КОД) Инициализация

    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Samsung Galaxy parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        # Старая логика
        if model.lower().startswith("galaxy a") :
            # Используем модель из extracted_attributes, если она есть
            if "model" in extracted_attributes :
                product_base = extracted_attributes["model"]
            else :
                # Если по какой-то причине модели нет в extracted_attributes, убираем префикс из исходной строки
                product_base = model.lower().replace("galaxy a ", "").capitalize()

            final_product_name = product_base

            # Если есть и RAM, и SSD — объединяем через '/'
            if "RAM" in extracted_attributes and "SSD" in extracted_attributes :
                final_product_name += f" {extracted_attributes['RAM']}/{extracted_attributes['SSD']}"
            else :
                # Если вдруг одно из значений отсутствует — добавляем по отдельности, если есть
                for attr in ["RAM", "SSD"] :
                    if attr in extracted_attributes :
                        final_product_name += f" {extracted_attributes[attr]}"

            # Добавляем цвет, если есть
            if "color" in extracted_attributes :
                final_product_name += f" {extracted_attributes['color']}"

        elif model.lower().startswith("galaxy m") :
            # Используем модель из extracted_attributes, если она есть
            if "model" in extracted_attributes :
                product_base = extracted_attributes["model"]
            else :
                # Если по какой-то причине модели нет в extracted_attributes, убираем префикс из исходной строки
                product_base = model.lower().replace("galaxy m ", "").capitalize()

            final_product_name = product_base

            # Если есть и RAM, и SSD — объединяем через '/'
            if "RAM" in extracted_attributes and "SSD" in extracted_attributes :
                final_product_name += f" {extracted_attributes['RAM']}/{extracted_attributes['SSD']}"
            else :
                # Если вдруг одно из значений отсутствует — добавляем по отдельности, если есть
                for attr in ["RAM", "SSD"] :
                    if attr in extracted_attributes :
                        final_product_name += f" {extracted_attributes[attr]}"

            # Добавляем цвет, если есть
            if "color" in extracted_attributes :
                final_product_name += f" {extracted_attributes['color']}"

        elif model.lower().startswith("galaxy s") :
            # Используем модель из extracted_attributes, если она есть
            if "model" in extracted_attributes :
                product_base = extracted_attributes["model"]
            else :
                # Если по какой-то причине модели нет в extracted_attributes, убираем префикс из исходной строки
                product_base = model.lower().replace("galaxy s ", "").capitalize()

            final_product_name = product_base

            # Если есть и RAM, и SSD — объединяем через '/'
            if "RAM" in extracted_attributes and "SSD" in extracted_attributes :
                final_product_name += f" {extracted_attributes['RAM']}/{extracted_attributes['SSD']}"
            else :
                # Если вдруг одно из значений отсутствует — добавляем по отдельности, если есть
                for attr in ["RAM", "SSD"] :
                    if attr in extracted_attributes :
                        final_product_name += f" {extracted_attributes[attr]}"

            # Добавляем цвет, если есть
            if "color" in extracted_attributes :
                final_product_name += f" {extracted_attributes['color']}"

        elif model.lower().startswith("galaxy z") :
            # Используем модель из extracted_attributes, если она есть
            if "model" in extracted_attributes :
                product_base = extracted_attributes["model"]
            else :
                # Если по какой-то причине модели нет в extracted_attributes, убираем префикс из исходной строки
                product_base = model.lower().replace("galaxy z ", "").capitalize()

            final_product_name = product_base

            # Если есть и RAM, и SSD — объединяем через '/'
            if "RAM" in extracted_attributes and "SSD" in extracted_attributes :
                final_product_name += f" {extracted_attributes['RAM']}/{extracted_attributes['SSD']}"
            else :
                # Если вдруг одно из значений отсутствует — добавляем по отдельности, если есть
                for attr in ["RAM", "SSD"] :
                    if attr in extracted_attributes :
                        final_product_name += f" {extracted_attributes[attr]}"

            # Добавляем цвет, если есть
            if "color" in extracted_attributes :
                final_product_name += f" {extracted_attributes['color']}"

        elif model.lower() in ["galaxy tab"] :
            final_product_name = f"{model}"
            for attr in ["model", "diagonal", "RAM", "SSD", "color", "Wi-Fi", "LTE"] :
                if attr in extracted_attributes :
                    if attr == "RAM" :
                        final_product_name += f" {extracted_attributes[attr]}"
                    elif attr == "SSD" :
                        final_product_name += f"/{extracted_attributes[attr]}"
                    else :
                        final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower().startswith("galaxy buds") :
            final_product_name = f"{model}"
            # Склеим color + years
            for attr in ["model", "case_size", "color"]:
                if attr in extracted_attributes:
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower().startswith("galaxy watch") :
            final_product_name = f"{model}"
            # Склеим color + years
            for attr in ["model", "case_size", "color"]:
                if attr in extracted_attributes:
                    final_product_name += f" {extracted_attributes[attr]}"

    # Если до сих пор переменная осталась None — значит ни один из if/elif не выполнился
    if final_product_name is None :
        final_product_name = "Unknown Samsung Galaxy"

    logger.info(f"[Samsung Galaxy parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5. Если страна не указана => ставим ""
    brand = "Samsung Galaxy"
    if brand == "Samsung Galaxy" and not countries:
        logger.debug("[Samsung Galaxy parser] Не указана страна => ''")
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

    logger.debug("[Samsung Galaxy parser] Успешно => True")
    return True


def handle_complex_samsung_galaxy(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки Samsung Galaxy:
      1) find_best_samsung_galaxy_model — чтобы не «застревать» на коротких алиас
         а собрать все совпадения и выбрать лучший.
      2) handle_samsung_galaxy_product — парсит атрибуты, формирует название, сохраняет.
    """
    best_model = find_best_samsung_galaxy_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_samsung_galaxy] Не нашли модель Samsung Galaxy для '{cleaned_line}'")
        return False

    brand = "Samsung Galaxy"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_samsung_galaxy] Лучшая модель Samsung Galaxy: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_samsung_galaxy_product(
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