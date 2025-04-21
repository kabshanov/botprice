# dyson_cleaner_utils.py

import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, STANDARD_COMPLETE_FOR_VERSION, COLOR_FOR_VERSION_COMPLETE,
    STANDARD_COLOR_FOR_VERSION_COMPLETE, COMPLETE_FOR_VERSION, WASH_STANDARD_COMPLETE_FOR_VERSION,
    WASH_COLOR_FOR_VERSION_COMPLETE, WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE, WASH_COMPLETE_FOR_VERSION,
MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)

def find_best_dyson_cleaner_model(user_input: str) -> Optional[str] :
    """
    Ищет модель dyson_cleaner
    НЕ останавливаясь на первом совпадении.
    Для каждой модели перебирает aliases, проверяет regex,
    и в итоге выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None,
    если совпадения не найдены.
    """

    brand_data = PRODUCT_LIBRARY.get("Пылесосы Dyson", {})
    if not brand_data :
        logger.warning("[find_best_dyson_cleaner_model] Нет 'Dyson cleaner' в PRODUCT_LIBRARY.")
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
                    f"[find_best_dyson_cleaner_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_dyson_cleaner_model] Ничего не найдено среди Dyson cleaner-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_dyson_cleaner_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_dyson_cleaner_product(cleaned_line: str, top_level_model: str) -> dict:
    """
    Парсит дополнительные атрибуты для «Dyson cleaner».

    dict
        Словарь извлечённых атрибутов.
        Если обнаружен специальный алиас, добавляется "final_product_name".
        Если атрибутов меньше заданного минимума и нет специального алиаса,
        возвращается пустой словарь {}.
    """

    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Пылесосы Dyson", {})
    if top_level_model not in brand_data:
        logger.warning(
            f"[parse_dyson_cleaner_product] Модель '{top_level_model}' нет в 'Dyson cleaner'."
        )
        return {}

    attributes = brand_data[top_level_model]["attributes"]

    # 1) Основной цикл парсинга атрибутов по алиасам
    for attr_name, attr_info in attributes.items():
        attr_aliases = attr_info["aliases"]

        found_aliases = []
        for value, aliases in attr_aliases.items():
            # Сортируем алиасы по длине в порядке убывания
            sorted_aliases = sorted(aliases, key=len, reverse=True)
            for alias in sorted_aliases:
                # Используем lookbehind/lookahead, чтобы '+' считался частью "слова"
                pattern = re.compile(
                    rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                    re.IGNORECASE
                )
                if pattern.search(cleaned_line):
                    found_aliases.append((alias, value))
                    # НЕ прерываемся – ищем возможность найти более длинный алиас.
        if found_aliases:
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

    # Новый блок 1: Парсинг атрибута "complete" с использованием COMPLETE_FOR_VERSION
    if top_level_model.lower() == "пылесосы dyson" and "version" in extracted_attributes:
        version_val = extracted_attributes["version"]
        if version_val in COMPLETE_FOR_VERSION:
            complete_mapping = COMPLETE_FOR_VERSION[version_val]
            found_complete = None
            # Перебираем канонические значения complete и их алиасы
            for candidate_complete, aliases in complete_mapping.items():
                # Сортируем алиасы по длине для приоритета более длинных вариантов
                sorted_aliases = sorted(aliases, key=len, reverse=True)
                for alias in sorted_aliases:
                    pattern = re.compile(
                        rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                        re.IGNORECASE
                    )
                    if pattern.search(cleaned_line):
                        found_complete = candidate_complete
                        logger.debug(
                            f"[parse_dyson_cleaner_product] Найден complete '{found_complete}' "
                            f"(alias: '{alias}') для версии '{version_val}' с помощью COMPLETE_FOR_VERSION."
                        )
                        break
                if found_complete:
                    break
            if found_complete:
                extracted_attributes["complete"] = found_complete
            else:
                logger.debug(
                    f"[parse_dyson_cleaner_product] Не удалось определить complete из COMPLETE_FOR_VERSION "
                    f"для версии '{version_val}'."
                )
        else:
            logger.debug(
                f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в COMPLETE_FOR_VERSION."
            )

    # Блок 2: Если атрибут complete не найден, но имеется version,
    # подставляем стандартное значение complete из STANDARD_COMPLETE_FOR_VERSION.
    if top_level_model.lower() == "пылесосы dyson":
        if "complete" not in extracted_attributes and "version" in extracted_attributes:
            version_val = extracted_attributes["version"]
            standard_complete = STANDARD_COMPLETE_FOR_VERSION.get(version_val)
            if standard_complete:
                extracted_attributes["complete"] = standard_complete
                logger.debug(
                    f"[parse_dyson_cleaner_product] Подставлено стандартное значение 'complete': "
                    f"'{standard_complete}' для версии '{version_val}'."
                )
            else:
                logger.debug(
                    f"[parse_dyson_cleaner_product] Для версии '{version_val}' стандартное значение 'complete' не найдено в STANDARD_COMPLETE_FOR_VERSION."
                )


    # Блок 3: Парсинг атрибута "color" с использованием COLOR_FOR_VERSION_COMPLETE
    if "version" in extracted_attributes and "complete" in extracted_attributes:
            version_val = extracted_attributes["version"]
            complete_val = extracted_attributes["complete"]
            if version_val in COLOR_FOR_VERSION_COMPLETE:
                if complete_val in COLOR_FOR_VERSION_COMPLETE[version_val]:
                    color_mapping = COLOR_FOR_VERSION_COMPLETE[version_val][complete_val]
                    found_color = None
                    for canonical_color, aliases in color_mapping.items():
                        sorted_aliases = sorted(aliases, key=len, reverse=True)
                        for alias in sorted_aliases:
                            pattern = re.compile(
                                rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                                re.IGNORECASE
                            )
                            if pattern.search(cleaned_line):
                                found_color = canonical_color
                                logger.debug(
                                    f"[parse_dyson_cleaner_product] Для 'color' найдено значение '{found_color}' "
                                    f"(alias: '{alias}') для версии '{version_val}' и complete '{complete_val}'."
                                )
                                break
                        if found_color:
                            break
                    if found_color:
                        extracted_attributes["color"] = found_color
                    else:
                        logger.debug(
                            f"[parse_dyson_cleaner_product] Не удалось определить 'color' по COLOR_FOR_VERSION_COMPLETE "
                            f"для версии '{version_val}' и complete '{complete_val}'."
                        )
                else:
                    logger.debug(
                        f"[parse_dyson_cleaner_product] Для версии '{version_val}' значение complete '{complete_val}' отсутствует в COLOR_FOR_VERSION_COMPLETE."
                    )
            else:
                logger.debug(
                    f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в COLOR_FOR_VERSION_COMPLETE."
                )

    # Блок 4: Если по предыдущему правилу не удалось определить 'color',
    # подставляем стандартное значение 'color' из STANDARD_COLOR_FOR_VERSION_COMPLETE.
    if "color" not in extracted_attributes and "version" in extracted_attributes and "complete" in extracted_attributes:
            version_val = extracted_attributes["version"]
            complete_val = extracted_attributes["complete"]
            if version_val in STANDARD_COLOR_FOR_VERSION_COMPLETE:
                if complete_val in STANDARD_COLOR_FOR_VERSION_COMPLETE[version_val]:
                    standard_color = STANDARD_COLOR_FOR_VERSION_COMPLETE[version_val][complete_val]
                    extracted_attributes["color"] = standard_color
                    logger.debug(
                        f"[parse_dyson_cleaner_product] Подставлено стандартное значение 'color': '{standard_color}' "
                        f"для версии '{version_val}' и complete '{complete_val}' из STANDARD_COLOR_FOR_VERSION_COMPLETE."
                    )
                else:
                    logger.debug(
                        f"[parse_dyson_cleaner_product] Для версии '{version_val}' значение complete '{complete_val}' отсутствует в STANDARD_COLOR_FOR_VERSION_COMPLETE."
                    )
            else:
                logger.debug(
                    f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в STANDARD_COLOR_FOR_VERSION_COMPLETE."
                )

    # Новый блок 5: Парсинг атрибута "complete" с использованием COMPLETE_FOR_VERSION
    if top_level_model.lower() == "пылесосы с влажной уборкой dyson" and "version" in extracted_attributes :
        version_val = extracted_attributes["version"]
        if version_val in WASH_COMPLETE_FOR_VERSION :
            complete_mapping = WASH_COMPLETE_FOR_VERSION[version_val]
            found_complete = None
            # Перебираем канонические значения complete и их алиасы
            for candidate_complete, aliases in complete_mapping.items() :
                # Сортируем алиасы по длине для приоритета более длинных вариантов
                sorted_aliases = sorted(aliases, key=len, reverse=True)
                for alias in sorted_aliases :
                    pattern = re.compile(
                        rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                        re.IGNORECASE
                    )
                    if pattern.search(cleaned_line) :
                        found_complete = candidate_complete
                        logger.debug(
                            f"[parse_dyson_cleaner_product] Найден complete '{found_complete}' "
                            f"(alias: '{alias}') для версии '{version_val}' с помощью STANDARD_COMPLETE_FOR_VERSION."
                        )
                        break
                if found_complete :
                    break
            if found_complete :
                extracted_attributes["complete"] = found_complete
            else :
                logger.debug(
                    f"[parse_dyson_cleaner_product] Не удалось определить complete из STANDARD_COMPLETE_FOR_VERSION "
                    f"для версии '{version_val}'."
                )
        else :
            logger.debug(
                f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в STANDARD_COMPLETE_FOR_VERSION."
            )

    # Блок 6: Если атрибут complete не найден, но имеется version,
    # подставляем стандартное значение complete из WASH_STANDARD_COMPLETE_FOR_VERSION.
    if top_level_model.lower() == "пылесосы с влажной уборкой dyson" :
        if "complete" not in extracted_attributes and "version" in extracted_attributes :
            version_val = extracted_attributes["version"]
            standard_complete = WASH_STANDARD_COMPLETE_FOR_VERSION.get(version_val)
            if standard_complete :
                extracted_attributes["complete"] = standard_complete
                logger.debug(
                    f"[parse_dyson_cleaner_product] Подставлено стандартное значение 'complete': "
                    f"'{standard_complete}' для версии '{version_val}'."
                )
            else :
                logger.debug(
                    f"[parse_dyson_cleaner_product] Для версии '{version_val}' стандартное значение 'complete' не найдено в WASH_STANDARD_COMPLETE_FOR_VERSION."
                )

    # Блок 7: Парсинг атрибута "color" с использованием WASH_COLOR_FOR_VERSION_COMPLETE
    if "version" in extracted_attributes and "complete" in extracted_attributes :
        version_val = extracted_attributes["version"]
        complete_val = extracted_attributes["complete"]
        if version_val in WASH_COLOR_FOR_VERSION_COMPLETE :
            if complete_val in WASH_COLOR_FOR_VERSION_COMPLETE[version_val] :
                color_mapping = WASH_COLOR_FOR_VERSION_COMPLETE[version_val][complete_val]
                found_color = None
                for canonical_color, aliases in color_mapping.items() :
                    sorted_aliases = sorted(aliases, key=len, reverse=True)
                    for alias in sorted_aliases :
                        pattern = re.compile(
                            rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])',
                            re.IGNORECASE
                        )
                        if pattern.search(cleaned_line) :
                            found_color = canonical_color
                            logger.debug(
                                f"[parse_dyson_cleaner_product] Для 'color' найдено значение '{found_color}' "
                                f"(alias: '{alias}') для версии '{version_val}' и complete '{complete_val}'."
                            )
                            break
                    if found_color :
                        break
                if found_color :
                    extracted_attributes["color"] = found_color
                else :
                    logger.debug(
                        f"[parse_dyson_cleaner_product] Не удалось определить 'color' по WASH_COLOR_FOR_VERSION_COMPLETE "
                        f"для версии '{version_val}' и complete '{complete_val}'."
                    )
            else :
                logger.debug(
                    f"[parse_dyson_cleaner_product] Для версии '{version_val}' значение complete '{complete_val}' отсутствует в WASH_COLOR_FOR_VERSION_COMPLETE."
                )
        else :
            logger.debug(
                f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в WASH_COLOR_FOR_VERSION_COMPLETE."
            )

    # Блок 8: Если по предыдущему правилу не удалось определить 'color',
    # подставляем стандартное значение 'color' из WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE.
    if "color" not in extracted_attributes and "version" in extracted_attributes and "complete" in extracted_attributes :
        version_val = extracted_attributes["version"]
        complete_val = extracted_attributes["complete"]
        if version_val in WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE :
            if complete_val in WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE[version_val] :
                standard_color = WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE[version_val][complete_val]
                extracted_attributes["color"] = standard_color
                logger.debug(
                    f"[parse_dyson_cleaner_product] Подставлено стандартное значение 'color': '{standard_color}' "
                    f"для версии '{version_val}' и complete '{complete_val}' из WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE."
                )
            else :
                logger.debug(
                    f"[parse_dyson_cleaner_product] Для версии '{version_val}' значение complete '{complete_val}' отсутствует в WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE."
                )
        else :
            logger.debug(
                f"[parse_dyson_cleaner_product] Версия '{version_val}' отсутствует в WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE."
            )

    logger.debug(f"[ipad parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_dyson_cleaner_product(
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
    extracted_attributes = parse_dyson_cleaner_product(cleaned_line, model)


    # 2. Проверяем, есть ли специальный алиас (final_product_name)
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 3. Если нет специального алиаса => проверяем набор атрибутов
    if not has_special_alias:

        # теперь переходим к конкретным "обязательным" атрибутам для каждой модели.

        # (НОВЫЙ КОММЕНТАРИЙ) Для каждой модели, в которой нет "спец.алиаса", укажем
        # точный набор требуемых атрибутов:
        required_attrs_mapping = {
            "пылесосы dyson" : {"version", "complete", "color"},
            "пылесосы с влажной уборкой dyson" : {"version", "complete", "color"},
            "проводные пылесосы dyson" : {"version", "complete"},
            "робот-пылесосы dyson" : {"version", "complete"},
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
            f"[handle_dyson_cleaner_product] Распознано {attr_count} атр.: {recognized_keys} для модели='{model}'"
        )

        # (НОВЫЙ КОММЕНТАРИЙ) Проверяем, не пропущены ли какие-то обязательные атрибуты
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            # Если есть пропущенные, логируем и возвращаем False
            logger.info(
                f"[handle_dyson_cleaner_product] Не хватает атрибутов={missing_attrs} для model='{model}' => return False"
            )
            return False

        # Если дошли сюда, значит все обязательные атрибуты присутствуют
        logger.info(
            f"[handle_dyson_cleaner_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'."
        )

    # 4. Формируем final_product_name
    #   Если есть алиас, используем extracted_attributes["final_product_name"]
    #   Иначе формируем вручную.

    final_product_name = None  # (НОВЫЙ КОД) Инициализация

    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Dyson cleaner parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        if model.lower().startswith("пылесосы dyson") :
            # Удаляем префикс "пылесосы dyson" и возможный пробел после него
            product_base = model[len("пылесосы dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "complete", "color"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()

        elif model.lower().startswith("пылесосы с влажной уборкой dyson") :
            # Удаляем префикс "пылесосы с влажной уборкой dyson" и возможный пробел после него
            product_base = model[len("пылесосы с влажной уборкой dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "complete", "color"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()

        elif model.lower().startswith("проводные пылесосы dyson") :
            # Удаляем префикс "пылесосы с влажной уборкой dyson" и возможный пробел после него
            product_base = model[len("проводные пылесосы dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "complete"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()

        elif model.lower().startswith("робот-пылесосы dyson") :
            # Удаляем префикс "пылесосы с влажной уборкой dyson" и возможный пробел после него
            product_base = model[len("робот-пылесосы dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "complete"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()



    # Если до сих пор переменная осталась None — значит ни один из if/elif не выполнился
    if final_product_name is None :
        final_product_name = "Unknown Dyson cleaner"

    logger.info(f"[Dyson cleaner parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 5. Если страна не указана => ставим ""
    brand = "Пылесосы Dyson"
    if brand == "Пылесосы Dyson" and not countries:
        logger.debug("[Dyson cleaner parser] Не указана страна => ''")
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

    logger.debug("[Dyson cleaner parser] Успешно => True")
    return True


def handle_complex_dyson_cleaner(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки Dyson cleaner:
      1) find_best_dyson_cleaner_model — чтобы не «застревать» на коротких алиас
         а собрать все совпадения и выбрать лучший.
      2) handle_dyson_cleaner_product — парсит атрибуты, формирует название, сохраняет.
    """
    best_model = find_best_dyson_cleaner_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_dyson_cleaner] Не нашли модель Dyson cleaner для '{cleaned_line}'")
        return False

    brand = "Пылесосы Dyson"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_dyson_cleaner] Лучшая модель Dyson cleaner: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_dyson_cleaner_product(
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