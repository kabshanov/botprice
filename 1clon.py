#utils.py

import re
import unicodedata
import emoji
import logging
import regex

from functools import lru_cache
from typing import Optional, Tuple, List, Dict, Union
from rapidfuzz import process, fuzz

from telegram import Update, Message, User
from telegram.ext import ContextTypes

from db_utils import add_product, track_user_activity

# Импортируем общие данные из shared_data
from shared_data import (
    PRODUCT_LIBRARY, USER_DATA, COMPLEX_BRANDS, MINIMUM_PRICE_FOR_BRAND,
    COUNTRY_EMOJI_MAP, ALLOWED_COMMENT_EMOJIS, EMOJIS_COLORS, SPECIAL_RULES_IPHONE,
    PATTERNS_FOR_COMPLEX_BRAND_SEARCH, FIRST_WORDS_PATTERNS_STRING_NOT_APPLY_TO_PRODUCT,
    COUNTRY_WORD_MAP, COMMENT_ADD, IGNORING_COMMENT
)

# ---------------------- НАСТРОЙКА ЛОГИРОВАНИЯ -------------------------------------

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ---------------------- ОСНОВНЫЕ ФУНКЦИИ ------------------------------------------

# =============================================================================
# Глобальные константы и предкомпилированные регулярные выражения

# Регулярное выражение для поиска кандидатов на цену
'''
PRICE_PATTERN = re.compile(
    r'(?<![\dA-Za-z])'                    # Слева не должно быть цифры или буквы
    r'[-–—]?'                             # Опциональное тире
    r'(?:'                                
    r'\d{1,3}(?:[.,’\s]\d{3})+'           # 1–3 цифры, затем одна или несколько групп из разделителя и 3 цифр
    r'|'                                  # ИЛИ
    r'\d+'                                # просто последовательность цифр
    r')'                                  
    r'(?:[.,]00)?'                        # дополнительно (опционально) .00 или ,00
    r'\s*[₽$€¥]?'                         # Опциональный знак валюты с пробелами
    r'(?!\d)'                             # После числа не должна идти цифра
)
'''

PRICE_PATTERN = re.compile(
    r'(?<![\dA-Za-z])'           # Слева не должно быть цифры/буквы
    r'[-–—]?'                    # Опционально тире
    r'(?:'
    r'\d{1,3}(?:[.,’\s]\d{3})+'  # 1–3 цифры, затем одна или несколько групп "разделитель + 3 цифры"
    r'|'                        
    r'\d+'                       # ИЛИ просто последовательность цифр
    r')'
    r'(?:[.,]00)?'               # Опционально ".00" или ",00"
    r'\s*[₽$€¥]?'
    r'(?!\d)'                    # Справа не должно идти цифра
)

# Регулярки для очистки
CURRENCY_REGEX     = re.compile(r'[₽$€¥]')
LEADING_DASH_REGEX = re.compile(r'^[-–—]+')
# Удаляем только точку, запятую, апостроф/акут (но уже после того, как попробовали «особый» шаблон)
PUNCTUATION_REGEX  = re.compile(r'[.,’\']')
NON_DIGIT_PATTERN  = re.compile(r'[^\d\s]')

# "Особый" шаблон для случаев вида:
#   1) "108 500,00"       -> группировка тысячи пробелом + ",00" на конце
#   2) "1 234 567,00"     -> несколько групп по 3 цифры
#   3) Можно расширить, если нужно ("1 234 567 890,00" и т.д.)
#   4) Позволяем \xa0 (неразрывный пробел) вместо обычного пробела
SPECIAL_PATTERN = re.compile(r'^\d{1,3}(?:[ \u00A0]\d{3})+,00$')

# Предкомпилированные шаблоны для словарей комментариев
COMMENT_ADD_PATTERN = re.compile(
    r'\b(?:%s)\b' % "|".join(re.escape(word) for word in COMMENT_ADD)  # Без include_symbols
    if len(COMMENT_ADD) > 1
    else r'\b%s\b' % re.escape(COMMENT_ADD[0]),
    flags=re.IGNORECASE
)

IGNORING_COMMENT_PATTERN = re.compile(
    r'\b(?:%s)\b' % "|".join(re.escape(word) for word in IGNORING_COMMENT)  # Без include_symbols
    if len(IGNORING_COMMENT) > 1
    else r'\b%s\b' % re.escape(IGNORING_COMMENT[0]),
    flags=re.IGNORECASE
)

# В разделе с регулярными выражениями:
CURRENCY_SYMBOLS = r'[₽рРуб$€]'  # Добавить все актуальные символы
# =============================================================================

def is_multiline_price_message(text: str) -> bool:
    """
    Проверяем, встречается ли в сообщении шаблон 'от <число>'.
    Если встречается, считаем, что это многострочный прайс.
    """
    import re  # На случай, если re ещё не импортирован внутри этой области (но у вас вверху уже есть)

    # Ищем в тексте хотя бы одно "от 1" или "от 3" (от любой цифры)
    pattern = r'(?i)\bот\s*\d+'
    match = re.search(pattern, text)
    return bool(match)


def parse_multiline_price(text: str) :
    """
    Разбирает сообщение из нескольких строк, где формат примерно такой:
      • Название товара
      От 1 - 62000
      От 3 - 61900    (игнорируем, нам надо только "от 1")

    Возвращает список словарей вида:
      [
        {"name": "Mi 15 12/512 White Leica", "price": 62000},
        {"name": "Airpods 4 USB-C MXP63", "price": 9900},
        ...
      ]
    Если не найдёт ни одного "от 1", вернёт пустой список.
    """
    import re
    lines = text.split('\n')
    results = []
    current_product_name = None

    # Шаблон, который ловит строку "от 1 ... цена".
    # Например: "От 1 - 62000", "от 1шт. -> 9500"
    # group(2) будет сама цифра цены.
    pattern_from1 = re.compile(r'(?i)(от|От)\s*1\s*(?:шт\.?)?\s*[-–—>]+\s*(\d+)', re.IGNORECASE)

    for raw_line in lines :
        line = raw_line.strip()
        if not line :
            continue  # пропускаем пустые строки

        match = pattern_from1.search(line)
        if match :
            # Если нашли "от 1" + цена
            price_str = match.group(2)  # то, что захватили в (\d+)
            price = int(price_str)

            # Если у нас уже есть current_product_name, считаем, что название идет "сверху"
            if current_product_name :
                product_name = current_product_name
            else :
                # Если название не запомнили, берем текст до "от 1"
                product_name = line[:match.start()].strip('•-–—').strip()
                if not product_name :
                    product_name = "Товар без названия"

            results.append({"name" : product_name, "price" : price})
        else :
            # Строка без "от 1" => вероятно это название товара
            # Запомним как current_product_name
            possible_name = line.strip('•-–—').strip()
            if possible_name :
                current_product_name = possible_name

    return results


def normalize_product_name(product_name: str) -> str:
    logger.debug(f"[normalize_product_name] Исходная строка (до нормализации): '{product_name}'")

    # Сохраняем цветовые эмодзи перед обработкой
    color_emojis = [c for c in product_name if c in EMOJIS_COLORS]
    leading_color_emojis = []
    clusters = regex.findall(r'\X', product_name)

    for cluster in clusters :
        if cluster in EMOJIS_COLORS :
            leading_color_emojis.append(cluster)
        else :
            break  # Прерываем цикл при первом не-эмодзи

    # 1) Заменяем специфические символы (турецкие и пр.)
    replacements = {
        'ı': 'i',
        'İ': 'I',
    }
    for old, new in replacements.items():
        product_name = product_name.replace(old, new)

    # 2) Unicode NFKC (нормализация)
    product_name = unicodedata.normalize('NFKC', product_name)

    # 3) Приводим к нижнему регистру и подрезаем крайние пробелы
    product_name = product_name.lower().strip()

    # 4)**НОВЫЙ ШАГ: Отделение цифр от слов с паттернами "pro" и "max"**
    # Проверяем наличие паттернов "pro" или "max" после цифр и отделяем их пробелом
    pro_max_pattern = re.compile(r'(\d+)(pro|max|plus)\b', re.IGNORECASE)
    product_name_before_pro_max = product_name  # Для отладки
    product_name = pro_max_pattern.sub(r'\1 \2', product_name)
    if product_name_before_pro_max != product_name :
        logger.debug(
            f"[normalize_product_name] После отделения цифр от 'Pro'/'Max': '{product_name_before_pro_max}' → '{product_name}'")

    # 5. Удаление скобок "(" и ")"
    # (НОВЫЙ КОММЕНТАРИЙ) Вместо полного удаления скобок мы подменяем их на пробел,
    # чтобы то, что было внутри, отделилось пробелом от остального текста.
    product_name = re.sub(r'[()]', ' ', product_name)

    # Убираем дубли пробелов, если вдруг получилось несколько подряд
    product_name = re.sub(r'\s+', ' ', product_name).strip()

    logger.debug(f"[normalize_product_name] После удаления скобок и нормализации: '{product_name}'")

    # 6. **НОВЫЙ БЛОК: Отделение паттерна "xxmm"**
    # Если встречается шаблон, где два числа и "mm" идут слитно с последующим текстом (например, "46mmJet"),
    # вставляем пробел между "mm" и следующим символом.
    xxmm_pattern = re.compile(r'(\d{2}mm)([a-zA-Z])', re.IGNORECASE)
    product_name_before_xxmm = product_name  # для отладки
    product_name = xxmm_pattern.sub(r'\1 \2', product_name)
    if product_name != product_name_before_xxmm:
        logger.debug(f"[normalize_product_name] После отделения 'xxmm' от текста: '{product_name_before_xxmm}' → '{product_name}'")



    # 7) Заменяем смешанные слова с кириллицей на чисто латинские
    #    (Теперь учитываем и наличие цифр)

    # Соответствие кириллических букв латинским
    cyrillic_to_latin = {
        'а': 'a', 'в': 'v', 'е': 'e', 'к': 'k', 'м': 'm',
        'н': 'n', 'о': 'o', 'р': 'p', 'с': 'c', 'т': 't',
        'у': 'y', 'х': 'x', 'ё': 'e', 'ж': 'zh', 'й': 'i',
        'ю': 'yu', 'я': 'ya', 'б': 'b', 'г': 'g', 'д': 'd',
        'з': 'z', 'и': 'i', 'л': 'l', 'п': 'p', 'ф': 'f',
        'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e',
    }

    def replace_cyrillic(word):
        return ''.join(cyrillic_to_latin.get(char, char) for char in word)

    words = product_name.split()
    new_words = []

    for word in words:
        has_latin = bool(re.search(r'[a-z]', word))     # есть ли латиница
        has_cyrillic = bool(re.search(r'[а-яё]', word)) # есть ли кириллица
        has_digit = bool(re.search(r'\d', word))        # есть ли цифры

        # Условие: если есть кириллица и (латиница или цифры), заменяем кириллич. буквы на латиницу
        if has_cyrillic and (has_latin or has_digit):
            logger.debug(f"[normalize_product_name] Смешанное слово (кириллица + латиница/цифры): '{word}'")
            new_word = replace_cyrillic(word)
            logger.debug(f"[normalize_product_name] После замены: '{new_word}'")
            new_words.append(new_word)
        else:
            new_words.append(word)

    product_name = ' '.join(new_words)
    logger.debug(f"[normalize_product_name] После замены смешанных слов: '{product_name}'")

    # 8) Замена шаблонов хранения данных на соответствующие значения
    # Создаем функцию для замены на основе соответствий
    mapping = {
        # Перевод цвета
        'strligt' : 'starlight',
        'starlit' : 'starlight',
        'antrazit' : 'anthrazit',
        'sylver' : 'silver',

    }

    # Генерируем список всех ключей из mapping
    storage_patterns = list(mapping.keys())  # ['strligt', 'starlit', '64gb', '128gb', ...]

    escaped_patterns = [re.escape(p) for p in storage_patterns]
    storage_regex = re.compile(r'\b(' + '|'.join(escaped_patterns) + r')\b', re.IGNORECASE)

    def replace_storage(match) :
        matched_text = match.group(0).lower()
        replacement = mapping.get(matched_text, matched_text)
        logger.debug(f"[normalize_product_name] Замена '{matched_text}' → '{replacement}'")
        return replacement

    product_name_before = product_name
    product_name = storage_regex.sub(replace_storage, product_name)
    logger.debug(f"[normalize_product_name] После замены шаблонов: '{product_name_before}' => '{product_name}'")

    # 9) Объединяем множественные пробелы в один
    product_name = re.sub(r'\s+', ' ', product_name).strip()

    normalized = f"{product_name} {''.join(color_emojis)}".strip()
    return normalized

    logger.debug(f"[normalize_product_name] Итоговая нормализованная строка: '{product_name}'")
    return product_name

def build_alias_dict(product_library: dict) -> dict:
    alias_dict = {}
    for brand, models in product_library.items():
        for model_group, details in models.items():

            if isinstance(details, dict):
                # Проверяем: сложный товар (имеет 'aliases' и 'attributes')
                if 'aliases' in details and 'attributes' in details:
                    # Сложный товар: не удаляем слово "apple"
                    model_aliases = details.get('aliases', [])
                    for alias in model_aliases:
                        normalized_alias = normalize_product_name(alias)
                        if normalized_alias:
                            alias_dict[normalized_alias] = (brand, model_group, None)
                else:
                    # Простые товары
                    for variant, variant_aliases in details.items():
                        for alias in variant_aliases:
                            normalized_alias = normalize_product_name(alias)
                            if normalized_alias:
                                alias_dict[normalized_alias] = (brand, model_group, variant)
            else:
                logger.warning(f"Unexpected structure: brand='{brand}', model_group='{model_group}'")

    logger.info(f"[build_alias_dict] Построен ALIAS_DICT с {len(alias_dict)} алиасами.")

    # Можно при желании вывести все ключи для отладки:
    # for k, v in alias_dict.items():
    #     logger.debug(f"ALIAS_DICT: '{k}' => {v}")

    return alias_dict

ALIAS_DICT = build_alias_dict(PRODUCT_LIBRARY)

def find_closest_product_name(user_input: str, threshold: float = 96.5) -> Optional[Tuple[str, str, Optional[str]]]:

    logger.info(f"[find_closest_product_name] Ищем для: '{user_input}'")

    # 1) Точное совпадение
    if user_input in ALIAS_DICT:
        brand, model, variant = ALIAS_DICT[user_input]
        logger.info(f"[find_closest_product_name] Точное совпадение: brand='{brand}', model='{model}', variant='{variant}'")
        return (brand, model, variant)

    # 2) Fuzzy-поиск
    best_match, score, _ = process.extractOne(
        user_input,
        ALIAS_DICT.keys(),
        scorer=fuzz.token_set_ratio
    )

    logger.debug(f"[find_closest_product_name] best_match='{best_match}', score={score}")
    if not best_match:
        logger.warning("[find_closest_product_name] Не нашли никакого совпадения.")
        return None

    user_tokens = set(user_input.split())
    best_tokens = set(best_match.split())
    overlap = len(user_tokens & best_tokens)
    total_tokens = max(len(user_tokens), len(best_tokens))
    token_score = (overlap / total_tokens * 100) if total_tokens else 0

    logger.debug(f"[find_closest_product_name] token_score={token_score:.2f}%, threshold={threshold}")

    if token_score < 70:
        logger.warning("[find_closest_product_name] Низкое пересечение токенов, обнуляем score.")
        score = 0

    if score >= threshold:
        brand, model, variant = ALIAS_DICT[best_match]
        logger.info(f"[find_closest_product_name] Найдено: brand='{brand}', model='{model}', variant='{variant}' (score={score}%)")
        return (brand, model, variant)
    else:
        logger.warning(f"[find_closest_product_name] Совпадение < threshold ({score} < {threshold}).")
        return None

@lru_cache(maxsize=1000)
def find_product_cached(user_input: str) -> Optional[Tuple[str, str, Optional[str]]]:
    normalized = normalize_product_name(user_input)
    return find_closest_product_name(normalized)

logging.info(f"SPECIAL_RULES_IPHONE: {list(SPECIAL_RULES_IPHONE.keys())}")

def is_price_line(line: str) -> bool:
    """
    Пример проверочного метода (не вызывается в текущем коде):
    проверяет, содержит ли строка цену.
    """
    price_pattern = r"(?i)\b(?:от\s+\d+\s*[-–—]\s*)?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?|\d+)\s*[₽$€¥]?\b"
    return bool(re.search(price_pattern, line))

def extract_supplier(update: Update) -> str :
    """
    Извлекает информацию о поставщике из пересланного сообщения.
    Возвращает строку с названием поставщика или пустую строку, если поставщик не найден.
    """
    supplier = ""
    message: Message = update.message

    if not message :
        logging.debug("Нет сообщения в обновлении.")
        return supplier

    # 1. Извлечение из forward_from_chat (для сообщений из чатов или каналов)
    forward_from_chat = getattr(message, 'forward_from_chat', None)
    if forward_from_chat :
        logging.debug(f"forward_from_chat: {forward_from_chat}")
    if forward_from_chat and getattr(forward_from_chat, 'title', None) :
        supplier = forward_from_chat.title
        logging.debug(f"Извлечён supplier из forward_from_chat: '{supplier}'")
        return supplier

    # 2. Извлечение из forward_from (для сообщений от пользователей)
    forward_from = getattr(message, 'forward_from', None)
    if forward_from :
        logging.debug(f"forward_from: {forward_from}")
        # Проверяем, является ли forward_from объектом User
        if isinstance(forward_from, User) :
            username = forward_from.username
            if username :
                supplier = f"@{username}"
                logging.debug(f"Извлечён username: '{username}', supplier: '{supplier}'")
            else :
                first_name = forward_from.first_name or ""
                last_name = forward_from.last_name or ""
                supplier = f"{first_name} {last_name}".strip()
                logging.debug(f"Извлечены имена: '{first_name} {last_name}', supplier: '{supplier}'")
        elif isinstance(forward_from, dict) :
            # Если forward_from представлен как словарь
            username = forward_from.get('username')
            if username :
                supplier = f"@{username}"
                logging.debug(f"Извлечён username из dict forward_from: '{username}', supplier: '{supplier}'")
            else :
                first_name = forward_from.get('first_name', "")
                last_name = forward_from.get('last_name', "")
                supplier = f"{first_name} {last_name}".strip()
                logging.debug(
                    f"Извлечены имена из dict forward_from: '{first_name} {last_name}', supplier: '{supplier}'")
        else :
            # Неизвестный тип forward_from
            logging.debug("forward_from имеет неизвестный тип.")

        if supplier :
            return supplier

    # 3. Извлечение из forward_sender_name (если forward_from отсутствует)
    forward_sender_name = getattr(message, 'forward_sender_name', None)
    if forward_sender_name :
        logging.debug(f"forward_sender_name: '{forward_sender_name}'")
        supplier = forward_sender_name
        return supplier

    # 4. Извлечение из forward_origin (специфично для некоторых библиотек и версий API)
    forward_origin = getattr(message, 'forward_origin', None)
    if forward_origin :
        logging.debug(f"forward_origin: {forward_origin}")
        # Проверяем наличие объекта chat в forward_origin
        forward_origin_chat = getattr(forward_origin, 'chat', None)
        if forward_origin_chat and getattr(forward_origin_chat, 'title', None) :
            supplier = forward_origin_chat.title
            logging.debug(f"Извлечён supplier из forward_origin.chat: '{supplier}'")
            return supplier

        # Проверяем наличие объекта sender_user в forward_origin
        forward_origin_sender_user = getattr(forward_origin, 'sender_user', None)
        if forward_origin_sender_user :
            logging.debug(f"forward_origin_sender_user: {forward_origin_sender_user}")
            if isinstance(forward_origin_sender_user, User) :
                username = forward_origin_sender_user.username
                if username :
                    supplier = f"@{username}"
                    logging.debug(
                        f"Извлечён username из forward_origin.sender_user: '{username}', supplier: '{supplier}'")
                else :
                    first_name = forward_origin_sender_user.first_name or ""
                    last_name = forward_origin_sender_user.last_name or ""
                    supplier = f"{first_name} {last_name}".strip()
                    logging.debug(
                        f"Извлечены имена из forward_origin.sender_user: '{first_name} {last_name}', supplier: '{supplier}'")
            elif isinstance(forward_origin_sender_user, dict) :
                # Если forward_origin_sender_user представлен как словарь
                username = forward_origin_sender_user.get('username')
                if username :
                    supplier = f"@{username}"
                    logging.debug(
                        f"Извлечён username из dict forward_origin.sender_user: '{username}', supplier: '{supplier}'")
                else :
                    first_name = forward_origin_sender_user.get('first_name', "")
                    last_name = forward_origin_sender_user.get('last_name', "")
                    supplier = f"{first_name} {last_name}".strip()
                    logging.debug(
                        f"Извлечены имена из dict forward_origin.sender_user: '{first_name} {last_name}', supplier: '{supplier}'")
            else :
                # Неизвестный тип forward_origin_sender_user
                logging.debug("forward_origin_sender_user имеет неизвестный тип.")

            if supplier :
                return supplier

    # Если поставщик не определён, возвращаем пустую строку
    logging.debug(f"Итоговый supplier: '{supplier}'")
    return supplier

def is_non_product_line(line: str) -> bool :
    """
    Проверяет, относится ли строка к никнейму Telegram, метаинформации или является пустой/содержит только эмодзи.

    Правила:
    1. Пустая строка.
    2. Строка содержит символ '@' (в любом месте).
    3. Строка состоит полностью из русских букв и пробелов.
    4. Строка состоит только из эмодзи.
    """
    original_line = line.strip()  # Сохраняем оригинальную строку для логирования

    # 1. Пустая строка
    if not original_line :
        logging.debug(f"Строка '{original_line}' является пустой.")
        return True

    # 2. Строка содержит '@' (в любом месте)
    if "@" in original_line :
        logging.debug(f"Строка '{original_line}' содержит '@', распознана как метаинформация.")
        return True

    # 3. Строка состоит полностью из русских букв и пробелов
    if re.match(r"^[а-яА-ЯёЁ\s]+$", original_line) :
        logging.debug(
            f"Строка '{original_line}' состоит из русских букв и пробелов, распознана как метаинформация или заголовок.")
        return True

    # 4. Строка состоит только из эмодзи
    # Используем библиотеку emoji для подсчёта эмодзи
    # emoji.emoji_count возвращает количество эмодзи в строке
    # Если количество эмодзи равно длине строки, считаем, что строка состоит только из эмодзи
    if emoji.emoji_count(original_line) == len(original_line) :
        logging.debug(f"Строка '{original_line}' состоит только из эмодзи.")
        return True

    # Если ни одно из правил не сработало, строка считается относящейся к товару
    logging.debug(f"Строка '{original_line}' распознана как строка с товаром.")
    return False

def extract_flags(line: str) -> Tuple[List[str], str, List[str]] :
    """
    Ищем флаги, представленные как эмодзи или текстовые слова,
    и возвращаем:
      (список найденных флагов, ИСХОДНУЮ строку (без удаления флагов!), список названий стран).

    ВАЖНО: Теперь НЕ удаляем эмодзи-флаги и слова стран из `line`,
    чтобы потом в других местах (например, для xCxC / CxCx) они оставались для парсинга.
    """
    flags = []
    countries = []

    # 1. Поиск эмодзи-флагов (двухсимвольные последовательности, где каждый символ – флаг)
    emoji_pattern = r'[\U0001F1E6-\U0001F1FF]{2}'
    emoji_flags = re.findall(emoji_pattern, line)
    for flag in emoji_flags :
        flags.append(flag)
        countries.append(COUNTRY_EMOJI_MAP.get(flag, "Неизвестно"))
        # РАНЬШЕ: line = line.replace(flag, "")
        # ТЕПЕРЬ: НЕ удаляем флаг из строки

    # 2. Поиск текстовых обозначений стран
    # Перебираем пары "ключ-значение" из COUNTRY_WORD_MAP.
    for word, country in COUNTRY_WORD_MAP.items() :
        pattern = r'\b' + re.escape(word) + r'\b'
        found = re.findall(pattern, line, flags=re.IGNORECASE)
        if found :
            flags.extend(found)
            countries.extend([country] * len(found))
            # РАНЬШЕ: line = re.sub(pattern, "", line, flags=re.IGNORECASE)
            # ТЕПЕРЬ: НЕ удаляем слова из строки

    # Просто возвращаем исходную строку "как есть"
    return flags, line, countries

def extract_data_with_multi_country_strict(line: str) -> Optional[List[Dict[str, Optional[str]]]] :
    """
    Пытается распознать "два товара" (два числа и ровно два флага) в строке.

    Условия:
      - Должно быть ровно 2 флага.
      - Сценарии:
         * xCxC: (число) (флаг1) (число) (флаг2)
         * CxCx: (флаг1) (число) (флаг2) (число)
      - Оба числа >= 513.

    Возвращает:
      - Список из двух словарей (два товара) при успехе.
      - `None`, если не удалось распознать ровно два товара.

    Пример использования в основном коде:

        results = extract_data_with_multi_country_strict(original_line)
        if results is not None:
            # ОК, получили 2 товара
            for item in results:
                # сохранить в USER_DATA...
        else:
            # нет, не получилось распарсить как "два товара"
            # вызываем extract_data(...) для одного товара

    """
    logger = logging.getLogger(__name__)

    # 1. Извлекаем флаги (НЕ удаляем их из строки)
    flags, unchanged_line, countries = extract_flags(line)
    logger.debug(f"[multi_country_strict] flags={flags}, countries={countries}, line='{unchanged_line}'")

    # Если флагов НЕ ровно 2, выходим
    if len(flags) != 2 :
        logger.debug("[multi_country_strict] Не ровно 2 флага => None")
        return None

    # Вспомогательный парсер для цены
    def parse_candidate(raw_cand: str) -> int :
        logger.debug(f"Парсинг кандидата: '{raw_cand}'")
        # 1) Убираем валютные символы и пунктуацию
        tmp = re.sub(r'[₽$€¥]', '', raw_cand).strip()
        tmp = re.sub(r'^[-–—]+', '', tmp)  # убираем возможный минус/тире спереди
        tmp = tmp.strip()
        tmp = re.sub(r'[,.’]', '', tmp)  # убираем запятые, точки, ’ и т.п.
        logger.debug(f"После очистки: '{tmp}'")

        # Если остались буквы (пример "46mm") — игнор
        if re.search(r'[^\d\s]', tmp) :
            logger.debug("Найдены недопустимые символы после очистки – кандидат игнорируется.")
            return 0

        parts = tmp.split()
        logger.debug(f"Разбивка кандидата на части: {parts}")

        if len(parts) > 1 :
            # 1) Проверяем группировку 3+3
            if (
                    parts[0].isdigit()
                    and 1 <= len(parts[0]) <= 3
                    and all(p.isdigit() and len(p) == 3 for p in parts[1 :])
            ) :
                joined_str = ''.join(parts)
                logger.debug(f"Кандидат соответствует группировке 3+3, объединённое число: {joined_str}")
                return int(joined_str)

            # 2) Шаблон (\d) (\d+)
            if (len(parts) == 2
                    and parts[0].isdigit() and len(parts[0]) == 1
                    and parts[1].isdigit()) :
                logger.debug(f"Шаблон (\\d) (\\d+), берём вторую часть: {parts[1]}")
                return int(parts[1])

            # 3) Две части, первая длиннее 3 цифр
            if (len(parts) == 2
                    and parts[0].isdigit() and len(parts[0]) > 3
                    and parts[1].isdigit()) :
                logger.debug(f"Длинная первая часть, используем её: {parts[0]}")
                return int(parts[0])

            # 4) Выбираем максимальное число из всех частей
            numbers = []
            for p in parts :
                if p.isdigit() :
                    numbers.append(int(p))
            if numbers :
                max_num = max(numbers)
                logger.debug(f"Максимальное число из частей: {max_num}")
                return max_num
            else :
                logger.debug("Нет чисел в частях – игнорируем.")
                return 0
        else :
            # Одна часть
            if parts and parts[0].isdigit() :
                logger.debug(f"Один токен, используем: {parts[0]}")
                return int(parts[0])
            return 0

    # Шаблоны (жадные), с учётом пробелов и опц. тире
    pattern_xCxC = re.compile(
        r'\s*[-–—]?\s*(\d[\d\s.,’]+)\s*'
        + re.escape(flags[0]) +
        r'\s*[-–—]?\s*(\d[\d\s.,’]+)\s*'
        + re.escape(flags[1])
    )
    pattern_CxCx = re.compile(
        re.escape(flags[0]) +
        r'\s*[-–—]?\s*(\d[\d\s.,’]+)\s*'
        + re.escape(flags[1]) +
        r'\s*[-–—]?\s*(\d[\d\s.,’]+)\s*'
    )

    match_x = pattern_xCxC.search(line)
    match_c = pattern_CxCx.search(line)

    # 2. Пытаемся xCxC
    if match_x :
        logger.debug("[multi_country_strict] Обнаружен xCxC")
        g1 = match_x.group(1)
        g2 = match_x.group(2)
        logger.debug(f"  group(1)={repr(g1)}, group(2)={repr(g2)}")
        v1 = parse_candidate(g1)
        v2 = parse_candidate(g2)
        logger.debug(f"  v1={v1}, v2={v2}")
        if v1 >= 513 and v2 >= 513 :
            logger.debug("  => Возвращаем 2 товара (xCxC)")
            return [
                {
                    "product_name" : line.strip(),
                    "price" : v1,
                    "countries" : [countries[0]],
                    "comment" : ""
                },
                {
                    "product_name" : line.strip(),
                    "price" : v2,
                    "countries" : [countries[1]],
                    "comment" : ""
                }
            ]
        else :
            logger.debug("  => xCxC найден, но цены <513 => None")
            return None

    # 3. Пытаемся CxCx
    if match_c :
        logger.debug("[multi_country_strict] Обнаружен CxCx")
        g1 = match_c.group(1)
        g2 = match_c.group(2)
        logger.debug(f"  group(1)={repr(g1)}, group(2)={repr(g2)}")
        v1 = parse_candidate(g1)
        v2 = parse_candidate(g2)
        logger.debug(f"  v1={v1}, v2={v2}")
        if v1 >= 513 and v2 >= 513 :
            logger.debug("  => Возвращаем 2 товара (CxCx)")
            return [
                {
                    "product_name" : line.strip(),
                    "price" : v1,
                    "countries" : [countries[0]],
                    "comment" : ""
                },
                {
                    "product_name" : line.strip(),
                    "price" : v2,
                    "countries" : [countries[1]],
                    "comment" : ""
                }
            ]
        else :
            logger.debug("  => CxCx найден, но цены <513 => None")
            return None

    # 4. Если ни xCxC, ни CxCx не сработали
    logger.debug("[multi_country_strict] Нет xCxC/CxCx => None")
    return None

def extract_data_with_multi_color_strict(line: str) -> Optional[List[Dict[str, Union[int, str, List, None]]]]:
    """
    Обрабатывает строки с двумя цветовыми эмодзи как два товара
    """
    logger = logging.getLogger(__name__)

    # Ищем цветовые эмодзи
    clusters = regex.findall(r'\X', line)
    color_emojis = [c for c in clusters if c in EMOJIS_COLORS]

    # Проверяем условия (ровно 2 уникальных эмодзи)
    if len(color_emojis) != 2 or len(set(color_emojis)) != 2 :
        return None

    # Вспомогательный парсер для цены
    def parse_candidate(raw_cand: str) -> int :
        logger.debug(f"Парсинг кандидата: '{raw_cand}'")
        # 1) Убираем валютные символы и пунктуацию
        tmp = re.sub(r'[₽$€¥]', '', raw_cand).strip()
        tmp = re.sub(r'^[-–—]+', '', tmp)  # убираем возможный минус/тире спереди
        tmp = tmp.strip()
        tmp = re.sub(r'[,.’]', '', tmp)  # убираем запятые, точки, ’ и т.п.
        logger.debug(f"После очистки: '{tmp}'")

        # Если остались буквы (пример "46mm") — игнор
        if re.search(r'[^\d\s]', tmp) :
            logger.debug("Найдены недопустимые символы после очистки – кандидат игнорируется.")
            return 0

        parts = tmp.split()
        logger.debug(f"Разбивка кандидата на части: {parts}")

        if len(parts) > 1 :
            # 1) Проверяем группировку 3+3
            if (
                    parts[0].isdigit()
                    and 1 <= len(parts[0]) <= 3
                    and all(p.isdigit() and len(p) == 3 for p in parts[1 :])
            ) :
                joined_str = ''.join(parts)
                logger.debug(f"Кандидат соответствует группировке 3+3, объединённое число: {joined_str}")
                return int(joined_str)

            # 2) Шаблон (\d) (\d+)
            if (len(parts) == 2
                    and parts[0].isdigit() and len(parts[0]) == 1
                    and parts[1].isdigit()) :
                logger.debug(f"Шаблон (\\d) (\\d+), берём вторую часть: {parts[1]}")
                return int(parts[1])

            # 3) Две части, первая длиннее 3 цифр
            if (len(parts) == 2
                    and parts[0].isdigit() and len(parts[0]) > 3
                    and parts[1].isdigit()) :
                logger.debug(f"Длинная первая часть, используем её: {parts[0]}")
                return int(parts[0])

            # 4) Выбираем максимальное число из всех частей
            numbers = []
            for p in parts :
                if p.isdigit() :
                    numbers.append(int(p))
            if numbers :
                max_num = max(numbers)
                logger.debug(f"Максимальное число из частей: {max_num}")
                return max_num
            else :
                logger.debug("Нет чисел в частях – игнорируем.")
                return 0
        else :
            # Одна часть
            if parts and parts[0].isdigit() :
                logger.debug(f"Один токен, используем: {parts[0]}")
                return int(parts[0])
            return 0

    # Формируем паттерны
    escaped_emojis = [re.escape(e) for e in color_emojis]

    # Паттерн xCxC: число эмодзи1 число эмодзи2
    pattern_xCxC = re.compile(
        r'\s*[-–—]?\s*(\d[\d\s.,’]+)\s*'
        + escaped_emojis[0]
        + r'\s*[-–—]?\s*(\d[\d\s.,’]+)\s*'
        + escaped_emojis[1]
        + r'(?:\s|$)',
        re.UNICODE
    )

    # Паттерн CxCx: эмодзи1 число эмодзи2 число
    pattern_CxCx = re.compile(
        escaped_emojis[0]
        + r'\s*[-–—]?\s*(\d[\d\s.,’]+)\s*'
        + escaped_emojis[1]
        + r'\s*[-–—]?\s*(\d[\d\s.,’]+)\s*',
        re.UNICODE
    )

    # Проверяем оба паттерна
    for pattern in [pattern_xCxC, pattern_CxCx] :
        match = pattern.search(line)
        if match :
            g1, g2 = match.group(1), match.group(2)
            v1, v2 = parse_candidate(g1), parse_candidate(g2)

            if v1 >= 513 and v2 >= 513 :
                # Формируем названия товаров с эмодзи
                common_prefix = line[:match.start(1)]
                tokens = match.group(1).split()
                if len(tokens) == 2 and tokens[0].isdigit() and len(tokens[0]) == 1 :
                    version = tokens[0]  # например, "2"
                    price1 = tokens[1]
                    product1 = common_prefix + version + " " + price1 + color_emojis[0]
                    product2 = common_prefix + version + " " + match.group(2) + color_emojis[1]
                else :
                    product1 = common_prefix + match.group(1) + color_emojis[0]
                    product2 = common_prefix + match.group(2) + color_emojis[1]

                return [
                    {
                        "product_name" : product1.strip(),
                        "price" : v1,
                        "countries" : [],
                        "comment" : ""
                    },
                    {
                        "product_name" : product2.strip(),
                        "price" : v2,
                        "countries" : [],
                        "comment" : ""
                    }
                ]

    return None

def extract_data_with_multi_color_multiple(line: str) -> Optional[List[Dict[str, Optional[str]]]]:
    """
    Ищет в строке РОВНО одну цену и 2+ цветовых эмодзи без чисел после них.
    Возвращает список "виртуальных" товаров, по одному на каждый цвет.

    Пример:
      "Onyx studio 8 - 22500⚫️.⚪️🔵"
    -> 3 товара:
      1) "⚫️ Onyx studio 8 - 22500"
      2) "⚪️ Onyx studio 8 - 22500"
      3) "🔵 Onyx studio 8 - 22500"
    """
    # 1) Берём результат extract_data
    product_name, price, comment_text = extract_data(line)
    if not product_name or not price:
        return None  # нет цены или нет названия - не подходит

    # 2) Ищем ВСЕ цветовые эмодзи. Лучше смотреть во ВСЕЙ строке, а не только в comment_text,
    #    т.к. могло что-то переместиться в product_name.
    clusters = regex.findall(r'\X', line)
    color_emojis = [c for c in clusters if c in EMOJIS_COLORS]

    # Если цветовых эмодзи < 2, нечего "делить" на несколько товаров
    if len(color_emojis) < 2:
        return None

    # 3) "Клонируем" N товаров (где N = количество эмодзи)
    #    Примерный формат:
    #      "<emoji> <product_name> - <price>"
    #    Но нужно убедиться, что product_name ещё не содержит цену.
    #    Т.к. extract_data вернёт product_name без цены, всё хорошо.
    results = []
    for color in color_emojis:
        # Собираем виртуальную строку
        new_line = f"{color} {product_name} - {price}"
        item = {
            "product_name": new_line.strip(),
            "price": price,
            "countries": [],      # по умолчанию нет стран
            "comment": ""         # нет комментария
        }
        results.append(item)

    return results

def process_emojis(product_name: str, original_line: str, allowed_emojis: List[str]) -> Tuple[str, str] :
    # Разбиваем на графемные кластеры
    product_clusters = regex.findall(r'\X', product_name)
    comment_clusters = regex.findall(r'\X', original_line)

    # Оставляем только разрешенные эмодзи
    cleaned_line = ''.join([
        cluster
        for cluster in product_clusters
        if cluster in EMOJIS_COLORS or not emoji.is_emoji(cluster)
    ]).strip()

    # Комментарий: только разрешенные эмодзи
    comment_emojis = [
        cluster
        for cluster in comment_clusters
        if cluster in allowed_emojis
    ]

    return cleaned_line, ' '.join(comment_emojis)

# =============================================================================
# Вспомогательные функции extract_data

def parse_candidate(raw_candidate: str) -> int:
    """
    Парсит строку-кандидат на цену, при этом сначала пытается распознать
    строго формат "xx xxx,00" (через пробел или \xa0), а если нет —
    идёт по «общей» логике сплитов.
    """
    logger.debug(f"Парсинг кандидата: {raw_candidate!r}")

    # 1. Удаляем символы валют, ведущие тире.
    candidate = CURRENCY_REGEX.sub('', raw_candidate).strip()
    candidate = LEADING_DASH_REGEX.sub('', candidate).strip()

    # Преобразуем неразрывные пробелы (\xa0) в обычные, чтобы REGEX проще сработал
    candidate = candidate.replace('\u00A0', ' ')

    # 2. Сначала проверяем «особый» формат "xx xxx,00", "xxx xxx,00" и т.д.
    #    Если он целиком соответствует SPECIAL_PATTERN, сразу парсим, минуя
    #    логику вырезания запятых.
    match = SPECIAL_PATTERN.match(candidate)
    if match:
        # Например: "108 500,00" -> разделяем на "108 500" и ",00"
        # group(0) — вся строка, но нам нужно убрать ",00"
        # сделаем простенько: candidate[:-3] -> "108 500"
        part_no00 = candidate[:-3]  # убираем ",00" с конца
        just_digits = part_no00.replace(' ', '')  # "108 500" -> "108500"
        # Можно на всякий случай ещё раз убедиться, что там только цифры
        if just_digits.isdigit():
            logger.debug(f"Особый формат: {candidate!r} -> {just_digits}")
            return int(just_digits)

    # 3. Если «особый» формат не сработал — продолжаем «старым» путём
    #    Удаляем точку, запятую, апостроф/акут и т.п.
    cleaned = PUNCTUATION_REGEX.sub('', candidate)
    logger.debug(f"После удаления пунктуации: {cleaned!r}")

    # Если остались «левые» символы
    if NON_DIGIT_PATTERN.search(cleaned):
        logger.debug("Обнаружены недопустимые символы — кандидат игнорируется.")
        return 0

    # 4. Разбиваем по пробелам
    tokens = cleaned.split()
    logger.debug(f"Токены: {tokens}")

    # Если несколько токенов, и все — цифры, просто объединяем
    if len(tokens) > 1 and all(t.isdigit() for t in tokens):
        joined = ''.join(tokens)
        logger.debug(f"Объединение всех токенов: {joined!r}")
        return int(joined) if joined.isdigit() else 0

    # Иначе – как у вас в логике
    if len(tokens) > 1:
        # a) Формат 3+3 и т. д. ("68 000", "12 500 000")
        if (
            tokens[0].isdigit() and 1 <= len(tokens[0]) <= 3
            and all(t.isdigit() and len(t) == 3 for t in tokens[1:])
        ):
            return int(''.join(tokens))
        # b) Если 2 токена: один из них коротенький, второй полный
        elif len(tokens) == 2 and tokens[0].isdigit() and len(tokens[0]) == 1 and tokens[1].isdigit():
            return int(tokens[1])
        else:
            # Берём максимум из распарсенных чисел
            numbers = [int(t) for t in tokens if t.isdigit()]
            return max(numbers) if numbers else 0
    else:
        # Один токен
        return int(tokens[0]) if tokens and tokens[0].isdigit() else 0

def find_price_position(line: str, price_str: str, price: int) -> Tuple[int, int] :
    """
    Находит позицию (индекс начала и длину совпадения) цены в строке,
    используя несколько вариантов представления цены.

    :param line: Исходная строка.
    :param price_str: Строка, как была обнаружена цена (например, "68.000").
    :param price: Числовое значение цены (например, 68000).
    :return: Кортеж (начальный индекс, длина совпадения). Если не найдено, возвращается (-1, 0).
    """
    # Список паттернов для поиска – учитываем разные форматы представления числа
    patterns = [
        re.escape(price_str),  # Исходный вариант, экранированный для точного поиска
        re.sub(r'\D', '', str(price)),  # Число без разделителей (например, "68000")
        re.sub(r'\D', '[., ]*', str(price))  # Паттерн для поиска с разделителями (например, "68[., ]*000")
    ]
    for pattern in patterns :
        match = re.search(pattern, line)
        if match :
            return match.start(), match.end() - match.start()
    return -1, 0

# =============================================================================
# Основная функция extract_data

def extract_data(line: str) -> Tuple[Optional[str], Optional[int], str]:
    """
    Извлекает название продукта, цену и комментарий из строки.

    Логика:
      1. Предварительно очищаем строку (удаляем точки в конце и лишние пробелы).
      2. Ищем все кандидаты на цену по предкомпилированному шаблону PRICE_PATTERN.
         Если сразу после найденного кандидата идёт тире и цифра — кандидат отбрасывается.
      3. Каждый кандидат обрабатывается функцией parse_candidate для получения числового значения.
         Принимаются только кандидаты с ценой >= 513.
      4. Выбирается финальный кандидат:
         - Если последний кандидат равен максимальному по значению, берём его,
         - иначе — берём максимальный.
      5. С помощью функции find_price_position определяется положение цены в исходной строке.
      6. На основании позиции формируются product_name (вся строка до цены) и comment_text (после цены).
      6.1 Проверка и перемещение цветовых эмодзи из комментария
      7. Производится финальная чистка product_name и comment_text:
         - Удаляются лишние тире, эмодзи заменяются на пробелы, нормализуются пробелы.
      8. Если в тексте до цены встречаются слова из COMMENT_ADD или процентное значение,
         дополнительно извлекается комментарий из круглых скобок или из токенов.
         При этом удаляются скобки из product_name.
      9. Если comment_text содержит слова из IGNORING_COMMENT, комментарий сбрасывается.
      10. Производится замена формата "Б У" на "Б/У" и проверка на валидность комментария.
      11. Если комментарий состоит только из цифры/пробелы/знаки препинания — сбрасываем

    :param line: Исходная строка с данными.
    :return: Кортеж из (product_name, цена, comment_text). Если не удалось извлечь цену — (None, None, "").
    """
    try:
        # -----------------------------------------------------------------------------
        # 1. Предобработка строки: удаляем завершающие точки и лишние пробелы
        # -----------------------------------------------------------------------------
        original_line = line.rstrip('.').strip()
        logger.debug(f"Строка после очистки: '{original_line}'")

        # -----------------------------------------------------------------------------
        # 2. Поиск кандидатов на цену с использованием PRICE_PATTERN
        # -----------------------------------------------------------------------------
        raw_candidates = []
        for match in PRICE_PATTERN.finditer(original_line):
            candidate = match.group(0)
            # Если сразу после кандидата идёт тире без пробела и далее цифра — отбрасываем кандидата
            if match.end() < len(original_line) and original_line[match.end()] in "-–—":
                next_index = match.end() + 1
                if next_index < len(original_line) and original_line[next_index].isdigit():
                    continue
            raw_candidates.append(candidate)
        logger.debug(f"Найденные кандидаты: {raw_candidates}")

        if not raw_candidates:
            logger.warning(f"Цена не найдена в строке: '{original_line}'")
            return None, None, ""

        # -----------------------------------------------------------------------------
        # 3. Парсинг кандидатов для получения числовых значений (принимаем, если >= 513)
        # -----------------------------------------------------------------------------
        parsed_prices = []
        for cand in raw_candidates:
            value = parse_candidate(cand)
            logger.debug(f"Кандидат '{cand}' распарсен как {value}")
            if value >= 513:
                parsed_prices.append((cand, value))
        if not parsed_prices:
            logger.warning(f"Подходящие цены (>=513) не найдены в строке: '{original_line}'")
            return None, None, ""

        # -----------------------------------------------------------------------------
        # 4. Выбор финального кандидата:
        #    - Если последний кандидат равен максимальному по значению, выбираем его,
        #      иначе выбираем максимальный.
        # -----------------------------------------------------------------------------
        last_str, last_val = parsed_prices[-1]
        max_str, max_val = max(parsed_prices, key=lambda x: x[1])
        logger.debug(f"Все валидные кандидаты: {parsed_prices}")
        logger.debug(f"Последний кандидат: '{last_str}' -> {last_val}")
        logger.debug(f"Максимальный кандидат: '{max_str}' -> {max_val}")

        if last_val == max_val:
            final_price_str, final_price = last_str, last_val
        else:
            final_price_str, final_price = max_str, max_val

        # -----------------------------------------------------------------------------
        # 5. Определение позиции цены в строке с учётом различных форматов представления
        # -----------------------------------------------------------------------------
        price_index, cut_len = find_price_position(original_line, final_price_str, final_price)
        if price_index == -1:
            logger.warning(f"Не удалось найти цену {final_price} в строке '{original_line}'")
            return None, None, ""
        logger.debug(f"Позиция цены: {price_index}, длина: {cut_len}")

        # -----------------------------------------------------------------------------
        # 6. Формирование product_name и comment_text на основе позиции цены
        # -----------------------------------------------------------------------------
        before_price_text = original_line[:price_index].strip()
        product_name = before_price_text
        comment_text = original_line[price_index + cut_len :].strip()
        logger.debug(f"Сырой product_name: '{product_name}'")
        logger.debug(f"Сырой comment_text: '{comment_text}'")

        # --------------------------------------------------------------------
        # 6.1 Проверка и перемещение цветовых эмодзи из комментария
        # --------------------------------------------------------------------
        if comment_text :
            comment_clusters = regex.findall(r'\X', comment_text)
            emoji_indices = []
            has_numbers_after_emoji = False

            for i, cluster in enumerate(comment_clusters) :
                if cluster in EMOJIS_COLORS :
                    emoji_indices.append(i)
                    tail = ''.join(comment_clusters[i + 1 :])
                    if re.search(r'\d', tail) :
                        has_numbers_after_emoji = True
                        break

            color_emojis_in_comment = [c for c in comment_clusters if c in EMOJIS_COLORS]

            if has_numbers_after_emoji :
                logger.debug("Обнаружены числа после эмодзи — пропускаем перемещение.")
            else :
                # Если больше одного цветового эмодзи — пропускаем перемещение, чтобы внешняя логика
                # (extract_data_with_multi_color_multiple) смогла «распилить» на несколько товаров.
                if len(color_emojis_in_comment) > 1 :
                    logger.debug(
                        "В комментарии несколько цветовых эмодзи и нет чисел после них. "
                        "Пропускаем перемещение, чтобы внешняя логика могла обработать несколько цветов."
                    )
                # Если 1 эмодзи, переносим, как и раньше
                elif len(color_emojis_in_comment) == 1 :
                    emojis_to_move = [comment_clusters[i] for i in emoji_indices]
                    product_name = f'{"".join(emojis_to_move)} {product_name}'.strip()
                    new_comment = ''.join(
                        [c for idx, c in enumerate(comment_clusters) if idx not in emoji_indices]
                    )
                    comment_text = new_comment.strip()
                    logger.debug(f"Перемещён одиночный эмодзи: {''.join(emojis_to_move)}")

        # --------------------------------------------------------------------
        # 7. Финальная чистка product_name
        # --------------------------------------------------------------------
        clusters = regex.findall(r'\X', product_name)
        product_name = ''.join([
            cluster if (cluster in EMOJIS_COLORS) or (not emoji.is_emoji(cluster)) else ' '
            for cluster in clusters
        ]).strip()

        # -----------------------------------------------------------------------------
        # 8. Блок дополнения комментария (если до цены встречаются ключевые слова или проценты)
        # -----------------------------------------------------------------------------
        if COMMENT_ADD_PATTERN.search(before_price_text) or re.search(r'\b\d+%\b', before_price_text):
            paren_matches = re.findall(r'\(([^)]*)\)', original_line)
            chosen_comment = None
            for candidate in paren_matches:
                if COMMENT_ADD_PATTERN.search(candidate) or re.search(r'\b\d+%\b', candidate):
                    chosen_comment = candidate.strip()
                    break
            if not chosen_comment:
                tokens = [m.group(0) for m in re.finditer(r'\d+%|[а-яёА-ЯЁ]+', original_line, flags=re.IGNORECASE)]
                chosen_comment = ' '.join(tokens).strip()
            if comment_text:
                comment_text = comment_text + " " + chosen_comment
            else:
                comment_text = chosen_comment
            product_name = re.sub(r'\([^)]*\)', '', product_name).strip()

        # -----------------------------------------------------------------------------
        # 9. Блок игнорирования комментариев: если comment_text содержит ключевые слова для игнорирования,
        #    сбрасываем комментарий.
        # -----------------------------------------------------------------------------
        if comment_text and IGNORING_COMMENT_PATTERN.search(comment_text):
            comment_text = ""

        # -----------------------------------------------------------------------------
        # 10. Дополнительная обработка comment_text
        #     - Замена "Б У" на "Б/У"
        #     - Если комментарий состоит только из неалфавитных символов, сбрасываем его.
        # -----------------------------------------------------------------------------
        comment_text = re.sub(r'\b[Бб]\s+[Уу]\b', 'Б/У', comment_text)
        if comment_text and not re.search(r'\w', comment_text) :
            comment_text = ""

        # -----------------------------------------------------------------------------
        # 11. (НОВЫЙ БЛОК): Если комментарий состоит только из цифры/пробелы/знаки препинания — сбрасываем
        # -----------------------------------------------------------------------------
        if comment_text :
            # Проверяем наличие букв (любых) и цветовых эмодзи
            has_letters = bool(re.search(r'[a-zA-Zа-яА-ЯёЁ]', comment_text))
            has_color_emoji = any(emoji in comment_text for emoji in EMOJIS_COLORS)

            if not has_letters and not has_color_emoji :
                logger.debug(
                    f"Комментарий '{comment_text}' не содержит ни букв, "
                    "ни цветовых эмодзи — сбрасываем."
                )
                comment_text = ""

        logger.debug(f"Финальный product_name: '{product_name}'")
        logger.debug(f"Финальный comment_text: '{comment_text}'")

        return product_name, final_price, comment_text

    except Exception as e :
        logger.error(f"Ошибка при извлечении данных из строки: {e}", exc_info=True)
        return None, None, ""
# =============================================================================

def apply_special_rules_iphone(model_group: str, country: str, variant: str, product_library: Dict, brand: str) -> str:
    """
    Применяет специальные правила для модели (model_group) и страны (country).
    Может, например, добавлять 'Dual sim' или 'eSim' к названию.
    """
    selected_variant = variant
    logger.debug(
        f"[apply_special_rules_iphone] Запущен с model_group='{model_group}', "
        f"country='{country}', variant='{variant}'"
    )

    if model_group in SPECIAL_RULES_IPHONE:
        logger.info(f"[apply_special_rules_iphone] Модель '{model_group}' есть в SPECIAL_RULES_IPHONE.")
        if country in SPECIAL_RULES_IPHONE[model_group]:
            rule = SPECIAL_RULES_IPHONE[model_group][country]
            logger.debug(f"[apply_special_rules_iphone] Нашли правило для страны '{country}': {rule}")

            # Применяем правило, например, добавляем "Dual sim" или "eSim"
            new_variant = rule["type"](variant)
            logger.debug(f"[apply_special_rules_iphone] Применили правило, получили новый вариант: '{new_variant}'")

            selected_variant = new_variant
            logger.info(f"[apply_special_rules_iphone] Итоговый вариант: '{selected_variant}'")
        else:
            logger.info(
                f"[apply_special_rules_iphone] Для страны '{country}' нет спец. правил в SPECIAL_RULES_IPHONE "
                f"для модели '{model_group}'."
            )
    else:
        logger.info(
            f"[apply_special_rules_iphone] Модель '{model_group}' не найдена в SPECIAL_RULES_IPHONE. "
            "Специальные правила не применяются."
        )

    logger.debug(f"[apply_special_rules_iphone] Результат: '{selected_variant}'")
    return selected_variant

def add_or_update_product(
    user_data,  # user_data вообще можно убрать из аргументов
    user_id: int,
    line: str,
    countries: List[str],
    selected_variant: str,
    model_group: str,
    price: int,
    supplier: str,
    comment: str,
    brand: str = ""
):
    """
    Раньше эта функция добавляла товар в user_data[user_id]["products"].
    Теперь - только запись в БД (add_product).
    """

    if countries:
        for country in countries:
            add_product(
                user_id=user_id,
                line=line,
                brand=brand,
                country=country,
                product_name=selected_variant,
                model_group=model_group,
                price=price,
                supplier=supplier,
                comment=comment
            )
            logger.info(
                f"Добавлен товар '{selected_variant}' (бренд: {brand}, "
                f"страна: {country}, цена: {price})"
            )
    else:
        add_product(
            user_id=user_id,
            line=line,
            brand=brand,
            country="",  # без указания страны
            product_name=selected_variant,
            model_group=model_group,
            price=price,
            supplier=supplier,
            comment=comment
        )
        logger.info(
            f"Добавлен товар '{selected_variant}' (бренд: {brand}, "
            f"без указания страны, цена: {price})"
        )

# -----------------------------------------------------------------------------------
# Логика "сложных" товаров
# -----------------------------------------------------------------------------------

def find_complex_brand_model(product_name: str) -> Optional[Tuple[str, str]]:
    """
    Находит бренд и модель продукта по его названию, используя PRODUCT_LIBRARY.

    :param product_name: Название продукта.
    :return: Кортеж (brand, model) или None, если не найдено.
    """
    logger.debug(f"[find_complex_brand_model] Проверяем '{product_name}' на сложный бренд...")
    normalized = product_name.lower().strip()

    # Итерация по брендам в PRODUCT_LIBRARY
    for brand, models in PRODUCT_LIBRARY.items():
        if brand not in COMPLEX_BRANDS:
            continue  # Пропускаем бренды, которые не считаются сложными

        # Итерация по моделям внутри бренда
        for model, model_data in models.items():
            # Проверяем, есть ли алиасы для модели
            aliases = model_data.get("aliases", [])
            if not aliases:
                continue  # Пропускаем модели без алиасов

            # Сортируем алиасы по убыванию длины, чтобы более длинные проверялись первыми
            aliases_sorted = sorted(aliases, key=len, reverse=True)

            # Итерация по отсортированным алиасам
            for alias in aliases_sorted:
                if not isinstance(alias, str):
                    logger.debug(f"[find_complex_brand_model] Алиас не строка: {alias}")
                    continue  # Пропускаем, если алиас не строка

                alias_lower = alias.lower()

                # Используем регулярное выражение с границами слов
                pattern = re.compile(rf'\b{re.escape(alias_lower)}\b', re.IGNORECASE)
                if pattern.search(normalized):
                    logger.debug(
                        f"[find_complex_brand_model] Успех: alias='{alias}', "
                        f"brand='{brand}', model='{model}'"
                    )
                    return (brand, model)

    logger.debug("[find_complex_brand_model] Не нашли соответствия сложному бренду.")
    return None

def handle_complex_brand(
    line: str,
    cleaned_line: str,
    brand: str,
    model: str,
    countries: List[str],
    price: int,
    supplier: str,
    comment: str,
    user_id: int
) -> bool:
    """
    Единая точка для обработки любых «сложных» брендов.
    Пока поддерживается только Apple Watch.
    Если появятся другие сложные бренды (iPad, MacBook и т.д.),
    можно расширить логику:
      if brand == "Apple Watch":
          handle_apple_watch_product(...)
      elif brand == "iPad":
          handle_ipad_product(...)
      ...

    Параметры:
    ----------
    line : str
        Исходная строка из сообщения пользователя (до очистки).
    cleaned_line : str
        Очищенная строка для парсинга атрибутов.
    brand : str
        Бренд товара (например, "Apple Watch").
    model : str
        Модель товара (например, "AW SE 2").
    countries : list
        Список стран.
    price : int
        Цена товара.
    supplier : str
        Поставщик товара.
    comment : str
        Комментарий к товару.
    user_id : int
        ID пользователя.

    Возвращает:
    ----------
    bool
        True, если товар обработан и сохранён как сложный.
        False, если товар должен быть обработан как простой.

    (НОВЫЙ КОММЕНТАРИЙ) Теперь, если «основной» brand не смог обработаться (вернул False),
    мы перебираем оставшиеся бренды из COMPLEX_BRANDS. Если ни один не справился,
    возвращаем False.
    """
    logger.debug(f"[handle_complex_brand] brand='{brand}', model='{model}'")

    # (НОВЫЙ КОММЕНТАРИЙ) Формируем список кандидатов так, чтобы сначала попробовать «основной» brand,
    # а если он не сработал — идти по остальным из COMPLEX_BRANDS.
    brand_candidates = COMPLEX_BRANDS[:]  # копируем оригинальный список
    if brand in brand_candidates:
        brand_candidates.remove(brand)
        brand_candidates.insert(0, brand)
    else:
        # Если вдруг brand не оказался в COMPLEX_BRANDS, просто перебираем всё подряд
        logger.warning(f"[handle_complex_brand] Найденный brand='{brand}' не в COMPLEX_BRANDS. Пробуем общий порядок.")

    # (НОВЫЙ КОММЕНТАРИЙ) Перебираем все возможные «сложные» бренды из списка.
    for brand_candidate in brand_candidates:
        logger.debug(f"[handle_complex_brand] Пытаемся brand_candidate='{brand_candidate}'")

        if brand_candidate == "Apple iPhone":
            from apple_iphone_utils import handle_complex_apple_iphone
            logger.debug("[handle_complex_brand] Вызываем handle_complex_apple_iphone...")
            handled = handle_complex_apple_iphone(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_apple_iphone вернул {handled}")
            if handled:
                return True

        elif brand_candidate == "Apple Аксессуары":
            from apple_accessories_utils import handle_complex_apple_accessories
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_apple_accessories] Вызываем handle_complex_apple_accessories...")
            handled = handle_complex_apple_accessories(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_apple_accessories вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Samsung Galaxy":
            from samsung_galaxy_utils import handle_complex_samsung_galaxy
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_samsung_galaxy] Вызываем handle_complex_samsung_galaxy...")
            handled = handle_complex_samsung_galaxy(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_samsung_galaxy вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Стайлеры для волос Dyson":
            from dyson_airwrap_utils import handle_complex_dyson_airwrap
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_dyson_airwrap] Вызываем handle_complex_dyson_airwrap...")
            handled = handle_complex_dyson_airwrap(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_dyson_airwrap вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Фены для волос Dyson":
            from dyson_supersonic_utils import handle_complex_dyson_supersonic
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_dyson_supersonic] Вызываем handle_complex_dyson_supersonic...")
            handled = handle_complex_dyson_supersonic(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_dyson_supersonic вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Выпрямители для волос Dyson":
            from dyson_airstrait_utils import handle_complex_dyson_airstrait
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_dyson_airstrait] Вызываем handle_complex_dyson_airstrait...")
            handled = handle_complex_dyson_airstrait(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_dyson_airstrait вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Пылесосы Dyson":
            from dyson_cleaner_utils import handle_complex_dyson_cleaner
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_dyson_cleaner] Вызываем handle_complex_dyson_cleaner...")
            handled = handle_complex_dyson_cleaner(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_dyson_cleaner вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Системы очистки воздуха Dyson":
            from dyson_climate_utils import handle_complex_dyson_climate
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_dyson_climate] Вызываем handle_complex_dyson_climate...")
            handled = handle_complex_dyson_climate(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_dyson_climate вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Сушилки для рук Dyson":
            from dyson_handdryer_utils import handle_complex_dyson_handdryer
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_dyson_handdryer] Вызываем handle_complex_dyson_handdryer...")
            handled = handle_complex_dyson_handdryer(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_dyson_handdryer вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Аксессуары Dyson":
            from dyson_accessories_utils import handle_complex_dyson_accessories
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_dyson_accessories] Вызываем handle_complex_dyson_accessories...")
            handled = handle_complex_dyson_accessories(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment='', #без комментария
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_dyson_accessories вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Xiaomi":
            from xiaomi_utils import handle_complex_xiaomi
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_xiaomi] Вызываем handle_complex_xiaomi...")
            handled = handle_complex_xiaomi(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_xiaomi вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "OnePlus":
            from oneplus_utils import handle_complex_oneplus
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_oneplus] Вызываем handle_complex_oneplus...")
            handled = handle_complex_oneplus(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_oneplus вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Google":
            from google_utils import handle_complex_google
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_xiaomi] Вызываем handle_complex_google...")
            handled = handle_complex_google(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_google вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Realme":
            from realme_utils import handle_complex_realme
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_realme] Вызываем handle_complex_realme...")
            handled = handle_complex_realme(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_realme вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Honor":
            from honor_utils import handle_complex_honor
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_honor] Вызываем handle_complex_honor...")
            handled = handle_complex_honor(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_honor вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Infinix":
            from infinix_utils import handle_complex_infinix
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_infinix] Вызываем handle_complex_infinix...")
            handled = handle_complex_infinix(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_infinix вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Doogee":
            from doogee_utils import handle_complex_doogee
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_doogee] Вызываем handle_complex_doogee...")
            handled = handle_complex_doogee(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_doogee вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Яндекс":
            from yandex_utils import handle_complex_yandex
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_yandex] Вызываем handle_complex_yandex...")
            handled = handle_complex_yandex(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_yandex вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "JBL":
            from jbl_utils import handle_complex_jbl
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_jbl] Вызываем handle_complex_jbl...")
            handled = handle_complex_jbl(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_jbl вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Beats":
            from beats_utils import handle_complex_beats
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_beats] Вызываем handle_complex_beats...")
            handled = handle_complex_beats(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_beats вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Sony":
            from sonyaudio_utils import handle_complex_sonyaudio
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_sonyaudio] Вызываем handle_complex_sonyaudio...")
            handled = handle_complex_sonyaudio(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_sonyaudio вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Marshall":
            from marshall_utils import handle_complex_marshall
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_marshall] Вызываем handle_complex_marshall...")
            handled = handle_complex_marshall(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_marshall вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Galaxy Buds":
            from galaxybuds_utils import handle_complex_galaxybuds
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_galaxybuds] Вызываем handle_complex_galaxybuds...")
            handled = handle_complex_galaxybuds(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_galaxybuds вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "OnePlus Buds":
            from oneplusbuds_utils import handle_complex_oneplusbuds
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_oneplus] Вызываем handle_complex_nothingear...")
            handled = handle_complex_oneplusbuds(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_nothingear вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Redmi Buds":
            from redmibuds_utils import handle_complex_redmibuds
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_redmibuds] Вызываем handle_complex_redmibuds...")
            handled = handle_complex_redmibuds(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_redmibuds вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Nothing Ear":
            from nothingear_utils import handle_complex_nothingear
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_oneplus] Вызываем handle_complex_oneplus...")
            handled = handle_complex_nothingear(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_oneplus вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "VK":
            from vk_utils import handle_complex_vk
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_vk] Вызываем handle_complex_vk...")
            handled = handle_complex_vk(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_vk вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Аудио прочее":
            from audio_utils import handle_complex_audio
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_audio] Вызываем handle_complex_audio...")
            handled = handle_complex_audio(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_audio вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Xbox":
            from xbox_utils import handle_complex_xbox
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_xbox] Вызываем handle_complex_xbox...")
            handled = handle_complex_xbox(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_xbox вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "PlayStation":
            from playstation_utils import handle_complex_playstation
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_playstation] Вызываем handle_complex_playstation...")
            handled = handle_complex_playstation(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_playstation вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Meta Quest":
            from meta_utils import handle_complex_meta
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_meta] Вызываем handle_complex_meta...")
            handled = handle_complex_meta(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_meta вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Valve Steam Deck":
            from steamdeck_utils import handle_complex_steamdeck
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_steamdeck] Вызываем handle_complex_steamdeck...")
            handled = handle_complex_steamdeck(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_steamdeck вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        elif brand_candidate == "Nintendo":
            from nintendo_utils import handle_complex_nintendo
            # "Ленивый" импорт, чтобы избежать циклических импортов.
            logger.debug("[handle_complex_Nintendo] Вызываем handle_complex_Nintendo...")
            handled = handle_complex_nintendo(
                line=line,
                cleaned_line=cleaned_line,
                countries=countries,
                price=price,
                supplier=supplier,
                comment=comment,
                user_id=user_id
            )
            logger.debug(f"[handle_complex_brand] handle_complex_Nintendo вернул {handled}")
            if handled:
                return True  # Возвращаем результат вызова функции

        else:
            logger.warning(f"[handle_complex_brand] Сложный бренд '{brand_candidate}' не поддерживается.")
            # Не возвращаем False сразу, даём шанс другим кандидатам

    # (НОВЫЙ КОММЕНТАРИЙ) Если ни один кандидат не вернул True, значит товар не обработан как сложный.
    logger.debug("[handle_complex_brand] Все кандидаты перепробованы, ни один не обработал товар -> False.")
    return False

# -----------------------------------------------------------------------------------
# Основной «обработчик» входящего сообщения (message_handler)
# -----------------------------------------------------------------------------------

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает входящее сообщение от пользователя, разбивает его на строки,
    извлекает данные о товарах, странах, ценах, поставщиках и комментариях.
    """

    # ------------------------------------------------------------------
    # СЧЁТЧИКИ и коллекции, к которым обращаются вложенные функции
    # Должны существовать ДО их объявления → поэтому идут первыми.
    # ------------------------------------------------------------------
    total_potential_products = 0
    recognized_count        = 0
    unrecognized_count      = 0
    unrecognized_products   = []
    recognized_products     = []

    # ------------------------------------------------------------------
    # 1) Новая вспомогательная функция для обработки нескольких товаров
    # ------------------------------------------------------------------
    async def handle_multiple_items(line: str, items: list) -> None:
        """
        Обрабатывает список "items", извлечённых из строки (например, несколько
        товаров). Ранее мы обрабатывали только "два" товара, теперь функция
        универсальна.
        """
        nonlocal recognized_count, recognized_products
        logging.info(f"[message_handler] Найдено {len(items)} товаров!")  # Новый комментарий

        for item in items:
            # Для каждого виртуального "товара" пытаемся определить сложный бренд
            complex_match = find_complex_brand_model(item["product_name"])
            if complex_match and handle_complex_brand(
                line=line,
                cleaned_line=item["product_name"],
                brand=complex_match[0],
                model=complex_match[1],
                countries=item["countries"],
                price=item["price"],
                supplier=supplier,
                comment=item["comment"],
                user_id=user_id
            ):
                recognized_count += 1
                recognized_products.append(line)
            else:
                # Если логика требует здесь дополнительный fallback
                # (например, find_product_cached), можно добавить, но в изначальном
                # handle_two_items этого не было, поэтому оставляем как было:
                # только попытка handle_complex_brand.
                pass

    # ------------------------------------------------------------------
    # process_single_line — стандартная логика «один товар в строке»
    # ------------------------------------------------------------------
    async def process_single_line(original_line: str, line: str) -> bool :
        nonlocal total_potential_products, recognized_count, unrecognized_count, recognized_products
        flags, cleaned_line, countries = extract_flags(original_line)

        # 1. Извлекаем данные (уже с перемещенными эмодзи)
        product_name, price, comment_text = extract_data(cleaned_line)

        if not product_name or not price:
            unrecognized_count += 1
            unrecognized_products.append({"line": line, "reason": "Нет названия или цены"})
            return False

        # 2. Обрабатываем эмодзи на ОСНОВЕ УЖЕ ИЗМЕНЕННЫХ ДАННЫХ
        product_name, comment_emojis = process_emojis(
            product_name, original_line, ALLOWED_COMMENT_EMOJIS
        )

        # 3. Нормализуем итоговое название
        product_name  = normalize_product_name(product_name)
        final_comment = f"{comment_text} {comment_emojis}".strip()

        if "❌" in comment_emojis:          # строка‑заглушка, не пишем в БД
            recognized_count += 1
            return True

        total_potential_products += 1

        # --- «сложный» бренд?
        detected_brand = next(
            (brand for brand, patterns in PATTERNS_FOR_COMPLEX_BRAND_SEARCH.items()
             if any(re.search(rf"\b{re.escape(p)}\b", product_name, re.I) for p in patterns)),
            None
        )
        complex_match = detected_brand or find_complex_brand_model(product_name)
        if complex_match:
            brand, model = (detected_brand, None) if isinstance(complex_match, str) else complex_match
            if handle_complex_brand(
                line, product_name, brand, model, countries, price, supplier,
                final_comment, user_id
            ):
                recognized_count    += 1
                recognized_products += [line]
            return True

        # --- «обычный» товар
        match = find_product_cached(product_name)
        if not match:
            unrecognized_count += 1
            unrecognized_products.append({"line": line, "reason": "Товар не найден в библиотеке"})
            return False

        brand, model_group, variant = match
        if brand in MINIMUM_PRICE_FOR_BRAND and price <= MINIMUM_PRICE_FOR_BRAND[brand]:
            recognized_count += 1
            return True

        # iPhone‑спец‑правила
        variant = apply_special_rules_iphone(
            model_group, countries[0] if countries else "", variant, PRODUCT_LIBRARY, brand
        )

        # каждой стране — своя запись (если стран нет → пустая строка)
        for country in (countries if countries else [""]):
            add_or_update_product(
                USER_DATA, user_id, line, [country], variant,
                model_group, price, supplier, final_comment
            )

        recognized_count    += 1
        recognized_products += [line]
        return True

    # ------------------------------------------------------------------
    # Извлечение поставщика
    # ------------------------------------------------------------------
    async def extract_and_handle_supplier() -> tuple:
        nonlocal lines
        supplier      = extract_supplier(update)
        forward_found = bool(supplier)
        if forward_found:
            logging.info(f"[message_handler] Поставщик извлечён из пересланного сообщения: '{supplier}'")
            return supplier, forward_found

        logging.info("[message_handler] Поставщик не извлечён из пересланного сообщения, проверяем последнюю строку...")
        if not lines:
            logging.info("[message_handler] Сообщение пустое после разделения на строки.")
            return None, forward_found

        # Поставщик может быть в квадратных скобках на последней строке
        last_line = lines[-1].strip()
        match     = re.match(r"^\[(.{1,25})]$", last_line)
        if not match:
            logging.info("[message_handler] Поставщик не указан в последней строке.")
            return None, forward_found

        extracted_supplier = match.group(1).strip()
        if len(extracted_supplier) > 25:
            logging.info("[message_handler] Поставщик … превышает допустимую длину.")
            return None, forward_found

        supplier = extracted_supplier
        logging.info(f"[message_handler] Извлечён поставщик из последней строки: '{supplier}'")
        lines = lines[:-1]             # убираем строку‑подпись из основного текста
        return supplier, forward_found

    # ------------------------------------------------------------------
    # Основное тело
    # ------------------------------------------------------------------
    try:
        # 1) user_id, username
        user_id      = update.effective_user.id
        username     = update.effective_user.username or ""   # иногда None
        user_message = update.message.text or update.message.caption
        track_user_activity(user_id, username)

        if not user_message:
            logging.info("[message_handler] У сообщения нет текста. Пропускаем обработку.")
            return

        # ------------------------------------------------------------------
        # МНОГОСТРОЧНЫЙ ПРАЙС «От 1 – …»
        # ------------------------------------------------------------------
        if is_multiline_price_message(user_message):
            logging.info("[message_handler] Обнаружен формат 'от N', парсим многострочный прайс...")
            items = parse_multiline_price(user_message)

            if not items:
                await update.message.reply_text(
                    "Не найдено товаров с 'от 1'. Возможно, минимальная партия больше 1."
                )
                return

            supplier = extract_supplier(update) or ""   # нужен для process_single_line

            # каждую позицию превращаем в «синтетическую» строку и прогоняем
            for item in items:
                synthetic_line = f"{item['name']} - {item['price']}"
                await process_single_line(synthetic_line, synthetic_line)

            # итоги
            await update.message.reply_text(
                f"Добавлено (мультиформат): {recognized_count} товаров."
            )
            return

        # ------------------------------------------------------------------
        # Обычный (однострочный) режим
        # ------------------------------------------------------------------
        logging.info(f"[message_handler] Получено сообщение от пользователя {user_id}: {user_message}")
        lines = user_message.split("\n")
        logging.info(f"[message_handler] Общее количество строк: {len(lines)}")

        supplier, forward_found = await extract_and_handle_supplier()

        for line in lines:
            original_line = line.strip()
            if not original_line:
                logging.debug("[message_handler] Пустая строка, пропускаем.")
                continue

            logging.info(f"[message_handler] Обрабатываем строку: '{original_line}'")

            # --- быстрые отсеки ---
            if len(original_line) <= 10 and "vr" not in original_line.lower():
                unrecognized_count += 1
                unrecognized_products.append({
                    "line": line,
                    "reason": "Строка ≤ 10 символов"
                })
                logging.info(f"[message_handler] Строка '{original_line}' слишком короткая.")
                continue

            if is_non_product_line(original_line):
                unrecognized_count += 1
                unrecognized_products.append({"line": line, "reason": "Метаинформация/заголовок"})
                logging.info(f"[message_handler] Пропускаем как метаинформацию: '{original_line}'")
                continue

            if any(original_line.lower().startswith(p.lower())
                   for p in FIRST_WORDS_PATTERNS_STRING_NOT_APPLY_TO_PRODUCT):
                unrecognized_count += 1
                unrecognized_products.append({"line": line, "reason": "Запрещённый стартовый паттерн"})
                logging.info(f"[message_handler] Пропускаем: запрещённый стартовый паттерн.")
                continue

            # --- особые парсеры (цвета/страны) ---
            multiple_colors_results = extract_data_with_multi_color_multiple(original_line)
            if multiple_colors_results:
                await handle_multiple_items(line, multiple_colors_results)
                continue

            color_results = extract_data_with_multi_color_strict(original_line)
            if color_results:
                await handle_multiple_items(line, color_results)
                continue

            country_results = extract_data_with_multi_country_strict(original_line)
            if country_results:
                await handle_multiple_items(line, country_results)
                continue

            # --- стандартный путь ---
            await process_single_line(original_line, line)

        # ------------------------------------------------------------------
        # Итоговая статистика
        # ------------------------------------------------------------------
        logging.info(f"[message_handler] Распознано: {recognized_count}, не распознано: {unrecognized_count}")
        failed_to_find          = sum(1 for item in unrecognized_products
                                      if item['reason'] == "Товар не найден в библиотеке")
        total_potential_products = recognized_count + failed_to_find

        await update.message.reply_text(
            f"Добавлено в список товаров: {recognized_count} из {total_potential_products}"
        )

    except Exception as e:
        logging.error(f"[message_handler] Ошибка: {e}", exc_info=True)
        await update.message.reply_text("Ошибка обработки сообщения. Попробуйте позже.")

