# dyson_airwrap_utils.py

import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)

def find_best_dyson_airwrap_model(user_input: str) -> Optional[str] :
    """
    Ищет модель dyson_airwrap accessories
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Стайлеры для волос Dyson", {})
    if not brand_data :
        logger.warning("[find_best_dyson_airwrap_model] Нет 'Dyson Airwrap' в PRODUCT_LIBRARY.")
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
                    f"[find_best_dyson_airwrap_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_dyson_airwrap_model] Ничего не найдено среди Dyson Airwrap-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_dyson_airwrap_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_dyson_airwrap_product(cleaned_line: str, top_level_model: str) -> dict:
    """
    Парсит дополнительные атрибуты
    для «Dyson Airwrap».

    dict
        Словарь извлечённых атрибутов.
        Если обнаружен специальный алиас, добавляется "final_product_name".
        Если атрибутов меньше заданного минимума и нет специального алиаса,
        возвращается пустой словарь {}.
    """

    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Стайлеры для волос Dyson", {})
    if top_level_model not in brand_data:
        logger.warning(
            f"[parse_dyson_airwrap_product] Модель '{top_level_model}' нет в 'Dyson Airwrap'."
        )
        return {}

    attributes = brand_data[top_level_model]["attributes"]

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
    # Если модель равна "Dyson Airwrap i.d.™ HS08" и отсутствует атрибут "dryer",
    # то добавляем его вручную со значением "Straight+Wavy".
    if top_level_model.lower() == "dyson airwrap i.d.™ hs08".lower() and "dryer" not in extracted_attributes:
        extracted_attributes["dryer"] = "(Straight+Wavy)"
        logger.debug(
            f"[dyson airwrap parser] Добавили атрибут 'dryer' со значением 'Straight+Wavy' для модели '{top_level_model}'"
        )

    logger.debug(f"[ipad parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_dyson_airwrap_product(
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
    extracted_attributes = parse_dyson_airwrap_product(cleaned_line, model)

    # 2. Проверяем, есть ли специальный алиас (final_product_name)
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 3. Если нет специального алиаса => проверяем набор атрибутов
    if not has_special_alias:

        # теперь переходим к конкретным "обязательным" атрибутам для каждой модели.

        # (НОВЫЙ КОММЕНТАРИЙ) Для каждой модели, в которой нет "спец.алиаса", укажем
        # точный набор требуемых атрибутов:
        required_attrs_mapping = {
            "dyson airwrap hs01" : {"color"},
            "dyson airwrap hs05" : {"color"},
            "dyson airwrap i.d.™ hs08": {"color", "dryer"}
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
            f"[handle_dyson_airwrap_product] Распознано {attr_count} атр.: {recognized_keys} для модели='{model}'"
        )

        # (НОВЫЙ КОММЕНТАРИЙ) Проверяем, не пропущены ли какие-то обязательные атрибуты
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            # Если есть пропущенные, логируем и возвращаем False
            logger.info(
                f"[handle_dyson_airwrap_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        # Если дошли сюда, значит все обязательные атрибуты присутствуют
        logger.info(
            f"[handle_dyson_airwrap_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # 4. Формируем final_product_name
    #   Если есть алиас, используем extracted_attributes["final_product_name"]
    #   Иначе формируем вручную.

    final_product_name = None  # (НОВЫЙ КОД) Инициализация

    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Dyson Airwrap parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        # Старая логика для Dyson Airwrap
        if model.lower().startswith("dyson airwrap hs01") :
            # Используем модель из extracted_attributes, если она есть
            if "model" in extracted_attributes :
                product_base = extracted_attributes["model"]
            else :
                # Если по какой-то причине модели нет в extracted_attributes, удаляем префикс из исходной строки.
                # Делаем это универсально, без привязки к конкретному значению (например, "hs05").
                temp = model.lower().replace("dyson airwrap ", "", 1)
                tokens = temp.split()
                if tokens :
                    first_token = tokens[0]
                    # Если первый токен состоит только из букв и цифр и его длина <= 5, преобразуем его в верхний регистр.
                    if re.fullmatch(r"[a-z0-9]+", first_token) and len(first_token) <= 5 :
                        tokens[0] = first_token.upper()
                    product_base = " ".join(tokens)
                else :
                    product_base = temp.capitalize()
            final_product_name = product_base
            for attr in ["complete", "color", "diffuse"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower().startswith("dyson airwrap hs05") :
            # Используем модель из extracted_attributes, если она есть
            if "model" in extracted_attributes :
                product_base = extracted_attributes["model"]
            else :
                # Если по какой-то причине модели нет в extracted_attributes, удаляем префикс из исходной строки.
                # Делаем это универсально, без привязки к конкретному значению (например, "hs05").
                temp = model.lower().replace("dyson airwrap ", "", 1)
                tokens = temp.split()
                if tokens :
                    first_token = tokens[0]
                    # Если первый токен состоит только из букв и цифр и его длина <= 5, преобразуем его в верхний регистр.
                    if re.fullmatch(r"[a-z0-9]+", first_token) and len(first_token) <= 5 :
                        tokens[0] = first_token.upper()
                    product_base = " ".join(tokens)
                else :
                    product_base = temp.capitalize()
            final_product_name = product_base
            for attr in ["complete", "color", "diffuse"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

        elif model.lower().startswith("dyson airwrap i.d.™ hs08") :
            # Используем модель из extracted_attributes, если она есть
            if "model" in extracted_attributes :
                product_base = extracted_attributes["model"]
            else :
                # Если по какой-то причине модели нет в extracted_attributes,
                # удаляем префикс "dyson airwrap i.d.™" из исходной строки.
                # Используем регулярное выражение, учитывающее возможные пробелы между частями префикса.
                temp = re.sub(r'^dyson airwrap\s*i\.d\.\s*™\s*', '', model, flags=re.IGNORECASE).strip()
                tokens = temp.split()
                if tokens :
                    first_token = tokens[0]
                    # Если первый токен состоит только из букв и цифр и его длина <= 5, преобразуем его в верхний регистр.
                    if re.fullmatch(r"[a-z0-9]+", first_token) and len(first_token) <= 5 :
                        tokens[0] = first_token.upper()
                    product_base = " ".join(tokens)
                else :
                    product_base = ""
            final_product_name = product_base
            for attr in ["color", "dryer"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"

    # Если до сих пор переменная осталась None — значит ни один из if/elif не выполнился
    if final_product_name is None :
        final_product_name = "Unknown Dyson Airwrap"

    logger.info(f"[Dyson Airwrap parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5. Если страна не указана => ставим ""
    brand = "Стайлеры для волос Dyson"
    if brand == "Стайлеры для волос Dyson" and not countries:
        logger.debug("[Dyson Airwrap parser] Не указана страна => ''")
        countries = ["Европа"]

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

    logger.debug("[Dyson Airwrap parser] Успешно => True")
    return True


def handle_complex_dyson_airwrap(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки Dyson Airwrap:
      1) find_best_dyson_airwrap_model — чтобы не «застревать» на коротких алиас
         а собрать все совпадения и выбрать лучший.
      2) handle_dyson_airwrap_product — парсит атрибуты, формирует название, сохраняет.
    """
    best_model = find_best_dyson_airwrap_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_dyson_airwrap] Не нашли модель Dyson Airwrap для '{cleaned_line}'")
        return False

    brand = "Стайлеры для волос Dyson"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_dyson_airwrap] Лучшая модель Dyson Airwrap: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_dyson_airwrap_product(
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