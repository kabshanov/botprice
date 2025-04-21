# dyson_accessories_utils.py

import logging
import re
from typing import Optional, List

from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, COLOR_FOR_VERSION_VERSION_ACCESSORIES, MINIMUM_PRICE_FOR_BRAND
)

logger = logging.getLogger(__name__)


def normalize_comment(comment: str) -> str :
    """
    Нормализует строку comment, заменяя шаблоны (например, цвета)
    на канонические значения согласно заданному mapping.
    """
    mapping = {
        # Перевод цвета
        'черный' : 'black',
        'чёрный' : 'black',
        'темный' : 'black',
        'тёмный' : 'black',
        'никель' : 'nickel',
        'серый' : 'gray',
        'серебристый' : 'silver',
        'графитовый' : 'graphite',

        'синий' : 'blue',
        'голубой' : 'blue',
        'бирюзовый' : 'turquoise',
        'лазурный' : 'azure',
        'индиго' : 'indigo',

        'золотой' : 'gold',
        'желтый' : 'yellow',
        'жёлтый' : 'yellow',
        'янтарный' : 'amber',
        'оранжевый' : 'orange',
        'медный' : 'copper',
        'бронзовый' : 'bronze',

        'белый' : 'white',
        'кремовый' : 'cream',
        'бежевый' : 'beige',

        'зеленый' : 'green',
        'зелёный' : 'green',
        'изумрудный' : 'emerald',
        'оливковый' : 'olive',
        'лаймовый' : 'lime',
        'хаки' : 'khaki',

        'красный' : 'red',
        'бордовый' : 'burgundy',
        'алый' : 'scarlet',
        'вишневый' : 'cherry',
        'малиновый' : 'crimson',

        'розовый' : 'pink',
        'пурпурный' : 'purple',
        'фиолетовый' : 'violet',
        'лавандовый' : 'lavender',

        'коричневый' : 'brown',
        'шоколадный' : 'chocolate',
        'кофейный' : 'coffee',
        'каштановый' : 'chestnut',

        'прозрачный' : 'transparent',
        'многоцветный' : 'multicolor',
        'радужный' : 'rainbow',
        'grey' : 'gray',
        'дайсон' : 'dyson',
    }

    storage_patterns = list(mapping.keys())
    escaped_patterns = [re.escape(p) for p in storage_patterns]
    storage_regex = re.compile(r'\b(' + '|'.join(escaped_patterns) + r')\b', re.IGNORECASE)

    def replace_storage(match) :
        matched_text = match.group(0).lower()
        replacement = mapping.get(matched_text, matched_text)
        logger.debug(f"[normalize_comment] Замена '{matched_text}' → '{replacement}'")
        return replacement

    comment_before = comment
    comment = storage_regex.sub(replace_storage, comment)
    logger.debug(f"[normalize_comment] После замены шаблонов: '{comment_before}' => '{comment}'")

    # Объединяем множественные пробелы в один
    comment = re.sub(r'\s+', ' ', comment).strip()
    logger.debug(f"[normalize_comment] Итоговая нормализованная строка: '{comment}'")
    return comment


def parse_comment_only(comment: str) -> dict :
    """
    Принимает строку комментария, выполняет её нормализацию (если необходимо)
    и возвращает пустой словарь.

    Используйте эту функцию, если дальнейший парсинг атрибутов не требуется.
    """
    normalized_comment = normalize_comment(comment)
    logger.info(
        f"[parse_comment_only] Нормализованный комментарий: '{normalized_comment}', возвращаем пустой результат.")
    # Возвращаем пустой словарь (то есть «пустое» значение)
    return {}


def find_best_dyson_accessories_model(user_input: str) -> Optional[str] :
    """
    Ищет модель Dyson accessories.
    Не останавливается на первом совпадении: для каждой модели перебирает aliases,
    проверяет регулярным выражением и выбирает ту, у которой alias самый длинный.

    Возвращает строку (название модели) или None, если совпадения не найдены.
    """
    brand_data = PRODUCT_LIBRARY.get("Аксессуары Dyson", {})
    if not brand_data :
        logger.warning("[find_best_dyson_accessories_model] Нет 'Dyson Accessories' в PRODUCT_LIBRARY.")
        return None

    user_input_lower = user_input.lower()
    found_entries = []  # Список кортежей (model_name, alias)

    for model_name, model_info in brand_data.items() :
        aliases = model_info.get("aliases", [])
        for alias in aliases :
            alias_lower = alias.lower()
            pattern = re.compile(rf"\b{re.escape(alias_lower)}\b", re.IGNORECASE)
            if pattern.search(user_input_lower) :
                logger.debug(f"[find_best_dyson_accessories_model] Совпадение alias='{alias}' -> модель='{model_name}'")
                found_entries.append((model_name, alias))

    if not found_entries :
        logger.info("[find_best_dyson_accessories_model] Ничего не найдено среди Dyson accessories-моделей.")
        return None

    best_model, best_alias = max(found_entries, key=lambda x : len(x[1]))
    logger.info(f"[find_best_dyson_accessories_model] Лучшая модель='{best_model}' (alias='{best_alias}')")
    return best_model


def parse_dyson_accessories_product(cleaned_line: str, comment: str, top_level_model: str) -> dict :
    """
    Парсит дополнительные атрибуты для Dyson accessories.
    Теперь учитывает как основную строку (cleaned_line), так и комментарий (comment).

    Возвращает словарь извлечённых атрибутов.
      - Если обнаружен специальный алиас, добавляется "final_product_name".
      - Если атрибутов меньше заданного минимума и нет спец. алиаса,
        возвращается пустой словарь {}.
    """
    extracted_attributes = {}

    brand_data = PRODUCT_LIBRARY.get("Аксессуары Dyson", {})
    if top_level_model not in brand_data :
        logger.warning(
            f"[parse_dyson_accessories_product] Модель '{top_level_model}' отсутствует в 'Dyson Accessories'.")
        return {}

    attributes = brand_data[top_level_model]["attributes"]

    # Объединяем cleaned_line и comment для расширенного поиска
    search_text = f"{cleaned_line} {comment}" if comment else cleaned_line

    # Перебор атрибутов и их алиасов
    for attr_name, attr_info in attributes.items() :
        attr_aliases = attr_info["aliases"]
        found_aliases = []
        for value, aliases in attr_aliases.items() :
            sorted_aliases = sorted(aliases, key=len, reverse=True)
            for alias in sorted_aliases :
                pattern = re.compile(rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])', re.IGNORECASE)
                if pattern.search(search_text) :
                    found_aliases.append((alias, value))
        if found_aliases :
            best_alias, best_value = max(found_aliases, key=lambda x : len(x[0]))
            extracted_attributes[attr_name] = best_value
            logger.debug(
                f"[accessories parser] Для attr='{attr_name}' выбрали value='{best_value}' (alias='{best_alias}', len={len(best_alias)})")
        else :
            logger.debug(f"[accessories parser] Для attr='{attr_name}' ничего не найдено в строке.")

    # Дополнительный блок: определение цвета на основе версии
    if top_level_model.lower() == "аксессуары dyson" and "version" in extracted_attributes :
        version_val = extracted_attributes["version"]
        if version_val in COLOR_FOR_VERSION_VERSION_ACCESSORIES :
            color_mapping = COLOR_FOR_VERSION_VERSION_ACCESSORIES[version_val]
            found_color = None
            for candidate_color, aliases in color_mapping.items() :
                sorted_aliases = sorted(aliases, key=len, reverse=True)
                for alias in sorted_aliases :
                    pattern = re.compile(rf'(?<![A-Za-z0-9+]){re.escape(alias)}(?![A-Za-z0-9+])', re.IGNORECASE)
                    if pattern.search(search_text) :
                        found_color = candidate_color
                        logger.debug(
                            f"[parse_dyson_accessories_product] Найден color '{found_color}' (alias: '{alias}') для версии '{version_val}' с помощью COLOR_FOR_VERSION_VERSION_ACCESSORIES.")
                        break
                if found_color :
                    break
            if found_color :
                extracted_attributes["color"] = found_color
            else :
                logger.debug(
                    f"[parse_dyson_accessories_product] Не удалось определить color из COLOR_FOR_VERSION_VERSION_ACCESSORIES для версии '{version_val}'.")
        else :
            logger.debug(
                f"[parse_dyson_accessories_product] Версия '{version_val}' отсутствует в COLOR_FOR_VERSION_VERSION_ACCESSORIES.")

    logger.debug(f"[dyson accessories parser] Итоговые атрибуты: {extracted_attributes}")
    return extracted_attributes


def handle_dyson_accessories_product(
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
    «Склейка» итогового названия для Dyson аксессуаров с учётом распознанных атрибутов,
    включая данные, полученные из комментария (предварительно нормализованные),
    и сохранение результата в USER_DATA.
    Возвращает True, если товар добавлен, иначе False (для дальнейшей обработки как простой товар).
    """
    from utils import add_or_update_product, apply_special_rules_iphone

    # 1. Нормализуем комментарий перед дальнейшим парсингом
    comment = normalize_comment(comment)

    # 2. Парсим дополнительные атрибуты с учётом информации из нормализованного комментария
    extracted_attributes = parse_dyson_accessories_product(cleaned_line, comment, model)

    # 3. Проверяем наличие специального алиаса ("final_product_name")
    has_special_alias = ("final_product_name" in extracted_attributes)

    # 4. Если специального алиаса нет, проверяем обязательные атрибуты
    if not has_special_alias :
        required_attrs_mapping = {
            "аксессуары dyson" : {"version", "color"},
        }
        required_attrs = required_attrs_mapping.get(model.lower(), set())
        if required_attrs is None :
            logger.info(
                f"[handle_dyson_accessories_product] Модель '{model}' не найдена в required_attrs_mapping => return False")
            return False

        recognized_keys = set(extracted_attributes.keys())
        logger.info(f"[handle_dyson_accessories_product] Распознано атрибутов: {recognized_keys} для модели='{model}'")
        missing_attrs = required_attrs - recognized_keys
        if missing_attrs :
            logger.info(
                f"[handle_dyson_accessories_product] Не хватает атрибутов {missing_attrs} для model='{model}' => return False")
            return False

        logger.info(
            f"[handle_dyson_accessories_product] Все обязательные атрибуты ({required_attrs}) найдены для '{model}'.")

    # 5. Формирование итогового названия (final_product_name)
    final_product_name = None
    if has_special_alias :
        final_product_name = extracted_attributes["final_product_name"]
        logger.info(f"[Dyson Accessories parser] Используем специальное итоговое название: '{final_product_name}'")
    else :
        if model.lower().startswith("аксессуары dyson") :
            product_base = model[len("аксессуары dyson") :].strip().capitalize()
            final_product_name = product_base
            for attr in ["version", "color"] :
                if attr in extracted_attributes :
                    final_product_name += f" {extracted_attributes[attr]}"
            final_product_name = final_product_name.lstrip()

    if final_product_name is None :
        final_product_name = "Unknown Dyson accessories"

    logger.info(f"[Dyson Accessories parser] Итоговое наименование сложного товара: '{final_product_name}'")

    # 6. Если страна не указана, ставим пустую строку
    brand = "Аксессуары Dyson"
    if brand == "Аксессуары Dyson" and not countries :
        logger.debug("[Dyson Accessories parser] Не указана страна => ''")
        countries = [""]

    # 7. Применяем специальные правила и сохраняем товар
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

    logger.debug("[Dyson Accessories parser] Успешно => True")
    return True


def handle_complex_dyson_accessories(
        line: str,
        cleaned_line: str,
        countries: List[str],
        price: int,
        supplier: str,
        comment: str,
        user_id: int
) -> bool :
    """
    Точка входа для обработки Dyson accessories:
      1) Определение лучшей модели с помощью find_best_dyson_accessories_model,
         чтобы собрать все совпадения и выбрать наиболее подходящий alias.
      2) Парсинг атрибутов, формирование итогового названия и сохранение товара через handle_dyson_accessories_product.
    """
    best_model = find_best_dyson_accessories_model(cleaned_line)
    if not best_model :
        logger.info(f"[handle_complex_dyson_accessories] Не нашли модель Dyson accessories для '{cleaned_line}'")
        return False

    brand = "Аксессуары Dyson"
    if brand in MINIMUM_PRICE_FOR_BRAND :
        min_price = MINIMUM_PRICE_FOR_BRAND[brand]
        if price < min_price :
            logger.info(
                f"[handle_complex_dyson_accessories] Цена товара ({price}) ниже минимальной ({min_price}) для бренда '{brand}'. Товар не сохраняем.")
            return False

    logger.info(f"[handle_complex_dyson_accessories] Лучшая модель Dyson accessories: '{best_model}'")
    result = handle_dyson_accessories_product(
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


