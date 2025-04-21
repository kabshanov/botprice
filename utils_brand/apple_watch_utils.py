#apple_watch_utils.py

import logging
import re

from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, SPECIAL_RULE_CASE_SIZE_APPLE_WATCH, SPECIAL_RULE_YEAR_RELEASE_APPLE_WATCH_ULTRA_2,
    IGNORING_APPLE_WATCH_STRAP_TYPE, IGNORING_APPLE_WATCH_WITHOUT_YEAR_RELEASE, MINIMUM_PRICE_FOR_BRAND,
    IGNORING_APPLE_WATCH_RECOGNITION
)

logger = logging.getLogger(__name__)


def find_best_apple_watch_model(user_input: str) -> Optional[str] :


    brand_data = PRODUCT_LIBRARY.get("Apple Watch", {})
    if not brand_data :
        logger.warning("[find_best_apple_watch_model] Нет 'Apple Watch' в PRODUCT_LIBRARY.")
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
                    f"[find_best_apple_watch_model] Совпадение alias='{alias}' -> модель='{model_name}'"
                )
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_apple_watch_model] Ничего не найдено среди watch-моделей.")
        return None

    # Выберем запись, у которой alias длиннее
    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(
        f"[find_best_apple_watch_model] Лучшая модель='{best_model}' (alias='{best_alias}')"
    )
    return best_model


def parse_apple_watch_product(cleaned_line: str, model: str, line: str) -> dict:
    """
    Парсит дополнительные атрибуты (case_size, case_type, strap_type, strap_size, year_release)
    для «Apple Watch».

    Параметры:
    ----------
    cleaned_line: str
        Очищенная строка (без цены и артикулов).
    model: str
        Модель (например, "AW Series 10").

    Возвращает:
    ----------
    dict
        Словарь извлечённых атрибутов. Например:
        {
            "case_size": "49mm",
            "year_release": "2024",
            "case_type": "Jet Black",
            "strap_type": "Sport Band",
            "strap_size": "S/M"
        }
        Если атрибутов меньше заданного минимума, возвращается пустой словарь {}.

    Дополнительная логика:
    ----------------------
    - Сортируем алиасы по длине (убывание), чтобы «Sport Band Starlight»
      проверялся раньше «Sport Band» и не «перебивался» коротким совпадением.
    - Если находим совпадение, добавляем его в список найденных для данного attr_name,
      а затем выбираем «самую длинную» подстроку.
    - Новый атрибут: «year_release» (год выпуска).
    - Если распознано меньше необходимого количества атрибутов, возвращаем {}.
    - Для определённых моделей и case_type игнорируем strap_type согласно IGNORING_APPLE_WATCH_STRAP_TYPE.
    - Для определённых моделей без указанного year_release товар не сохраняется согласно IGNORING_APPLE_WATCH_WITHOUT_YEAR_RELEASE.
    """

    # Достаём описание атрибутов Apple Watch из PRODUCT_LIBRARY
    attributes = PRODUCT_LIBRARY["Apple Watch"][model]["attributes"]
    extracted_attributes = {}
    # Сохраним для case_type использованный alias, чтобы потом сверяться со словарём спецправил
    case_type_alias = None

    for attr_name, attr_info in attributes.items():
        attr_aliases = attr_info["aliases"]

        found_aliases = []
        # Ищем все возможные совпадения по атрибуту
        for value, aliases in attr_aliases.items():
            # Чтобы более специфичные алиасы проверялись в первую очередь
            sorted_aliases = sorted(aliases, key=len, reverse=True)

            for alias in sorted_aliases:
                # Новый паттерн: если строка содержит "ultra" и "blue/black",
                # то пропускаем алиасы "blue" и "black", чтобы "blue/black" парсился как единое целое.
                if "ultra" in cleaned_line.lower() and "blue/black" in cleaned_line.lower() and str(alias).lower() in {"blue", "black"}:
                    logger.debug(
                        f"[Apple Watch parser] Пропускаем alias '{alias}' так как найден паттерн ultra и blue/black."
                    )
                    continue

                pattern = re.compile(rf'\b{re.escape(alias)}\b', re.IGNORECASE)
                if pattern.search(cleaned_line):
                    found_aliases.append((alias, value))
                    # НЕ прерываемся: ищем вдруг ещё более длинный алиас

        if found_aliases:
            # Выбираем из найденных тот алиас, у которого сама строка длиннее — он считается «точнее»
            best_alias, best_value = max(found_aliases, key=lambda x: len(x[0]))
            extracted_attributes[attr_name] = best_value

            # Если атрибут — case_type, сохраняем alias для проверки спец. правила
            if attr_name == "case_type":
                case_type_alias = best_alias

            logger.debug(
                f"[Apple Watch parser] Для attr='{attr_name}' выбрали value='{best_value}' "
                f"(alias='{best_alias}', len={len(best_alias)})"
            )

            # ВАЖНО: «Вырезаем» найденный алиас из строки (чтобы не дублировать в других атрибутах)
            cleaned_line = re.sub(
                rf'\b{re.escape(best_alias)}\b',
                '',  # заменяем на пустую строку
                cleaned_line,
                flags=re.IGNORECASE
            ).strip()
        else:
            logger.debug(f"[Apple Watch parser] Для attr='{attr_name}' ничего не найдено.")

    for ignore_word in IGNORING_APPLE_WATCH_RECOGNITION:
        # Используем \b, чтобы не совпадать по подстрокам вроде "WifiHotspot"
        pattern = re.compile(rf"\b{re.escape(ignore_word.lower())}\b", re.IGNORECASE)
        if pattern.search(cleaned_line.lower()):
            logger.debug(f"[parse_apple_iphone_product] Найдено слово-исключение '{ignore_word}' => возвращаем {{}}.")
            return {}

    # --- Дальше ваша логика дополнительных правил ---
    # 1) Спец. правило для case_size
    if model in SPECIAL_RULE_CASE_SIZE_APPLE_WATCH:  # проверил
        default_case_size = SPECIAL_RULE_CASE_SIZE_APPLE_WATCH[model]
        if "case_size" not in extracted_attributes:
            extracted_attributes["case_size"] = default_case_size
            logger.debug(
                f"[Apple Watch parser] Для модели '{model}' не указано case_size, "
                f"ставим по умолчанию '{default_case_size}'"
            )

    # 2) Спец. правило для Ultra 2 (SPECIAL_RULE_YEAR_RELEASE_APPLE_WATCH_ULTRA_2)
    # Для модели "AW Ultra 2": если не найден атрибут "year_release", но найден атрибут "case_type"
    # и его значение входит в список значений из SPECIAL_RULE_YEAR_RELEASE_APPLE_WATCH_ULTRA_2,
    # то устанавливаем "year_release" равным соответствующему ключу (например, "2024" или "2023").
    if model == "AW Ultra 2" and "year_release" not in extracted_attributes:
        if "case_type" in extracted_attributes:
            # Приводим значение атрибута к нижнему регистру и удаляем лишние пробелы
            case_type_value = extracted_attributes["case_type"].strip().lower()
            for year, case_types in SPECIAL_RULE_YEAR_RELEASE_APPLE_WATCH_ULTRA_2.items():
                # Сравниваем тоже в нижнем регистре
                if case_type_value in (ct.strip().lower() for ct in case_types):
                    extracted_attributes["year_release"] = year
                    logger.debug(
                        f"[Apple Watch parser] Для модели '{model}' и case_type '{extracted_attributes['case_type']}' "
                        f"проставляем year_release '{year}' согласно SPECIAL_RULE_YEAR_RELEASE_APPLE_WATCH_ULTRA_2."
                    )
                    break

    # 2.1) Спец. правило для AW Ultra 2: если не найдены атрибуты "year_release" и "case_type"
    if model == "AW Ultra 2" :
        if "year_release" not in extracted_attributes and "case_type" not in extracted_attributes :
            extracted_attributes["year_release"] = "2023"
            extracted_attributes["case_type"] = "Titanium"
            logger.debug(
                f"[Apple Watch parser] Для модели '{model}' не найдены 'year_release' и 'case_type', "
                "проставляем year_release '2023' и case_type 'Titanium' согласно правилу 2.1."
            )
        elif "year_release" in extracted_attributes and "case_type" not in extracted_attributes :
            extracted_attributes["case_type"] = "Titanium"
            logger.debug(
                f"[Apple Watch parser] Для модели '{model}' найден 'year_release', но отсутствует 'case_type', "
                "проставляем case_type 'Titanium' согласно правилу 2.1."
            )

    # 3) Игнорирование strap_type для некоторых сочетаний
    if model in IGNORING_APPLE_WATCH_STRAP_TYPE:
        current_case_type = extracted_attributes.get("case_type")
        current_strap_type = extracted_attributes.get("strap_type")
        if current_case_type and current_strap_type:
            ignoring_strap_types = IGNORING_APPLE_WATCH_STRAP_TYPE[model].get(current_case_type, [])
            if current_strap_type in ignoring_strap_types:
                del extracted_attributes["strap_type"]
                logger.debug(
                    f"[Apple Watch parser] Для '{model}' и case_type '{current_case_type}' "
                    f"strap_type '{current_strap_type}' игнорируется. Удаляем 'strap_type'."
                )

    # 4) Игнорирование товаров без year_release для некоторых моделей
    if model in IGNORING_APPLE_WATCH_WITHOUT_YEAR_RELEASE:
        if "year_release" not in extracted_attributes:
            logger.debug(
                f"[Apple Watch parser] Для модели '{model}' не указан year_release, "
                "товар не сохраняем (возвращаем пустой словарь)."
            )
            return {}

    # 5) Логика для извлечения strap_size из line, если он там есть
    if "strap_size" not in extracted_attributes :
        # Парсим strap_size из line, если он там присутствует
        strap_size_match = re.search(r'(\bS/M\b|\bM/L\b|\bS\b|\bM\b|\bL\b)', line)
        if strap_size_match :
            extracted_attributes["strap_size"] = strap_size_match.group(0)

    logger.debug(f"[Apple Watch parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes

def handle_apple_watch_product(
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
    «Склейка» итогового названия для Apple Watch с учётом распознанных атрибутов
    и сохранение результата в USER_DATA.

    Возвращает:
    ----------
    bool
        True, если товар обработан и сохранён как сложный.
        False, если товар должен быть обработан как простой.
    """
    from utils import add_or_update_product, apply_special_rules_iphone

    # 1.0) Парсим дополнительные атрибуты (case_size, year_release, case_type, strap_type, strap_size)
    extracted_attributes = parse_apple_watch_product(cleaned_line, model, line)


    # 1.1) Проверяем, есть ли спец. алиас
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 1.2) Проверяем «обязательные» атрибуты, если нет спец. алиаса
    if not has_special_alias:
        required_attrs_mapping = {
            "aw se 2" : {"case_size"},
            "aw s8" : {"case_size"},
            "aw s9" : {"case_size"},
            "aw s10" : {"case_size"},
            "aw ultra 2" : {"case_size", "year_release", "case_type"}
        }

        required_attrs = required_attrs_mapping.get(model.lower(), set())
        if required_attrs is None:
            logger.info(f"[handle_apple_watch_product] Модель '{model}' не найдена => return False")
            return False

        recognized_keys = set(extracted_attributes.keys())
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs:
            logger.info(
                f"[handle_apple_watch_product] Для '{model}' не хватает атрибутов {missing_attrs} => return False"
            )
            return False #"case_size", "year_release", "case_type", "strap_type", "strap_size"

    # 2. Склеиваем итоговое название.
    final_product_name = f"{model}"
    for attr in ["case_size", "year_release", "case_type", "strap_type", "strap_size"]:
        if attr in extracted_attributes:
            final_product_name += f" {extracted_attributes[attr]}"

    logger.info(f"[Apple Watch parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # НОВОЕ ПРАВИЛО: Если это Apple Watch и список countries пуст, проставляем "США" по умолчанию.
    brand = "Apple Watch"  # жёстко указываем, т. к. функция handle_apple_watch_product вызывается именно для Apple Watch
    if brand == "Apple Watch" and not countries:
        logger.debug("[Apple Watch parser] Не указана страна, ставим 'США' по умолчанию.")
        countries = ["США"]
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # 3. Применяем специальные правила (если есть) и добавляем в USER_DATA
    if countries:
        # Если есть несколько стран (несколько флагов)
        for country in countries:
            selected_variant = apply_special_rules_iphone(
                model_group=model,
                country=country,
                variant=final_product_name,
                product_library=PRODUCT_LIBRARY,
                brand="Apple Watch"
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
                brand
            )
    else:
        selected_variant = apply_special_rules_iphone(
            model_group=model,
            country="",
            variant=final_product_name,
            product_library=PRODUCT_LIBRARY,
            brand="Apple Watch"
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
            brand
        )

    logger.debug("[Apple Watch parser] Успешно обработано как сложный товар. Возвращаем True.")
    return True  # Успешно обработано как сложный товар


def handle_complex_apple_watch(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки watch:
      1) find_best_apple_watch_model — чтобы не коротком алиасе,
         а собрать все совпадения и выбрать лучший.
      2) handle_apple_watch_product — парсит атрибуты.
    """
    best_model = find_best_apple_watch_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_apple_watch] Не нашли модель Apple Watch для '{cleaned_line}'")
        return False

    brand = "Apple Watch"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_cleaner] Цена товара ({price}) ниже минимальной "
                f"({min_price}) для бренда '{brand}'. Товар не сохраняем."
            )
            return False

    logger.info(f"[handle_complex_apple_watch] Лучшая модель Apple Watch: '{best_model}'")

    # Теперь парсим атрибуты и сохраняем
    result = handle_apple_watch_product(
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

