# dyson_climate_utils.py

import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, COLOR_FOR_VERSION_VERSION_CLIMATE_TP, STANDARD_COLOR_FOR_VERSION_CLIMATE_TP,
    COLOR_FOR_VERSION_VERSION_CLIMATE_PH, STANDARD_COLOR_FOR_VERSION_CLIMATE_PH,
    COLOR_FOR_VERSION_VERSION_CLIMATE_HP, STANDARD_COLOR_FOR_VERSION_CLIMATE_HP,
    COLOR_FOR_VERSION_VERSION_CLIMATE_AM, STANDARD_COLOR_FOR_VERSION_CLIMATE_AM,
    MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)

def find_best_dyson_climate_model(user_input: str) -> Optional[str] :
    """
    Ищет модель dyson_climate
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Системы очистки воздуха Dyson", {})
    if not brand_data :
        logger.warning("[find_best_dyson_climate_model] Нет 'Dyson Сlimate' в PRODUCT_LIBRARY.")
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
                    f"[find_best_dyson_climate_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_dyson_climate_model] Ничего не найдено среди Dyson Сlimate-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_dyson_climate_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_dyson_climate_product(cleaned_line: str, top_level_model: str) -> dict:
    """
    Парсит дополнительные атрибуты
    для «Dyson Сlimate».

    dict
        Словарь извлечённых атрибутов.
        Если обнаружен специальный алиас, добавляется "final_product_name".
        Если атрибутов меньше заданного минимума и нет специального алиаса,
        возвращается пустой словарь {}.
    """

    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Системы очистки воздуха Dyson", {})
    if top_level_model not in brand_data:
        logger.warning(
            f"[parse_dyson_climate_product] Модель '{top_level_model}' нет в 'Dyson Сlimate'."
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

    # Блок 1: Парсинг атрибута "color" с использованием color_FOR_VERSION
    if top_level_model.lower() == "очистители воздуха dyson" and "version" in extracted_attributes :
                version_val = extracted_attributes["version"]
                if version_val in COLOR_FOR_VERSION_VERSION_CLIMATE_TP :
                    color_mapping = COLOR_FOR_VERSION_VERSION_CLIMATE_TP[version_val]
                    found_color = None
                    # Перебираем канонические значения color и их алиасы
                    for candidate_color, aliases in color_mapping.items() :
                        # Сортируем алиасы по длине для приоритета более длинных вариантов
                        sorted_aliases = sorted(aliases, key=len, reverse=True)
                        for alias in sorted_aliases :
                            pattern = re.compile(
                                rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                                re.IGNORECASE
                            )
                            if pattern.search(cleaned_line) :
                                found_color = candidate_color
                                logger.debug(
                                    f"[parse_dyson_climate_product] Найден color '{found_color}' "
                                    f"(alias: '{alias}') для версии '{version_val}' с помощью COLOR_FOR_VERSION_VERSION_CLIMATE_TP."
                                )
                                break
                        if found_color :
                            break
                    if found_color :
                        extracted_attributes["color"] = found_color
                    else :
                        logger.debug(
                            f"[parse_dyson_climate_product] Не удалось определить color из COLOR_FOR_VERSION_VERSION_CLIMATE_TP "
                            f"для версии '{version_val}'."
                        )
                else :
                    logger.debug(
                        f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в COLOR_FOR_VERSION_VERSION_CLIMATE_TP."
                    )

    # Блок 2: Если атрибут "color" не найден, но имеется version,
    # подставляем стандартное значение color из STANDARD_COLOR_FOR_VERSION_CLIMATE_TP.
    if top_level_model.lower() == "очистители воздуха dyson" :
        if "color" not in extracted_attributes and "version" in extracted_attributes :
            version_val = extracted_attributes["version"]
            standard_color = STANDARD_COLOR_FOR_VERSION_CLIMATE_TP.get(version_val)
            if standard_color :
                extracted_attributes["color"] = standard_color
                logger.debug(
                    f"[parse_dyson_cleaner_product] Подставлено стандартное значение 'color': "
                    f"'{standard_color}' для версии '{version_val}'."
                )
            else :
                logger.debug(
                    f"[parse_dyson_cleaner_product] Для версии '{version_val}' стандартное значение 'color' не найдено в STANDARD_COLOR_FOR_VERSION_CLIMATE_TP."
                )

    # Блок 3: Парсинг атрибута "color" с использованием color_FOR_VERSION
    if top_level_model.lower() == "очистители-увлажнители воздуха dyson" and "version" in extracted_attributes :
                version_val = extracted_attributes["version"]
                if version_val in COLOR_FOR_VERSION_VERSION_CLIMATE_PH :
                    color_mapping = COLOR_FOR_VERSION_VERSION_CLIMATE_PH[version_val]
                    found_color = None
                    # Перебираем канонические значения color и их алиасы
                    for candidate_color, aliases in color_mapping.items() :
                        # Сортируем алиасы по длине для приоритета более длинных вариантов
                        sorted_aliases = sorted(aliases, key=len, reverse=True)
                        for alias in sorted_aliases :
                            pattern = re.compile(
                                rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                                re.IGNORECASE
                            )
                            if pattern.search(cleaned_line) :
                                found_color = candidate_color
                                logger.debug(
                                    f"[parse_dyson_climate_product] Найден color '{found_color}' "
                                    f"(alias: '{alias}') для версии '{version_val}' с помощью COLOR_FOR_VERSION_VERSION_CLIMATE_PH."
                                )
                                break
                        if found_color :
                            break
                    if found_color :
                        extracted_attributes["color"] = found_color
                    else :
                        logger.debug(
                            f"[parse_dyson_climate_product] Не удалось определить color из COLOR_FOR_VERSION_VERSION_CLIMATE_PH "
                            f"для версии '{version_val}'."
                        )
                else :
                    logger.debug(
                        f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в COLOR_FOR_VERSION_VERSION_CLIMATE_PH."
                    )

    # Блок 4: Если атрибут "color" не найден, но имеется version,
    # подставляем стандартное значение color из STANDARD_COLOR_FOR_VERSION_CLIMATE_PH.
    if top_level_model.lower() == "очистители-увлажнители воздуха dyson" :
        if "color" not in extracted_attributes and "version" in extracted_attributes :
            version_val = extracted_attributes["version"]
            standard_color = STANDARD_COLOR_FOR_VERSION_CLIMATE_PH.get(version_val)
            if standard_color :
                extracted_attributes["color"] = standard_color
                logger.debug(
                    f"[parse_dyson_cleaner_product] Подставлено стандартное значение 'color': "
                    f"'{standard_color}' для версии '{version_val}'."
                )
            else :
                logger.debug(
                    f"[parse_dyson_cleaner_product] Для версии '{version_val}' стандартное значение 'color' не найдено в STANDARD_COLOR_FOR_VERSION_CLIMATE_PH."
                )

    # Блок 5: Парсинг атрибута "color" с использованием color_FOR_VERSION
    if top_level_model.lower() == "очистители-обогреватели воздуха dyson" and "version" in extracted_attributes :
        version_val = extracted_attributes["version"]
        if version_val in COLOR_FOR_VERSION_VERSION_CLIMATE_HP :
            color_mapping = COLOR_FOR_VERSION_VERSION_CLIMATE_HP[version_val]
            found_color = None
            # Перебираем канонические значения color и их алиасы
            for candidate_color, aliases in color_mapping.items() :
                # Сортируем алиасы по длине для приоритета более длинных вариантов
                sorted_aliases = sorted(aliases, key=len, reverse=True)
                for alias in sorted_aliases :
                    pattern = re.compile(
                        rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                        re.IGNORECASE
                    )
                    if pattern.search(cleaned_line) :
                        found_color = candidate_color
                        logger.debug(
                            f"[parse_dyson_climate_product] Найден color '{found_color}' "
                            f"(alias: '{alias}') для версии '{version_val}' с помощью COLOR_FOR_VERSION_VERSION_CLIMATE_HP."
                        )
                        break
                if found_color :
                    break
            if found_color :
                extracted_attributes["color"] = found_color
            else :
                logger.debug(
                    f"[parse_dyson_climate_product] Не удалось определить color из COLOR_FOR_VERSION_VERSION_CLIMATE_HP "
                    f"для версии '{version_val}'."
                )
        else :
            logger.debug(
                f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в COLOR_FOR_VERSION_VERSION_CLIMATE_HP."
            )

    # Блок 6: Если атрибут "color" не найден, но имеется version, подставляем стандартное значение color из STANDARD_COLOR_FOR_VERSION_CLIMATE_HP.
    if top_level_model.lower() == "очистители-обогреватели воздуха dyson" :
        if "color" not in extracted_attributes and "version" in extracted_attributes :
            version_val = extracted_attributes["version"]
            standard_color = STANDARD_COLOR_FOR_VERSION_CLIMATE_HP.get(version_val)
            if standard_color :
                extracted_attributes["color"] = standard_color
                logger.debug(
                    f"[parse_dyson_cleaner_product] Подставлено стандартное значение 'color': "
                    f"'{standard_color}' для версии '{version_val}'."
                )
            else :
                logger.debug(
                    f"[parse_dyson_cleaner_product] Для версии '{version_val}' стандартное значение 'color' не найдено в STANDARD_COLOR_FOR_VERSION_CLIMATE_HP."
                )

    # Блок 7: Парсинг атрибута "color" с использованием color_FOR_VERSION
    if top_level_model.lower() == "беслопастные вентиляторы и увлажнители dyson" and "version" in extracted_attributes :
        version_val = extracted_attributes["version"]
        if version_val in COLOR_FOR_VERSION_VERSION_CLIMATE_AM :
            color_mapping = COLOR_FOR_VERSION_VERSION_CLIMATE_AM[version_val]
            found_color = None
            # Перебираем канонические значения color и их алиасы
            for candidate_color, aliases in color_mapping.items() :
                # Сортируем алиасы по длине для приоритета более длинных вариантов
                sorted_aliases = sorted(aliases, key=len, reverse=True)
                for alias in sorted_aliases :
                    pattern = re.compile(
                        rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                        re.IGNORECASE
                    )
                    if pattern.search(cleaned_line) :
                        found_color = candidate_color
                        logger.debug(
                            f"[parse_dyson_climate_product] Найден color '{found_color}' "
                            f"(alias: '{alias}') для версии '{version_val}' с помощью COLOR_FOR_VERSION_VERSION_CLIMATE_AM."
                        )
                        break
                if found_color :
                    break
            if found_color :
                extracted_attributes["color"] = found_color
            else :
                logger.debug(
                    f"[parse_dyson_climate_product] Не удалось определить color из COLOR_FOR_VERSION_VERSION_CLIMATE_AM "
                    f"для версии '{version_val}'."
                )
        else :
            logger.debug(
                f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в COLOR_FOR_VERSION_VERSION_CLIMATE_AM."
            )

    # Блок 8: Если атрибут "color" не найден, но имеется version, подставляем стандартное значение color из STANDARD_COLOR_FOR_VERSION_CLIMATE_AM.
    if top_level_model.lower() == "беслопастные вентиляторы и увлажнители dyson" :
        if "color" not in extracted_attributes and "version" in extracted_attributes :
            version_val = extracted_attributes["version"]
            standard_color = STANDARD_COLOR_FOR_VERSION_CLIMATE_AM.get(version_val)
            if standard_color :
                extracted_attributes["color"] = standard_color
                logger.debug(
                    f"[parse_dyson_cleaner_product] Подставлено стандартное значение 'color': "
                    f"'{standard_color}' для версии '{version_val}'."
                )
            else :
                logger.debug(
                    f"[parse_dyson_cleaner_product] Для версии '{version_val}' стандартное значение 'color' не найдено в STANDARD_COLOR_FOR_VERSION_CLIMATE_AM."
                )

    logger.debug(f"[ipad parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_dyson_climate_product(
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

    # 1. Парсим дополнительные атрибуты
    extracted_attributes = parse_dyson_climate_product(cleaned_line, model)

    # 2. Проверяем, есть ли специальный алиас (final_product_name)
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 3. Если нет специального алиаса => проверяем набор атрибутов
    if not has_special_alias:

        # теперь переходим к конкретным "обязательным" атрибутам для каждой модели.

        # (НОВЫЙ КОММЕНТАРИЙ) Для каждой модели, в которой нет "спец.алиаса", укажем
        # точный набор требуемых атрибутов:
        required_attrs_mapping = {
            "очистители воздуха dyson" : {"version", "color"},
            "очистители-увлажнители воздуха dyson" : {"version", "color"},
            "очистители-обогреватели воздуха dyson" : {"version", "color"},
            "беслопастные вентиляторы и увлажнители dyson" : {"version", "color"},

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
            f"[handle_dyson_climate_product] Распознано {attr_count} атр.: {recognized_keys} для модели='{model}'"
        )

        # (НОВЫЙ КОММЕНТАРИЙ) Проверяем, не пропущены ли какие-то обязательные атрибуты
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            # Если есть пропущенные, логируем и возвращаем False
            logger.info(
                f"[handle_dyson_climate_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        # Если дошли сюда, значит все обязательные атрибуты присутствуют
        logger.info(
            f"[handle_dyson_climate_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # 4. Формируем final_product_name
    #   Если есть алиас, используем extracted_attributes["final_product_name"]
    #   Иначе формируем вручную.

    final_product_name = None  # (НОВЫЙ КОД) Инициализация

    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Dyson Climat parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        if model.lower().startswith("очистители воздуха dyson") :
            # Удаляем префикс "Очистители воздуха Dyson" и возможный пробел после него
            product_base = model[len("очистители воздуха dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "color"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()

        elif model.lower().startswith("очистители-увлажнители воздуха dyson") :
            product_base = model[len("очистители-увлажнители воздуха dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "color"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()

        elif model.lower().startswith("очистители-обогреватели воздуха dyson") :
            product_base = model[len("очистители-обогреватели воздуха dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "color"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()

        elif model.lower().startswith("беслопастные вентиляторы и увлажнители dyson") :
            product_base = model[len("очистители-обогреватели воздуха dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "color"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()


    # Если до сих пор переменная осталась None — значит ни один из if/elif не выполнился
    if final_product_name is None :
        final_product_name = "Unknown Dyson Сlimate"

    logger.info(f"[Dyson Climat parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5. Если страна не указана => ставим ""
    brand = "Системы очистки воздуха Dyson"
    if brand == "Системы очистки воздуха Dyson" and not countries:
        logger.debug("[Dyson Climat parser] Не указана страна => ''")
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

    logger.debug("[Dyson Climat parser] Успешно => True")
    return True


def handle_complex_dyson_climate(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки Dyson Сlimate:
      1) find_best_dyson_climate_model — чтобы не «застревать» на коротких алиас
         а собрать все совпадения и выбрать лучший.
      2) handle_dyson_climate_product — парсит атрибуты, формирует название, сохраняет.
    """
    best_model = find_best_dyson_climate_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_dyson_climate] Не нашли модель Dyson Сlimate для '{cleaned_line}'")
        return False

    brand = "Системы очистки воздуха Dyson"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_dyson_climate] Лучшая модель Dyson Сlimate: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_dyson_climate_product(
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