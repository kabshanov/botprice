# sorting_rules.py

import logging
import re
from typing import Tuple, List

logger = logging.getLogger(__name__)


def parse_memory_gb(product: str) -> int :
    """
    Извлекает объём встроенной памяти (ROM) из строки по шаблону «.../<число>(tb)?».
    Примеры:
      "8/256"  → 256
      "12/512" → 512
      "12/1TB" → 1000   (1 TB = 1000 ГБ)
    Если не найдено, возвращает 0.
    """
    m = re.search(r'\b\d+/\s*(\d+)(tb)?\b', product, re.IGNORECASE)
    if m :
        mem = int(m.group(1))
        if m.group(2) :
            mem *= 1000
        return mem
    return 0


def parse_ram_and_memory(product: str) -> tuple :
    """
    Извлекает из строки значения оперативной памяти (RAM) и встроенной памяти (ROM)
    по формату "x/a", где x – объём оперативки, a – объём памяти.

    Для ROM используется parse_memory_gb, для RAM ищется первое число до символа "/".

    Примеры:
      "Redmi Note 14 Pro 4G 8/256 Black"  → (256, 8)
      "Xiaomi 12T 12/512"                   → (512, 12)

    Если ничего не найдено, возвращает (0, 0).
    """
    product_lower = product.lower()
    memory = parse_memory_gb(product_lower)
    m = re.search(r'\b(\d+)\s*/', product_lower)
    if m :
        try :
            ram = int(m.group(1))
        except ValueError :
            ram = 0
    else :
        ram = 0
    return (memory, ram)

# ------------------ iPhone-специфические приоритеты ------------------

def sim_priority(product_name: str) -> int:
    name_lower = product_name.lower()
    if "dual sim" in name_lower:
        return 3
    elif "esim" in name_lower:
        return 2
    else:
        return 1

def capacity_priority(product_name: str) -> int:
    name_lower = product_name.lower()

    # 1) Если есть "1tb"
    if "1tb" in name_lower:
        return 1000

    # 2) Ищем (\d+)\s?gb
    match_gb = re.search(r"(\d+)\s?gb", name_lower)
    if match_gb:
        return int(match_gb.group(1))

    # 3) Ищем известные capacities
    known_caps = [64, 128, 256, 512, 1024, 2048, 3072, 4096]
    found_nums = re.findall(r"\b(\d{2,4})\b", name_lower)
    candidates = []
    for x in found_nums:
        val = int(x)
        if val in known_caps:
            candidates.append(val)
    if candidates:
        return max(candidates)

    return 0

def sort_key_iphone(product_name: str) -> Tuple[int, int, str]:
    sim = sim_priority(product_name)
    cap = capacity_priority(product_name)
    alpha = product_name.lower()

    key = (sim, cap, alpha)
    logger.debug(
        f"[sort_key_iphone] product='{product_name}', "
        f"sim={sim}, cap={cap}, alpha='{alpha}' => key={key}"
    )
    return key

# ------------------ Apple Watch-специфические приоритеты ------------------

def parse_color_tokens(tokens: List[str], known_colors: List[str]) -> (str, List[str]):
    """
    Пытается найти самое «длинное» совпадение в known_colors,
    используя первые 1..3 токенов.
    Возвращает (color_str, leftover_tokens).
    Если не находим ни 1, ни 2, ни 3, то color_str="", leftover_tokens=tokens
    """

    # до 3 токенов максимум (вы можете ограничиться 2, если надо)
    for length in (3, 2, 1):
        if len(tokens) >= length:
            candidate = " ".join(tokens[:length]).strip()  # напр. "silver m/l"
            if candidate in known_colors:
                # нашли совпадение
                leftover = tokens[length:]
                return candidate, leftover

    # если дошли сюда => ни 1, ни 2, ни 3 токена не совпало
    return "", tokens

def sort_key_apple_watch(product_name: str) -> tuple:
    import re

    # Список известных вариантов цвета
    KNOWN_COLORS_ORDER = [
        "titanium",
        "black ti",
        "natural ti",
        "midnight",
        "jet black",
        "rose gold",
        "silver",
        "starlight",
        "pink",
        "red",
        "silver stainless",
        "gold stainless",
        "graphite stainless",
        "slate titanium",
        "gold titanium",
        "natural titanium",
        "silver titanium hermes",
    ]

    # Допустимые размеры, которые могут встречаться после цвета
    ALLOWED_SIZES_ORDER = ["s", "s/m", "m", "m/l", "l"]

    name_lower = product_name.lower()

    # Извлекаем год (например, 2022, 2023, 2024 и т.д.)
    year_match = re.search(r'\b(20\d{2})\b', product_name)
    if year_match:
        year = int(year_match.group(1))
        has_year_flag = 0  # товары с годом сортируются первыми
    else:
        year = 9999
        has_year_flag = 1

    # Извлекаем размер часов (например, "42mm")
    mm_match = re.search(r"(\d{2,3})mm", name_lower)
    if mm_match:
        watch_size = int(mm_match.group(1))
        mm_index = mm_match.end()
    else:
        watch_size = 999
        mm_index = 0

    # Остаток строки после размера
    remainder = name_lower[mm_index:].strip()
    remainder = remainder.lstrip("-–— \t")
    tokens = remainder.split()

    # Если первым токеном оказался год, удаляем его
    if tokens and re.fullmatch(r"20\d{2}", tokens[0]):
        tokens = tokens[1:]

    # Определяем цвет с помощью вспомогательной функции
    color_str, leftover_tokens = parse_color_tokens(tokens, KNOWN_COLORS_ORDER)
    try:
        color_index = KNOWN_COLORS_ORDER.index(color_str)
    except ValueError:
        color_index = len(KNOWN_COLORS_ORDER)

    # Анализируем оставшиеся токены (вариант)
    # Приводим их к нижнему регистру для сравнения с ALLOWED_SIZES_ORDER
    leftover_lower = [token.lower() for token in leftover_tokens]

    # Флаг, показывающий, что остаточные токены состоят исключительно из допустимых размеров
    if leftover_lower and all(token in ALLOWED_SIZES_ORDER for token in leftover_lower):
        # Вариант состоит только из размеров
        variant_type = 0  # тип 0 – только размер
        # Преобразуем каждый токен в его индекс в ALLOWED_SIZES_ORDER
        variant_order_key = tuple(ALLOWED_SIZES_ORDER.index(token) for token in leftover_lower)
        variant_base = ""  # базовой части нет
    else:
        # Если остаток не является исключительно размерами
        variant_type = 1  # тип 1 – есть слова, отличные от размеров
        # Проверяем, заканчивается ли последовательность на допустимый размер
        if leftover_lower and leftover_lower[-1] in ALLOWED_SIZES_ORDER:
            # Отделяем трейлинг размер
            trailing_size = leftover_lower[-1]
            base_tokens = leftover_lower[:-1]
            # Если базовая часть пуста, используем пустую строку
            variant_base = " ".join(base_tokens)
            trailing_flag = 1  # наличие трейлинг размера
            trailing_order = ALLOWED_SIZES_ORDER.index(trailing_size)
        else:
            variant_base = " ".join(leftover_lower)
            trailing_flag = 0  # трейлинг размера нет
            trailing_order = -1  # чтобы товары без трейлинга шли раньше
        # Используем кортеж, в котором сначала базовая строка, потом флаг и индекс трейлинга
        variant_order_key = (variant_base, trailing_flag, trailing_order)

    # Формируем итоговый сортировочный ключ:
    # Ключ состоит из:
    # 1. has_year_flag, year
    # 2. watch_size
    # 3. color_index
    # 4. variant_type (0 если остаток – только размеры, 1 иначе)
    # 5. variant_order_key (кортеж, рассчитанный выше)
    key = (
        has_year_flag,
        year,
        watch_size,
        color_index,
        variant_type,
        variant_order_key
    )
    logger.debug(f"... => key={key}")
    return key


# ------------------ Apple Mac-специфические приоритеты ------------------

def sort_key_apple_mac(product_name: str) -> tuple:
    """
    Многокритериальная сортировка для Apple Mac:
      1) диагональ (xx") => ascending
      2) чип (по CHIP_ORDER)
      3) RAM (16 -> 32 -> ...)
      4) SSD (512 -> 1000(1TB) -> 2000(2TB) ...)
      5) leftover (цвет) — алфавит

    Пример названий:
      "MacBook Pro 16” (M4 Pro 16/512) Space Black"
      "iMac 24” (M1 16/2tb) Green"
    """

    # Порядок приоритета чипов (индекс меньше — «раньше» сортируется):
    CHIP_ORDER = [
        "intel i5","intel i6","intel i7","intel i8","intel i9",
        "m1","m1 pro","m1 max","m1 ultra",
        "m2","m2 pro","m2 max","m2 ultra",
        "m3","m3 pro","m3 max",
        "m4","m4 pro","m4 max"
    ]
    # Для удобства создадим словарь { "m4 pro": <индекс>, ... },
    # чтобы быстро получить chip_index.
    chip_index_map = {chip_name: i for i, chip_name in enumerate(CHIP_ORDER)}

    # Создадим список чипов, отсортированных по длине (убывание),
    # чтобы при поиске «M4 Pro» не срабатывало «M4» первым.
    chips_sorted_by_len = sorted(CHIP_ORDER, key=len, reverse=True)

    name_lower = product_name.lower().strip()

    # ---------------- (1) Диагональ (xx") ----------------
    diagonal = 999
    diag_match = re.search(r"(\d{1,2})[”\"]", name_lower)
    if diag_match:
        diagonal = int(diag_match.group(1))

    # ---------------- (2) Ищем чип (Longest match) --------
    # Проходим по списку, отсортированному по длине,
    # чтобы "m4 pro" проверялось раньше, чем "m4".
    chip_found = None
    chip_index = len(CHIP_ORDER)  # если не найдём, ставим в конец
    for chip_candidate in chips_sorted_by_len:
        # Составляем regex для точного совпадения: \bm4 pro\b
        pattern = re.compile(rf"\b{re.escape(chip_candidate)}\b", re.IGNORECASE)
        if pattern.search(name_lower):
            chip_found = chip_candidate
            chip_index = chip_index_map[chip_candidate]
            break

    # ---------------- (3) RAM/SSD -------------------------
    # Формат "16/512" или "16/2tb" => RAM=16, SSD=512 или 2000
    ram_val = 0
    ssd_val = 0
    ramssd_match = re.search(r"(\d+)\s*/\s*(\d+)(tb)?", name_lower)
    if ramssd_match:
        ram_str = ramssd_match.group(1)   # "16"
        ssd_str = ramssd_match.group(2)   # "512" или "2"
        ssd_tb_flag = ramssd_match.group(3) # "tb" или None

        ram_val = int(ram_str)
        if ssd_tb_flag:  # => .../2tb
            ssd_val = int(ssd_str) * 1000
        else:            # => .../512
            ssd_val = int(ssd_str)

    # ---------------- (4) leftover (удалить чип, ram/ssd, диагональ) ---
    leftover_str = name_lower

    # Удаляем диагональ
    leftover_str = re.sub(r"(\d{1,2})[”\"]", "", leftover_str)

    # Удаляем найденный чип (точно, с \b):
    if chip_found:
        pattern_remove_chip = re.compile(rf"\b{re.escape(chip_found)}\b", re.IGNORECASE)
        leftover_str = pattern_remove_chip.sub("", leftover_str)

    # Удаляем ram/ssd
    leftover_str = re.sub(r"(\d+)\s*/\s*(\d+)(tb)?", "", leftover_str)

    leftover_str = leftover_str.strip()

    # ---------------- Формируем итоговый ключ ----------------
    # Порядок:
    #   (diagonal, chip_index, ram_val, ssd_val, leftover_str)
    # leftover_str => алфавит в конце
    key = (
        diagonal,
        chip_index,
        ram_val,
        ssd_val,
        leftover_str
    )
    return key

# ------------------ Apple iPad -специфические приоритеты ------------------

def sort_key_ipad(product_name: str) -> tuple:
    """
    Многокритериальная сортировка для iPad:
      1) diagonal: число (5, 11, 13...) => ascending
      2) chip_index: "нет чипа"=0, "M1"=1, "M2"=2, "M3"=3, "M4"=4, ...
      3) capacity_val: (256GB->256, 1TB->1000, 2TB->2000...) => ascending
      4) leftover_str: алфавит (Wi-Fi, Wi-Fi + Cellular, цвет...)
    """

    # 1) Диагональ
    # Ищем паттерн: (\d{1,2})? с кавычками или без (например, "11”" или "11 ")
    # Упростим: попробуем сначала \d{1,2}[”"] если есть, иначе \b(\d{1,2})\b
    # (но нужно аккуратно не поймать 5 (поколение) за диагональ.
    # Для примера возьмём: "(\d+)[”\"]?" если есть, воспринимаем как diagonal
    diagonal = 999
    # Пробуем поиск \b(\d{1,2})[”"]\b?
    diag_match = re.search(r"\b(\d{1,2})(?:[”\"])?\b", product_name)
    if diag_match:
        # Например, "13" => 13
        diagonal = int(diag_match.group(1))

    # 2) Чип (M\d).
    # Если нет => chip_index=0 => «без чипа» идёт первым
    chip_index = 0
    chip_match = re.search(r"\bM(\d)\b", product_name, re.IGNORECASE)
    if chip_match:
        # Если нашли M1 -> chip=1, M2 -> chip=2...
        chip_digit = int(chip_match.group(1))
        chip_index = chip_digit  # M1=1, M2=2, M3=3, M4=4, ...
    # если не нашли, оставляем 0

    # 3) capacity (64GB => 64, 128GB => 128, 1TB => 1000, 2TB => 2000,...)
    capacity_val = 0
    # Ищем (\d+)(gb|tb)
    cap_match = re.search(r"(\d+)(gb|tb)", product_name, re.IGNORECASE)
    if cap_match:
        c_num_str = cap_match.group(1)  # "256" / "1" ...
        c_unit = cap_match.group(2).lower()  # "gb" / "tb"
        c_num = int(c_num_str)
        if c_unit == "tb":
            capacity_val = c_num * 1000
        else:
            capacity_val = c_num

    # 4) leftover_str
    # Удаляем диагональ, чип, и capacity из строки, что останется — leftover
    leftover_str = product_name

    # (A) Удаляем диагональ
    leftover_str = re.sub(r"(\d{1,2})([”\"])?", "", leftover_str)

    # (B) Удаляем "M\d"
    leftover_str = re.sub(r"\bM(\d)\b", "", leftover_str, flags=re.IGNORECASE)

    # (C) Удаляем capacity ((\d+)(gb|tb))
    leftover_str = re.sub(r"(\d+)(gb|tb)", "", leftover_str, flags=re.IGNORECASE)

    leftover_str = leftover_str.strip()

    # Итоговый ключ
    key = (
        diagonal,       # (1) diag
        chip_index,     # (2) chip
        capacity_val,   # (3) memory
        leftover_str    # (4) leftover alpha
    )
    return key

# ------------------ Apple AirPods -специфические приоритеты ------------------

def sort_key_apple_airpods(product_name: str) -> tuple :
    """
    Сортирует AirPods по жёсткому списку:
      (индекс 0) AirPods 2
      (1) AirPods 3
      (2) AirPods Pro 2
      (3) AirPods 4
      (4) AirPods Max

    "Longest match first", чтобы 'AirPods Pro 2' не путался с 'AirPods 2'.

    Доп. условие:
    - Если модель = 'AirPods Max', ищем год (например, 2024) => year_val=2024
      иначе year_val=0 => (сначала без года, потом с годом по возрастанию).

    Итоговый ключ:
      (model_index, year_val, leftover_str)
    """

    MODELS = [
        "AirPods 2",
        "AirPods 3",
        "AirPods Pro 2",
        "AirPods 4",
        "AirPods Max"
    ]

    model_index_map = {m : i for i, m in enumerate(MODELS)}
    # Сортируем по длине (убывание) => Longest match first
    models_by_length = sorted(MODELS, key=len, reverse=True)

    name_lower = product_name.lower()

    found_model = None
    model_index = len(MODELS)  # если не нашли => идёт в конец
    for candidate in models_by_length :
        cand_lower = candidate.lower()
        # точный regex: \b(airpods pro 2)\b
        pattern = re.compile(rf"\b{re.escape(cand_lower)}\b", re.IGNORECASE)
        if pattern.search(name_lower) :
            found_model = candidate
            model_index = model_index_map[candidate]
            break

    # Если модель = "AirPods Max", ищем год (например, 2024).
    year_val = 0
    if found_model == "AirPods Max" :
        # Ищем \b(\d{4})\b (год)
        match_year = re.search(r"\b(\d{4})\b", name_lower)
        if match_year :
            year_val = int(match_year.group(1))

    # leftover_str (для сортировки внутри одинаковой модели + года)
    leftover_str = name_lower

    # Удаляем найденную модель
    if found_model :
        pat_remove_model = re.compile(rf"\b{re.escape(found_model.lower())}\b", re.IGNORECASE)
        leftover_str = pat_remove_model.sub("", leftover_str)

    # Удаляем год, если есть
    leftover_str = re.sub(r"\b(\d{4})\b", "", leftover_str)
    leftover_str = leftover_str.strip()

    # Итоговый ключ
    key = (
        model_index,  # 0..4, или 5 если не найдена модель
        year_val,  # если AirPods Max => год, иначе 0
        leftover_str  # цвет / leftover
    )
    return key

# ------------------ Samsung Galaxy-специфические приоритеты ------------------

def sort_key_samsung_galaxy(product_name: str) -> Tuple[int, int, int, int, int, int, str] :
    """
    Логика сортировки для Samsung Galaxy:
      1. Базовая модель: извлекается числовая часть из названия модели.
         Например, "A05" и "A05s" оба дадут число 5.
      2. s_suffix: если после числа присутствует буква "s" (например, "A05s"), то s_suffix = 1, иначе 0.
         Таким образом, модель без "s" (s_suffix=0) будет сортироваться раньше.
      3. Модификация модели (mod_rank):
         - Если в строке встречается "FE" или "Edge" – mod_rank = 0.
         - Если модификация отсутствует (чистая модель) – mod_rank = 1.
         - Если присутствует символ "+" – mod_rank = 2.
         - Если присутствует "Ultra" – mod_rank = 3.
      4. Флаг 5G (fiveg_flag): если в строке встречается "5G" (без учёта регистра), то fiveg_flag = 1, иначе 0
         (товары без "5G" сортируются выше).
      5. Далее сортировка по объёму встроенной памяти (ROM) и оперативной памяти (RAM):
         сначала memory, затем ram.
      6. Tie-breaker: полное название в нижнем регистре.

    Итоговый ключ имеет вид:
       (base_model_num, s_suffix, mod_rank, fiveg_flag, memory, ram, name_lower)
    """
    name_lower = product_name.lower()

    # Извлекаем базовую модель и s_suffix:
    base_model_match = re.search(r'\b[a-zA-Z]*(\d+)(s?)\b', name_lower)
    if base_model_match :
        try :
            base_model_num = int(base_model_match.group(1))
        except ValueError :
            base_model_num = 0
        s_suffix = 1 if base_model_match.group(2) == 's' else 0
    else :
        base_model_num = 0
        s_suffix = 0

    # Определяем модификацию модели:
    mod_rank = 1  # чистая модель по умолчанию
    if re.search(r'\b(fe|edge)\b', name_lower) :
        mod_rank = 0
    elif re.search(r'\+', name_lower) :
        mod_rank = 2
    elif re.search(r'\bultra\b', name_lower) :
        mod_rank = 3

    # Флаг 5G:
    fiveg_flag = 1 if re.search(r'\b5g\b', name_lower) else 0

    # Извлекаем встроенную память (ROM) и оперативную память (RAM)
    memory, ram = parse_ram_and_memory(name_lower)

    return (base_model_num, s_suffix, mod_rank, fiveg_flag, memory, ram, name_lower)


# ------------------ Пылесосы Dyson-специфические приоритеты ------------------

def sort_dyson_clear(product_name: str) -> tuple :
    """
    Функция для сортировки пылесосов Dyson.

    Сортировка выполняется по следующему принципу:
      1. Сначала идут модели, в названии которых обнаружена буква "V" (приоритет 0),
      2. Затем модели с буквой "G" (приоритет 1),
      3. Если ни "V", ни "G" не найдены, то модели получают приоритет 2.

    При наличии в названии цифр после буквы (например, "V10", "G9") они извлекаются
    и используются как второй элемент сортировочного ключа.
    """
    product_lower = product_name.lower()
    # Ищем паттерн: буква V или G, за которой следует одна или более цифр.
    match = re.search(r'\b([vg])(\d+)', product_lower)
    if match :
        model_letter = match.group(1)
        model_number = int(match.group(2))
        # Задаём приоритет: для "v" — 0, для "g" — 1.
        letter_priority = 0 if model_letter == 'v' else 1
    else :
        letter_priority = 2
        model_number = 0

    # Ключ сортировки: (приоритет по букве, номер модели, наименование продукта для альфавитного порядка)
    return (letter_priority, model_number, product_lower)

# ------------------ Аксессуары Dyson-специфические приоритеты ------------------

def sort_dyson_accessories(product_name: str) -> tuple :
    """
    Функция сортировки аксессуаров Dyson по заданному порядку:
      0. Названия, содержащие "расческа" (например, "Расческа Dyson Paddle Brush")
      1. Названия, содержащие "подставка" (например, "Подставка для …")
      2. Названия, содержащие "кейс" (например, "Кейс Dyson Presentation")
      3. Названия, содержащие "чехол" (например, "Чехол Dyson Travel Bag")

    Если ни одно из ключевых слов не найдено, товар получает приоритет 4.
    Второй элемент кортежа – само название в нижнем регистре для стабильной алфавитной сортировки.
    """
    product_lower = product_name.lower()

    if "расческа" in product_lower :
        priority = 0
    elif "подставка" in product_lower :
        priority = 1
    elif "кейс" in product_lower :
        priority = 2
    elif "чехол" in product_lower :
        priority = 3
    else :
        priority = 4

    return (priority, product_lower)


# ------------------ Xiaomi-специфические приоритеты ------------------

def get_standard_variant_order(variant: str) -> int :
    """
    Возвращает порядковый номер варианта для стандартной серии.

    Жёстко заданный порядок (чем меньше число, тем раньше товар):
      "lite"     → 0   (всегда первым, даже если встречается пустой вариант)
      ""         → 1   (например, просто "12")
      "t"        → 2   (например, "12T")
      "t pro"    → 3   (например, "12T Pro")
      "pro"      → 4   (например, "12 Pro")
      "s pro"    → 5   (например, "12S Pro")
      "ultra"    → 6   (например, "12 Ultra" – всегда последний)
      "s ultra"  → 7   (например, "12S Ultra" – ещё ниже)

    Если вариант не найден в маппинге, то:
      – если в варианте присутствует "ultra", возвращает 100,
      – если присутствует "pro" (без ultra), возвращает 99,
      – иначе возвращает 50.
    """
    variant = variant.strip().lower()
    mapping = {
        "lite" : 0,
        "" : 1,
        "t" : 2,
        "t pro" : 3,
        "pro" : 4,
        "s pro" : 5,
        "ultra" : 6,
        "s ultra" : 7
    }
    if variant in mapping :
        return mapping[variant]
    if "ultra" in variant :
        return 100
    if "pro" in variant :
        return 99
    return 50


def parse_standard_series(product: str) -> (int, str) :
    """
    Извлекает номер серии и текстовую часть варианта для стандартных моделей.
    Например, из "xiaomi 12 pro 8/256 ..." вернёт (12, "pro").
    Если не удаётся распарсить, возвращает (999, "").
    """
    m = re.match(r'^xiaomi\s+(\d+)(.*)$', product, re.IGNORECASE)
    if not m :
        return (999, "")
    try :
        series = int(m.group(1))
    except ValueError :
        series = 999
    remainder = m.group(2).strip()
    # Отрезаем всё, что похоже на начало спецификации памяти (например, "8/256")
    remainder = re.split(r'\d+/\s*\d+(tb)?', remainder, maxsplit=1, flags=re.IGNORECASE)[0]
    return (series, remainder.strip())


def sort_key_xiaomi_standard(product_name: str) -> tuple :
    """
    Для стандартных моделей Xiaomi (не относящихся к Redmi).
    Сортировка производится по:
      - номеру серии (например, 12, 13, 14),
      - порядку варианта (через get_standard_variant_order),
      - встроенной памяти (ROM) – по возрастанию,
      - оперативной памяти (RAM) – по возрастанию,
      - алфавитному порядку полного названия.

    Итоговый ключ имеет вид:
       (0, series, variant_order, memory, ram, product_lower)
    """
    plower = product_name.strip().lower()
    if not plower.startswith("xiaomi ") :
        return (999, plower)

    # Обработка специальных случаев (например, "civi" или "mix"):
    if "civi" in plower :
        m_a = re.match(r'^xiaomi\s+civi\s+(\d+)', plower, re.IGNORECASE)
        if m_a :
            try :
                num = int(m_a.group(1))
            except :
                num = 999
            variant_order = 1 if "pro" in plower else 0
            memory, ram = parse_ram_and_memory(plower)
            return (1, 0, num, memory, ram, plower)
        m_b = re.match(r'^xiaomi\s+(\d+)\s+civi', plower, re.IGNORECASE)
        if m_b :
            try :
                num = int(m_b.group(1))
            except :
                num = 999
            memory, ram = parse_ram_and_memory(plower)
            return (1, 1, num, memory, ram, plower)
        memory, ram = parse_ram_and_memory(plower)
        return (1, 99, 999, memory, ram, plower)

    if "mix" in plower :
        m_mix = re.search(r'\bmix\s+fold\s+(\d+)\b', plower, re.IGNORECASE)
        try :
            num = int(m_mix.group(1)) if m_mix else 999
        except :
            num = 999
        memory, ram = parse_ram_and_memory(plower)
        return (2, num, memory, ram, plower)

    # Стандартная серия
    series, variant = parse_standard_series(plower)
    variant_order = get_standard_variant_order(variant)
    memory, ram = parse_ram_and_memory(plower)
    return (0, series, variant_order, memory, ram, plower)


def sort_key_redmi(product_name: str) -> tuple :
    """
    Функция сортировки для моделей Redmi с многокритериальной логикой.

    Общая логика:
      • Если после слова "redmi" в названии идет "note" (без учёта регистра),
        то товар относится к Note‑серии и получает ключ вида:
            (3, note_num, variant_order, memory, ram, designation, original_name)
        где:
          – note_num – числовое значение после слова "note";
          – variant_order: 0, если после числа нет слова "pro";
                         1, если встречается "pro" (без "pro+");
                         2, если встречается "pro+".
      • Если модель не Note, то она распределяется по подгруппам:
            Группа 0: A‑серия (например, "A3")
            Группа 1: Модели с суффиксом C (например, "12C")
            Группа 2: Чисто цифровые модели (например, "12")
         Если ни один шаблон не сработал – fallback: группа 2.

      Во всех случаях дополнительно учитываются встроенная память (ROM) и оперативная память (RAM),
      полученные через parse_ram_and_memory.

      Таким образом, все non‑Note модели (группы 0, 1 или 2) всегда сортируются раньше,
      чем Note‑модели (группа 3).
    """
    s = product_name.strip()
    lower_s = s.lower()
    memory, ram = parse_ram_and_memory(lower_s)

    # Извлекаем часть названия после "redmi" (ожидается формат "xiaomi redmi <designation>")
    m = re.match(r'^xiaomi\s+redmi\s+([^-–]+)', lower_s)
    if m :
        designation = m.group(1).strip()
    else :
        parts = lower_s.split("redmi", 1)
        designation = parts[1].strip() if len(parts) > 1 else ""

    # Если designation начинается со слова "note" -> Note‑серия (группа 3)
    if designation.startswith("note") :
        m_note = re.match(r'^note\s+(\d+)(.*)$', designation, re.IGNORECASE)
        if m_note :
            try :
                note_num = int(m_note.group(1))
            except :
                note_num = 999
            remainder = m_note.group(2).strip()
            r_lower = remainder.lower()
            # Определяем variant_order:
            # Если слово "pro" не встречается – базовая модель (0)
            # Если встречается "pro+" – variant_order = 2
            # Если встречается "pro" (без "pro+") – variant_order = 1
            if "pro" not in r_lower :
                variant_order = 0
            elif "pro+" in r_lower :
                variant_order = 2
            elif "pro" in r_lower :
                variant_order = 1
            else :
                variant_order = 99
            return (3, note_num, variant_order, memory, ram, designation, s)
        else :
            return (3, 999, 99, memory, ram, designation, s)

    # Non‑Note модели – разбиваем на подгруппы:
    # Группа 0: A‑серия, формат "a" + число (например, "A3")
    m_a = re.match(r'^a(\d+)$', designation, re.IGNORECASE)
    if m_a :
        try :
            num = int(m_a.group(1))
        except :
            num = 999
        return (0, num, memory, ram, designation)

    # Группа 1: модели с суффиксом C, формат "<число>c" (например, "12C")
    m_c = re.match(r'^(\d+)c\b', designation, re.IGNORECASE)
    if m_c :
        try :
            num = int(m_c.group(1))
        except :
            num = 999
        return (1, num, memory, ram, designation)

    # Группа 2: чисто цифровые модели, формат "<число>" (например, "12")
    m_num = re.match(r'^(\d+)$', designation, re.IGNORECASE)
    if m_num :
        try :
            num = int(m_num.group(1))
        except :
            num = 999
        return (2, num, memory, ram, designation)

    # Fallback для нераспознанных non‑Note моделей – помещаем их в группу 2
    return (2, 999, memory, ram, designation)


def sort_key_poco(product_name: str) -> tuple:
    """
    Сортировка для моделей Poco.

    Логика:
      1. Если название (после приведения к нижнему регистру) не начинается с "poco ",
         возвращается ключ (999, 0, <полное название>).
      2. Иначе удаляется префикс "poco" и анализируется оставшаяся часть.
      3. С помощью регулярного выражения извлекается:
             - первая буква (определяющая серию, например, c, m, x, f),
             - числовая часть,
             - оставшийся текст.
      4. Итоговый ключ сортировки имеет вид:
             (series_rank, numeric_part, memory, ram, remainder, full_lower_name)
         где memory и ram извлекаются через parse_ram_and_memory.
    """
    s = product_name.strip().lower()
    if not s.startswith("poco "):
        return (999, 0, s)
    s_rem = s[len("poco "):].strip()
    memory, ram = parse_ram_and_memory(s)
    m = re.match(r'^([a-z])(\d+)(.*)$', s_rem)
    if m:
        series_letter = m.group(1)
        try:
            number_part = int(m.group(2))
        except ValueError:
            number_part = 999
        remainder = m.group(3).strip()
        series_order = {"c": 0, "m": 1, "x": 2, "f": 3}
        rank = series_order.get(series_letter, 999)
        return (rank, number_part, memory, ram, remainder, s)
    else:
        return (999, memory, ram, s)



def sort_key_redmi_pad(product_name: str) -> tuple :
    """
    Функция сортировки для моделей Redmi Pad.

    Логика сортировки:
      - Если название (после удаления префикса "xiaomi") начинается с "redmi pad se",
        то модель получает группу 0 (идёт первой).
      - Если название начинается с "redmi pad pro", то группа 2 (идёт последней).
      - Иначе – группа 1.
    Дополнительно сортировка производится по встроенной памяти и оперативке,
    извлечённым через parse_ram_and_memory, а затем по полному названию.

    Итоговый ключ имеет вид: (group, memory, ram, lower_name)
    """
    lower_name = product_name.strip().lower()
    if lower_name.startswith("xiaomi ") :
        lower_name = lower_name[len("xiaomi ") :].strip()
    if not lower_name.startswith("redmi pad") :
        return (999, 0, 0, lower_name)
    if lower_name.startswith("redmi pad se") :
        group = 0
    elif lower_name.startswith("redmi pad pro") :
        group = 2
    else :
        group = 1
    memory, ram = parse_ram_and_memory(lower_name)
    return (group, memory, ram, lower_name)


def sort_key_xiaomi_by_model_group(model_group: str, product_name: str) -> tuple :
    """
    Выбирает функцию сортировки в зависимости от model_group:
      - "xiaomi"    → sort_key_xiaomi_standard
      - "redmi"     → sort_key_redmi
      - "poco"      → sort_key_poco
      - "redmi pad" → sort_key_redmi_pad
    Если model_group не распознан, используется стандартная логика.
    """
    mg = model_group.lower().strip()
    if mg == "xiaomi" :
        return sort_key_xiaomi_standard(product_name)
    elif mg == "redmi" :
        return sort_key_redmi(product_name)
    elif mg == "poco" :
        return sort_key_poco(product_name)
    elif mg == "redmi pad" :
        return sort_key_redmi_pad(product_name)
    else :
        return sort_key_xiaomi_standard(product_name)

def sort_key_tecno_mobile(product_name: str) -> tuple:
    """
    Многокритериальная сортировка для Tecno Mobile:
      1) Go      → категория 0
      2) число+C → категория 1
      3) Pro     → категория 2
      4) Neo     → категория 3
      5) остальные → категория 4
    Затем — по объёму ROM (из parse_memory_gb) и лексикографически.
    """
    name_lower = product_name.lower()

    if re.search(r'\bgo\b', name_lower):
        cat = 0
    elif re.search(r'\b\d+c\b', name_lower):
        cat = 1
    elif re.search(r'\bpro\b', name_lower):
        cat = 2
    elif 'neo' in name_lower:
        cat = 3
    else:
        cat = 4

    # ROM в гигабайтах
    rom = parse_memory_gb(name_lower)
    return (cat, rom, name_lower)

# ------------------------------------

# Словарь для остальных специальных брендов (без Xiaomi, у которого своя логика с model_group)
SPECIAL_SORTING_BRAND = {
    "apple iphone" : sort_key_iphone,
    "apple watch" : sort_key_apple_watch,
    "apple mac" : sort_key_apple_mac,
    "apple ipad" : sort_key_ipad,
    "apple airpods" : sort_key_apple_airpods,
    "samsung galaxy" : sort_key_samsung_galaxy,
    "пылесосы dyson" : sort_dyson_clear,
    "аксессуары dyson" : sort_dyson_accessories,
    "tecno mobile" : sort_key_tecno_mobile
    # Если потребуется добавить ещё бренды…
}



# Дефолтная логика сортировки
def sort_key_default(product_name: str) -> tuple :
    return (product_name.lower(),)


# Основной механизм получения сортировочного ключа с учётом brand и model_group
def get_sort_key(brand: str, model_group: str, product_name: str) -> tuple :
    brand_lower = brand.lower().strip()
    model_group_lower = model_group.lower().strip()
    if brand_lower == "xiaomi" :
        # Выбираем функцию сортировки по model_group
        key = sort_key_xiaomi_by_model_group(model_group_lower, product_name)
        logger.debug(
            f"[get_sort_key] BRAND='{brand}', model_group='{model_group}', product='{product_name}' => key={key}")
        return key
    elif brand_lower in SPECIAL_SORTING_BRAND :
        func = SPECIAL_SORTING_BRAND[brand_lower]
        key = func(product_name)
        logger.debug(f"[get_sort_key] BRAND='{brand}', product='{product_name}' => use {func.__name__}, key={key}")
        return key
    else :
        key = sort_key_default(product_name)
        logger.debug(f"[get_sort_key] BRAND='{brand}', product='{product_name}' => default, key={key}")
        return key

