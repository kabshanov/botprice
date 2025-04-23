#shared_data.py

from typing import Dict, Any
from currency_api import CurrencyAPI, ExchangeRateAPI

currency_api_cbr = CurrencyAPI()
exchange_api = ExchangeRateAPI(api_key="a9bcac2dc59778eb01b5b350")

# Временное хранилище данных пользователей
USER_DATA: Dict[int, Dict[str, Any]] = {}

# Словарь для сопоставления эмодзи-флагов с названием стран
COUNTRY_EMOJI_MAP = {
    "🇦🇫": "Афганистан",
    "🇦🇱": "Албания",
    "🇩🇿": "Алжир",
    "🇦🇩": "Андорра",
    "🇦🇴": "Ангола",
    "🇦🇬": "Антигуа и Барбуда",
    "🇦🇷": "Аргентина",
    "🇦🇲": "Армения",
    "🇦🇺": "Австралия",
    "🇦🇹": "Австрия",
    "🇦🇿": "Азербайджан",
    "🇧🇸": "Багамы",
    "🇧🇭": "Бахрейн",
    "🇧🇩": "Бангладеш",
    "🇧🇧": "Барбадос",
    "🇧🇾": "Беларусь",
    "🇧🇪": "Бельгия",
    "🇧🇿": "Белиз",
    "🇧🇯": "Бенин",
    "🇧🇹": "Бутан",
    "🇧🇴": "Боливия",
    "🇧🇦": "Босния и Герцеговина",
    "🇧🇼": "Ботсвана",
    "🇧🇷": "Бразилия",
    "🇧🇳": "Бруней",
    "🇧🇬": "Болгария",
    "🇧🇫": "Буркина-Фасо",
    "🇧🇮": "Бурунди",
    "🇨🇻": "Кабо-Верде",
    "🇰🇭": "Камбоджа",
    "🇨🇲": "Камерун",
    "🇨🇦": "Канада",
    "🇨🇫": "Центральноафриканская Республика",
    "🇹🇩": "Чад",
    "🇨🇱": "Чили",
    "🇨🇳": "Китай",
    "🇨🇴": "Колумбия",
    "🇰🇲": "Коморы",
    "🇨🇬": "Конго - Браззавиль",
    "🇨🇩": "Конго - Киншаса",
    "🇨🇷": "Коста-Рика",
    "🇭🇷": "Хорватия",
    "🇨🇺": "Куба",
    "🇨🇾": "Кипр",
    "🇨🇿": "Чехия",
    "🇩🇰": "Дания",
    "🇩🇯": "Джибути",
    "🇩🇲": "Доминика",
    "🇩🇴": "Доминиканская Республика",
    "🇪🇨": "Эквадор",
    "🇪🇬": "Египет",
    "🇸🇻": "Сальвадор",
    "🇬🇶": "Экваториальная Гвинея",
    "🇪🇷": "Эритрея",
    "🇪🇪": "Эстония",
    "🇪🇹": "Эфиопия",
    "🇫🇯": "Фиджи",
    "🇫🇮": "Финляндия",
    "🇫🇷": "Франция",
    "🇬🇦": "Габон",
    "🇬🇲": "Гамбия",
    "🇬🇪": "Грузия",
    "🇩🇪": "Германия",
    "🇬🇭": "Гана",
    "🇬🇷": "Греция",
    "🇬🇩": "Гренада",
    "🇬🇹": "Гватемала",
    "🇬🇳": "Гвинея",
    "🇬🇼": "Гвинея-Бисау",
    "🇬🇾": "Гайана",
    "🇭🇹": "Гаити",
    "🇭🇳": "Гондурас",
    "🇭🇺": "Венгрия",
    "🇮🇸": "Исландия",
    "🇮🇳": "Индия",
    "🇮🇩": "Индонезия",
    "🇮🇷": "Иран",
    "🇮🇶": "Ирак",
    "🇮🇪": "Ирландия",
    "🇮🇱": "Израиль",
    "🇮🇹": "Италия",
    "🇯🇲": "Ямайка",
    "🇯🇵": "Япония",
    "🇯🇴": "Иордания",
    "🇰🇿": "Казахстан",
    "🇰🇪": "Кения",
    "🇰🇮": "Кирибати",
    "🇰🇼": "Кувейт",
    "🇰🇬": "Киргизия",
    "🇱🇦": "Лаос",
    "🇱🇻": "Латвия",
    "🇱🇧": "Ливан",
    "🇱🇸": "Лесото",
    "🇱🇷": "Либерия",
    "🇱🇾": "Ливия",
    "🇱🇮": "Лихтенштейн",
    "🇱🇹": "Литва",
    "🇱🇺": "Люксембург",
    "🇲🇴": "Макао",
    "🇲🇰": "Северная Македония",
    "🇲🇬": "Мадагаскар",
    "🇲🇼": "Малави",
    "🇲🇾": "Малайзия",
    "🇲🇻": "Мальдивы",
    "🇲🇱": "Мали",
    "🇲🇹": "Мальта",
    "🇲🇭": "Маршалловы Острова",
    "🇲🇷": "Мавритания",
    "🇲🇺": "Маврикий",
    "🇲🇽": "Мексика",
    "🇫🇲": "Федеративные Штаты Микронезии",
    "🇲🇩": "Молдова",
    "🇲🇨": "Монако",
    "🇲🇳": "Монголия",
    "🇲🇪": "Черногория",
    "🇲🇦": "Марокко",
    "🇲🇿": "Мозамбик",
    "🇲🇲": "Мьянма",
    "🇳🇦": "Намибия",
    "🇳🇷": "Науру",
    "🇳🇵": "Непал",
    "🇳🇱": "Нидерланды",
    "🇳🇿": "Новая Зеландия",
    "🇳🇮": "Никарагуа",
    "🇳🇪": "Нигер",
    "🇳🇬": "Нигерия",
    "🇰🇵": "Северная Корея",
    "🇵🇰": "Пакистан",
    "🇵🇼": "Палау",
    "🇵🇦": "Панама",
    "🇵🇬": "Папуа — Новая Гвинея",
    "🇵🇾": "Парагвай",
    "🇵🇪": "Перу",
    "🇵🇭": "Филиппины",
    "🇵🇱": "Польша",
    "🇵🇹": "Португалия",
    "🇶🇦": "Катар",
    "🇷🇴": "Румыния",
    "🇷🇺": "Россия",
    "🇷🇼": "Руанда",
    "🇰🇳": "Сент-Китс и Невис",
    "🇱🇨": "Сент-Люсия",
    "🇻🇨": "Сент-Винсент и Гренадины",
    "🇼🇸": "Самоа",
    "🇸🇲": "Сан-Марино",
    "🇸🇹": "Сан-Томе и Принсипи",
    "🇸🇦": "Саудовская Аравия",
    "🇸🇳": "Сенегал",
    "🇷🇸": "Сербия",
    "🇸🇨": "Сейшельские Острова",
    "🇸🇱": "Сьерра-Леоне",
    "🇸🇬": "Сингапур",
    "🇸🇰": "Словакия",
    "🇸🇮": "Словения",
    "🇸🇧": "Соломоновы Острова",
    "🇸🇴": "Сомали",
    "🇿🇦": "ЮАР",
    "🇰🇷": "Южная Корея",
    "🇸🇸": "Южный Судан",
    "🇪🇸": "Испания",
    "🇱🇰": "Шри-Ланка",
    "🇸🇩": "Судан",
    "🇸🇷": "Суринам",
    "🇸🇪": "Швеция",
    "🇨🇭": "Швейцария",
    "🇸🇾": "Сирия",
    "🇹🇼": "Тайвань",
    "🇹🇯": "Таджикистан",
    "🇹🇿": "Танзания",
    "🇹🇭": "Таиланд",
    "🇹🇱": "Восточный Тимор",
    "🇹🇬": "Того",
    "🇹🇴": "Тонга",
    "🇹🇹": "Тринидад и Тобаго",
    "🇹🇳": "Тунис",
    "🇹🇷": "Турция",
    "🇹🇲": "Туркменистан",
    "🇺🇬": "Уганда",
    "🇺🇦": "Украина",
    "🇦🇪": "ОАЭ",
    "🇬🇧": "Великобритания",
    "🇺🇸": "США",
    "🇺🇾": "Уругвай",
    "🇺🇿": "Узбекистан",
    "🇻🇺": "Вануату",
    "🇻🇪": "Венесуэла",
    "🇻🇳": "Вьетнам",
    "🇾🇪": "Йемен",
    "🇿🇲": "Замбия",
    "🇿🇼": "Зимбабве",
    "🇪🇺" : "Европа",
    "🇭🇰" : "Гонконг",

}

COUNTRY_WORD_MAP = {
    "EAC" : "Россия",
    "ЕАЭС" : "Россия",
    "RU" : "Россия",
}

# Словарь для сопоставления названия стран с эмодзи
TEXT_TO_FLAG = {
    "Афганистан": "🇦🇫",
    "Албания": "🇦🇱",
    "Алжир": "🇩🇿",
    "Андорра": "🇦🇩",
    "Ангола": "🇦🇴",
    "Антигуа и Барбуда": "🇦🇬",
    "Аргентина": "🇦🇷",
    "Армения": "🇦🇲",
    "Австралия": "🇦🇺",
    "Австрия": "🇦🇹",
    "Азербайджан": "🇦🇿",
    "Багамы": "🇧🇸",
    "Бахрейн": "🇧🇭",
    "Бангладеш": "🇧🇩",
    "Барбадос": "🇧🇧",
    "Беларусь": "🇧🇾",
    "Бельгия": "🇧🇪",
    "Белиз": "🇧🇿",
    "Бенин": "🇧🇯",
    "Бутан": "🇧🇹",
    "Боливия": "🇧🇴",
    "Босния и Герцеговина": "🇧🇦",
    "Ботсвана": "🇧🇼",
    "Бразилия": "🇧🇷",
    "Бруней": "🇧🇳",
    "Болгария": "🇧🇬",
    "Буркина-Фасо": "🇧🇫",
    "Бурунди": "🇧🇮",
    "Кабо-Верде": "🇨🇻",
    "Камбоджа": "🇰🇭",
    "Камерун": "🇨🇲",
    "Канада": "🇨🇦",
    "Центральноафриканская Республика": "🇨🇫",
    "Чад": "🇹🇩",
    "Чили": "🇨🇱",
    "Китай": "🇨🇳",
    "Колумбия": "🇨🇴",
    "Коморы": "🇰🇲",
    "Конго - Браззавиль": "🇨🇬",
    "Конго - Киншаса": "🇨🇩",
    "Коста-Рика": "🇨🇷",
    "Хорватия": "🇭🇷",
    "Куба": "🇨🇺",
    "Кипр": "🇨🇾",
    "Чехия": "🇨🇿",
    "Дания": "🇩🇰",
    "Джибути": "🇩🇯",
    "Доминика": "🇩🇲",
    "Доминиканская Республика": "🇩🇴",
    "Эквадор": "🇪🇨",
    "Египет": "🇪🇬",
    "Сальвадор": "🇸🇻",
    "Экваториальная Гвинея": "🇬🇶",
    "Эритрея": "🇪🇷",
    "Эстония": "🇪🇪",
    "Эфиопия": "🇪🇹",
    "Фиджи": "🇫🇯",
    "Финляндия": "🇫🇮",
    "Франция": "🇫🇷",
    "Габон": "🇬🇦",
    "Гамбия": "🇬🇲",
    "Грузия": "🇬🇪",
    "Германия": "🇩🇪",
    "Гана": "🇬🇭",
    "Греция": "🇬🇷",
    "Гренада": "🇬🇩",
    "Гватемала": "🇬🇹",
    "Гвинея": "🇬🇳",
    "Гвинея-Бисау": "🇬🇼",
    "Гайана": "🇬🇾",
    "Гаити": "🇭🇹",
    "Гондурас": "🇭🇳",
    "Венгрия": "🇭🇺",
    "Исландия": "🇮🇸",
    "Индия": "🇮🇳",
    "Индонезия": "🇮🇩",
    "Иран": "🇮🇷",
    "Ирак": "🇮🇶",
    "Ирландия": "🇮🇪",
    "Израиль": "🇮🇱",
    "Италия": "🇮🇹",
    "Ямайка": "🇯🇲",
    "Япония": "🇯🇵",
    "Иордания": "🇯🇴",
    "Казахстан": "🇰🇿",
    "Кения": "🇰🇪",
    "Кирибати": "🇰🇮",
    "Кувейт": "🇰🇼",
    "Киргизия": "🇰🇬",
    "Лаос": "🇱🇦",
    "Латвия": "🇱🇻",
    "Ливан": "🇱🇧",
    "Лесото": "🇱🇸",
    "Либерия": "🇱🇷",
    "Ливия": "🇱🇾",
    "Лихтенштейн": "🇱🇮",
    "Литва": "🇱🇹",
    "Люксембург": "🇱🇺",
    "Макао": "🇲🇴",
    "Северная Македония": "🇲🇰",
    "Мадагаскар": "🇲🇬",
    "Малави": "🇲🇼",
    "Малайзия": "🇲🇾",
    "Мальдивы": "🇲🇻",
    "Мали": "🇲🇱",
    "Мальта": "🇲🇹",
    "Маршалловы Острова": "🇲🇭",
    "Мавритания": "🇲🇷",
    "Маврикий": "🇲🇺",
    "Мексика": "🇲🇽",
    "Федеративные Штаты Микронезии": "🇫🇲",
    "Молдова": "🇲🇩",
    "Монако": "🇲🇨",
    "Монголия": "🇲🇳",
    "Черногория": "🇲🇪",
    "Марокко": "🇲🇦",
    "Мозамбик": "🇲🇿",
    "Мьянма": "🇲🇲",
    "Намибия": "🇳🇦",
    "Науру": "🇳🇷",
    "Непал": "🇳🇵",
    "Нидерланды": "🇳🇱",
    "Новая Зеландия": "🇳🇿",
    "Никарагуа": "🇳🇮",
    "Нигер": "🇳🇪",
    "Нигерия": "🇳🇬",
    "Северная Корея": "🇰🇵",
    "Пакистан": "🇵🇰",
    "Палау": "🇵🇼",
    "Панама": "🇵🇦",
    "Папуа — Новая Гвинея": "🇵🇬",
    "Парагвай": "🇵🇾",
    "Перу": "🇵🇪",
    "Филиппины": "🇵🇭",
    "Польша": "🇵🇱",
    "Португалия": "🇵🇹",
    "Катар": "🇶🇦",
    "Румыния": "🇷🇴",
    "Россия": "🇷🇺",
    "Руанда": "🇷🇼",
    "Сент-Китс и Невис": "🇰🇳",
    "Сент-Люсия": "🇱🇨",
    "Сент-Винсент и Гренадины": "🇻🇨",
    "Самоа": "🇼🇸",
    "Сан-Марино": "🇸🇲",
    "Сан-Томе и Принсипи": "🇸🇹",
    "Саудовская Аравия": "🇸🇦",
    "Сенегал": "🇸🇳",
    "Сербия": "🇷🇸",
    "Сейшельские Острова": "🇸🇨",
    "Сьерра-Леоне": "🇸🇱",
    "Сингапур": "🇸🇬",
    "Словакия": "🇸🇰",
    "Словения": "🇸🇮",
    "Соломоновы Острова": "🇸🇧",
    "Сомали": "🇸🇴",
    "ЮАР": "🇿🇦",
    "Южная Корея": "🇰🇷",
    "Южный Судан": "🇸🇸",
    "Испания": "🇪🇸",
    "Шри-Ланка": "🇱🇰",
    "Судан": "🇸🇩",
    "Суринам": "🇸🇷",
    "Швеция": "🇸🇪",
    "Швейцария": "🇨🇭",
    "Сирия": "🇸🇾",
    "Тайвань": "🇹🇼",
    "Таджикистан": "🇹🇯",
    "Танзания": "🇹🇿",
    "Таиланд": "🇹🇭",
    "Восточный Тимор": "🇹🇱",
    "Того": "🇹🇬",
    "Тонга": "🇹🇴",
    "Тринидад и Тобаго": "🇹🇹",
    "Тунис": "🇹🇳",
    "Турция": "🇹🇷",
    "Туркменистан": "🇹🇲",
    "Уганда": "🇺🇬",
    "Украина": "🇺🇦",
    "ОАЭ": "🇦🇪",
    "Великобритания": "🇬🇧",
    "США": "🇺🇸",
    "Уругвай": "🇺🇾",
    "Узбекистан": "🇺🇿",
    "Вануату": "🇻🇺",
    "Венесуэла": "🇻🇪",
    "Вьетнам": "🇻🇳",
    "Йемен": "🇾🇪",
    "Замбия": "🇿🇲",
    "Зимбабве": "🇿🇼",
    "Европа" : "🇪🇺",
    "Гонконг" : "🇭🇰"
}

# Разрешённые эмодзи в cleaned_line
EMOJIS_COLORS = ["⚫", "⚫️", "🖤", "💛", "🟡", "❤️", "🔴", "⚪", "⚪️", "🤍", "💚",
                 "🟢", "🔵", "💙", "💖", "💜", "🟣", "🟠", "🍊", "🤎", "🟤", "🩶"]


# Разрешённые эмодзи в комментариях
ALLOWED_COMMENT_EMOJIS = ["🚚", "🚛", "🚗", "🚙", "🚕", "❌", "✈️", "🚘", "📦"]

MAX_TELEGRAM_TEXT = 4096

#Словарь не разрешенных комментариев
IGNORING_COMMENT = ["без гребня", "с гребнем", "HIT", "NEW", "m1",
    "m2", "m3", "m4", "CPU", "GPU", "НОВИНКА", "р", "орига!!", "орига!", "орига",
    "S/M", "M/L", "S", "M", "L",
    "кейсом", "с кейсом", "без кейса", "(без кейса)", "с кейсом наша вилка", "с чехлом", #для дайсон
    "1шт", "2шт", "3шт", "4шт", "5шт", "6шт", "7шт", "шт",
    "NFC", "esim", "e-sim", "2 Sim", "2-Sim", "2Sim","SD8gen3", "наша вилка", "остаток - фото", "mryp3",
    "Маруся",]

#Словарь для сопоставления комментария
COMMENT_ADD = ["коробка", "акб", "б/у", "бу", "ошибка", "как новые", "потертости", "царапина", "царапинки", "скол",
               "актив", "Обменка", "скол", "Asis+ No Box", "Asis+", "No Box", "RFB", "Asis", "распак", "вскрыта",
               "пломба", "повреждена", "упаковка", "Открыт"]

# 💵💰 Минимальные цены в рублях для бренда 💰💵
MINIMUM_PRICE_FOR_BRAND = {
    "Apple iPhone": 25000,
    "Apple Watch": 8000,
    "Apple Mac": 40000,
    "Apple iPad": 10000,
    "Apple Airpods" : 8000,
    "Стайлеры для волос Dyson" : 20000,
    "Фены для волос Dyson" : 20000,
    "Выпрямители для волос Dyson" : 20000,
    "Пылесосы Dyson" : 20000,
    "Системы очистки воздуха Dyson" : 20000,
    "Сушилки для рук Dyson" : 100000,
    "Samsung Galaxy" : 3000,
    "Marshall" : 3000
}

# ❌ Эти первые слова не относятся к товару ❌
FIRST_WORDS_PATTERNS_STRING_NOT_APPLY_TO_PRODUCT = [
    "от",
    "( От ",
    "(От ",
    "🛡 +3 месяца",
    "🛡 +6 месяцев",
    "🛡 +12 месяцев",
    "Гравировка",
    "📍💻Гравировка",
    "💻Гравировка",
    "Гарантия",
    "Цены актуальны на",
    "Прайс"
]

CODES_NO_PRICE = {
    #Дайсоны:
    "594817", "560847", "400726", "599030", "596926",
    "448852", "448872", "470521", "448799", "447033",
}


# 📱 Специальные правила для IPHONE 📱>>>>>>>>>>>>>>>>>>
SPECIAL_RULES_IPHONE = {
    "iPhone 11" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 11 Pro" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 11 Pro Max" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 12" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 12 Pro" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 12 Pro Max" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 13" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 13 Mini" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 13 Pro" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 13 Pro Max" : {
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 14" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 14 Plus" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 14 Pro" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 14 Pro Max" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        # Добавьте другие страны при необходимости
    },
    "iPhone 15" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Сингапур" : {
            "type" : lambda model : f"{model} Dual sim"
        }
        # Добавьте другие страны при необходимости
    },
    "iPhone 15 Plus" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Сингапур" : {
            "type" : lambda model : f"{model} Dual sim"
        }
        # Добавьте другие страны при необходимости
    },
    "iPhone 15 Pro" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Сингапур" : {
            "type" : lambda model : f"{model} Dual sim"
        }
        # Добавьте другие страны при необходимости
    },
    "iPhone 15 Pro Max" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Сингапур" : {
            "type" : lambda model : f"{model} Dual sim"
        }
        # Добавьте другие страны при необходимости
    },
    "iPhone 16": {
        "США": {
            "type": lambda model: f"{model} eSim"
        },
        "Китай": {
            "type": lambda model: f"{model} Dual sim"
        },
        "Гонконг": {
            "type": lambda model: f"{model} Dual sim"
        },
        "Сингапур" : {
            "type" : lambda model : f"{model} Dual sim"
        }
        # Добавьте другие страны при необходимости
    },
    "iPhone 16 Plus" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Сингапур" : {
            "type" : lambda model : f"{model} Dual sim"
        }
        # Добавьте другие страны при необходимости
    },
    "iPhone 16 Pro" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Сингапур" : {
            "type" : lambda model : f"{model} Dual sim"
        }
        # Добавьте другие страны при необходимости
    },
    "iPhone 16 Pro Max" : {
        "США" : {
            "type" : lambda model : f"{model} eSim"
        },
        "Китай" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Гонконг" : {
            "type" : lambda model : f"{model} Dual sim"
        },
        "Сингапур" : {
            "type" : lambda model : f"{model} Dual sim"
        }
        # Добавьте другие страны при необходимости
    },
}

IGNORING_APPLE_IPHONE_RECOGNITION = [
    # не считаем за apple iphone если содержаться слова
    "WiFi", "WiFi", "Wi-Fi", "ipad", "mac", "2TB", "3TB", "4TB", "m1",
    "m2", "m3", "m4", "Macbook", "Air",
    "CPU", "GPU", "Xiaomi", "samsung", "note", "Redmi", "pad", "Galaxy", "Pixel", "Doogee", "CMF"
]
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# ⌚️Специальные правила для APPLE WATCH ⌚️>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
SPECIAL_RULE_CASE_SIZE_APPLE_WATCH = {
    # Модель "AW Ultra 2" всегда 49mm, если явно не указано
    "AW Ultra 2": "49mm",

    # В будущем вы можете добавлять и другие модели:
    # "AW Ultra 3": "51mm",
    # "AW SE X": "40mm",
    # ...
}

SPECIAL_RULE_YEAR_RELEASE_APPLE_WATCH_ULTRA_2 = {
    "2024" : ["Natural Ti", "Black Ti",],
    "2023" : ["Titanium"]
}

IGNORING_APPLE_WATCH_STRAP_TYPE = {
    # игнорирование strap_type для следующих case_type
    "AW Series 10" : {
        "Slate Titanium" : [
            "Sport Band Denim",
            "Sport Band Plum",
            "Sport Band Lake Green",
            "Sport Band Starlight",
            "Sport Band Light Blush",
            "Sport Band Stone Gray",
            "Sport Band Black",
            "Sport Band Pride Edition",
            "Sport Band Black Unity",
            "Sport Band Midnight",
            "Sport Band"
        ],
        "Gold Titanium" : [
            "Sport Band Denim",
            "Sport Band Plum",
            "Sport Band Lake Green",
            "Sport Band Starlight",
            "Sport Band Light Blush",
            "Sport Band Stone Gray",
            "Sport Band Black",
            "Sport Band Pride Edition",
            "Sport Band Black Unity",
            "Sport Band Midnight",
            "Sport Band"
        ]
    }
    #в будущем можно добавить другие модели
}

IGNORING_APPLE_WATCH_WITHOUT_YEAR_RELEASE = [
    # не считаем за apple watch если не содержаться год выпуска
    "AW SE 2", "AW Ultra 2"
]

IGNORING_APPLE_WATCH_RECOGNITION = [
    # не считаем за apple iphone если содержаться слова
    "WiFi", "WiFi", "Wi-Fi", "ipad", "mac", "2TB", "3TB", "4TB", "m1",
    "m2", "m3", "m4", "Macbook", "Air",
    "CPU", "GPU", "Xiaomi", "samsung", "note", "Redmi", "pad", "ipad", "Galaxy",
]
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# 💻 Специальные правила для Apple Mac 💻>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
IGNORING_APPLE_MAC_RECOGNITION = [
    # не считаем за apple mac если содержаться слова
    "iPad"
]

SPECIAL_ALIASES_FOR_FINAL_PRODUCT_NAME_APPLE_MAC = {
    # Специальные aliases для итогового названия Apple Mac
    # БЛОК MacBook Pro
    "MRX43" : ["MacBook Pro 14” (M3 Pro 18/1TB) Space Black"], #MacBook Pro 14” (M3 Pro, 18GB, 1024GB) MRX43 Space Black
    "MX2J3" : ["MacBook Pro 14” (M4 Pro 24/1TB) Space Black"], #MacBook Pro 14” (M4 Pro, 24GB, 1024GB) MX2J3 Space Black
    "MUW73" : ["MacBook Pro 16” (M3 Max 48/1TB) Silver"],  # MacBook Pro 16” (M3 Max, 48 GB, 1024 GB) MUW73 Silver
    "MX303" : ["MacBook Pro 16” (M4 Max 36/1TB) Space Black"],# MacBook Pro 16” (M4 Max, 36 GB, 1024 GB) MX303 Space Black
    "MX313" : ["MacBook Pro 16” (M4 Max 48/1TB) Space Black"], # MacBook Pro 16” (M4 Max, 48 GB, 1024 GB) MX313 Space Black
    "MPHE3" : ["MacBook Pro 14” (M2 Pro 16/512) Space Gray"],
    "MRW43" : ["MacBook Pro 16” (M3 Pro 18/512) Silver"],
    "MUW63" : ["MacBook Pro 16” (M3 Max 48/1TB) Space Black"],
    "MCX14" : ["MacBook Pro 14” (M4 24/1TB) Silver"],
    "MX2F3" : ["MacBook Pro 14” (M4 Pro 24/1TB) Silver"],
    "MX2K3" : ["MacBook Pro 14” (M4 Max 36/1TB) Space Black"],
    "MX2Y3" : ["MacBook Pro 14” (M4 Pro 48/512) Space Black"],
    "MRW13" : ["MacBook Pro 16” (M3 Pro 18/512) Space Black"],
    "MRX33" : ["MacBook Pro 14” (M3 Pro 18/512) Space Black"],
    "MRX63" : ["MacBook Pro 14” (M3 Pro 18/512) Silver"],
    "MRX73" : ["MacBook Pro 14” (M3 Pro 18/1TB) Silver"], #MacBook Pro 14" MRX73 (M3 Pro 12-Core, GPU 18-Core, 18GB, 1TB) (Silver)
    "MK193" : ["MacBook Pro 16” (M1 Pro 16/1TB) Space Gray"], #Apple MacBook Pro 16" (2021) 1Tb Space Gray (MK193) (M1 Pro 10C CPU, 16 ГБ, 1TB SSD, Touch ID)
    "MW2U3" : ["MacBook Pro 14” (M4 16/512) Space Black"], #MacBook Pro 14" MW2U3 (M4 10-Core, GPU 10-Core, 16GB, 512GB) (Space Black)
    "MX2E3" : ["MacBook Pro 14” (M4 Pro 24/512) Silver"], #MacBook Pro 14" MX2E3 (M4 Pro 12-Core, GPU 16-Core, 24GB, 512GB) (Silver)
    "MX2G3" : ["MacBook Pro 14” (M4 Max 36/1TB) Silver"], #MacBook Pro 14" MX2G3 (M4 Max 14-Core, GPU 32-Core, 36GB, 1TB) (Silver)
    "MRW73" : ["MacBook Pro 16” (M3 Max 36/1TB) Silver"], #MacBook Pro 16" MRW73 (M3 Max 14-Core, GPU 30-Core, 36GB, 1TB) (Silver)
    "MRW23" : ["MacBook Pro 16” (M3 Pro 36/512) Space Black"], #MacBook Pro 16" MRW23 (M3 Pro 12-Core, GPU 18-Core, 36GB, 512GB) (Space Black)
    "Z1FW0000T" : ["MacBook Pro 16” (M4 Max 128/8TB) Space Black"], #Ноутбук MacBook Pro 16 M4 Max (Z1FW0000T), 128/8192 ГБ, Space black, космический черный
    "Z1FW0000S" : ["MacBook Pro 16” (M4 Max 128/4TB) Space Black"], #Ноутбук MacBook Pro 16 M4 Max (Z1FW0000S), 128/4096 ГБ, Space black, космический черный
    "Z1FS0000T" : ["MacBook Pro 16” (M4 Max 128/8TB) Silver"], #Ноутбук MacBook Pro 16 M4 Max (Z1FS0000T), 128/8192 ГБ, Silver, серебристый
    "Z1FS0000Q" : ["MacBook Pro 16” (M4 Max 64/4TB) Silver"], #Ноутбук MacBook Pro 16 M4 Max (Z1FS0000Q), 64/4096 ГБ, Silver, серебристый
    "Z1FS0000P" : ["MacBook Pro 16” (M4 Max 128/2TB) Silver"], #Ноутбук MacBook Pro 16 M4 Max (Z1FS0000P), 128/2048 ГБ, Silver, серебристый
    "Z1FS0000M" : ["MacBook Pro 16” (M4 Max 128/1TB) Silver"], #Ноутбук MacBook Pro 16 M4 Max (Z1FS0000M), 128/1024 ГБ, Silver, серебристый
    "Z1AF001AL" : ["MacBook Pro 16” (M3 Pro 128/1TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Pro (Z1AF001AL), 128/1024 GB, Space Black
    "Z1AF001AF" : ["MacBook Pro 16” (M3 Pro 64/1TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Pro (Z1AF001AF), 64/1024 GB, Space Black
    "Z1FG0000V" : ["MacBook Pro 14” (M4 Max 128/8TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Max (Z1FG0000V), 128/8192 ГБ, Space black
    "Z1FG0000R" : ["MacBook Pro 14” (M4 Max 64/4TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Max (Z1FG0000R), 64/4096 ГБ, Space black
    "Z1FG0000N" : ["MacBook Pro 14” (M4 Max 64/2TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Max (Z1FG0000N), 64/2048 ГБ, Space black
    "Z1FG0000L" : ["MacBook Pro 14” (M4 Max 128/1TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Max (Z1FG0000L), 128/1024 ГБ, Space black
    "Z1FG0000K" : ["MacBook Pro 14” (M4 Max 64/1TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Max (Z1FG0000K), 64/1024 ГБ, Space black
    "Z1FD0000L" : ["MacBook Pro 14” (M4 Max 64/1TB) Silver"], #Ноутбук MacBook Pro 14 M4 Max (Z1FD0000L), 64/1024 ГБ, Silver
    "MW2V3" : ["MacBook Pro 14” (M4 16/1TB) Space Black"], #Ноутбук MacBook Pro 14 M4 (MW2V3), 16/1024 ГБ, Space black
    "MCX04" : ["MacBook Pro 14” (M4 24/1TB) Space Black"], #Ноутбук MacBook Pro 14 M4 (MCX04), 24/1024 ГБ, Space black
    "Z1AU002AC" : ["MacBook Pro 14” (M3 Max 64/1TB) Space Black"], #Ноутбук MacBook Pro 14 M3 Max (Z1AU002AC), 64/1024 GB, Space Black
    "MTL83" : ["MacBook Pro 14” (M3 8/1TB) Space Black"], #Ноутбук MacBook Pro 14 M3 (MTL83), 8/1024 Гб, Space Black
    "MMQX3" : ["MacBook Pro 14” (M1 Max 64/2TB) Silver"], #Ноутбук MacBook Pro 14 M1 Max (MMQX3), 64/2048 Гб, Silver
    "MKH53" : ["MacBook Pro 14” (M1 Max 64/2TB) Space Gray"], #Ноутбук MacBook Pro 14 M1 Max (MKH53), 64/2048 GB, Space Gray
    "MX2T3" : ["MacBook Pro 16” (M4 Pro 24/512) Silver"], #Ноутбук MacBook Pro 16 M4 Pro (MX2T3), 24/512 Гб, Silver
    "Z1FW0000R" : ["MacBook Pro 16” (M4 Max 128/2TB) Space Black"], #Ноутбук MacBook Pro 16 M4 Max (Z1FW0000R), 128/2048 ГБ, Space Black
    "Z1FW0000P" : ["MacBook Pro 16” (M4 Max 64/4TB) Space Black"], #Ноутбук MacBook Pro 16 M4 Max (Z1FW0000P), 64/4096 ГБ, Space Black
    "Z1FW0000N" : ["MacBook Pro 16” (M4 Max 64/2TB) Space Black"], #Ноутбук MacBook Pro 16 M4 Max (Z1FW0000N), 64/2048 ГБ, Space Black
    "Z1FW0000M" : ["MacBook Pro 16” (M4 Max 128/1TB) Space Black"], #Ноутбук MacBook Pro 16 M4 Max (Z1FW0000M), 128/1024 ГБ, Space Black
    "Z1FV00006" : ["MacBook Pro 16” (M4 Max 36/2TB) Space Black"], #Ноутбук MacBook Pro 16 M4 Max (Z1FV00006), 36/2048 ГБ, Space Black
    "Z1FS0000R" : ["MacBook Pro 16” (M4 Max 128/4TB) Silver"], #Ноутбук MacBook Pro 16 M4 Max (Z1FS0000R), 128/4096 ГБ, Silver
    "Z1FR00003" : ["MacBook Pro 16” (M4 Max 36/2TB) Silver"], #Ноутбук MacBook Pro 16 M4 Max (Z1FR00003), 36/2048 ГБ, Silver
    "MX2W3" : ["MacBook Pro 16” (M4 Max 48/1TB) Silver"], #Ноутбук MacBook Pro 16 M4 Max (MX2W3), 48/1024 ГБ, Silver
    "MX2V3" : ["MacBook Pro 16” (M4 Max 36/1TB) Silver"], #Ноутбук MacBook Pro 16 M4 Max (MX2V3), 36/1024 Гб, Silver
    "Z1AH00174" : ["MacBook Pro 16” (M3 Max 96/1TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Pro (Z1AH00174), 96/1024 Гб, серый
    "Z1AF0019Y" : ["MacBook Pro 16” (M3 Pro 36/1TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Pro (Z1AF0019Y), 36/1024 Гб, Space Black
    "Z1AF0019W" : ["MacBook Pro 16” (M3 Pro 36/512) Space Black"], #Ноутбук MacBook Pro 16 M3 Pro (Z1AF0019W), 36/512 GB, Space Black
    "MRW63" : ["MacBook Pro 16” (M3 Pro 18/512) Silver"], #Ноутбук MacBook Pro 16 M3 Pro (MRW63), 18/512, Silver
    "Z1CM0000J" : ["MacBook Pro 16” (M3 Max 128/4TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Max (Z1CM0000J), 128/4096 GB, Space Black
    "Z1CM0000G" : ["MacBook Pro 16” (M3 Max 128/2TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Max (Z1CM0000G), 128/2048 GB, Space Black
    "Z1AG00002" : ["MacBook Pro 16” (M3 Max 36/1TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Max (Z1AG00002), 36/1024 GB, Space Black
    "Z1AF001VB" : ["MacBook Pro 16” (M3 Max 128/8TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Max (Z1AF001VB), 128/8192 Гб, Space Black
    "Z1AF001V9" : ["MacBook Pro 16” (M3 Max 128/2TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Max (Z1AF001V9), 128/2048 Гб, Space Black
    "Z1AF001V7" : ["MacBook Pro 16” (M3 Max 64/2TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Max (Z1AF001V7), 64/2048 Гб, Space Black
    "Z1AF001V3" : ["MacBook Pro 16” (M3 Max 96/2TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Max (Z1AF001V3), 96/2048 Гб, Space Black
    "Z1AF001S7" : ["MacBook Pro 16” (M3 Max 128/4TB) Space Black"], #Ноутбук MacBook Pro 16 M3 Max (Z1AF001S7), 128/4096 Гб, Space black
    "Z1760005S" : ["MacBook Pro 16” (M2 Pro 32/2TB) Space Gray"], #Ноутбук MacBook Pro 16 M2 Pro (Z1760005S), 32/2048 Гб, Space gray
    "Z1740017J" : ["MacBook Pro 16” (M2 Pro 32/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M2 Pro (Z1740017J), 32/1024 Гб, Space gray
    "MNWD3" : ["MacBook Pro 16” (M2 Pro 16/1TB) Silver"], #Ноутбук MacBook Pro 16 M2 Pro (MNWD3LL/A), 16/1024 Гб, Silver
    "MNWC3" : ["MacBook Pro 16” (M2 Pro 16/512) Silver"], #Ноутбук MacBook Pro 16 M2 Pro (MNWC3), 16/512, Silver
    "MNW93" : ["MacBook Pro 16” (M2 Pro 16/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M2 Pro (MNW93), 16/1024 Гб, Space gray
    "MNW83" : ["MacBook Pro 16” (M2 Pro 16/512) Space Gray"], #Ноутбук MacBook Pro 16 M2 Pro (MNW83), 16/512, Space gray
    "Z177000NE" : ["MacBook Pro 16” (M2 Max 64/1TB) Silver"], #Ноутбук MacBook Pro 16 M2 Max (Z177000NE), 64/1024 Гб, Silver
    "Z177000E9" : ["MacBook Pro 16” (M2 Max 32/512) Silver"], #Ноутбук MacBook Pro 16 M2 Max (Z177000E9), 32/512, Silver
    "Z1760005V" : ["MacBook Pro 16” (M2 Max 64/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M2 Max (Z1760005V), 64/1024 Гб, Space gray
    "MNWE3" : ["MacBook Pro 16” (M2 Max 32/1TB) Silver"], #Ноутбук MacBook Pro 16 M2 Max (MNWE3), 32/1024 Гб, Silver
    "MNWA3" : ["MacBook Pro 16” (M2 Max 32/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M2 Max (MNWA3), 32/1024 Гб, Space gray
    "Z14Y001M4" : ["MacBook Pro 16” (M1 Pro 32/512) Silver"], #Ноутбук MacBook Pro 16 M1 Pro (Z14Y001M4), 32/512, Silver
    "Z14V0023L" : ["MacBook Pro 16” (M1 Pro 32/512) Space Gray"], #Ноутбук MacBook Pro 16 M1 Pro (Z14V0023L), 32/512, Space gray
    "Z14V00234" : ["MacBook Pro 16” (M1 Pro 32/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Pro (Z14V00234), 32/1024 Гб, Space gray
    "Z14V0008Z" : ["MacBook Pro 16” (M1 Pro 32/8TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Pro (Z14V0008Z), 32/8192 Гб, Space gray
    "MK1F3" : ["MacBook Pro 16” (M1 Pro 16/1TB) Silver"], #Ноутбук MacBook Pro 16 M1 Pro (MK1F3), 16/1024 Гб, Silver
    "MK1E3" : ["MacBook Pro 16” (M1 Pro 16/512) Silver"], #Ноутбук MacBook Pro 16 M1 Pro (MK1E3), 16/512, Silver
    "MK183" : ["MacBook Pro 16” (M1 Pro 16/512) Space Gray"], #Ноутбук MacBook Pro 16 M1 Pro (MK183RU), 16/512 GB, Space Gray
    "Z14Y0026L" : ["MacBook Pro 16” (M1 Max 64/8TB) Silver"], #Ноутбук MacBook Pro 16 M1 Max (Z14Y0026L), 64/8192 Гб, Silver
    "Z14Y001M6" : ["MacBook Pro 16” (M1 Max 32/1TB) Silver"], #Ноутбук MacBook Pro 16 M1 Max (Z14Y001M6), 32/1024 Гб, Silver
    "Z14Y001JD" : ["MacBook Pro 16” (M1 Max 64/1TB) Silver"], #Ноутбук MacBook Pro 16 M1 Max (Z14Y001JD), 64/1024 Гб, Silver
    "Z14Y0008W" : ["MacBook Pro 16” (M1 Max 32/4TB) Silver"], #Ноутбук MacBook Pro 16 M1 Max (Z14Y0008W), 32/4096 Гб, Silver
    "Z14Y0008M" : ["MacBook Pro 16” (M1 Max 32/4TB) Silver"], #Ноутбук MacBook Pro 16 M1 Max (Z14Y0008M), 32/4096 Гб, Silver
    "Z14V0028J" : ["MacBook Pro 16” (M1 Max 32/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V0028J), 32/1024 Гб, Space gray
    "Z14V0027K" : ["MacBook Pro 16” (M1 Max 64/8TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V0027K), 64/8192 Гб, Space gray
    "Z14V0027J" : ["MacBook Pro 16” (M1 Max 64/4TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V0027J), 64/4096 Гб, Space gray
    "Z14V0024F" : ["MacBook Pro 16” (M1 Max 32/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V0024F), 32/1024 Гб, Space gray
    "Z14V0023R" : ["MacBook Pro 16” (M1 Max 64/512) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V0023R), 64/512, Space gray
    "Z14V001XN" : ["MacBook Pro 16” (M1 Max 64/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V001XN), 64/1024 Гб, Space gray
    "Z14V00092" : ["MacBook Pro 16” (M1 Max 32/8TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V00092) 32/8192 Гб, Space gray
    "Z14V00090" : ["MacBook Pro 16” (M1 Max 32/8TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V00090) 32/8192 Гб, Space gray
    "Z14V0008V" : ["MacBook Pro 16” (M1 Max 32/4TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (Z14V0008V) 32/4096 Гб, Space gray
    "MMQW3" : ["MacBook Pro 16” (M1 Max 64/4TB) Silver"], #Ноутбук MacBook Pro 16 M1 Max (MMQW3), 64/4096 ГБ, Silver
    "MK233" : ["MacBook Pro 16” (M1 Max 64/4TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (MK233LL/A) 64/4096 Гб, Space gray
    "MK1A3" : ["MacBook Pro 16” (M1 Max 32/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 Max (MK1A3) 32/1024 Гб, Space gray
    "Z14Y001T7" : ["MacBook Pro 16” (M1 32/2TB) Silver"], #Ноутбук MacBook Pro 16 M1 (Z14Y001T7), 32/2048 Гб, Silver
    "Z14Y001PA" : ["MacBook Pro 16” (M1 32/1TB) Silver"], #Ноутбук MacBook Pro 16 M1 (Z14Y001PA), 32/1024 Гб, Silver
    "Z14Y0008J" : ["MacBook Pro 16” (M1 32/8TB) Silver"], #Ноутбук MacBook Pro 16 M1 (Z14Y0008J), 32/8192 Гб, Silver
    "Z14X002DY" : ["MacBook Pro 16” (M1 64/1TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 (Z14X002DY), 64/1024 Гб, Space gray
    "Z14X000HQ" : ["MacBook Pro 16” (M1 64/2TB) Space Gray"], #Ноутбук MacBook Pro 16 M1 (Z14X000HQ), 64/2048 Гб, Space gray
    "Z1FF0000B" : ["MacBook Pro 14” (M4 Pro 48/1TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Pro (Z1FF0000B), 48/1024 ГБ, Space black
    "Z1FE00012" : ["MacBook Pro 14” (M4 Pro 48/512) Space Black"], #Ноутбук MacBook Pro 14 M4 Pro (Z1FE00012), 48/512, Space black
    "Z1FE0000E" : ["MacBook Pro 14” (M4 Pro 48/512) Space Black"], #Ноутбук MacBook Pro 14 M4 Pro (Z1FE0000E), 48/512, Space black
    "Z1FB00014" : ["MacBook Pro 14” (M4 Pro 48/512) Silver"], #Ноутбук MacBook Pro 14 M4 Pro (Z1FB00014), 48/512, Silver
    "MX2H3" : ["MacBook Pro 14” (M4 Pro 24/512) Space Black"], #Ноутбук MacBook Pro 14 M4 Pro (MX2H3), 24/512, Space black
    "Z1FG0000S" : ["MacBook Pro 14” (M4 Max 128/4TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Max (Z1FG0000S), 128/4096 ГБ, Space black
    "Z1FG0000P" : ["MacBook Pro 14” (M4 Max 128/2TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Max (Z1FG0000P), 128/2048 ГБ, Space black
    "Z1FG0000C" : ["MacBook Pro 14” (M4 Max 48/1TB) Space Black"], #Ноутбук MacBook Pro 14 M4 Max (Z1FG0000C), 48/1024 ГБ, Space black
    "Z1FD0000T" : ["MacBook Pro 14” (M4 Max 128/4TB) Silver"], #Ноутбук MacBook Pro 14 M4 Max (Z1FD0000T), 128/4096 ГБ, Silver
    "Z1FD0000S" : ["MacBook Pro 14” (M4 Max 64/4TB) Silver"], #Ноутбук MacBook Pro 14 M4 Max (Z1FD0000S), 64/4096 ГБ, Silver
    "Z1FD0000Q" : ["MacBook Pro 14” (M4 Max 128/2TB) Silver"], #Ноутбук MacBook Pro 14 M4 Max (Z1FD0000Q), 128/2048 ГБ, Silver
    "MW2X3" : ["MacBook Pro 14” (M4 16/1TB) Silver"], #Ноутбук MacBook Pro 14 M4 (MW2X3), 16/1024 ГБ, Silver
    "Z1CM000ZQ" : ["MacBook Pro 14” (M3 Pro 48/2TB) Space Black"], #Ноутбук MacBook Pro 14 M3 Pro (Z1CM000ZQ), 48/2048 Гб, Space black
    "Z1C800047" : ["MacBook Pro 14” (M3 Pro 8/512) Space Black"], #Ноутбук MacBook Pro 14 M3 Pro (Z1C800047), 8/512 Гб, Space black
    "Z1AU0000M" : ["MacBook Pro 14” (M3 Pro 36/512) Space Black"], #Ноутбук MacBook Pro 14 M3 Pro (Z1AU0000M), 36/512 ГБ, Space black
    "Z1CM000UW" : ["MacBook Pro 14” (M3 Max 64/2TB) Space Black"], #Ноутбук MacBook Pro 14 M3 Max (Z1CM000UW), 64/2048 Гб, Space black
    "Z1AY001JB" : ["MacBook Pro 14” (M3 Max 64/1TB) Silver"], #Ноутбук MacBook Pro 14 M3 Max (Z1AY001JB), 64/1024 GB, Silver
    "Z1AW0000W" : ["MacBook Pro 14” (M3 Max 128/2TB) Space Black"], #Ноутбук MacBook Pro 14 M3 Max (Z1AW0000W), 128/2048 GB, Space Black
    "Z1AW0000U" : ["MacBook Pro 14” (M3 Max 64/2TB) Gray"], #Ноутбук MacBook Pro 14 M3 Max (Z1AW0000U), 64/2048 Гб, серый
    "Z1AW0000S" : ["MacBook Pro 14” (M3 Max 128/1TB) Space Black"], #Ноутбук MacBook Pro 14 M3 Max (Z1AW0000S), 128/1024 GB, Space Black
    "Z1AU002M9" : ["MacBook Pro 14” (M3 Max 36/512) Space Black"], #Ноутбук MacBook Pro 14 M3 Max (Z1AU002M9), 36/512 ГБ, Space black
    "Z1AJ0019D" : ["MacBook Pro 14” (M3 Max 64/1TB) Silver"], #Ноутбук MacBook Pro 14 M3 Max (Z1AJ0019D), 64/1024 GB, Silver
    "Z1AJ0018V" : ["MacBook Pro 14” (M3 Max 36/512) Silver"], #Ноутбук MacBook Pro 14 M3 Max (Z1AJ0018V), 36/512 GB, Silver
    "MXE03" : ["MacBook Pro 14” (M3 Max 16/1TB) Grey"], #Ноутбук MacBook Pro 14 M3 Max (MXE03), 16/1024 GB, Grey
    "MRX83" : ["MacBook Pro 14” (M3 Max 36/1TB) Silver"], #Ноутбук MacBook Pro 14 M3 Max (MRX83), 36/1024 Гб, Silver
    "MRX53" : ["MacBook Pro 14” (M3 Max 36/1TB) Space Black"], #Ноутбук MacBook Pro 14 M3 Max (MRX53), 36/1024 ГБ, Space black
    "Z1C80001D" : ["MacBook Pro 14” (M3 16/512) Space Gray"], #Ноутбук MacBook Pro 14 M3 (Z1C80001D), 16/512 Гб, Space gray
    "MTL73" : ["MacBook Pro 14” (M3 8/512) Space Gray"], #Ноутбук MacBook Pro 14 M3 (MTL73), 8/512 Гб, Space gray
    "MR7K3" : ["MacBook Pro 14” (M3 8/1TB) Silver"], #Ноутбук MacBook Pro 14 M3 (MR7K3), 8/1024 Гб, Silver
    "MR7J3" : ["MacBook Pro 14” (M3 8/512) Silver"], #Ноутбук MacBook Pro 14 M3 (MR7J3), 8/512 Гб, Silver
    "Z17G002HT" : ["MacBook Pro 14” (M2 Pro 32/1TB) Space Gray"], #Ноутбук MacBook Pro 14 M2 Pro (Z17G002HT), 32/1024 Гб, Space gray
    "Z17G000NA" : ["MacBook Pro 14” (M2 Pro 16/1TB) Space Gray"], #Ноутбук MacBook Pro 14 M2 Pro (Z17G000NA), 16/1024 Гб, Space gray
    "MPHJ3" : ["MacBook Pro 14” (M2 Pro 16/1TB) Silver"], #Ноутбук MacBook Pro 14 M2 Pro (MPHJ3), 16/1024 Гб, Silver
    "MPHH3" : ["MacBook Pro 14” (M2 Pro 16/512) Silver"], #Ноутбук MacBook Pro 14 M2 Pro (MPHH3), 16/512 Гб, Silver
    "MPHG3" : ["MacBook Pro 14” (M2 Pro 32/1TB) Space Gray"], #Ноутбук MacBook Pro 14 M2 Pro (MPHG3), 32/1024 Гб, Space gray
    "MPHF3" : ["MacBook Pro 14” (M2 Pro 16/1TB) Space Gray"], #Ноутбук MacBook Pro 14 M2 Pro (MPHF3), 16/1024 Гб, Space gray
    "Z17K002UN" : ["MacBook Pro 14” (M2 Max 64/1TB) Silver"], #Ноутбук MacBook Pro 14 M2 Max (Z17K002UN), 64/1024 Гб, Silver
    "Z17K002UM" : ["MacBook Pro 14” (M2 Max 32/1TB) Silver"], #Ноутбук MacBook Pro 14 M2 Max (Z17K002UM), 32/1024 Гб, Silver
    "Z17J00165" : ["MacBook Pro 14” (M2 Max 64/4TB) Space Gray"], #Ноутбук MacBook Pro 14 M2 Max (Z17J00165), 64/4096 Гб, Space gray
    "Z17G003AN" : ["MacBook Pro 14” (M2 Max 32/1TB) Space Gray"], #Ноутбук MacBook Pro 14 M2 Max (Z17G003AN), 32/1024 Гб, Space gray
    "Z17G002KJ" : ["MacBook Pro 14” (M2 Max 96/1TB) Silver"], #Ноутбук MacBook Pro 14 M2 Max (Z17G002KJ), 96/1024 Гб, Silver
    "Z17G001BC" : ["MacBook Pro 14” (M2 Max 32/1TB) Space Gray"], #Ноутбук MacBook Pro 14 M2 Max (Z17G001BC), 32/1024 Гб, Space gray
    "MPHK3" : ["MacBook Pro 14” (M2 Max 32/1TB) Silver"], #Ноутбук MacBook Pro 14 M2 Max (MPHK3), 32/1024 Гб, Silver
    "Z15G00460" : ["MacBook Pro 14” (M1 Pro 32/1TB) Space Gray"], #Ноутбук MacBook Pro 14 M1 Pro (Z15G00460), 32/1024 Гб, Space gray
    "MKGT3" : ["MacBook Pro 14” (M1 Pro 16/1TB) Silver"], #Ноутбук MacBook Pro 14 M1 Pro (MKGT3), 16/1024 Гб, Silver
    "MKGR3" : ["MacBook Pro 14” (M1 Pro 16/512) Silver"], #Ноутбук MacBook Pro 14 M1 Pro (MKGR3), 16/512 Гб, Silver
    "MKGQ3" : ["MacBook Pro 14” (M1 Pro 16/1TB) Space Gray"], #Ноутбук MacBook Pro 14 M1 Pro (MKGQ3), 16/1024 Гб, Space gray
    "MKGP3" : ["MacBook Pro 14” (M1 Pro 16/512) Space Gray"], #Ноутбук MacBook Pro 14 M1 Pro (MKGP3), 16/512 Гб, Space gray
    "Z15J004WS" : ["MacBook Pro 14” (M1 Max 32/2TB) Silver"], #Ноутбук MacBook Pro 14 M1 Max (Z15J004WS), 32/2048 Гб, Silver
    "Z15J0030H" : ["MacBook Pro 14” (M1 Max 32/512) Silver"], #Ноутбук MacBook Pro 14 M1 Max (Z15J0030H), 32/512 Гб, Silver
    "Z15J000DJ" : ["MacBook Pro 14” (M1 Max 32/8TB) Silver"], #Ноутбук MacBook Pro 14 M1 Max (Z15J000DJ), 32/8192 Гб, Silver
    "Z15G007C6" : ["MacBook Pro 14” (M1 Max 32/4TB) Space Gray"], #Ноутбук MacBook Pro 14 M1 Max (Z15G007C6), 32/4096 Гб, Space gray
    "Z15G0047Q" : ["MacBook Pro 14” (M1 Max 32/2TB) Space Gray"], #Ноутбук MacBook Pro 14 M1 Max (Z15G0047Q), 32/2048 Гб, Space gray
    "Z15G0045J" : ["MacBook Pro 14” (M1 Max 32/512) Space Gray"], #Ноутбук MacBook Pro 14 M1 Max (Z15G0045J), 32/512 Гб, Space gray
    "Z15G000DV" : ["MacBook Pro 14” (M1 Max 32/8TB) Space Gray"], #Ноутбук MacBook Pro 14 M1 Max (Z15G000DV), 32/8192 Гб, Space gray
    "Z15G000DT" : ["MacBook Pro 14” (M1 Max 32/4TB) Space Gray"], #Ноутбук MacBook Pro 14 M1 Max (Z15G000DT), 32/4096 Гб, Space gray
    "Z15G000DR" : ["MacBook Pro 14” (M1 Max 32/2TB) Space Gray"], #Ноутбук MacBook Pro 14 M1 Max (Z15G000DR), 32/2048 Гб, Space gray
    "MK1H3" : ["MacBook Pro Max 14” (M1 32/1TB) Silver"], #Ноутбук Macbook Pro Max 14 M1 (MK1H3KS/A) 32/1024 ГБ, Silver
    "Z16U00025" : ["MacBook Pro 13” (M2 16/512) Silver"], #Ноутбук Macbook Pro 13 M2 (Z16U00025) 16/512, Silver
    "Z16R000UA" : ["MacBook Pro 13” (M2 24/1TB) Space Gray"], #Ноутбук Macbook Pro 13 M2 (Z16R000UA) 24/1024, Space gray
    "Z16R0005J" : ["MacBook Pro 13” (M2 8/1TB) Space Gray"], #Ноутбук Macbook Pro 13 M2 (Z16R0005J) 8/1024, Space gray
    "MNEQ3" : ["MacBook Pro 13” (M2 8/512) Silver"], #Ноутбук Macbook Pro 13 M2 (MNEQ3) 8/512, Silver
    "MNEP3" : ["MacBook Pro 13” (M2 8/256) Silver"], #Ноутбук Macbook Pro 13 M2 (MNEP3) 8/256, Silver
    "MNEJ3" : ["MacBook Pro 13” (M2 8/512) Space Gray"], #Ноутбук Macbook Pro 13 M2 (MNEJ3) 8/512, Space gray
    "MNEH3" : ["MacBook Pro 13” (M2 8/256) Space Gray"], #Ноутбук Macbook Pro 13 M2 (MNEH3) 8/256, Space gray
    "G16S6" : ["MacBook Pro 13” (M2 24/1TB) Space Gray"], #Ноутбук Macbook Pro 13 M2 (G16S6LL/A) 24/1024 ГБ, Space gray
    "Z11F0002Z" : ["MacBook Pro 13” (M1 16/512) Silver"], #Ноутбук Macbook Pro 13 M1 (Z11F0002Z) 16/512, Silver
    "MYDC2" : ["MacBook Pro 13” (M1 8/512) Silver"], #Ноутбук Macbook Pro 13 M1 (MYDC2) 8/512, Silver
    "MYD92" : ["MacBook Pro 13” (M1 8/512) Space Gray"], #Ноутбук Macbook Pro 13 M1 (MYD92) 8/512, Space gray
    "MYD82" : ["MacBook Pro 13” (M1 8/256) Space Gray"], #Ноутбук Macbook Pro 13 M1 (MYD82) 8/256, Space gray
    "MX2X3" : ["MacBook Pro 16” (M4 Pro 24/512) Space Black"], #MacBook Pro 16" MX2X3 (M4 Pro 14-Core, GPU 20-Core, 24GB, 512GB) («Чёрный космос» | Space Black)
    #2025
    "MW2W3" : ["MacBook Pro 14″ (M4 16/512) Silver"],
    "MX2Z3" : ["MacBook Pro 16″ (M4 Max 36/1TB) Silver"],
    "MX2N3" : ["MacBook Pro 16″ (M4 Max 48/1TB) Silver"],

    # БЛОК MacBook Air
    "MGN63" : ["MacBook Air 13” (M1 8/256) Space Gray"], # MacBook Air 13” (M1, 8 GB, 256 GB) MGN63 Space Gray
    "MLXW3" : ["MacBook Air 13” (M2 8/256) Space Gray"], #MacBook Air 13" MLXW3 (M2 8-Core, GPU 8-Core, 8GB, 256GB) (Space Gray)
    "MLY33" : ["MacBook Air 13” (M2 8/256) Midnight"], #MacBook Air 13” (M2, 8 GB, 256 GB) MLY33 Midnight
    "MLY13" : ["MacBook Air 13” (M2 8/256) Starlight"], #MacBook Air 13” (M2, 8 GB, 256 GB) MLY13 Starlight
    "MLXX3" : ["MacBook Air 13” (M2 8/512) Space Gray"], #MacBook Air 13" MLXX3 (M2 8-Core, GPU 10-Core, 8GB, 512GB) (Space Gray)
    "MLY03" : ["MacBook Air 13” (M2 8/512) Silver"], #MacBook Air 13" MLY03 (M2 8-Core, GPU 10-Core, 8GB, 512GB) (Silver)
    "MLY23" : ["MacBook Air 13” (M2 8/512) Starlight"], #MacBook Air 13" MLY23 (M2 8-Core, GPU 10-Core, 8GB, 512GB) (Starlight)
    "MC7U4" : ["MacBook Air 13” (M2 16/256) Space Gray"], #MacBook Air 13” (M2, 16 GB, 256 GB) MC7U4 Space Gray
    "MC7V4" : ["MacBook Air 13” (M2 16/256) Silver"], #MacBook Air 13” (M2, 16 GB, 256 GB) MC7V4 Silver
    "MC7W4" : ["MacBook Air 13” (M2 16/256) Starlight"], #MacBook Air 13” (M2, 16 GB, 256 GB)  MC7W4 Starlight
    "MC7X4" : ["MacBook Air 13” (M2 16/256) Midnight"], #MacBook Air 13” (M2, 16 GB, 256 GB)  MC7X4  Midnight
    "MC8J4" : ["MacBook Air 13” (M3 16/256) Starlight"], #MacBook Air 13” (M3, 16 GB, 256 GB)  MC8J4 Starlight
    "MC8M4" : ["MacBook Air 13” (M3 24/512) Space Gray"], #MacBook Air 13” (M3, 24 GB, 512 GB) MC8M4 Space Gray
    "MC8Q4" : ["MacBook Air 13” (M3 24/512) Midnight"], #MacBook Air 13” (M3, 24 GB, 512 GB) MC8Q4 Midnight
    "MC8N4" : ["MacBook Air 13” (M3 24/512) Silver"],
    "MC8P4" : ["MacBook Air 13” (M3 24/512) Starlight"],
    "MRYQ3" : ["MacBook Air 15” (M3 8/512) Silver"], #MacBook Air 15-inch (M3, 8 GB, 512GB) MRYQ3 Silver
    "MRYV3" : ["MacBook Air 15” (M3 8/512) Midnight"], #MacBook Air 15-inch (M3, 8 GB, 512GB) MRYV3 Midnight
    "MRYT3" : ["MacBook Air 15” (M3 8/512) Starlight"], #MacBook Air 15-inch (M3, 8 GB, 512GB) MRYT3 Starlight
    "MRYN3" : ["MacBook Air 15” (M3 8/512) Space Gray"], #MacBook Air 15-inch (M3, 8 GB, 512GB) MRYN3 Space Gray
    "MC9E4" : ["MacBook Air 15” (M3 16/256) Silver"], #MacBook Air 15-inch (M3, 16 GB, 256GB) MC9E4 Silver
    "MC9F4" : ["MacBook Air 15” (M3 16/256) Starlight"], #MacBook Air 15-inch (M3, 16 GB, 256GB) MC9F4 Starlight
    "MC9D4" : ["MacBook Air 15” (M3 16/256) Space Gray"], #MacBook Air 15-inch (M3, 16 GB, 256GB) MC9D4 Space Gray
    "MGND3" : ["MacBook Air 13” (M1 8/256) Gold"],
    "MC9G4" : ["MacBook Air 15” (M3 16/256) Midnight"], #MacBook Air 15" MC9G4 (M3 8-Core, GPU 10-Core, 16GB, 256GB) (Midnight)
    "MLY43" : ["MacBook Air 13” (M2 8/512) Midnight"], #MacBook Air 13" MLY43 (M2 8-Core, GPU 10-Core, 8GB, 512GB) (Midnight)
    "MRXN3" : ["MacBook Air 13” (M3 8/256) Space Gray"], #MacBook Air 13" MRXN3 (M3 8-Core, GPU 8-Core, 8GB, 256GB) (Space Gray)
    "MRXV3" : ["MacBook Air 13” (M3 8/256) Midnight"], #MacBook Air 13" MRXV3 (M3 8-Core, GPU 8-Core, 8GB, 256GB) (Midnight)
    "MRXQ3" : ["MacBook Air 13” (M3 8/256) Silver"], #MacBook Air 13" MRXQ3 (M3 8-Core, GPU 8-Core, 8GB, 256GB) (Silver)
    "MRXT3" : ["MacBook Air 13” (M3 8/256) Starlight"], #MacBook Air 13" MRXT3 (M3 8-Core, GPU 8-Core, 8GB, 256GB) (Starlight)
    "MRXP3" : ["MacBook Air 13” (M3 8/512) Space Gray"], #MacBook Air 13" MRXP3 (M3 8-Core, GPU 10-Core, 8GB, 512GB) (Space Gray)
    "MRXW3" : ["MacBook Air 13” (M3 8/512) Midnight"], #MacBook Air 13" MRXW3 (M3 8-Core, GPU 10-Core, 8GB, 512GB) (Midnight)
    "MRXR3" : ["MacBook Air 13” (M3 8/512) Silver"], #MacBook Air 13" MRXR3 (M3 8-Core, GPU 10-Core, 8GB, 512GB) (Silver)
    "MRXU3" : ["MacBook Air 13” (M3 8/512) Starlight"], #MacBook Air 13" MRXU3 (M3 8-Core, GPU 10-Core, 8GB, 512GB) (Starlight)
    "MXCR3" : ["MacBook Air 13” (M3 16/512) Space Gray"], #MacBook Air 13" MXCR3 (M3 8-Core, GPU 10-Core, 16GB, 512GB) (Space Gray)
    "MXCT3" : ["MacBook Air 13” (M3 16/512) Silver"], #MacBook Air 13" MXCT3 (M3 8-Core, GPU 10-Core, 16GB, 512GB) (Silver)
    "MXCV3" : ["MacBook Air 13” (M3 16/512) Midnight"], #MacBook Air 13" MXCV3 (M3 8-Core, GPU 10-Core, 16GB, 512GB) (Midnight)
    "MXCU3" : ["MacBook Air 13” (M3 16/512) Starlight"], #MacBook Air 13" MXCU3 (M3 8-Core, GPU 10-Core, 16GB, 512GB) (Starlight)
    "Z1BR000L3" : ["Macbook Air 15” (M3 24/1TB) Silver"], #Ноутбук Apple Macbook Air 15 M3 (Z1BR000L3) 24/1024 GB, Silver
    "Z1BP000LW" : ["Macbook Air 15” (M3 24/1TB) Space Gray"], #Ноутбук Apple Macbook Air 15 M3 (Z1BP000LW) 24/1024 GB, Space Gray, Серый Космос
    "MC9L4" : ["Macbook Air 15” (M3 24/512) Midnight"], #Ноутбук Apple Macbook Air 15 M3 (MC9L4) 24/512 Гб, Midnight, тёмная ночь
    "MXD33" : ["Macbook Air 15” (M3 16/512) Starlight"], #Ноутбук Apple Macbook Air 15 M3 (MXD33) 16/512, сияющая звезда
    "MXD23" : ["Macbook Air 15” (M3 16/512) Silver"], #Ноутбук Apple Macbook Air 15 M3 (MXD23) 16/512, серебристый
    "MXD13" : ["Macbook Air 15” (M3 16/512) Space Gray"], #Ноутбук Apple Macbook Air 15 M3 (MXD13) 16/512, серый
    "MRYU3" : ["Macbook Air 15” (M3 8/256) Midnight"], #Ноутбук Apple Macbook Air 15 M3 (MRYU3) 8/256, темная ночь
    "MRYR3" : ["Macbook Air 15” (M3 8/256) Starlight"], #Ноутбук Apple Macbook Air 15 M3 (MRYR3) 8/256, сияющая звезда
    "MRYP3" : ["Macbook Air 15” (M3 8/256) Silver"], #Ноутбук Apple Macbook Air 15 M3 (MRYP3) 8/256, серебристый
    "MRYM3" : ["Macbook Air 15” (M3 8/256) Space Gray"], #Ноутбук Apple Macbook Air 15 M3 (MRYM3) 8/256, серый космос
    "MQKX3" : ["MacBook Air 15” (M2 8/512) Midnight"], #Ноутбук Apple MacBook Air 15 M2, RAM 8 ГБ, SSD 512 ГБ, MQKX3, Midnight, тёмная ночь
    "MQKV3" : ["MacBook Air 15” (M2 8/512) Starlight"], #Ноутбук Apple MacBook Air 15 M2, RAM 8 ГБ, SSD 512 ГБ, MQKV3, Starlight, "Starlight"
    "MQKT3" : ["MacBook Air 15” (M2 8/512) Silver"], #Ноутбук Apple MacBook Air 15 M2, RAM 8 ГБ, SSD 512 ГБ, MQKT3, серебристый
    "MQKQ3" : ["MacBook Air 15” (M2 8/512) Space Gray"], #Ноутбук Apple MacBook Air 15 M2, RAM 8 ГБ, SSD 512 ГБ, MQKQ3,  Gray, серый
    "MQKR3LL/A" : ["MacBook Air 15” (M2 8/256) Silver"], #Ноутбук Apple MacBook Air 15 M2, RAM 8 ГБ, SSD 256 ГБ, MQKR3LL/A, Silver, серебристый
    "MQKP3" : ["MacBook Air 15” (M2 8/256) Space Gray"], #Ноутбук Apple MacBook Air 15 M2, RAM 8 ГБ, SSD 256 ГБ, MQKP3,  Gray, серый
    "Z1BV000SC" : ["Macbook Air 13” (M3 16/256) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BV000SC) 16/256 GB, Midnight
    "Z1BV000RL" : ["Macbook Air 13” (M3 24/512) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BV000RL) 24/512 GB, Midnight
    "Z1BV000Q8" : ["Macbook Air 13” (M3 24/1TB) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BV000Q8) 24/1024 GB, Midnight
    "Z1BV0006S" : ["Macbook Air 13” (M3 24/2TB) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BV0006S) 24/2048 GB, Midnight
    "Z1BV0006P" : ["Macbook Air 13” (M3 16/1TB) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BV0006P) 16/1024 GB, Midnight
    "Z1BV0006K" : ["Macbook Air 13” (M3 16/256) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BV0006K) 16/256 GB, Midnight
    "Z1BR000L5" : ["Macbook Air 13” (M3 16/1TB) Silver"], #Ноутбук Apple Macbook Air 13 M3 (Z1BR000L5) 16/1024 GB, Silver
    "Z1BR000KD" : ["Macbook Air 13” (M3 24/512) Silver"], #Ноутбук Apple Macbook Air 13 M3 (Z1BR000KD) 24/512 GB, Silver
    "Z1BP000QF" : ["Macbook Air 13” (M3 16/256) Space Gray"], #Ноутбук Apple Macbook Air 13 M3 (Z1BP000QF) 16/256, серый
    "Z1BP000MD" : ["Macbook Air 13” (M3 24/512) Space Gray"], #Ноутбук Apple Macbook Air 13 M3 (Z1BP000MD) 24/512 GB, Gray
    "Z1BP000LM" : ["Macbook Air 13” (M3 16/1TB) Space Gray"], #Ноутбук Apple Macbook Air 13 M3 (Z1BP000LM) 16/1024 GB, Gray
    "Z1BP0006M" : ["Macbook Air 13” (M3 16/256) Space Gray"], #Ноутбук Apple Macbook Air 13 M3 (Z1BP0006M) 16/256 GB, Gray
    "Z1BD000MJ" : ["Macbook Air 13” (M3 24/512) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BD000MJ) 24/512 GB, Midnight
    "Z1BD000MG" : ["Macbook Air 13” (M3 16/1TB) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BD000MG) 16/1024 GB, Midnight
    "Z1BC0017C" : ["Macbook Air 13” (M3 16/256) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BC0017C) 16/256, темная ночь
    "Z1BC0015S" : ["Macbook Air 13” (M3 16/256) Midnight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BC0015S) 16/256 GB, Midnight
    "Z1BB000MG" : ["Macbook Air 13” (M3 24/1TB) Starlight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BB000MG) 24/1024 GB, Starlight
    "Z1BB000M6" : ["Macbook Air 13” (M3 24/512) Starlight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BB000M6) 24/512 GB, Starlight
    "Z1BB000M5" : ["Macbook Air 13” (M3 16/1TB) Starlight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BB000M5) 16/1024 GB, Starlight
    "Z1BA0017J" : ["Macbook Air 13” (M3 16/256) Starlight"], #Ноутбук Apple Macbook Air 13 M3 (Z1BA0017J) 16/256 GB, Starlight
    "Z1B9000N0" : ["Macbook Air 13” (M3 24/2TB) Silver"], #Ноутбук Apple Macbook Air 13 M3 (Z1B9000N0) 24/2048 GB, Silver
    "Z1B9000MT" : ["Macbook Air 13” (M3 16/1TB) Silver"], #Ноутбук Apple Macbook Air 13 M3 (Z1B9000MT) 16/1024 GB, Silver
    "Z1B80015Z" : ["Macbook Air 13” (M3 16/256) Silver"], #Ноутбук Apple Macbook Air 13 M3 (Z1B80015Z) 16/256 GB, Silver
    "Z1B7000MG" : ["Macbook Air 13” (M3 16/1TB) Space Gray"], #Ноутбук Apple Macbook Air 13 M3 (Z1B7000MG), 16/1024 GB, Gray
    "Z1B7000MD" : ["Macbook Air 13” (M3 24/512) Space Gray"], #Ноутбук Apple Macbook Air 13 M3 (Z1B7000MD) 24/512 GB, Gray
    "Z1B60019P" : ["Macbook Air 13” (M3 16/256) Space Gray"], #Ноутбук Apple Macbook Air 13 M3 (Z1B60019P) 16/256, серый
    "MC8H4" : ["Macbook Air 13” (M3 16/256) Silver"], #Ноутбук Apple Macbook Air 13 M3 (MC8H4) 16/256, серебристый
    "MC8G4" : ["Macbook Air 13” (M3 16/256) Space Gray"], #Ноутбук Apple Macbook Air 13 M3 (MC8G4RU/A) 16/256 GB, Space Gray
    "Z16000190" : ["MacBook Air 13” (M2 16/512) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z16000190) 16/512, Midnight, "Midnight"
    "Z16100074" : ["MacBook Air 13” (M2 8/512) Midnight"], #Ноутбук Apple MacBook Air 13 M2 (Z16100074) 8/512, Midnight, "Midnight"
    "Z1600040U" : ["MacBook Air 13” (M2 24/2TB) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040U) 24/2048, тёмная ночь
    "Z1600040T" : ["MacBook Air 13” (M2 24/1TB) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040T) 24/1024, Midnight, "Midnight"
    "Z1600040S" : ["MacBook Air 13” (M2 24/512) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040S) 24/512, тёмная ночь
    "Z1600040R" : ["MacBook Air 13” (M2 24/256) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040R) 24/256, тёмная ночь
    "Z1600040Q" : ["MacBook Air 13” (M2 16/2TB) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040Q) 16/2048, тёмная ночь
    "Z1600040P" : ["MacBook Air 13” (M2 16/1TB) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040P) 16/1024, тёмная ночь
    "Z1600040N" : ["MacBook Air 13” (M2 16/512) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040N) 16/512, тёмная ночь
    "Z1600040M" : ["MacBook Air 13” (M2 16/256) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040M) 16/256, тёмная ночь
    "Z1600040L" : ["MacBook Air 13” (M2 8/1TB) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040L) 8/1024, тёмная ночь
    "Z1600040J" : ["MacBook Air 13” (M2 8/256) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z1600040J) 8/256, тёмная ночь
    "Z160000B1" : ["MacBook Air 13” (M2 16/512) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z160000B1) 16/512, тёмная ночь
    "Z160000AU" : ["MacBook Air 13” (M2 16/256) Midnight"], #Ноутбук Apple MacBook Air 13 M2 2022 (Z160000AU) 16/256, тёмная ночь
    "Z15Z0005L" : ["Macbook Air 13” (M2 24/2TB) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Z0005L) 24/2048, сияющая звезда
    "Z15Z0005K" : ["Macbook Air 13” (M2 24/1TB) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Z0005K) 24/1024, сияющая звезда
    "Z15Z00028" : ["Macbook Air 13” (M2 8/512) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Z00028) 8/512, Starlight, "Starlight"
    "Z15Y002N6" : ["Macbook Air 13” (M2 24/1TB) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y002N6) 24/1024, сияющая звезда
    "Z15Y002N5" : ["Macbook Air 13” (M2 24/512) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y002N5) 24/512, Starlight, "Starlight"
    "Z15Y002N4" : ["Macbook Air 13” (M2 24/256) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y002N4) 24/256, сияющая звезда
    "Z15Y002N3" : ["Macbook Air 13” (M2 16/1TB) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y002N3) 16/1024, сияющая звезда
    "Z15Y002N2" : ["Macbook Air 13” (M2 16/512) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y002N2) 16/512, Starlight, "Starlight"
    "Z15Y002N1" : ["Macbook Air 13” (M2 16/256) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y002N1) 16/256, Starlight, "Starlight"
    "Z15Y002N0" : ["Macbook Air 13” (M2 8/1TB) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y002N0) 8/1024, сияющая звезда
    "Z15Y002MY" : ["Macbook Air 13” (M2 8/256) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y002MY) 8/256, сияющая звезда
    "Z15Y000B3" : ["Macbook Air 13” (M2 16/1TB) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y000B3) 16/1024, сияющая звезда
    "Z15Y0000B" : ["Macbook Air 13” (M2 16/256) Starlight"], #Ноутбук Apple Macbook Air 13 M2 (Z15Y0000B) 16/256 Гб, Starlight, "Starlight"
    "Z15X0005M" : ["Macbook Air 13” (M2 24/2TB) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15X0005M) 24/2048, серебристый
    "Z15X0000D" : ["Macbook Air 13” (M2 16/1TB) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15X0000D) 16/1024 GB, Silver
    "Z15W002B6" : ["Macbook Air 13” (M2 24/2TB) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002B6) 24/2048, Silver, серебристый
    "Z15W002B5" : ["Macbook Air 13” (M2 24/1TB) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002B5) 24/1024, серебристый
    "Z15W002B4" : ["Macbook Air 13” (M2 24/512) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002B4) 24/512, серебристый
    "Z15W002B3" : ["Macbook Air 13” (M2 24/256) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002B3) 24/256, серебристый
    "Z15W002B2" : ["MacBook Air 13” (M2 16/2TB) Silver"], #Ноутбук Apple MacBook Air 13 M2 (Z15W002B2) 16/2048, Silver, серебристый
    "Z15W002B1" : ["MacBook Air 13” (M2 16/1TB) Silver"], #Ноутбук Apple MacBook Air 13 M2 (Z15W002B1) 16/1024, Silver, серебристый
    "Z15W002B0" : ["Macbook Air 13” (M2 16/512) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002B0) 16/512, серебристый
    "Z15W002AZ" : ["Macbook Air 13” (M2 16/256) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002AZ) 16/256, серебристый
    "Z15W002AY" : ["Macbook Air 13” (M2 8/1TB) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002AY) 8/1024, серебристый
    "Z15W002AW" : ["Macbook Air 13” (M2 8/256) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002AW) 8/256, серебристый
    "Z15W002AR" : ["Macbook Air 13” (M2 16/256) Silver"], #Ноутбук Apple Macbook Air 13 M2 (Z15W002AR) 16/256, серебристый
    "Z15T0000F" : ["Macbook Air 13” (M2 16/1TB) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15T0000F) 16/1024 GB, Space Gray
    "Z15S002L3" : ["MacBook Air 13” (M2 24/2TB) Space Gray"], #Ноутбук Apple MacBook Air 13 M2 (Z15S002L3) 24/2048, Space gray, "Space Gray"
    "Z15S002L2" : ["MacBook Air 13” (M2 24/1TB) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15S002L2) 24/1024, серый космос
    "Z15S002L1" : ["MacBook Air 13” (M2 24/512) Space Gray"], #Ноутбук Apple MacBook Air 13 M2 (Z15S002L1) 24/512, серый космос
    "Z15S002L0" : ["MacBook Air 13” (M2 24/256) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15S002L0) 24/256, серый космос
    "Z15S002KZ" : ["MacBook Air 13” (M2 16/2TB) Space Gray"], #Ноутбук Apple MacBook Air 13 M2 (Z15S002KZ) 16/2048, серый космос
    "Z15S002KY" : ["MacBook Air 13” (M2 16/1TB) Space Gray"], #Ноутбук Apple MacBook Air 13 M2 (Z15S002KY) 16/1024, Space gray, "Space Gray"
    "Z15S002KX" : ["Macbook Air 13” (M2 16/512) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15S002KX) 16/512, Space gray, "Space Gray"
    "Z15S002KV" : ["Macbook Air 13” (M2 8/1TB) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15S002KV) 8/1024, серый космос
    "Z15S002KT" : ["Macbook Air 13” (M2 8/256) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15S002KT) 8/256, серый космос
    "Z15S002KS" : ["Macbook Air 13” (M2 24/512) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15S002KS) 24/512, серый космос
    "Z15S00112" : ["Macbook Air 13” (M2 16/256) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15S00112) 16/256, Space gray, "Space Gray"
    "Z15S000V9" : ["Macbook Air 13” (M2 16/512) Space Gray"], #Ноутбук Apple Macbook Air 13 M2 (Z15S000V9) 16/512, серый космос
    "MN703" : ["MacBook Air 13” (M2 16/1TB) Midnight"], #Ноутбук Apple MacBook Air 13 M2 (MN703) 16/1024 GB, Midnight
    "MLXY3" : ["MacBook Air 13” (M2 8/256) Silver"], #Ноутбук Apple MacBook Air 13 M2 (MLXY3) 8/256, серебристый
    "Z127000NL" : ["Macbook Air 13” (M1 16/256) Silver"], #Ноутбук Apple Macbook Air 13 M1 2020 (Z127000NL) 16/256, Silver, серебристый
    "Z12A000P5" : ["Macbook Air 13” (M1 16/256) Gold"], #Ноутбук Apple Macbook Air 13 M1 (Z12A000P5) 16/256, Gold, золотой
    "Z12700036" : ["Macbook Air 13” (M1 16/512) Space Gray"], #Ноутбук Apple Macbook Air 13 M1 (Z12700036) 16/512, Space gray, "Space Gray"
    "MGN93ZE/A/R1" : ["Macbook Air 13” (M1 16/256) Space Gray"], #Ноутбук Apple Macbook Air 13 M1 (MGN93ZE/A/R1) 16/256, серый космос
    "MGN93" : ["Macbook Air 13” (M1 8/256) Silver"], #Ноутбук Apple Macbook Air 13 M1 (MGN93) 8/256, серебристый"
    "MC9K4" : ["Macbook Air 15” (M3 24/512) Starlight"], #Ноутбук Apple Macbook Air 15 M3 (MC9K4) 24/512, Starlight, "Starlight"
    "Z18T000PR" : ["MacBook Air 15” (M2 24/2TB) Midnight"], # Ноутбук Apple MacBook Air 15 M2, RAM 24 ГБ, SSD 2048 ГБ, Z18T000PR, темная ночь
    "Z18T000PT" : ["MacBook Air 15” (M2 24/1TB) Midnight"], # Ноутбук Apple MacBook Air 15 M2, RAM 24 ГБ, SSD 1024 ГБ, Z18T000PT, темная ночь
    "Z18U2" : ["MacBook Air 15” (M2 16/512) Midnight"], # Ноутбук Apple MacBook Air 15 M2, RAM 16 ГБ, SSD 512 ГБ, Z18U2, темная ночь
    "Z18S000Q7" : ["MacBook Air 15” (M2 16/512) Starlight"], # Ноутбук Apple MacBook Air 15 M2, RAM 16 ГБ, SSD 512 ГБ, Z18S000Q7, сияющая звезда
    "Z18R000XA" : ["MacBook Air 15” (M2 16/512) Starlight"], # Ноутбук Apple MacBook Air 15 M2, RAM 16 ГБ, SSD 512 ГБ, Z18R000XA, Starlight, "Starlight"
    "Z18L000Y0" : ["MacBook Air 15” (M2 16/512) Space Gray"], # Ноутбук Apple MacBook Air 15 M2, RAM 16 ГБ, SSD 512 ГБ, Z18L000Y0,  Gray, серый
    "Z18P0006L" : ["MacBook Air 15” (M2 16/256) Silver"], # Ноутбук Apple MacBook Air 15 M2, RAM 16 ГБ, SSD 256 ГБ, Z18P0006L, Silver, серебристый
    "Z18UO" : ["MacBook Air 15” (M2 16/1TB) Midnight"], # Ноутбук Apple MacBook Air 15 M2, RAM 16 ГБ, SSD 1024 ГБ, Z18UO, темная ночь
    "Z18T000PQ" : ["MacBook Air 15” (M2 16/1TB) Midnight"], # Ноутбук Apple MacBook Air 15 M2, RAM 16 ГБ, SSD 1024 ГБ, Z18T000PQ, Midnight, тёмная ночь
    "Z1BP000LV" : ["Macbook Air 13” (M3 24/2TB) Space Gray"], # Ноутбук Apple Macbook Air 13 M3 (Z1BP000LV) 24/2048 GB, Gray
    "Z1BC00148" : ["Macbook Air 13” (M3 24/1TB) Midnight"], # Ноутбук Apple Macbook Air 13 M3 (Z1BC00148) 24/1024 GB, Midnight
    "Z1B9000MY" : ["Macbook Air 13” (M3 24/1TB) Silver"], # Ноутбук Apple Macbook Air 13 M3 (Z1B9000MY) 24/1024 GB, Silver
    "Z1B7000P2" : ["Macbook Air 13” (M3 24/2TB) Space Gray"], # Ноутбук Apple Macbook Air 13 M3 (Z1B7000P2) 24/2048 GB, Gray
    "Z1B7000N3" : ["Macbook Air 13” (M3 24/1TB) Space Gray"], # Ноутбук Apple Macbook Air 13 M3 (Z1B7000N3) 24/1024 GB, Gray
    "MC9J4" : ["Macbook Air 13” (M3 24/512) Silver"], # Ноутбук Apple Macbook Air 13 M3 (MC9J4) 24/512 GB, Silver
    "MC8K4" : ["Macbook Air 13” (M3 16/256) Midnight"], # Ноутбук Apple Macbook Air 13 M3 (MC8K4) 16/256, темная ночь
    "Z1BT000L8" : ["Macbook Air 15” (M3 16/1TB) Starlight"], # Ноутбук Apple Macbook Air 15 M3 (Z1BT000L8) 16/1024 Гб, Starlight, сияющая звезда
    "Z1BT000L2" : ["Macbook Air 15” (M3 24/512) Starlight"], # Ноутбук Apple Macbook Air 15 M3 (Z1BT000L2), 24/512 GB, Starlight
    "Z1BT000KB" : ["Macbook Air 15” (M3 24/1TB) Starlight"], # Ноутбук Apple Macbook Air 15 M3 (Z1BT000KB), 24/1024 GB, Starlight
    "Z1BR000LF" : ["Macbook Air 15” (M3 24/2TB) Silver"], # Ноутбук Apple Macbook Air 15 M3 (Z1BR000LF), 24/2048 GB, Silver
    "MC9H4" : ["Macbook Air 15” (M3 24/512) Space Gray"], # Ноутбук Apple Macbook Air 15 M3 (MC9H4RU/A) 24/512 GB, Space Gray
    "Z15S000CT" : ["MacBook Air 13” (M2 16/256) Space Gray"], #Apple MacBook Air 13" Z15S000CT (M2, 2022), 16
    "Z15S002KW" : ["MacBook Air 13” (M2 16/256) Space Gray"], #Apple MacBook Air 13" Z15S002KW (M2, 2022), 16
    "Z15W000BB" : ["MacBook Air 13” (M2 24/1TB) Silver"], #Apple MacBook Air 13" Z15W000BB (M2, 2022), 24 ГБ,
    "Z15Y000B2" : ["MacBook Air 13” (M2 16/512) Starlight"], #Apple MacBook Air 13" Z15Y000B2 (M2, 2022), 16 Г
    "Z1600040F" : ["MacBook Air 13” (M2 16/1TB) Midnight"], #Apple MacBook Air 13" Z1600040F (M2, 2022), 16 ГБ
    "Z18T000PP" : ["MacBook Air 15” (M2 16/512) Midnight"], #Apple MacBook Air 15" (M2, 2023), 16 ГБ, 512 ГБ S
    "Z18L000PR" : ["MacBook Air 15” (M2 16/512) Space Gray"], #Apple MacBook Air 15" (M2, 2023), 16 ГБ, 512 ГБ
    "MQKW3" : ["MacBook Air 15” (M2 8/256) Midnight"], #Apple MacBook Air 15" (M2, 2023), 8 ГБ, 256 ГБ SSD, Mi
    "MQKR3" : ["MacBook Air 15” (M2 8/256) Silver"], #Apple MacBook Air 15" (M2, 2023), 8 ГБ, 256 ГБ SSD, Silv
    "MQKU3" : ["MacBook Air 15” (M2 8/256) Starlight"], #Apple MacBook Air 15" (M2, 2023), 8 ГБ, 256 ГБ SSD, S
    "MGNE3" : ["MacBook Air 13” (M1 8/512) Gold"], #Apple MacBook Air 13 MGNE3 (M1, 2020) 8 ГБ, 512 ГБ SSD, зо
    "Z124000FK" : ["MacBook Air 13” (M1 16/256) Space Gray"], #Apple MacBook Air Z124000FK (M1, 2020) 16 ГБ, 2
    "MXD43" : ["MacBook Air 15” (M3 16/512) Midnight"], #Apple Macbook Air 15 M3 (MXD43) 16/512 ГБ, Midnight
    #2025
    "MW133" : ["MacBook Air 13” (M4 16/512) Midnight"], #Apple MacBook Air 13” MW133 (M4 10-Core, GPU 10-Core, 16GB, 512GB) (Midnight)
    "MC6U4" : ["MacBook Air 13” (M4 16/512) Sky Blue"], #MacBook Air 13” MC6U4 (M4 10-Core, GPU 10-Core, 16GB, 512GB) (Sky Blue)
    "MC6A4" : ["MacBook Air 13” (M4 24/512) Starlight"], #Apple MacBook Air 13” MC6A4 (M4 10-Core, GPU 10-Core, 24GB, 512GB) («Сияющая звезда» | Starlight)
    "MW1G3" : ["MacBook Air 15” (M4 16/256) Silver"], #Apple MacBook Air 15” MW1G3 (M4 , 16GB, 256GB) (Silver)
    "MW1L3" : ["MacBook Air 15” (M4 16/256) Midnight"], #MacBook Air 15” MW1L3 (M4  16GB, 256GB) (Midnight)
    "MW1J3" : ["MacBook Air 15” (M4 16/256) Starlight"], #MacBook Air 15” MW1J3 (M4 16GB, 256GB) (Starlight)
    "MW1M3" : ["MacBook Air 15” (M4 16/512) Midnight"], #MacBook Air 15” MW1M3 (M4 10-Core, GPU 10-Core, 16GB, 512GB) («Тёмная ночь» | Midnight)
    "MC7C4" : ["MacBook Air 15” (M4 16/512) Sky Blue"], #MacBook Air 15” MC7C4 (M4 16GB, 512GB) (Sky Blue)
    "MC6T4": ["MacBook Air 13″ (M4 16/256) Sky Blue"],
    "MW0W3": ["MacBook Air 13″ (M4 16/256) Silver"],
    "MW0Y3": ["MacBook Air 13″ (M4 16/256) Starlight"],
    "MW123": ["MacBook Air 13″ (M4 16/256) Midnight"],
    "MW0X3": ["MacBook Air 13″ (M4 16/512) Silver"],
    "MW103": ["MacBook Air 13″ (M4 16/512) Starlight"],
    "MC6V4": ["MacBook Air 13″ (M4 24/512) Sky Blue"],
    "MC654": ["MacBook Air 13″ (M4 24/512) Silver"],
    "MC6C4": ["MacBook Air 13″ (M4 24/512) Midnight"],
    "MC7A4": ["MacBook Air 15″ (M4 16/256) Sky Blue"],
    "MW1H3": ["MacBook Air 15″ (M4 16/512) Silver"],
    "MW1K3": ["MacBook Air 15″ (M4 16/512) Starlight"],

    #iMac
    "MWUY3" : ["iMac 24” (M4 16/512) Green"], #Apple iMac 24 2024 M4/16 GB/256 GB 10-Core (MWUY3) Green
    "MWUW3" : ["iMac 24” (M4 16/256) Yellow"],  # Apple iMac 24 2024 M4/16 GB/256 GB 10-Core (MWUW3) Yellow
    "MWV83" : ["iMac 24” (M4 16/256) Orange"],  # Apple iMac 24 2024 M4/16 GB/256 GB 10-Core (MWV83) Orange
    "MWV43" : ["iMac 24” (M4 16/256) Pink"],  # Apple iMac 24 2024 M4/16 GB/256 GB 10-Core (MWV43) Pink
    "MWV63" : ["iMac 24” (M4 16/256) Purple"],  # Apple iMac 24 2024 M4/16 GB/256 GB 10-Core (MWV63) Purple
    "MWUF3" : ["iMac 24” (M4 16/256) Blue"],  # Apple iMac 24 2024 M4/16 GB/256 GB 8-Core (MWUF3) Blue
    "MWUC3" : ["iMac 24” (M4 16/256) Silver"],  # Apple iMac 24 2024 M4/16 GB/256 GB 8-Core (MWUC3) Silver
    "MWV03" : ["iMac 24” (M4 16/512) Green"],  # Apple iMac 24 2024 M4/16 GB/512 GB 10-Core (MWV03) Green
    "MWUX3" : ["iMac 24” (M4 16/512) Yellow"],  # Apple iMac 24 2024 M4/16 GB/512 GB 10-Core (MWUX3) Yellow
    "MWV93" : ["iMac 24” (M4 16/512) Orange"],  # Apple iMac 24 2024 M4/16 GB/512 GB 10-Core (MWV93) Orange
    "MWV53" : ["iMac 24” (M4 16/512) Pink"],  # Apple iMac 24 2024 M4/16 GB/512 GB 10-Core (MWV53) Pink
    "MWV73" : ["iMac 24” (M4 16/512) Purple"],  # Apple iMac 24 2024 M4/16 GB/512 GB 10-Core (MWV73) Purple
    "MWV33" : ["iMac 24” (M4 16/512) Blue"],  # Apple iMac 24 2024 M4/16 GB/512 GB 10-Core (MWV33) Blue
    "MWUV3" : ["iMac 24” (M4 16/512) Silver"],  # Apple iMac 24 2024 M4/16 GB/512 GB 10-Core (MWUV3) Silver
    "MD2Q4" : ["iMac 24” (M4 24/512) Green"],  # Apple iMac 24 2024 M4/24 GB/512 GB 10-Core (MD2Q4) Green
    "MD2P4" : ["iMac 24” (M4 24/512) Yellow"],  # Apple iMac 24 2024 M4/24 GB/512 GB 10-Core (MD2P4) Yellow
    "MD2W4" : ["iMac 24” (M4 24/512) Orange"],  # Apple iMac 24 2024 M4/24 GB/512 GB 10-Core (MD2W4) Orange
    "MD2U4" : ["iMac 24” (M4 24/512) Pink"],  # Apple iMac 24 2024 M4/24 GB/512 GB 10-Core (MD2U4) Pink
    "MD2V4" : ["iMac 24” (M4 24/512) Purple"],  # Apple iMac 24 2024 M4/24 GB/512 GB 10-Core (MD2V4) Purple
    "MD2T4" : ["iMac 24” (M4 24/512) Blue"],  # Apple iMac 24 2024 M4/24 GB/512 GB 10-Core (MD2T4) Blue
    "MCR24" : ["iMac 24” (M4 24/512) Silver"],  # Apple iMac 24 2024 M4/24 GB/512 GB 10-Core (MCR24) Silver
    "MQRJ3" : ["iMac 24” (M3 8/256) Green"], #Apple iMac 24 2023 M3/8GB/256GB/M3 10-Core (MQRJ3 - Late 2023) Green
    "MQR93" : ["iMac 24” (M3 8/256) Silver"],  # Apple iMac 24 2023 M3/8GB/256GB/M2 8-Core (MQR93 - Late 2023) Silver
    "MQRD3" : ["iMac 24” (M3 8/256) Red"],  # Apple iMac 24 2023 M3/8GB/256GB/M2 8-Core (MQRD3 - Late 2023) Red
    "MQRC3" : ["iMac 24” (M3 8/256) Blue"],  # Apple iMac 24 2023 M3/8GB/256GB/M2 8-Core (MQRC3 - Late 2023) Blue
    "MQRP3" : ["iMac 24” (M3 8/512) Green"],  # Apple iMac 24 2023 M3/8GB/512GB/M3 10-Core (MQRP3 - Late 2023) Green
    "MQRK3" : ["iMac 24” (M3 8/512) Silver"],  # Apple iMac 24 2023 M3/8GB/512GB/M3 10-Core (MQRK3 - Late 2023) Silver
    "MQRU3" : ["iMac 24” (M3 8/512) Red"],  # Apple iMac 24 2023 M3/8GB/512GB/M3 10-Core (MQRU3 - Late 2023) Red
    "MQRR3" : ["iMac 24” (M3 8/512) Blue"],  # Apple iMac 24 2023 M3/8GB/512GB/M3 10-Core (MQRR3 - Late 2023) Blue
    "Z1K80000L" : ["iMac 24” (M4 32/1TB) Green"],  # Моноблок Apple iMac 24 2024 (Z1K80000L), 32/1TB GB, Orange
    "Z1K50000M" : ["iMac 24” (M4 32/2TB) Blue"],  # Моноблок Apple iMac 24 2024 (Z1K50000M), 32/2048 GB, Blue
    "Z1K50000L" : ["iMac 24” (M4 32/1TB) Blue"],  # Моноблок Apple iMac 24 2024 (Z1K50000L), 32/1TB GB, Blue
    "Z1K30000M" : ["iMac 24” (M4 32/2TB) Green"],  # Моноблок Apple iMac 24 2024 (Z1K30000M), 32/2048 GB, Green
    "Z1K30000L" : ["iMac 24” (M4 32/1TB) Green"],  # Моноблок Apple iMac 24 2024 (Z1K30000L), 32/1TB GB, Green
    "Z1K300003" : ["iMac 24” (M4 24/1TB) Green"],  # Моноблок Apple iMac 24 2024 (Z1K300003), 24/1TB GB, Green
    "Z1K10000L" : ["iMac 24” (M4 32/1TB) Silver"],  # Моноблок Apple iMac 24 2024 (Z1K10000L), 32/1TB GB, Silver
    "Z1K100003" : ["iMac 24” (M4 24/1TB) Silver"],  # Моноблок Apple iMac 24 2024 (Z1K100003), 24/1TB GB, Silver
    "Z1EQ00003" : ["iMac 24” (M4 16/1TB) Blue"],  # Моноблок Apple iMac 24 2024 (Z1EQ00003), 16/1TB GB, Blue
    "Z1EN00003" : ["iMac 24” (M4 16/1TB) Green"],  # Моноблок Apple iMac 24 2024 (Z1EN00003), 16/1TB GB, Green
    "Z1EJ00003" : ["iMac 24” (M4 16/1TB) Silver"],  # Моноблок Apple iMac 24 2024 (Z1EJ00003), 16/1TB GB, Silver
    "Z19R001DF" : ["iMac 24” (M3 16/512) Orange"],  # Моноблок Apple iMac 24 2023 (Z19R001DF), 16/512 GB, Orange
    "Z19L00033" : ["iMac 24” (M3 16/1TB) Blue"],  # Моноблок Apple iMac 24 2023 (Z19L00033), 16/1TB GB, Blue
    "Z19K0019C" : ["iMac 24” (M3 16/512) Blue"],  # Моноблок Apple iMac 24 2023 (Z19K0019C), 16/512 ГБ, Blue
    "Z19J0001L" : ["iMac 24” (M3 16/1TB) Green"],  # Моноблок Apple iMac 24 2023 (Z19J0001L), 16/1TB GB, Green
    "Z19H001LZ" : ["iMac 24” (M3 16/512) Green"],  # Моноблок Apple iMac 24 2023 (Z19H001LZ), 16/512 ГБ, Green
    "Z19H0011L" : ["iMac 24” (M3 16/512) Green"],  # Моноблок Apple iMac 24 2023 (Z19H0011L), 16/512 GB, Green
    "Z19D0023H" : ["iMac 24” (M3 16/2TB) Silver"],  # Моноблок Apple iMac 24 2023 (Z19D0023H), 16/2 ТБ, Silver
    "MGPL3" : ["iMac 24” (M1 8/512) Blue"],  # Моноблок Apple iMac 24 2021 (MGPL3), 8/512 ГБ, Blue
    "MGPK3" : ["iMac 24” (M1 8/256) Blue"],  # Моноблок Apple iMac 24 2021 (MGPK3), 8/256 ГБ, Blue
    "MGPH3" : ["iMac 24” (M1 8/256) Green"],  # Моноблок Apple iMac 24 2021 (MGPH3), 8/256 ГБ, Green
    "Z1K70000L" : ["iMac 24” (M4 32/1TB) Purple"],  # Моноблок Apple iMac 24 2024 (Z1K70000L), 32/1TB GB, Purple
    "Z1EU00003" : ["iMac 24” (M4 16/1TB) Purple"],  # Моноблок Apple iMac 24 2024 (Z1EU00003), 16/1TB GB, Purple
    "MWV13" : ["iMac 24” (M4 16/256) Blue"],  # Моноблок Apple iMac 24 2024 (MWV13), 16/256 GB, Blue
    "MD3H4" : ["iMac 24” (M4 16/256) Silver"],  # Моноблок Apple iMac 24 2024 (MD3H4), 16/256 GB, Silver
    "Z19S000YC" : ["iMac 24” (M3 24/1TB) Orange"], #Моноблок Apple iMac 24 2023 (Z19S000YC), 24/1024 GB, Orange
    "Z19S00043" : ["iMac 24” (M3 24/1TB) Orange"], #Моноблок Apple iMac 24 2023 (Z19S00043), 24/1024 ГБ, оранжевый
    "Z19S00033" : ["iMac 24” (M3 16/1TB) Orange"], #Моноблок Apple iMac 24 2023 (Z19S00033), 16/1024 ГБ, оранжевый
    "Z19R001KO" : ["iMac 24” (M3 16/1TB) Orange"], #Моноблок Apple iMac 24 2023 (Z19R001KO), 16/1024 GB, Orange
    "Z19Q0001M" : ["iMac 24” (M3 24/1TB) Purple"], #Моноблок Apple iMac 24 2023 (Z19Q0001M), 24/1024 GB, Purple
    "Z19Q0001G" : ["iMac 24” (M3 16/512) Purple"], #Моноблок Apple iMac 24 2023 (Z19Q0001G), 16/512 GB, Purple
    "Z19L001B7" : ["iMac 24” (M3 24/2TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19L001B7), 24/2048 ГБ, Light blue , голубой
    "Z19L001AY" : ["iMac 24” (M3 16/512) Blue"], #Моноблок Apple iMac 24 2023 (Z19L001AY), 16/512 ГБ, голубой
    "Z19L00101" : ["iMac 24” (M3 24/2TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19L00101), 24/2048 ГБ, синий
    "Z19L000ZA" : ["iMac 24” (M3 24/1TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19L000ZA), 24/1024 ГБ, синий
    "Z19L000ER" : ["iMac 24” (M3 16/1TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19L000ER), 16/1024 ГБ, синий
    "Z19L00036" : ["iMac 24” (M3 24/2TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19L00036), 24/2048 GB, Blue
    "Z19L00034" : ["iMac 24” (M3 24/1TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19L00034), 24/1024 GB, Blue
    "Z19L0001N" : ["iMac 24” (M3 16/2TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19L0001N), 16/2048 ГБ, Light blue , голубой
    "Z19K002CN" : ["iMac 24” (M3 24/2TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19K002CN), 24/2048 ГБ, Light blue, голубой
    "Z19K0001V" : ["iMac 24” (M3 16/1TB) Blue"], #Моноблок Apple iMac 24 2023 (Z19K0001V), 16/1024 GB, Blue
    "Z19K0001T" : ["iMac 24” (M3 16/512) Blue"], #Моноблок Apple iMac 24 2023 (Z19K0001T), 16/512 GB, Blue
    "Z19H0001W" : ["iMac 24” (M3 24/1TB) Green"], #Моноблок Apple iMac 24 2023 (Z19H0001W), 24/1024 GB, Green
    "Z19H0001V" : ["iMac 24” (M3 16/1TB) Green"], #Моноблок Apple iMac 24 2023 (Z19H0001V), 16/1024 GB, Green
    "Z19H0001P" : ["iMac 24” (M3 16/256) Green"], #Моноблок Apple iMac 24 2023 (Z19H0001P), 16/256 GB, Green
    "Z19G000Z8" : ["iMac 24” (M3 24/1TB) Yellow"], #Моноблок Apple iMac 24 2023 (Z19G000Z8), 24/1024 ГБ, желтый
    "Z19F001HV" : ["iMac 24” (M3 24/2TB) Yellow"], #Моноблок Apple iMac 24 2023 (Z19F001HV), 24/2048 ГБ, желтый
    "Z19E001CL" : ["iMac 24” (M3 24/2TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19E001CL), 24/2 ТБ, серебристый
    "Z19E000ZY" : ["iMac 24” (M3 24/2TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19E000ZY), 24/2 ТБ, Silver, серебристый
    "Z19E000ZC" : ["iMac 24” (M3 24/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19E000ZC), 24/1 ТБ, серебристый
    "Z19E000Y4" : ["iMac 24” (M3 16/512) Silver"], #Моноблок Apple iMac 24 2023 (Z19E000Y4), 16/512 ГБ, серебристый
    "Z19E000Y3" : ["iMac 24” (M3 16/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19E000Y3), 16/1 ТБ, серебристый
    "Z19E00036" : ["iMac 24” (M3 24/2TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19E00036), 24/2048 GB, Silver
    "Z19E00034" : ["iMac 24” (M3 24/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19E00034), 24/1 ТБ, серебристый
    "Z19E00033" : ["iMac 24” (M3 16/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19E00033), 16/1024 GB, Silver
    "Z19D0023E" : ["iMac 24” (M3 16/512) Silver"], #Моноблок Apple iMac 24 2023 (Z19D0023E), 16/512 ГБ, серебристый
    "Z19D001KC" : ["iMac 24” (M3 24/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19D001KC), 24/1024 GB, Silver
    "Z19D0015E" : ["iMac 24” (M3 24/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19D0015E), 24/1024 GB, Silver
    "Z19D0012Y" : ["iMac 24” (M3 24/2TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19D0012Y), 24/2048 GB, Silver
    "Z19D0012G" : ["iMac 24” (M3 16/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19D0012G), 16/1024 GB, Silver
    "Z19D0001U" : ["iMac 24” (M3 16/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19D0001U), 16/1024 GB, Silver
    "Z19D0001P" : ["iMac 24” (M3 16/256) Silver"], #Моноблок Apple iMac 24 2023 (Z19D0001P), 16/256 GB, Silver
    "Z197000HL" : ["iMac 24” (M3 16/512) Silver"], #Моноблок Apple iMac 24 2023 (Z197000HL), 16/512 ГБ, Silver, серебристый
    "Z1970004P" : ["iMac 24” (M3 16/512) Blue"], #Моноблок Apple iMac 24 2023 (Z1970004P), 16/512 ГБ, синий
    "Z195001А1" : ["iMac 24” (M3 16/512) Silver"], #Моноблок Apple iMac 24 2023 (Z195001А1), 16/512 ГБ, серебристый
    "Z195001LZ" : ["iMac 24” (M3 24/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z195001LZ), 24/1024 ГБ, Silver, серебристый
    "Z1950004S" : ["iMac 24” (M3 16/512) Silver"], #Моноблок Apple iMac 24 2023 (Z1950004S), 16/512 ГБ, серебристый
    "Z1950004R" : ["iMac 24” (M3 16/512) Silver"], #Моноблок Apple iMac 24 2023 (Z1950004R), 16/512 ГБ, серебристый
    "Z19500025" : ["iMac 24” (M3 16/1TB) Silver"], #Моноблок Apple iMac 24 2023 (Z19500025), 16/1024 ГБ, Silver, серебристый
    "Z19500023" : ["iMac 24” (M3 16/512) Silver"], #Моноблок Apple iMac 24 2023 (Z19500023), 16/512 ГБ, серебристый
    "Z1950001Z" : ["iMac 24” (M3 16/256) Silver"], #Моноблок Apple iMac 24 2023 (Z1950001Z), 16/256 ГБ, серебристый
    "MR7E3" : ["iMac 24” (M3 16/512) Silver"], #Моноблок Apple iMac 24 2023 (MR7E3), 16/512 GB, Silver
    "MQRX3" : ["iMac 24” (M3 8/256) Orange"], #Моноблок Apple iMac 24 2023 (MQRX3), 8/256 ГБ, оранжевый
    "MQRT3" : ["iMac 24” (M3 8/256) Pink"], #Моноблок Apple iMac 24 2023 (MQRT3), 8/256 ГБ, Pink, розовый
    "MQRQ3" : ["iMac 24” (M3 8/256) Blue"], #Моноблок Apple iMac 24 2023 (MQRQ3B/A), 8/256 ГБ, голубой
    "MQRN3" : ["iMac 24” (M3 8/256) Green"], #Моноблок Apple iMac 24 2023 (MQRN3), 8/256 ГБ, зеленый
    "MQRL3" : ["iMac 24” (M3 8/256) Yellow"], #Моноблок Apple iMac 24 2023 (MQRL3), 8/256 ГБ, Yellow, желтый
    "MQRA3" : ["iMac 24” (M3 8/256) Green"], #Моноблок Apple iMac 24 2023 (MQRA3), 8/256 ГБ, зеленый
    "MQR83" : ["iMac 24” (M3 8/256) Green"], #Моноблок Apple iMac 24 2023 (MQR83X/A), 8/256 ГБ, Green, зеленый
    "MGTF3" : ["iMac 24” (M1 8/256) Silver"], #Apple iMac 24 M1(7-Core GPU)/8GB/256GB (MGTF3 - Mid 2021) Silver
    "MJV83" : ["iMac 24” (M1 8/256) Green"], #Apple iMac 24 M1(7-Core GPU)/8GB/256GB (MJV83 - Mid 2021) Green
    "MJV93" : ["iMac 24” (M1 8/256) Blue"], #Apple iMac 24 M1(7-Core GPU)/8GB/256GB (MJV93 - Mid 2021) Blue
    "MJVA3" : ["iMac 24” (M1 8/256) Pink"], #Apple iMac 24 M1(7-Core GPU)/8GB/256GB (MJVA3 - Mid 2021) Pink
    "MGPC3" : ["iMac 24” (M1 8/256) Silver"], #Apple iMac 24 M1(8-Core GPU)/8GB/256GB (MGPC3 - Mid 2021) Silver
    "MGPM3" : ["iMac 24” (M1 8/256) Pink"], #Apple iMac 24 M1(8-Core GPU)/8GB/256GB (MGPM3 - Mid 2021) Pink
    "Z12SIMAC01" : ["iMac 24” (M1 8/256) Yellow"], #Apple iMac 24 M1(8-Core GPU)/8GB/256GB (Z12SIMAC01-Mid 2021) Yellow
    "Z130IMAC01" : ["iMac 24” (M1 8/256) Purple"], #Apple iMac 24 M1(8-Core GPU)/8GB/256GB (Z130IMAC01 - Mid-2021) Purple
    "Z132IMAC01" : ["iMac 24” (M1 8/256) Orange"], #Apple iMac 24 M1(8-Core GPU)/8GB/256GB (Z132IMAC01-Mid 2021) Orange
    "MGPD3" : ["iMac 24” (M1 8/512) Silver"], #Apple iMac 24 M1(8-Core GPU)/8GB/512GB (MGPD3 - Mid 2021) Silver
    "MGPJ3" : ["iMac 24” (M1 8/512) Green"], #Apple iMac 24 M1(8-Core GPU)/8GB/512GB (MGPJ3 - Mid 2021) Green
    "MGPN3" : ["iMac 24” (M1 8/512) Pink"], #Apple iMac 24 M1(8-Core GPU)/8GB/512GB (MGPN3 - Mid 2021) Pink
    "Z12TIMAC01" : ["iMac 24” (M1 8/512) Yellow"], #Apple iMac 24 M1(8-Core GPU)/8GB/512GB (Z12TIMAC01-Mid 2021) Yellow
    "Z131IMAC01" : ["iMac 24” (M1 8/512) Purple"], #Apple iMac 24 M1(8-Core GPU)/8GB/512GB (Z131IMAC01 - Mid-2021) Purple
    "Z133IMAC01" : ["iMac 24” (M1 8/512) Orange"], #Apple iMac 24 M1(8-Core GPU)/8GB/512GB (Z133IMAC01-Mid 2021) Orange
    "Z12Q003AY" : ["iMac 24” (M1 8/1024) Silver"], #iMac 24" 2021 (Z12Q003AY), 8/1024 ГБ, серебристый
    "MGPP3" : ["iMac 24” (M1 8/256) Purple"], #iMac 24 Retina 4,5K (MGPP3), M1 (8C CPU, 8C GPU), 8 ГБ, 256 ГБ SSD, Purple, фиолетовый
    "MGPR3" : ["iMac 24” (M1 8/256) Orange"], #iMac 24" (MGPR3), M1 (8C CPU, 8C GPU), 8 ГБ, 256 ГБ SSD, оранжевый
    "MWUE3" : ["iMac 24” (M4 8/256) Green"], #iMac 24" (MWUE3), M4 (8C CPU, 8C GPU), 16 ГБ, 256 ГБ SSD, зеленый
    "MWUG3" : ["iMac 24” (M4 8/256) Pink"], #iMac 24" (MWUG3), M4 (8C CPU, 8C GPU), 16 ГБ, 256 ГБ SSD, розовый
    "MWUU3" : ["iMac 24” (M4 10/256) Silver"], #iMac 24" (MWUU3), M4 (10C CPU, 10C GPU), 16 ГБ, 256 ГБ SSD, серебристый
    "Z1K1000ES" : ["iMac 24” (M4 10/1024) Silver"], #iMac 24" (Z1K1000ES), M4 (10C CPU, 10C GPU), 32 ГБ, 1024 ГБ SSD, Nano-texture glass, серебристый
    "Z19D001G5" : ["iMac 24” (M3 24/2048) Silver"], #iMac 24 M3 Z19D001G5 (8C CPU, 10C GPU) 24/2048 ГБ SSD, серебристый
    "Z19K001QC" : ["iMac 24” (M3 24/2048) Blue"], #iMac 24 M3 Z19K001QC (8C CPU, 10C GPU) 24/2048 ГБ SSD, синий
    "Z1330024S" : ["iMac 24” (M1 16/1TB) Orange"], #iMac 24 2021 (Z1330024S), M1 16/1024 ГБ, Orange
    "Z13300107" : ["iMac 24” (M1 16/1TB) Orange"], #iMac 24 2021 (Z13300107), M1 16/1024 ГБ, Orange
    "Z131002M1" : ["iMac 24” (M1 16/2TB) Purple"], #iMac 24 2021 (Z131002M1), M1 16/2048 ГБ, Purple
    "Z131002LK" : ["iMac 24” (M1 16/512) Purple"], #iMac 24 2021 (Z131002LK), M1 16/512 ГБ, Purple
    "Z131002LG" : ["iMac 24” (M1 16/512) Purple"], #iMac 24 2021 (Z131002LG), M1 16/512 ГБ, Purple
    "Z131002LF" : ["iMac 24” (M1 16/2TB) Purple"], #iMac 24 2021 (Z131002LF), M1 16/2048 ГБ, Purple
    "Z131002LE" : ["iMac 24” (M1 16/1TB) Purple"], #iMac 24 2021 (Z131002LE), M1 16/1024 ГБ, Purple
    "Z1310027W" : ["iMac 24” (M1 16/1TB) Purple"], #iMac 24 2021 (Z1310027W), M1 16/1024 ГБ, Purple
    "Z1310006P" : ["iMac 24” (M1 8/512) Purple"], #iMac 24 2021 (Z1310006P), M1 8/512 ГБ, Purple
    "Z1310005F" : ["iMac 24” (M1 8/512) Purple"], #iMac 24 2021 (Z1310005F), M1 8/512 ГБ, Purple
    "Z130002B8" : ["iMac 24” (M1 8/256) Purple"], #iMac 24 2021 (Z130002B8), M1 8/256 ГБ, Purple
    "Z130002A7" : ["iMac 24” (M1 8/512) Purple"], #iMac 24 2021 (Z130002A7), M1 8/512 ГБ, Purple
    "Z130002A6" : ["iMac 24” (M1 16/512) Purple"], #iMac 24 2021 (Z130002A6), M1 16/512 ГБ, Purple
    "Z130000NR" : ["iMac 24” (M1 16/256) Purple"], #iMac 24 2021 (Z130000NR), M1 16/256 ГБ, Purple
    "Z1300007H" : ["iMac 24” (M1 8/256) Purple"], #iMac 24 2021 (Z1300007H), M1 8/256 ГБ, Purple
    "Z12X003SJ" : ["iMac 24” (M1 16/2TB) Blue"], #iMac 24 2021 (Z12X003SJ), M1 16/2048 ГБ, Blue
    "Z12X003SH" : ["iMac 24” (M1 16/1TB) Blue"], #iMac 24 2021 (Z12X003SH), M1 16/1024 ГБ, Blue
    "Z12X003SG" : ["iMac 24” (M1 16/2TB) Blue"], #iMac 24 2021 (Z12X003SG), M1 16/2048 ГБ, Blue
    "Z12X003HR" : ["iMac 24” (M1 16/1TB) Blue"], #iMac 24 2021 (Z12X003HR), M1 16/1024 ГБ, Blue
    "Z12X0036C" : ["iMac 24” (M1 16/512) Blue"], #iMac 24 2021 (Z12X0036C), M1 16/512 ГБ, Blue
    "Z12X002BC" : ["iMac 24” (M1 16/512) Blue"], #iMac 24 2021 (Z12X002BC), M1 16/512 ГБ, Blue
    "Z12X000TA" : ["iMac 24” (M1 16/1TB) Blue"], #iMac 24 2021 (Z12X000TA), M1 16/1024 ГБ, Blue
    "Z12X0006P" : ["iMac 24” (M1 8/512) Blue"], #iMac 24 2021 (Z12X0006P), M1 8/512 ГБ, Blue
    "Z12X0005F" : ["iMac 24” (M1 8/512) Blue"], #iMac 24 2021 (Z12X0005F), M1 8/512 ГБ, Blue
    "Z12W0036V" : ["iMac 24” (M1 16/512) Blue"], #iMac 24 2021 (Z12W0036V), M1 16/512 ГБ, Blue
    "Z12W001E5" : ["iMac 24” (M1 16/512) Blue"], #iMac 24 2021 (Z12W001E5), M1 16/512 ГБ, Blue
    "Z12W000LS" : ["iMac 24” (M1 16/512) Blue"], #iMac 24 2021 (Z12W000LS), M1 16/512 ГБ, Blue
    "Z12W0007H" : ["iMac 24” (M1 8/256) Blue"], #iMac 24 2021 (Z12W0007H), M1 8/256 ГБ, Blue
    "Z12W00064" : ["iMac 24” (M1 8/256) Blue"], #iMac 24 2021 (Z12W00064), M1 8/256 ГБ, Blue
    "Z12V002WN" : ["iMac 24” (M1 16/1TB) Green"], #iMac 24 2021 (Z12V002WN), M1 16/1024 ГБ, Green
    "Z12V002WM" : ["iMac 24” (M1 16/2TB) Green"], #iMac 24 2021 (Z12V002WM), M1 16/2048 ГБ, Green
    "Z12V002VH" : ["iMac 24” (M1 16/2TB) Green"], #iMac 24 2021 (Z12V002VH), M1 16/2048 ГБ, Green
    "Z12V002VG" : ["iMac 24” (M1 16/1TB) Green"], #iMac 24 2021 (Z12V002VG), M1 16/1024 ГБ, Green
    "Z12V002VF" : ["iMac 24” (M1 16/512) Green"], #iMac 24 2021 (Z12V002VF), M1 16/512 ГБ, Green
    "Z12V0006P" : ["iMac 24” (M1 8/512) Green"], #iMac 24 2021 (Z12V0006P), M1 8/512 ГБ, Green
    "Z12U002EP" : ["iMac 24” (M1 8/512) Green"], #iMac 24 2021 (Z12U002EP), M1 8/512 ГБ, Green
    "Z12U002EN" : ["iMac 24” (M1 16/512) Green"], #iMac 24 2021 (Z12U002EN), M1 16/512 ГБ, Green
    "Z12U0007H" : ["iMac 24” (M1 8/256) Green"], #iMac 24 2021 (Z12U0007H), M1 8/256 ГБ, Green
    "Z12T002HK" : ["iMac 24” (M1 16/1TB) Yellow"], #iMac 24 2021 (Z12T002HK), M1 16/1024 ГБ, Yellow
    "Z12T002HJ" : ["iMac 24” (M1 16/1TB) Yellow"], #iMac 24 2021 (Z12T002HJ), M1 16/1024 ГБ, Yellow
    "Z12T000W0" : ["iMac 24” (M1 16/512) Yellow"], #iMac 24 2021 (Z12T000W0), M1 16/512 ГБ, Yellow
    "Z12R003QE" : ["iMac 24” (M1 16/512) Silver"], #iMac 24 2021 (Z12R003QE), M1 16/512 ГБ, Silver
    "Z12R003QD" : ["iMac 24” (M1 16/2TB) Silver"], #iMac 24 2021 (Z12R003QD), M1 16/2048 ГБ, Silver
    "Z12R003QC" : ["iMac 24” (M1 16/2TB) Silver"], #iMac 24 2021 (Z12R003QC), M1 16/2048 ГБ, Silver
    "Z12R003QB" : ["iMac 24” (M1 16/1TB) Silver"], #iMac 24 2021 (Z12R003QB), M1 16/1024 ГБ, Silver
    "Z12R002N8" : ["iMac 24” (M1 16/1TB) Silver"], #iMac 24 2021 (Z12R002N8), M1 16/1024 ГБ, Silver
    "Z12R0006P" : ["iMac 24” (M1 8/512) Silver"], #iMac 24 2021 (Z12R0006P), M1 8/512 ГБ, Silver
    "Z12R0005F" : ["iMac 24” (M1 8/512) Silver"], #iMac 24 2021 (Z12R0005F), M1 8/512 ГБ, Silver
    "Z12Q0034M" : ["iMac 24” (M1 16/512) Silver"], #iMac 24 2021 (Z12Q0034M), M1 16/512 ГБ, Silver
    "Z12Q0034K" : ["iMac 24” (M1 16/512) Silver"], #iMac 24 2021 (Z12Q0034K), M1 16/512 ГБ, Silver
    "Z12Q001SB" : ["iMac 24” (M1 16/1TB) Silver"], #iMac 24 2021 (Z12Q001SB), M1 16/1024 ГБ, Silver
    "Z12Q000V6" : ["iMac 24” (M1 16/256) Silver"], #iMac 24 2021 (Z12Q000V6), M1 16/256 GB, Silver
    "Z12Q000BV" : ["iMac 24” (M1 8/256) Silver"], #iMac 24 2021 (Z12Q000BV), M1 8/256 ГБ, Silver
    "Z12Q0007H" : ["iMac 24” (M1 8/256) Silver"], #iMac 24 2021 (Z12Q0007H), M1 8/256 ГБ, Silver
    "Z12Q00064" : ["iMac 24” (M1 8/256) Silver"], #iMac 24 2021 (Z12Q00064), M1 8/256 GB, Silver
    "Z1970004R" : ["iMac 24” (M3 16/1TB) Blue"], #iMac 24 (Z1970004R), M3 16/1024 ГБ, Blue
    "Z12X000LY" : ["iMac 24” (M1 16/2TB) Blue"], #iMac 24 (Z12X000LY), M1 16/2048 ГБ, Blue
    "Z12V001CW" : ["iMac 24” (M1 16/1TB) Green"], #iMac 24 (Z12V001CW), M1 16/1024 ГБ, Green
    "Z12V000QK" : ["iMac 24” (M1 16/2TB) Green"], #iMac 24 (Z12V000QK), M1 16/2048 ГБ, Green
    "MXWT2A" : ["iMac 27” (Intel i5 8/256) Silver"], #8/256Gb (INTEL i5 3.1 ГГЦ) Silver MXWT2A
    "MXWU2A" : ["iMac 27” (Intel i5 8/512) Silver"], #8/512Gb (INTEL i5 3.3 ГГЦ) Silver MXWU2A
    "MXWV2" : ["iMac 27” (Intel i7 8/512) Silver"], #8/512Gb (INTEL i7 3.8 ГГЦ) Silver MXWV2
    "MHJY3L" : ["iMac 27” (Intel i9 16/1TB) Silver"], #16/1TB (INTEL i9 3.6 ГГЦ) Silver MHJY3L

    #Mac Studio
    "Z14K0000V": ["Mac Studio (M1 Ultra 128/1TB)"], # Настольный компьютер Apple Mac Studio (2022) M1 Ultra (Z14K0000V), 128/1024 ГБ, серебристый
    "Z140004T": ["Mac Studio (M1 Ultra 128/1TB)"], # Настольный компьютер Apple Mac Studio (2022) M1 Ultra (Z140004T), 128/1024 GB, Silver
    "Z14K0000Q": ["Mac Studio (M1 Ultra 64/2TB)"], # Настольный компьютер Apple Mac Studio (2022) M1 Ultra (Z14K0000Q), 64/2048 ГБ, серебристый
    "MJMW3": ["Mac Studio (M1 Ultra 64/1TB)"], # Настольный компьютер Apple Mac Studio (2022) M1 Ultra (MJMW3), 64/1024 ГБ, серебристый
    "MJMV3": ["Mac Studio (M1 Max 32/512)"], # Настольный компьютер Apple Mac Studio (2022) M1 Max ( (MJMV3), 32/512 ГБ, Silver, серебристый
    "MQH63": ["Mac Studio (M2 Ultra 64/1TB)"], # Настольный компьютер Apple Mac Studio M2 Ultra (MQH63), 64/1024 ГБ, серебристый
    "MQH73": ["Mac Studio (M2 Max 32/512)"], # Настольный компьютер Apple Mac Studio M2 Max (MQH73HN/A), 32/512 ГБ, серебристый
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# 📱 Специальные правила для Apple IPAD 📱 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
IPAD_YEAR_RELEASE_PATTERN_CHIP = {
    # Если есть паттерн для определенной модели в виде года выбираем чип для определенной модели
    "iPad Air" : {"2024" : "M2"},
    "iPad Pro" : {
        "2022" : "M2",
        "2024" : "M4"}
}

IGNORING_IPAD_NO_CHIP = {
    "iPad Air" : {"11”", "13”"},
    "iPad Pro" : {"11”", "13”"}
}

GLASS_IPAD_STANDARD = {
    "iPad Pro": {
        "M4": {
            "1TB": "Standard Glass",
            "2TB": "Standard Glass",
        }
    }
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#🎧Специальные правила для Apple Airpods 🎧>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
AIRPODS_MAX_YEAR_RELEASE_PATTERN_COLOR = {
    #Если атрибут color у Airpods Max из этого списка ставим год 2024
    "Midnight" : "2024",
    "Starlight" : "2024",
    "Purple" : "2024",
    "Orange" : "2024"
}

AIRPODS_MAX_YEAR_RELEASE_PATTERN_PRICE = 53000  # Если цена выше этого => 2024

AIRPODS_CASE = {
    "3" : {
        "case MagSafe" : ["MagSafe"],
        "case Lightning" : ["Lightning"]
    },
    "Pro 2" : {
        "case MagSafe (USB-C)" : ["USB-C", "USB C", "Type-C", "Type C"],
        "case MagSafe (Lightning)" : ["Lightning"]
    }
}

IGNORING_APPLE_AIRPODS_RECOGNITION = [
    "DEPPO", "ухо", "L", "R", "Кейс",
    "левый наушник", "левый", "левое",
    "правый наушник", "правый", "правое",
    "зарядный футляр", "Box","Galaxy", "samsung", "JBL"
    ]
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для Samsung Galaxy 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
GALAXY_S_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "S21" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Phantom White" : ["Phantom White", "White"],
            "Green" : ["Green"],
            "Pink Gold" : ["Pink Gold", "PinkGold"],
            "Graphite" : ["Graphite", "Gray"],
            "Cream" : ["Cream"],
            "Sky Blue" : ["Sky Blue", "Blue"],
            "Violet" : ["Violet", "Purple"]
        },
    },
    "S21 FE" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Phantom White" : ["Phantom White", "White"],
            "Green" : ["Green"],
            "Pink Gold" : ["Pink Gold", "PinkGold"],
            "Graphite" : ["Graphite", "Gray"],
            "Cream" : ["Cream"],
            "Sky Blue" : ["Sky Blue", "Blue"],
            "Violet" : ["Violet", "Purple"]
        },
    },
    "S21+" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Phantom White" : ["Phantom White", "White"],
            "Green" : ["Green"],
            "Pink Gold" : ["Pink Gold", "PinkGold"],
            "Graphite" : ["Graphite", "Gray"],
            "Cream" : ["Cream"],
            "Sky Blue" : ["Sky Blue", "Blue"],
            "Violet" : ["Violet", "Purple"]
        },
    },
    "S21 Ultra" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Phantom White" : ["Phantom White", "White"],
            "Green" : ["Green"],
            "Burgundy" : ["Burgundy", "Red"],
            "Graphite" : ["Graphite", "Gray", "Grey"],
            "Sky Blue" : ["Sky Blue", "Blue"],
            "Red" : ["Red"]
        },
    },
    "S22" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Phantom White" : ["Phantom White", "White"],
            "Green" : ["Green"],
            "Pink Gold" : ["Pink Gold", "PinkGold"],
            "Graphite" : ["Graphite", "Gray", "Grey"],
            "Cream" : ["Cream"],
            "Sky Blue" : ["Sky Blue", "Blue"],
            "Violet" : ["Violet", "Purple"]
        },
    },
    "S22 FE" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Phantom White" : ["Phantom White", "White"],
            "Green" : ["Green"],
            "Pink Gold" : ["Pink Gold", "PinkGold"],
            "Graphite" : ["Graphite", "Gray", "Grey"],
            "Cream" : ["Cream"],
            "Sky Blue" : ["Sky Blue", "Blue"],
            "Violet" : ["Violet", "Purple"]
        },
    },
    "S22+" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Phantom White" : ["Phantom White", "White"],
            "Green" : ["Green"],
            "Pink Gold" : ["Pink Gold", "PinkGold"],
            "Graphite" : ["Graphite", "Gray", "Grey"],
            "Cream" : ["Cream"],
            "Sky Blue" : ["Sky Blue", "Blue"],
            "Violet" : ["Violet", "Purple"]
        },
    },
    "S22 Ultra" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Phantom White" : ["Phantom White", "White"],
            "Green" : ["Green"],
            "Burgundy" : ["Burgundy", "Red"],
            "Graphite" : ["Graphite", "Gray", "Grey"],
            "Sky Blue" : ["Sky Blue", "Blue"],
            "Red" : ["Red"]
        },
    },
    "S23" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Cream" : ["Cream"],
            "Green" : ["Green"],
            "Lavender" : ["Lavender"]
        },
    },
    "S23+" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Cream" : ["Cream"],
            "Green" : ["Green"],
            "Lavender" : ["Lavender"]
        },
    },
    "S23 Ultra" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Cream" : ["Cream"],
            "Green" : ["Green"],
            "Lavender" : ["Lavender"]
        },
    },
    "S23 FE" : {
        "color" : {
            "Mint" : ["Mint"],
            "Graphite" : ["Graphite"],
            "Cream" : ["Cream"],
            "Purple" : ["Purple"]
        },
    },
    "S24" : {
        "color" : {
            "Onyx Black" : ["Onyx Black", "Black"],
            "Marble Gray" : ["Marble Gray", "Gray", "Grey"],
            "Cobalt Violet" : ["Cobalt Violet", "Violet"],
            "Amber Yellow" : ["Amber Yellow", "Yellow"]
        }
    },
    "S24+" : {
        "color" : {
            "Onyx Black" : ["Onyx Black", "Black"],
            "Marble Gray" : ["Marble Gray", "Gray", "Grey"],
            "Cobalt Violet" : ["Cobalt Violet", "Violet"],
            "Amber Yellow" : ["Amber Yellow", "Yellow"]
        }
    },
    "S24 Ultra" : {
        "color" : {
            "Titanium Black" : ["Titanium Black", "Black"],
            "Titanium Gray" : ["Titanium Gray", "Gray", "Grey"],
            "Titanium Violet" : ["Titanium Violet", "Violet"],
            "Titanium Yellow" : ["Titanium Yellow", "Yellow"]
        }
    },
    "S24 FE" : {
        "color" : {
            "Blue" : ["Blue"],
            "Graphite" : ["Graphite"],
            "Gray" : ["Gray", "Grey"],
            "Mint" : ["Mint"],
            "Yellow" : ["Yellow"]
        }
    },
    "S25" : {
        "color" : {
            "Icy Blue" : ["Icy Blue", "Blue"],
            "Mint" : ["Mint"],
            "Navy" : ["Navy", "Dark Blue"],
            "Silver Shadow" : ["Silver Shadow", "Silver", "Gray"],
            "Pink Gold" : ["Pink Gold", "PinkGold"],
            "Coral Red" : ["Coral Red", "Red"],
            "Blue Black" : ["Blue Black", "BlueBlack"]
        },
    },
    "S25+" : {
        "color" : {
            "Icy Blue" : ["Icy Blue", "Blue"],
            "Mint" : ["Mint"],
            "Navy" : ["Navy", "Dark Blue"],
            "Silver Shadow" : ["Silver Shadow", "Silver", "Gray"],
            "Pink Gold" : ["Pink Gold", "PinkGold"],
            "Coral Red" : ["Coral Red", "Red"],
            "Blue Black" : ["Blue Black", "BlueBlack"]
        },
    },
    "S25 Ultra" : {
        "color" : {
            "Titanium Silver Blue" : ["Titanium Silver Blue", "Silver Blue", "SilverBlue", "Blue"],
            "Titanium Black" : ["Titanium Black", "Black"],
            "Titanium White Silver" : ["Titanium White Silver", "White Silver", "WhiteSilver", "White", "Silver"],
            "Titanium Gray" : ["Titanium Gray", "Gray"],
            "Titanium Jade Green" : ["Titanium Jade Green", "Green"],
            "Titanium Jet Black" : ["Titanium Jet Black", "Jet Black"],
            "Titanium Pink Gold" : ["Titanium Pink Gold", "PinkGold"]
        }
    },
    "S25 Edge" : {
        "color" : {
            "Onyx Black" : ["Onyx Black", "Black"],
            "Marble Gray" : ["Marble Gray", "Gray"],
            "Cobalt Violet" : ["Cobalt Violet", "Violet"],
            "Amber Yellow" : ["Amber Yellow", "Yellow"]
        },
    },
    "Z Fold 4" : {
        "color" : {
            "Phantom Black" : ["Phantom Black", "Black"],
            "Graygreen" : ["Graygreen", "Green"],
            "Beige" : ["Beige"],
            "Burgundy" : ["Burgundy", "Red"]
        },
    },
    "Z Flip 4" : {
        "color" : {
            "Bora Purple" : ["Bora Purple", "Purple"],
            "Graphite" : ["Graphite", "Gray", "Black"],
            "Pink Gold" : ["Pink Gold", "Pink"],
            "Blue" : ["Blue"],
            "Yellow" : ["Yellow"],
            "White" : ["White"],
            "Navy" : ["Navy", "Blue"],
            "Khaki" : ["Khaki", "Green"],
            "Red" : ["Red"]
        },
    },
    "Z Fold 5" : {
        "color" : {
            "Icy Blue" : ["Icy Blue"],
            "Phantom Black" : ["Phantom Black", "Black"],
            "Cream" : ["Cream", "Beige"],
            "Gray" : ["Gray", "Grey"],
            "Blue" : ["Blue"]
        },
    },
    "Z Flip 5" : {
        "color" : {
            "Mint" : ["Mint", "Green"],
            "Graphite" : ["Graphite"],
            "Cream" : ["Cream", "Beige"],
            "Lavender" : ["Lavender", "Purple"],
            "Gray" : ["Gray", "Grey"],
            "Blue" : ["Blue"],
            "Green" : ["Green"],
            "Yellow" : ["Yellow"]
        },
    },
    "Z Fold 6" : {
        "color" : {
            "Silver Shadow" : ["Silver Shadow", "Silver"],
            "Pink" : ["Pink"],
            "Navy" : ["Navy", "Blue"],
            "Crafted Black" : ["Crafted Black", "Black"],
            "White" : ["White"]
        },
    },
    "Z Flip 6" : {
        "color" : {
            "Yellow" : ["Yellow"],
            "Silver Shadow" : ["Silver Shadow", "Silver"],
            "Mint" : ["Mint", "Green"],
            "Blue" : ["Blue"],
            "Black" : ["Black"],
            "White" : ["White"],
            "Peach" : ["Peach", "Orange"]
        },
    },
}

IGNORING_SAMSUNG_GALAXY_RECOGNITION = ["Apple", "iPhone", "OnePlus", "Nothing Ear", "Redmi", "Xiaomi", "mi",
                                       "Poco", "ipad", "mac", "imac", "Pad", "Pixel", "Realme", "Honor",
                                       "Doogee", "CMF", "JBL"
                                       ]

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для XIAOMI 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

XIAOMI_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "Poco" : {
        "C40" : {
            "color" : {
                "Black" : ["Black"],
                "Green" : ["Green"],
                "Yellow" : ["Yellow"]
            }
        },
        "C50" : {
            "color" : {
                "Green" : ["Green"],
                "Blue" : ["Blue"]
            }
        },
        "C55" : {
            "color" : {
                "Blue" : ["Blue"],
                "Black" : ["Black"],
                "Green" : ["Green"],
                "White" : ["White"]
            }
        },
        "C65" : {
            "color" : {
                "Blue" : ["Blue"],
                "Black" : ["Black"],
                "Green" : ["Green"],
                "White" : ["White"]
            }
        },
        "C61" : {
            "color" : {
                "Blue" : ["Blue"],
                "Black" : ["Black"],
                "Green" : ["Green"],
                "White" : ["White"]
            }
        },
        "C75" : {
            "color" : {
                "Black" : ["Black"],
                "Green" : ["Green"],
                "Gold" : ["Gold"],
                "Gray" : ["Gray", "Grey"],
                "Blue" : ["Blue"],
                "Orange" : ["Orange"]
            }
        },
        "C75 5G" : {
            "color" : {
                "Black" : ["Black"],
                "Green" : ["Green"],
                "Gold" : ["Gold"],
                "Gray" : ["Gray", "Grey"],
                "Blue" : ["Blue"],
                "Orange" : ["Orange"]
            }
        },
        "M4 Pro": {
            "color": {
                "Black": ["Black"],
                "Blue": ["Blue"],
                "Yellow": ["Yellow"]
            }
        },
        "M4 Pro 5G": {
            "color": {
                "Black": ["Black"],
                "Blue": ["Blue"],
                "Yellow": ["Yellow"]
            }
        },
        "M5": {
            "color": {
                "Black": ["Black"],
                "Yellow": ["Yellow"],
                "Grey" : ["Grey"],
                "Green": ["Green"]
            }
        },
        "M5s": {
            "color": {
                "Grey" : ["Grey"],
                "White" : ["White"],
                "Blue": ["Blue"]
            }
        },
        "M6": {
            "color": {
                "Black": ["Black"],
                "Silver": ["Silver"],
                "Purple": ["Purple"]
            }
        },
        "M6 Pro 5G": {
            "color": {
                "Black": ["Black"],
                "Green": ["Green"],
                "Purple" : ["Purple"],
                "Blue" : ["blue"]
            }
        },
        "M7 Pro 5G": {
            "color": {
                "Lavender Frost": ["Lavender Frost", "Lavender", "Frost"],
                "Lunar Dust": ["Lunar Dust", "Dust"],
                "Olive Twilight": ["Olive Twilight", "Olive"]
            }
        },
        "X4 Pro 5G": {
            "color": {
                "Black": ["Black"],
                "Blue": ["Blue"],
                "Yellow": ["Yellow"]
            }
        },
        "X4 GT 5G": {
            "color": {
                "Silver": ["Silver"],
                "Black": ["Black"],
                "Blue": ["Blue"]
            }
        },
        "X5 5G": {
            "color": {
                "Green": ["Green"],
                "Blue": ["Blue"],
                "Black": ["Black"]
            }
        },
        "X5 Pro 5G": {
            "color": {
                "Blue": ["Blue"],
                "Black": ["Black"],
                "Yellow": ["Yellow"]
            }
        },
        "X6 5G": {
            "color": {
                "Gray": ["Gray", "Grey"],
                "Blue": ["Blue"],
                "Yellow": ["Yellow"],
                "Black" : ["Black"],
                "Silver" : ["Silver"]
            }
        },
        "X6 Pro 5G": {
            "color": {
                "Black": ["Black"],
                "Blue": ["Blue"],
                "Yellow": ["Yellow"],
                "Gray" : ["Gray", "Grey"],
                "Silver" : ["Silver"]
            }
        },
        "X7 Pro 5G" : {
            "color" : {
                "Black" : ["Black"],
                "Green" : ["Green"],
                "Yellow" : ["Yellow"],
                "Silver" : ["Silver"]
            }
        },
        "X7 5G": {
            "color": {
                "Black": ["Black"],
                "Green": ["Green"],
                "Yellow": ["Yellow"],
                "Silver" : ["Silver"]
            }
        },
        "F4 5G": {
            "color": {
                "Black": ["Black"],
                "Green": ["Green"],
                "Silver": ["Silver"]
            }
        },
        "F4 GT 5G": {
            "color": {
                "Black": ["Black"],
                "Silver": ["Silver"],
                "Yellow": ["Yellow"]
            }
        },
        "F5 5G": {
            "color": {
                "Black": ["Black"],
                "Silver": ["Silver"],
                "Blue": ["Blue"],
                "Gray" : ["Gray", "Grey"],
                "Green" : ["Green"],
                "White" : ["White"]
            }
        },
        "F5 Pro 5G": {
            "color": {
                "Black": ["Black"],
                "Silver": ["Silver"],
                "Blue": ["Blue"],
                "Gray" : ["Gray", "Grey"],
                "Green" : ["Green"],
                "White" : ["White"]
            }
        },
        "F6 5G": {
            "color": {
                "Gray": ["Gray", "Grey"],
                "Green": ["Green"],
                "Blue": ["Blue"],
                "Black" : ["Black"],
                "White" : ["White"],
                "Titanium" : ["Titanium"]
            }
        },
        "F6 Pro 5G": {
            "color": {
                "Black": ["Black"],
                "Silver": ["Silver"],
                "Blue": ["Blue"],
                "Gray" : ["Gray", "Grey"],
                "Green" : ["Green"],
                "White" : ["White"],
                "Titanium" : ["Titanium"]
            }
        },
        "F7 5G": {
            "color": {
                "Yellow": ["Yellow"],
                "Black" : ["Black"],
                "Silver" : ["Silver"],
                "Blue" : ["Blue"],
                "Gray" : ["Gray", "Grey"],
                "Green" : ["Green"],
                "White" : ["White"],
                "Titanium" : ["Titanium"]
            }
        },
        "F7 Pro 5G": {
            "color": {
                "Orange": ["Orange"],
                "Black" : ["Black"],
                "Silver" : ["Silver"],
                "Blue" : ["Blue"],
                "Gray" : ["Gray", "Grey"],
                "Green" : ["Green"],
                "White" : ["White"],
                "Titanium" : ["Titanium"]
            }
        }
    },
    "Redmi" :{
        "A1 4G" : {
            "color" : {
                "Green" : ["Light Green", "Green"],
                "Blue" : ["Light Blue", "Blue"],
                "Black" : ["Black"]
            }
        },
        "12 4G" : {
            "color" : {
                "Black" : ["Midnight Black", "Black"],
                "Blue" : ["Sky Blue", "Blue"],
                "Silver" : ["Polar Silver", "Silver"]
            }
        },
        "12 5G" : {
            "color" : {
                "Black" : ["Midnight Black", "Black"],
                "Blue" : ["Sky Blue", "Blue"],
                "Silver" : ["Polar Silver", "Silver"]
            }
        },
        "12C 4G": {
            "color": {
                "Gray": ["Graphite Gray", "Gray", "Grey"],
                "Blue": ["Ocean Blue", "Blue"],
                "Green": ["Mint Green", "Green"],
                "Purple": ["Lavender Purple", "Purple"]
                }
            },
        "Note 12 4G" : {
            "color" : {
                "Gray" : ["Onyx Gray", "Gray", "Grey"],
                "Blue" : ["Ice Blue", "Blue"],
                "Green" : ["Mint Green", "Green", "Mint"]
            }
        },
        "Note 12 5G" : {
            "color" : {
                "Gray" : ["Onyx Gray", "Gray", "Grey"],
                "Blue" : ["Ice Blue", "Blue"],
                "Green" : ["Mint Green", "Green", "Mint"]
            }
        },
        "Note 12 Pro 5G" : {
            "color" : {
                "Gray" : ["Graphite Gray", "Gray", "Grey","Graphite"],
                "White" : ["Polar White", "White"],
                "Blue" : ["Sky Blue", "Blue"]
            }
        },
        "Note 12 Pro+ 5G" : {
            "color" : {
                "Black" : ["Midnight Black", "Black", "Midnight"],
                "White" : ["White"],
                "Blue" : ["Sky Blue", "Blue"]
            }
        },
        "A2 4G" : {
            "color" : {
                "Blue" : ["Light Blue", "Blue"],
                "Green" : ["Light Green", "Green"],
                "Black" : ["Black"]
            }
        },
        "A2+ 4G" : {
            "color" : {
                "Blue" : ["Light Blue", "Blue"],
                "Green" : ["Light Green", "Green"],
                "Black" : ["Black"]
            }
        },
        "Note 12 Turbo 5G" : {
            "color" : {
                "Black" : ["Black"],
                "Blue" : ["Blue"],
                "White" : ["White"]
            }
        },
        "13 4G": {
            "color": {
                "Black": ["Midnight Black", "Black"],
                "Green": ["Mint Green", "Green"],
                "Blue": ["Ice Blue", "Blue"],
                "Ocean": ["Ocean Sunset"],
                "Gold" : ["Sandy Gold", "Gold"]
            },
        },
        "13 5G" : {
            "color" : {
                "Black" : ["Midnight Black", "Black"],
                "Green" : ["Mint Green", "Green"],
                "Blue" : ["Ice Blue", "Blue"],
                "Ocean" : ["Ocean Sunset"],
                "Gold" : ["Sandy Gold", "Gold"]
            },
        },
        "13C 4G" : {
            "color" : {
                "Gray" : ["Graphite Gray", "Graphite", "Gray", "Grey"],
                "Blue" : ["Ocean Blue", "Blue"],
                "Green" : ["Mint Green", "Green"]
            }
        },
        "Note 13 4G" : {
            "color" : {
                "Black" : ["Midnight Black", "Midnight", "Black"],
                "Green" : ["Mint Green", "Green"],
                "Blue" : ["Ice Blue", "Blue"],
                "Ocean Sunset" : ["Ocean Sunset", "Ocean", "Sunset"]
            }
        },
        "Note 13 5G" : {
            "color" : {
                "Black" : ["Midnight Black", "Midnight", "Black"],
                "Green" : ["Mint Green", "Green"],
                "Blue" : ["Ice Blue", "Blue"],
                "Ocean Sunset" : ["Ocean Sunset", "Ocean", "Sunset"]
            }
        },
        "Note 13 Pro 4G": {
            "color": {
                "Black": ["Midnight Black", "Black"],
                "Green": ["Forest Green", "Green"],
                "Purple": ["Lavender Purple", "Purple"],
                "Ocean" : ["Ocean Teal", "O.Teal", "Teal"],
                "Arctic" : ["Arctic White", "White"]
            }
        },
        "Note 13 Pro 5G" : {
            "color" : {
                "Black" : ["Midnight Black", "Black"],
                "Green" : ["Forest Green", "Green"],
                "Purple" : ["Lavender Purple", "Purple"],
                "Ocean" : ["Ocean Teal", "O.Teal", "Teal"],
                "Arctic" : ["Arctic White", "White"]
            }
        },
        "Note 13 Pro+ 5G" : {
            "color" : {
                "Black" : ["Midnight Black", "Midnight", "Black"],
                "Moonlight" : ["Moonlight"],
                "Purple" : ["Aurora Purple", "Purple"],
                "White" : ["White"]
            }
        },
        "A3 4G" : {
            "color" : {
                "Black" : ["Midnight Black", "Black", "Midnight"],
                "Green" : ["Forest Green", "Forest", "Green"],
                "Blue" : ["Lake Blue", "Lake", "Blue"]
            }
        },
        "14C 4G": {
        "color": {
            "Black": ["Midnight Black", "Black"],
            "Purple": ["Dreamy Purple", "Purple"],
            "Green": ["Sage Green", "Green"],
            "Blue": ["Starry Blue", "Blue"]
        }
    },
        "Note 14 4G" : {
            "color" : {
                "Purple": ["Mist Purple", "Purple"],
                "Green": ["Lime Green", "Green"],
                "Black": ["Midnight Black", "Black"],
                "Blue": ["Ocean Blue", "Blue", "Ocean"]
            }
        },
        "Note 14 5G" : {
            "color" : {
                "Purple" : ["Mist Purple", "Purple"],
                "Green" : ["Lime Green", "Green"],
                "Black" : ["Midnight Black", "Black"],
                "Blue" : ["Ocean Blue", "Blue", "Ocean"]
            }
        },
        "Note 14 Pro 4G" : {
            "color" : {
                "Green" : ["Coral Green", "Green"],
                "Purple" : ["Twilight Purple", "Purple"],
                "White" : ["Mirror Porcelain White", "White"],
                "Black" : ["Midnight Black", "Black", "Midnight"],
                "Blue": ["Blue", "Ocean"]
            }
        },
        "Note 14 Pro 5G" : {
            "color" : {
                "Green" : ["Coral Green", "Green"],
                "Purple" : ["Twilight Purple", "Purple"],
                "White" : ["Mirror Porcelain White", "White"],
                "Black" : ["Midnight Black", "Black", "Midnight"],
                "Blue" : ["Blue"]
            }
        },
        "Note 14 Pro+ 5G" : {
            "color" : {
                "Green" : ["Dark Green", "Green"],
                "White" : ["Mirror Porcelain White", "White"],
                "Black" : ["Midnight Black", "Black"],
                "Blue" : ["Blue"],
                "Purple": ["Lavender", "Purple"]
            }
        },
        "K80 5G" : {
            "color" : {
                "Black" : ["Black"],
                "White" : ["White"],
                "Mint" : ["Mint"],
                "Lamborghini Green" : ["Lamborghini Green", "Green"],
                "Lamborghini Black" : ["Lamborghini Black", ]
            }
        },
        "K80 Pro 5G" : {
            "color" : {
                "Black" : ["Black"],
                "White" : ["White"],
                "Mint" : ["Mint"],
                "Lamborghini Green" : ["Lamborghini Green", "Green"],
                "Lamborghini Black" : ["Lamborghini Black"]
            }
        },
    },
    "Xiaomi" : {
        "12 Lite": {
            "color": {
                "Black": ["Black"],
                "Green": ["Lite Green", "Green"],
                "Pink": ["Lite Pink", "Pink"]
            },
        },
        "12" : {
            "color" : {
                "Black" : ["Black"],
                "Blue" : ["Blue"],
                "Purple" : ["Purple"]
            }
        },
        "12T": {
            "color": {
                "Black": ["Black"],
                "Silver": ["Silver"],
                "Blue": ["Blue"]
            },
        },
        "12T Pro" : {
            "color" : {
                "Black" : ["Black"],
                "Silver" : ["Silver"],
                "Blue" : ["Blue"]
            },
        },
        "12 Pro" : {
            "color" : {
                "Gray" : ["Gray", "Grey"],
                "Blue" : ["Blue"],
                "Purple" : ["Purple"]
            },
        },
        "12S" : {
            "color" : {
                "Black" : ["Black"],
                "White" : ["White"],
                "Purple" : ["Purple"],
                "Green" : ["Green"]
            }
        },
        "12S Pro" : {
            "color" : {
                "Black" : ["Black"],
                "White" : ["White"],
                "Purple" : ["Purple"],
                "Green" : ["Green"]
            },
        },
        "12S Ultra" : {
            "color" : {
                "Classic Black" : ["Classic Black", "Black"],
                "Green" : ["Green"]
            },
        },
        "13" : {
            "color" : {
                "Black" : ["Black"],
                "White" : ["White"],
                "Flora Green" : ["Flora Green", "Flora", "Green"],
                "Mountain Blue" : ["Mountain Blue", "Mountain", "Blue"]
            },
        },
        "13 Pro" : {
            "color" : {
                "Ceramic White" : ["Ceramic White", "White"],
                "Ceramic Black" : ["Ceramic Black", "Black"],
                "Flora Green" : ["Flora Green", "Green"],
                "Mountain Blue" : ["Mountain Blue", "Blue"]
            }
        },
        "MIX Fold 2" : {
            "color" : {
                "Black" : ["Black"],
                "Gold" : ["Gold"]
            },
        },
        "13 Lite" : {
            "color" : {
                "Black" : ["Black"],
                "Blue" : ["Blue"],
                "Pink" : ["Pink"]
            }
        },
        "Civi 3" : {
            "color" : {
                "Rose Purple" : ["Rose Purple", "Rose"],
                "Mint Green" : ["Mint Green", "Green"],
                "Adventure Gold" : ["Adventure Gold", "Gold"],
                "Coconut Grey" : ["Coconut Grey", "Grey"]
            }
        },
        "13T" : {
            "color" : {
                "Meadow Green" : ["Meadow Green", "Green"],
                "Black" : ["Black"],
                "Alpine Blue" : ["Alpine Blue", "Blue"]
            }
        },
        "13T Pro" : {
            "color" : {
                "Meadow Green" : ["Meadow Green", "Green"],
                "Black" : ["Black"],
                "Alpine Blue" : ["Alpine Blue", "Blue"]
            }
        },
        "13 Ultra" : {
            "color" : {
                "Black" : ["Black"],
                "White" : ["White"],
                "Olive Green" : ["Olive Green", "Green"]
            }
        },
        "14" : {
            "color" : {
                "Black" : ["Black"],
                "White" : ["White"],
                "Flora Green" : ["Flora Green", "Green"],
                "Mountain Blue" : ["Mountain Blue", "Blue"]
            }
        },
        "14 Pro" : {
            "color" : {
                "Ceramic White" : ["Ceramic White", "White"],
                "Ceramic Black" : ["Ceramic Black", "Black"],
                "Flora Green" : ["Flora Green", "Green"],
                "Mountain Blue" : ["Mountain Blue", "Blue"]
            }
        },
        "MIX Fold 3" : {
            "color" : {
                "Black" : ["Black"],
                "Gold" : ["Gold"]
            }
        },
        "14 Civi": {
            "color": {
                "Shadow Black": ["Shadow Black", "Black"],
                "Matcha Green": ["Matcha Green", "Green"],
                "Cruise Blue": ["Cruise Blue", "Blue"]
            }
        },
        "Civi 4 Pro": {
            "color": {
                "Black": ["Black"],
                "Blue": ["Blue"],
                "Green": ["Green"],
                "Pink": ["Pink"]
            }
        },
        "14T" : {
            "color" : {
                "Titan Black" : ["Titan Black", "Black"],
                "Titan Gray" : ["Titan Gray", "Gray", "Grey"],
                "Titan Blue" : ["Titan Blue", "Blue"],
                "Lemon Green" : ["Lemon Green", "Green"]
            }
        },
        "14T Pro" : {
            "color" : {
                "Titan Black" : ["Titan Black", "Black"],
                "Titan Gray" : ["Titan Gray", "Gray", "Grey"],
                "Titan Blue" : ["Titan Blue", "Blue"]
            }
        },
        "14 Ultra": {
            "color": {
                "Black": ["Black"],
                "White": ["White"],
                "Dragon Crystal Blue": ["Dragon Crystal Blue", "Blue", "Crystal"],
                "Titanium Special Edition": ["Titanium Special Edition", "Titanium", "Special"]
            }
        },
        "15": {
            "color": {
                "Black": ["Black"],
                "White": ["White"],
                "Purple": ["Purple"],
                "Green": ["Green"]
            }
        },
        "15 Pro": {
            "color": {
                "Bright Silver Edition": ["Bright Silver Edition", "Silver"],
                "Rock Ash": ["Rock Ash", "Rock"],
                "Spruce Green": ["Spruce Green", "Green"],
                "White": ["White"],
                "Black": ["Black"],
                "Gentian Blue": ["Gentian Blue", "Blue"]
            }
        },
        "MIX Fold 4": {
            "color": {
                "Black": ["Black"],
                "White": ["White"],
                "Blue": ["Blue"]
            }
        },
        "15 Ultra": {
            "color": {
                "Silver Chrome" : ["Silver Chrome", "Silver"],
                "Black": ["Black"],
                "White": ["White"],
                "Green ": ["Green "]
            }
        },
    },
    "Xiaomi Watch" : {
        "Xiaomi Redmi Watch 4" : {
            "color" : {
                "Obsidian Black" : ["Obsidian Black", "Black"],
                "Silver Gray" : ["Silver Gray", "Silver", "Gray"],
            }
        },
        "Xiaomi Redmi Watch 5": {
        "color": {
            "Obsidian Black" : ["Obsidian Black", "Black"],
            "Silver Gray" : ["Silver Gray", "Silver", "Gray"],
            "Lavender Purple": ["Lavender Purple", "Purple", "Lavender"]
        }
    },
        "Xiaomi Redmi Watch 5 Active": {
            "color": {
                "Midnight Black": ["Midnight Black", "Black", "Midnight"],
                "Matte Silver": ["Matte Silver", "Silver"]
            }
        },
        "Xiaomi Redmi Watch 5 Lite": {
            "color": {
                "Black": ["Black"],
                "Light Gold": ["Light Gold", "Gold"]
            }
        },
        "Xiaomi Smart Band 9": {
            "color": {
                "Midnight Black": ["Midnight Black", "Black", "Midnight"],
                "Glacier Silver": ["Glacier Silver", "Glacier", "Silver"],
                "Mystic Rose": ["Mystic Rose", "Mystic", "Rose"],
                "Arctic Blue": ["Arctic Blue", "Arctic", "Blue"],
                "Titan Gray": ["Titan Gray", "Gray"]
            }
        },
        "Xiaomi Smart Band 9 Pro": {
            "color": {
                "Obsidian Black": ["Obsidian Black", "Black"],
                "Rose Gold": ["Rose Gold", "Gold", "Rose"],
                "Moonlight Silver": ["Moonlight Silver", "Moonlight", "Silver"]
            }
        },
        "Xiaomi Smart Band 9 Active": {
            "color": {
                "Black": ["Black"],
                "Beige White": ["Beige White", "Beige", "White"],
                "Pink": ["Pink"]
            }
        },
        "Xiaomi Watch 2": {
            "color": {
                "Black": ["Black"],
                "Grey": ["Grey"],
                "Titan Gray": ["Titan Gray", "Gray"],
                "Silver": ["Silver"],
            }
        },
        "Xiaomi Watch 2 Pro": {
            "color": {
                "Black": ["Black"],
                "Grey": ["Grey"],
                "Titan Gray": ["Titan Gray", "Gray"],
                "Silver": ["Silver"],
            }
        },
        "Xiaomi Watch S2": {
            "color": {
                "Black": ["Black"],
                "Light Gold": ["Light Gold", "Gold"],
                "Silver": ["Silver"],
                "Grey" : ["Grey"],
                "Titan Gray" : ["Titan Gray", "Gray"],
            }
        },
        "Xiaomi Watch 3" : {
            "color" : {
                "Black" : ["Black"],
                "Grey" : ["Grey"],
                "Titan Gray" : ["Titan Gray", "Gray"]
            }
        },
        "Xiaomi Watch 3 Pro" : {
            "color" : {
                "Silver" : ["Silver"],
                "Black" : ["Black"]
            }
        },
        "Xiaomi Watch S3": {
            "color": {
                "Black": ["Black"],
                "Silver": ["Silver"],
                "Chrome Yellow": ["Chrome Yellow", "Yellow"],
                "Rainbow": ["Rainbow"]
            }
        }



    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_XIAOMI = {
    "Xiaomi" : ["Pro+", "Note", "Redmi", "poco", "Realme", "Honor",  "Doogee", "CMF", "iPhone",
                "Redmi PAD", "pad", "Watch", "band", "Galaxy", "samsung", "OnePlus", "Pixel"],
    "Redmi" : ["Xiaomi", "Mi", "poco", "Realme", "Honor",  "Doogee", "CMF", "iPhone",
               "Redmi PAD", "pad", "Watch", "Galaxy", "samsung", "OnePlus", "Pixel", "Realme"
               ],
    "Poco" : ["Pro+", "Note", "Redmi", "Xiaomi", "Mi", "Redmi PAD", "Redmi PAD", "Watch", "band", "Realme", "iphone",
              "MIX Fold 4", "Galaxy", "samsung", "OnePlus", "Pixel", "Honor",  "Doogee", "CMF", "iPhone",
              ],
    "Xiaomi Pad" : ["Pro+", "Note", "Redmi", "poco", "Realme", "Honor",  "Doogee", "CMF", "iPhone",
                "Redmi PAD", "Watch", "band", "Galaxy", "samsung", "OnePlus", "Pixel"],
    "Redmi Pad" : ["Xiaomi", "Mi", "poco", "Realme", "Honor",  "Doogee", "CMF", "iPhone",
               "Xiaomi PAD", "Watch", "band", "Galaxy", "samsung", "OnePlus", "Pixel"],
    "Poco Pad" : ["Xiaomi", "Mi", "Redmi", "Realme", "Honor",  "Doogee", "CMF", "iPhone",
               "Xiaomi PAD", "Watch", "band", "Galaxy", "samsung", "OnePlus", "Pixel"]
}

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для Oneplus 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
ONEPLUS_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "OnePlus" : {
        "OnePlus 12": {
            "color": {
                "Silky Black": ["Black"],
                "Flowy Emerald": ["Green", "Flowy", "Emerald"],
                "Glacial White": ["White"]
    }
},
        "OnePlus 13R": {
            "color": {
                "Nebula Noir": ["Black", "Noir", "Nebula"],
                "Astral Trail": ["Blue", "Astral", "Trail"]
    }
},
        "OnePlus 13": {
            "color": {
                "Midnight Ocean": ["Blue", "Midnight", "Ocean"],
                "Arctic Dawn": ["White", "Arctic", "Dawn"],
                "Black Eclipse": ["Black"]
            }
        },
        "OnePlus Nord 4": {
            "color": {
                "Mercurial Silver": ["Silver"],
                "Oasis Green": ["Green"],
                "Obsidian Midnight": ["Black", "Midnight"]
            }
        },
    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_ONEPLUS = {
    "OnePlus" : ["Pro+", "Note", "Redmi", "Apple", "ipad", "xiaomi", "Realme", "Honor",  "Doogee", "CMF", "iphone",
                "Redmi PAD", "pad", "Watch", "band", "Galaxy", "samsung", "Buds", "Ear"],
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для Oneplus buds 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
ONEPLUS_BUDS_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "Наушники OnePlus Buds" : {
        "OnePlus Buds 3": {
            "color": {
                "Metallic Gray": ["Gray"],
                "Metallic Black" : ["Black"],
                "Splendid Blue": ["Blue"],
                "Khaki Green": ["Green"]
    }
},
        "OnePlus Buds Pro 2": {
            "color": {
                "Obsidian Black": ["Black"],
                "Arbor Green": ["Green"],
                "White": ["White"]
            }
        },
        "OnePlus Buds Pro 3": {
            "color": {
                "Midnight Opus": ["Black", "Midnight"],
                "Lunar Radiance": ["White", "Lunar", "Radiance"],
                "Sapphire Blue": ["Blue"]
            }
        },
        "OnePlus Nord Buds 2": {
            "color": {
                "Thunder Gray": ["Gray"],
                "Lightning White": ["White"]
            }
        },
        "OnePlus Nord Buds 3 Pro": {
            "color": {
                "Soft Jade": ["Green"],
                "Starry Black": ["Black"]
            }
        }


    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_ONEPLUS_BUDS = {
    "Наушники OnePlus Buds" : ["Note", "Redmi", "Apple", "ipad", "xiaomi", "Nothing Ear", "Realme",  "Doogee", "CMF",
                 "Redmi PAD", "pad", "Watch", "band", "Galaxy", "samsung", "JBL"],
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для Google 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
GOOGLE_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "Pixel" : {
        "Pixel 7" : {
            "color" : {
                "Obsidian" : ["Obsidian"],
                "Snow" : ["Snow"],
                "Lemongrass" : ["Lemongrass"]
            }
        },
        "Pixel 7 Pro": {
            "color": {
                "Obsidian": ["Obsidian"],
                "Snow": ["Snow"],
                "Hazel": ["Hazel"]
            }
        },
        "Pixel 8": {
            "color": {
                "Obsidian": ["Obsidian"],
                "Hazel": ["Hazel"],
                "Rose": ["Rose"],
                "Mint": ["Mint"]
            }
        },
        "Pixel 8a": {
            "color": {
                "Obsidian": ["Obsidian"],
                "Porcelain": ["Porcelain"],
                "Bay": ["Bay"],
                "Aloe": ["Aloe"]
            }
        },
        "Pixel 8 Pro": {
            "color": {
                "Obsidian": ["Obsidian"],
                "Porcelain": ["Porcelain"],
                "Bay": ["Bay"],
                "Mint": ["Mint"]
            }
        },
        "Pixel 9": {
            "color": {
                "Peony": ["Peony"],
                "Wintergreen": ["Wintergreen"],
                "Porcelain": ["Porcelain"],
                "Obsidian": ["Obsidian"]
            }
        },
        "Pixel 9 Pro XL": {
            "color": {
                "Obsidian": ["Obsidian"],
                "Porcelain": ["Porcelain"],
                "Hazel": ["Hazel"],
                "Rose Quartz": ["Rose Quartz", "Rose"]
            }
        },
        "Pixel Fold": {
            "color": {
                "Obsidian": ["Obsidian"],
                "Porcelain": ["Porcelain"]
            }
        }

    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_GOOGLE = {
    "Pixel" : ["Pro+", "Note", "Redmi", "Apple", "ipad", "xiaomi", "Realme", "Honor",  "Doogee", "CMF", "iphone",
                "Redmi PAD", "pad", "Watch", "band", "Galaxy", "samsung", "Buds", "Ear"],
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для Realme 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
REALME_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "Realme" : {
        "Realme 12 5G": {
            "color": {
                "Twilight Purple": ["Twilight Purple", "Purple"],
                "Woodland Green": ["Woodland Green", "Green"]
    }
},
        "Realme 12 Pro 5G": {
            "color": {
                "Submarine Blue": ["Submarine Blue", "Blue"],
                "Navigator Beige": ["Navigator Beige", "Beige"]
            }
        },
        "Realme 12 Pro+ 5G": {
            "color": {
                "Submarine Blue": ["Submarine Blue", "Blue"],
                "Navigator Beige": ["Navigator Beige", "Beige"],
                "Explorer Red": ["Explorer Red", "Red"]
            }
        },
        "Realme 13 5G": {
            "color": {
                "Victory Gold": ["Victory Gold", "Gold"],
                "Speed Green": ["Speed Green", "Green"],
                "Dark Purple": ["Dark Purple", "Purple"]
            }
        },
        "Realme 13+ 5G": {
            "color": {
                "Victory Gold": ["Victory Gold", "Gold"],
                "Speed Green": ["Speed Green", "Green"],
                "Dark Purple": ["Dark Purple", "Purple"]
            }
        },
        "Realme 13 Pro 5G": {
            "color": {
                "Monet Gold": ["Monet Gold", "Gold"],
                "Ocean Blue": ["Ocean Blue", "Blue", "Ocean"],
                "Emerald Green" : ["Emerald Green", "Green"],
            }
        },
        "Realme 13 Pro+ 5G": {
            "color": {
                "Emerald Green": ["Emerald Green", "Green"],
                "Monet Gold": ["Monet Gold", "Gold"],
                "Ocean Blue" : ["Ocean Blue", "Blue", "Ocean"],
            }
        },
        "Realme GT 6T": {
            "color": {
                "Black": ["Black"],
                "Fluid Silver": ["Silver"],
                "Razor Green": ["Green"]
            }
        },
        "Realme GT 6" : {
            "color" : {
                "Black" : ["Black"],
                "Fluid Silver": ["Silver"],
                "Razor Green": ["Green"]
            }
        },



    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_REALME = {
    "Pixel" : ["Pro+", "Note", "Redmi", "Apple", "ipad", "xiaomi", "Pixel", "Honor",  "Doogee", "CMF", "iphone",
                "Redmi PAD", "pad", "Watch", "band", "Galaxy", "samsung", "Buds", "Ear", "JBL"],
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#📱Специальные правила для HONOR 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
HONOR_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "Honor" : {
        "Honor 200" : {
            "color" : {
                "Moonlight White" : ["Moonlight White", "White"],
                "Emerald Green" : ["Emerald Green", "Green"],
                "Velvet Black" : ["Velvet Black", "Black"]
            }
        },
        "Honor 200 Lite": {
            "color": {
                "Ocean Blue": ["Ocean Blue", "Ocean"],
                "Starry Blue": ["Starry Blue", "Blue"],
                "Midnight Black": ["Midnight Black", "Midnight", "Black"]
    }
},
        "Honor Magic V3": {
            "color": {
                "Green": ["Green"],
                "Reddish Brown": ["Reddish Brown", "Brown"],
                "Black": ["Black"]
            }
        },
        "Honor Magic 6 Pro": {
            "color": {
                "Sage Green": ["Sage Green", "Green"],
                "Graphite Black": ["Graphite Black", "Black", "Graphite"]
            }
        },
        "Honor X9c": {
            "color": {
                "Midnight Black": ["Midnight Black", "Black"],
                "Emerald Green": ["Emerald Green", "Green"],
                "Diamond Silver": ["Diamond Silver", "Silver"],
                "Ocean Blue" : ["Ocean Blue", "Blue"],
                "Titanium Silver" : ["Titanium Silver", "Silver"]
            }
        },
        "Honor X8c": {
            "color": {
                "Midnight Black": ["Midnight Black", "Black"],
                "Emerald Green": ["Emerald Green", "Green"],
                "Diamond Silver": ["Diamond Silver", "Silver"],
                "Ocean Blue" : ["Ocean Blue", "Blue"],
                "Titanium Silver" : ["Titanium Silver", "Silver"]
            }
        },
        "Honor X7b": {
            "color": {
                "Midnight Black": ["Midnight Black", "Black"],
                "Emerald Green": ["Emerald Green", "Green"],
                "Diamond Silver": ["Diamond Silver", "Silver"],
                "Ocean Blue" : ["Ocean Blue", "Blue"],
                "Titanium Silver" : ["Titanium Silver", "Silver"]
            }
        },
        "Honor X6a": {
            "color": {
                "Midnight Black": ["Midnight Black", "Black"],
                "Emerald Green": ["Emerald Green", "Green"],
                "Diamond Silver": ["Diamond Silver", "Silver"],
                "Ocean Blue" : ["Ocean Blue", "Blue"],
                "Titanium Silver" : ["Titanium Silver", "Silver"]
            }
        },
        "Honor Magic 7 Pro": {
            "color": {
                "Lunar Shadow Grey": ["Lunar Shadow Grey", "Grey"],
                "Black": ["Black"]
            }
        },
        "Honor Magic 7 Lite": {
            "color": {
                "Titanium Purple": ["Titanium Purple", "Purple"],
                "Titanium Black": ["Titanium Black", "Black"]
            }
        },
        "Honor X7c": {
            "color": {
                "Midnight Black": ["Midnight Black", "Black"],
                "Forest Green": ["Forest Green", "Green"],
                "Moonlight White": ["Moonlight White", "White"]
            }
        },
        "Honor X6b": {
            "color": {
                "Forest Green": ["Forest Green", "Green"],
                "Starry Purple": ["Starry Purple", "Purple"],
                "Ocean Cyan": ["Ocean Cyan", "Ocean"],
                "Midnight Black": ["Midnight Black", "Midnight", "Black"]
            }
        },
    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_HONOR = {
    "Pixel" : ["Pro+", "Note", "Redmi", "Apple", "ipad", "xiaomi", "Pixel", "Realme", "iphone",
                "Redmi PAD", "pad", "Watch", "band", "Galaxy", "samsung", "Buds", "Ear"],
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для DOOGEE 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
DOOGEE_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "Doogee" : {
        "Doogee V Max Plus" : {
            "color" : {
                "Black" : ["Black"],
                "Grey" : ["Gray", "Grey"],
                "Blue" : ["Blue"]
            }
        },
        "Doogee V40 Pro" : {
            "color" : {
                "Black" : ["Black"],
                "Grey" : ["Gray", "Grey"],
                "Blue" : ["Blue"]
            }
        },
        "Doogee S200" : {
            "color" : {
                "Black" : ["Black"],
                "Grey" : ["Gray", "Grey"],
                "Blue" : ["Blue"]
            }
        },
        "Doogee Smini" : {
            "color" : {
                "Black" : ["Black"],
                "Grey" : ["Gray", "Grey"],
                "Blue" : ["Blue"]
            }
        },
        "Doogee R10" : {
            "color" : {
                "Black" : ["Black"],
                "Grey" : ["Gray", "Grey"],
                "Blue" : ["Blue"]
            }
        },
    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_DOOGEE = {
    "Pixel" : ["Pro+", "Note", "Redmi", "Apple", "ipad", "xiaomi", "Pixel", "Realme", "honor", "iphone",
                "Redmi PAD", "pad", "Watch", "band", "Galaxy", "samsung", "Buds", "Ear"],
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для Infinix 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
INFINIX_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "Infinix" : {
        "Infinix Hot 50 Pro" : {
            "color" : {
                "Sleek Black" : ["Black"],
                "Titanium Grey" : ["Grey", "Gray"],
                "Glacier Blue" : ["Blue"],
                "Aurora Green" : ["Green"],
                "Rising Red" : ["Red"],
                "Blossom Pink" : ["Pink"],
                "Dreamy Purple" : ["Purple"],
            }
        },
        "Infinix Hot 50 Pro+" : {
            "color" : {
                "Sleek Black" : ["Black"],
                "Titanium Grey" : ["Grey", "Gray"],
                "Glacier Blue" : ["Blue"],
                "Aurora Green" : ["Green"],
                "Rising Red" : ["Red"],
                "Blossom Pink" : ["Pink"],
                "Dreamy Purple" : ["Purple"],
            }
        },
        "Infinix Note 50 Pro+ 5G" : {
            "color" : {
                "Obsidian Black" : ["Black"],
                "Blossom Pink" : ["Pink"],
                "Vintage Green" : ["Green"]
            }
        },
        "Infinix GT 20 Pro" : {
            "color" : {
                "Metallic Black" : ["Black"],
                "Neo Titanium" : ["Grey", "Neo"],
                "Mint Green" : ["Green"],
                "Sandstone Gold" : ["Gold"]
            }
        },
        "Infinix Smart 9" : {
            "color" : {
                "Metallic Black" : ["Black"],
                "Neo Titanium" : ["Grey", "Neo"],
                "Mint Green" : ["Green"],
                "Sandstone Gold" : ["Gold"]
            }
        }
    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_INFINIX = {
    "Infinix" : ["Note", "Redmi", "Apple", "ipad", "xiaomi", "Pixel", "Realme", "honor", "iphone", "Doogee",
                "Redmi PAD", "pad", "Watch", "band", "Galaxy", "samsung", "Buds", "Ear"],
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для Tecno Mobile 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

TECNO_MOBILE_PATTERN_COLOR = {
    #Если определенный атрибут model из списка парсим цвет от сюда
    "Tecno Mobile" : {
        "Tecno Spark Go" : {
            "color" : {
                "Black" : ["Black"],
                "Green" : ["Green"],
                "Yellow" : ["Yellow"]
            }
        },
    },
}

#Игнорирование определенных слов
IGNORING_MODEL_FOR_TECNO_MOBILE = {
    "Tecno Mobile": [
    "Pro+",
    "Note",
    "Redmi",
    "poco",
    "Realme",
    "Honor",
    "Doogee",
    "CMF",
    "iPhone",
    "Redmi PAD",
    "pad",
    "Watch",
    "band",
    "Galaxy",
    "samsung",
    "OnePlus",
    "Pixel",
    "Xiaomi",
    "Mi",
    "iphone",
    "MIX Fold 4",
    "Xiaomi PAD"
  ]
}

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#📱Специальные правила для Беспроводные пылесосы Dyson 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#"Пылесосы Dyson"
COMPLETE_FOR_VERSION = {
    #парсим атрибут "complete" для конкретного "version" относительно для "Беспроводные пылесосы Dyson"
    "V8" : {
        "Absolute" : ["Absolute"],
        "Animal" : ["Animal"],
        "Animal+" : ["Animal+", "Animal +", "Animal plus"],
        "Motorhead" : ["Motorhead"],
    },
    "V10" : {
        "Absolute" : ["Absolute"],
        "Animal" : ["Animal"],
        "Motorhead" : ["Motorhead"],
    },
    "V11" : {
        "Absolute" : ["Absolute"],
        "Advanced" : ["Advanced"],
        "Animal" : ["Animal"],
        "Torque Drive" : ["Torque Drive", "Torque", "Drive"],
        "Outsize" : ["Outsize"]
    },
    "V12" : {
        "Detect Slim Absolute" : ["Detect Slim Absolute", "Slim Absolute detected", "Slim Absolute", "Absolute detected", "Absolute"],
        "Detect Slim" : ["Detect Slim"],
    },
    "V15" : {
        "Detect" : ["DetectDetect"],
        "Detect Absolute" : ["Detect Absolute", "Absolute"],
        "Detect Complete" : ["Detect Complete", "Complete"],
        "Detect Total Clean" : ["Detect Total Clean", "Total", "Clean"],
    },
    "Gen5" : {
        "Detect Absolute" : ["Detect Absolute", "Detect"],
        "Outsize Absolute:" : ["outsize Absolute:", "Outsize"]
    },
}

STANDARD_COMPLETE_FOR_VERSION = {
    #припысываем стандартный атрибут "complete" для конкретной "version" если не указано другое
    #для "Беспроводные пылесосы Dyson"
    "V8" : "Absolute",
    "V10" : "Absolute",
    "V11" : "Absolute",
    "V12" : "Detect Slim Absolute",
    "V15" : "Detect",
    "Gen5" : "Detect Absolute",
}

COLOR_FOR_VERSION_COMPLETE = {
    #парсим атрибут "color" для конкретного "version" относительно его "complete" для "Беспроводные пылесосы Dyson"
    "V8" : {
        "Absolute" : {
            "Silver/Nickel" : ["Silver/Nickel", "Silver"],
            "Yellow/Nickel" : ["Yellow/Nickel", "Yellow"]
        },
        "Animal" : {
            "Iron/Purple" : ["Iron/Purple", "Iron"],
            "Silver/Purple" : ["Silver/Purple", "Silver"],
            "Titanium" : ["Titanium", "Titanium"],
        },
        "Animal+" : {
            "Iron/Sprayed Nickel/Purple" : ["Iron/Sprayed Nickel/Purple", "Iron", "Nickel", "Purple", "Sprayed"],
        },
        "Motorhead" : {
            "Silver/Nickel" : ["Silver/Nickel", "Silver"],
            "Yellow/Nickel" : ["Yellow/Nickel", "Yellow"]
        },
    },
    "V10" : {
        "Absolute" : {
            "Nickel/Copper:" : ["Nickel/Copper:", "Copper", "Медный"],
            "Black/Nickel" : ["Black/Nickel", "Black"],
            "Iron/Nickel" : ["Iron/Nickel", "Iron"]
        },
        "Animal" : {
            "Iron/Purple" : ["Iron/Purple", "Iron"],
            "Silver/Purple" : ["Silver/Purple", "Silver"],
        },
        "Motorhead" : {
            "Iron/Red" : ["Iron/Red", "Iron", "Red"],
        },
    },
    "V11" : {
        "Absolute" : {
            "Nickel/Blue" : ["Nickel/Blue", "Nickel", "Blue"],
        },
        "Advanced" : {
            "Nickel/Purple" : ["Nickel/Purple", "Purple", "Nickel"],
        },
        "Animal" : {
            "Nickel/Purple" : ["Nickel/Purple", "Purple", "Nickel"],
        },
        "Torque Drive" : {
            "Nickel/Blue" : ["Nickel/Blue",  "Nickel", "Blue"],
        },
        "Outsize" : {
            "Nickel/Red" : ["Nickel/Red", "Nickel", "Red"],
        },
    },
    "V12" : {
        "Detect Slim Absolute" : {
            "Yellow/Nickel" : ["Yellow/Nickel", "Yellow"],
            "Iron/Nickel" : ["Iron/Nickel", "Iron", "Black"],
            "Gold/Gold" : ["Gold/Gold", "Gold"],
            "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian", "Blue", "Rich", "Copper"]
        },
        "Detect Slim" : {
            "Yellow/Nickel" : ["Yellow/Nickel", "Yellow"],
            "Iron/Nickel" : ["Iron/Nickel", "Iron", "Black"],
            "Gold/Gold" : ["Gold/Gold", "Gold"],
            "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian", "Blue", "Rich", "Copper"]
        },
    },
    "V15" : {
        "Detect" : {
            "Yellow/Nickel" : ["Yellow/Nickel", "Yellow"],
            "Iron/Nickel" : ["Iron/Nickel", "Iron", "Black"],
            "Bronze/Purple" : ["Bronze/Purple", "Bronze", "Purple"],
            "Nickel/Blue" : ["Nickel/Blue", "Blue"],
            "Gold/Gold" : ["Gold/Gold", "Gold"]
        },
        "Detect Absolute" : {
            "Yellow/Nickel" : ["Yellow/Nickel", "Yellow"],
            "Iron/Nickel" : ["Iron/Nickel", "Iron", "Black"],
            "Turquoise Blue/Gold" : ["Turquoise Blue/Gold", "Turquoise"],
            "Purple/Gold:" : ["Purple/Gold", "Purple"],
            "Gold/Gold" : ["Gold/Gold", "Gold"],
            "Bronze/Purple" : ["Bronze/Purple", "Bronze"],
            "Nickel/Red" : ["Nickel/Red", "Red"],
            "Nickel/Blue" : ["Nickel/Blue", "Blue"]
        },
        "Detect Complete" : {
            "Yellow/Nickel" : ["Yellow/Nickel", "Yellow"],
            "Iron/Nickel" : ["Iron/Nickel", "Iron", "Black"],
            "Turquoise Blue/Gold" : ["Turquoise Blue/Gold", "Turquoise"],
            "Purple/Gold:" : ["Purple/Gold", "Purple"],
            "Gold/Gold" : ["Gold/Gold", "Gold"],
            "Bronze/Purple" : ["Bronze/Purple", "Bronze"],
            "Nickel/Red" : ["Nickel/Red", "Red"],
            "Nickel/Blue" : ["Nickel/Blue", "Blue"]
        },
        "Detect Total Clean" : {
            "Yellow/Nickel" : ["Yellow/Nickel", "Yellow"],
            "Iron/Nickel" : ["Iron/Nickel", "Iron", "Black"],
            "Turquoise Blue/Gold" : ["Turquoise Blue/Gold", "Turquoise"],
            "Purple/Gold:" : ["Purple/Gold", "Purple"],
            "Gold/Gold" : ["Gold/Gold", "Gold"],
            "Bronze/Purple" : ["Bronze/Purple", "Bronze"],
            "Nickel/Red" : ["Nickel/Red", "Red"],
            "Nickel/Blue" : ["Nickel/Blue", "Blue"]
        },
    },
    "Gen5" : {
        "Detect Absolute" : {
            "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian", "Blue", "Copper"],
            "Iron/Purple" : ["Iron/Purple", "Iron", "Black", "Purple"],
        },
        "Outsize Absolute" : {
            "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian", "Blue", "Copper", "Rich"],
            "Nickel/Blue" : ["Nickel/Blue", "Nickel"],
        },
    },
}

STANDARD_COLOR_FOR_VERSION_COMPLETE = {
    #припысываем стандартный атрибут "color" для конкретного "version" относительно его "complete" для "Беспроводные пылесосы Dyson"
    "V8" : {
        "Absolute" : "Silver/Nickel",
        "Animal" : "Iron/Purple",
        "Animal+" : "Iron/Sprayed Nickel/Purple",
        "Motorhead" : "Silver/Nickel",
    },
    "V10" : {
        "Absolute" : "Nickel/Copper",
        "Animal" : "Iron/Purple",
        "Motorhead" : "Iron/Red",
    },
    "V11" : {
        "Absolute" : "Nickel/Blue",
        "Advanced" : "Nickel/Purple",
        "Animal" : "Nickel/Purple",
        "Torque Drive" : "Nickel/Blue",
        "Nickel/Red" : "Nickel/Red",
    },
    "V12" : {
        "Detect Slim Absolute" : "Yellow/Nickel",
        "Detect Slim" : "Yellow/Nickel",
    },
    "V15" : {
        "Detect" : "Yellow/Nickel",
        "Detect Absolute" : "Yellow/Nickel",
        "Detect Complete" : "Yellow/Nickel",
        "Detect Total Clean" : "Yellow/Nickel",
    },
    "Gen5" : {
        "Detect Absolute" : "Iron/Purple",
        "Outsize Absolute" : "Nickel/Blue",
    },
}

#"Пылесосы Dyson с влажной уборкой"

WASH_COMPLETE_FOR_VERSION = {
    #парсим атрибут "complete" для конкретного "version" относительно для "Беспроводные пылесосы Dyson"
    "G1" : {
        "Wash" : ["Wash", "WashG1", "G1Wash"],
    },
    "V12s Detect" : {
        "Slim Submarine™" : ["Slim Submarine™", "Submarine™", "Submarine"],
        "Slim Absolute" : ["Slim Absolute", "Absolute"],
    },
    "V15s Detect" : {
        "Submarine™" : ["rere"],
        "Submarine™ Absolute" : ["Submarine™ Absolute", "Submarine Absolute", "Absolute"],
    },
}

WASH_STANDARD_COMPLETE_FOR_VERSION = {
    #припысываем стандартный атрибут "complete" для конкретной "version" если не указано другое
    #для "Беспроводные пылесосы Dyson"
    "G1" : "Wash",
    "V12s Detect" : "Submarine™",
    "V15s Detect" : "Submarine™",
}

WASH_COLOR_FOR_VERSION_COMPLETE = {
    #парсим атрибут "color" для конкретного "version" относительно его "complete" для "Беспроводные пылесосы Dyson"
    "G1" : {
        "Wash" : {
            "Matte Black/Ultra Blue" : ["Matte Black/Ultra Blue", "Black", "Matte", "Blue"],
        },
    },
    "V12s Detect" : {
        "Slim Submarine™" : {
            "Yellow/Nickel" : ["Yellow/Nicke", "Yellow", "Nickel"],
            "Gold/Gold" : ["Gold/Gold", "Gold"],
        },
        "Slim Absolute" : {
            "Gold/Gold" : ["Gold/Gold", "Gold"],
            "Yellow/Nickel" : ["Yellow/Nicke", "Yellow", "Nickel"],
        },
    },
    "V15s Detect" : {
        "Submarine™" : {
            "Yellow/Nickel" : ["Yellow/Nicke", "Yellow", "Nickel"],
        },
        "Submarine™ Absolute" : {
            "Gold/Gold" : ["Gold/Gold", "Gold"],
        },
    },
}

WASH_STANDARD_COLOR_FOR_VERSION_COMPLETE = {
    #припысываем стандартный атрибут "color" для конкретного "version" относительно его "complete" для "Беспроводные пылесосы Dyson"
    "G1" : {
        "Wash" : "Matte Black/Ultra Blue",
    },
    "V12s Detect" : {
        "Slim Submarine™" : "Gold/Gold",
        "Slim Absolute" : "Gold/Gold"
    },
    "V15s Detect" : {
        "Submarine™" : "Yellow/Nickel",
        "Submarine™ Absolute" : "Gold/Gold"
    },
}

#"Очистители воздуха Dyson"

COLOR_FOR_VERSION_VERSION_CLIMATE_TP = {
    #парсим атрибут "color" для конкретного "version" для "Очистители воздуха Dyson"
    "TP07 Purifier Cool™" : {
        "Black/Nickel" : ["Black/Nickel", "Black", "Nickel"],
        "White/Silver" : ["White/Silver", "White", "Silver"],
    },
    "TP08 Pure Cool™" : {
        "White/Silver" : ["White/Silver", "White", "Silver"],
    },
    "TP09 Purifier Cool Formaldehyde™" : {
        "Nickel/Gold" : ["Nickel/Gold", "Nickel"],
        "White/Gold" : ["White/Gold", "White"],
    },
    "BP03 Purifier Big+Quiet Formaldehyde™" : {
        "Bright Nickel/Prussian Blue" : ["Bright Nickel/Prussian Blue"]
    },
    "BP04 Purifier Big+Quiet Formaldehyde™" : {
        "Prussian Blue/Gold" : ["Prussian Blue/Gold"]
    },
}

STANDARD_COLOR_FOR_VERSION_CLIMATE_TP = {
    #припысываем стандартный атрибут "color" для конкретной "version" если не указано другое
    #для "Очистители воздуха Dyson"
    "TP07 Purifier Cool™" : "White/Silver",
    "TP08 Pure Cool™" : "White/Silver",
    "TP09 Purifier Cool Formaldehyde™" : "White/Gold",
    "BP03 Purifier Big+Quiet Formaldehyde™" : "Bright Nickel/Prussian Blue",
    "BP04 Purifier Big+Quiet Formaldehyde™" : "Prussian Blue/Gold"
}

#"Очистители-увлажнители воздуха Dyson"

COLOR_FOR_VERSION_VERSION_CLIMATE_PH = {
    #парсим атрибут "color" для конкретного "version" для "Очистители-увлажнители воздуха Dyson"
    "PH03 Purifier Humidify+Cool™" : {
        "Black/Nickel" : ["Black/Nickel", "Black", "Nickel"],
        "White/Silver" : ["White/Silver", "White", "Silver"],
    },
    "PH04 Purifier Humidify+Cool Formaldehyde™" : {
        "White/Gold" : ["White/Silver", "White"],
        "Nickel/Gold" : ["Nickel/Gold", "Nickel"],
    },
}

STANDARD_COLOR_FOR_VERSION_CLIMATE_PH = {
    #припысываем стандартный атрибут "color" для конкретной "version" если не указано другое
    #для "Очистители-увлажнители воздуха Dyson"
    "PH03 Purifier Humidify+Cool™" : "White/Silver",
    "PH04 Purifier Humidify+Cool Formaldehyde™" : "White/Gold",
}

#"Очистители-обогреватели воздуха"

COLOR_FOR_VERSION_VERSION_CLIMATE_HP = {
    #парсим атрибут "color" для конкретного "version" для "Очистители-обогреватели воздуха"
    "HP07 Purifier Hot+Cool™" : {
        "Black/Nickel" : ["Black/Nickel", "Black", "Nickel"],
        "White/Silver" : ["White/Silver", "White", "Silver"],
    },
    "HP09 Purifier Hot+Cool Formaldehyde™" : {
        "White/Gold" : ["White/Gold", "White", "Gold"],
    },
    "HP10 Purifier Hot+Cool™ Gen1" : {
        "Black/Nickel" : ["Black/Nickel", "Black", "Nickel"],
        "White/Silver" : ["White/Silver", "Silver",],
        "White" : ["White"],
    },
}

STANDARD_COLOR_FOR_VERSION_CLIMATE_HP = {
    #припысываем стандартный атрибут "color" для конкретной "version" если не указано другое
    #для "Очистители-обогреватели воздуха"
    "HP07 Purifier Hot+Cool™" : "White/Silver",
    "HP09 Purifier Hot+Cool Formaldehyde™" : "White/Gold",
    "HP10 Purifier Hot+Cool™ Gen1" : "White/Silver",
}


#"Беслопастные вентиляторы и увлажнители Dyson"

COLOR_FOR_VERSION_VERSION_CLIMATE_AM = {
    #парсим атрибут "color" для конкретного "version" для "Беслопастные вентиляторы и увлажнители Dyson"
    "AM09 Hot+Cool™" : {
        "White/Silver" : ["White/Silver", "White", "Silver"],
        "Metallic" : ["Metallic"],
    },
    "AM10 Humidifier" : {
        "White/Silver" : ["White/Silver", "White", "Silver"],
        "Iron/Blue" : ["Iron/Blue", "Iron", "Blue"],
        "Black/Nickel" : ["Black/Nickel", "Black", "Nickel"],
    },
}

STANDARD_COLOR_FOR_VERSION_CLIMATE_AM = {
    #припысываем стандартный атрибут "color" для конкретной "version" если не указано другое
    #для "Беслопастные вентиляторы и увлажнители Dyson"
    "AM09 Hot+Cool™" : "White/Silver",
    "AM10 Humidifier" : "White/Silver",
}

#"Аксессуары Dyson"

COLOR_FOR_VERSION_VERSION_ACCESSORIES = {
    #парсим атрибут "color" для конкретного "version" для "Аксессуары Dyson"
    "Расческа Dyson Paddle Brush" : {
        "Fuchsia" : ["Fuchsia"],
        "Pale Rose" : ["Pale Rose", "Pale", "Rose"],
        "Nickel/Black" : ["Nickel/Black", "Nickel", "Black"],
        "Blue/Cooper" : ["Blue/Cooper", "Blue", "Cooper"]
    },
    "Чехол Dyson Travel Bag" : {
        "Fuchsia/Black" : ["Fuchsia/Black", "Fuchsia"],
        "Purple/Black" : ["Purple/Black", "Purple"],
        "Black/Copper" : ["Black/Copper", "Cooper"],
        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian", "Rich", "Blue"],
        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vinca", "Topaz"],
        "Black/Nickel" : ["Black/Nickel", "Nickel"],
        "Black" : ["Black"]
    },
    "Кейс Dyson Presentation" : {
        "Fuchsia/Black" : ["Fuchsia/Black", "Fuchsia"],
        "Purple/Black" : ["Purple/Black", "Purple"],
        "Black/Copper" : ["Black/Copper", "Cooper"],
        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian", "Rich", "Blue"],
        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vinca", "Topaz"],
        "Black/Nickel" : ["Black/Nickel", "Nickel"],
        "Black" : ["Black"],
        "Ceramic/Pink" : ["Ceramic/Pink", "Ceramic", "Pink", "HT01"]
    },
    "Подставка для" : {
        "стайлеров Dyson" : ["стайлеров", "стайлера", "стайлер", "Airwrap", "HS01", "HS05", "HS08", "dryer"],
        "выпрямителей Dyson" : ["выпрямителей", "выпрямителя", "HS03", "HS07", "HT01", "Corrale", "AirStrait"],
        "фенов Dyson" : ["фенов", "фена", "фен", "Supersonic", "HD07", "HD08", "HD15", "HD16", "HD18"],
        "пылесосов Dyson" : ["пылесосов", "пылесоса", "V8", "V10", "V11", "V12", "V15", "Gen5", "G1", "V12s", "V15s"]
    },
}

#📱Специальные правила для JBL 📱>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
JBL_NO_COLOR_REQUIRED = {
    "Акустические системы JBL" : {
        "JBL PartyBox Ultimate",
        "JBL PartyBox Encore",
        "JBL PartyBox Encore Essential",
        "JBL PartyBox Encore 2",
        "JBL PartyBox On-The-Go"}
}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#🟡Специальные правила для PlayStation PLAYSTATION🟡>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Игнорирование определенных слов
IGNORING_MODEL_FOR_PLAYSTATION = {
    "Консоли PlayStation" : ["DualSense", "Consoles", "VR2", "VR", "Подставка", "Док-Станция", "Док", "Станция",
                     "Pulse", "Portal", "дисковод", "Drive", "DualShock", "Геймпад", "Зарядная станция",
                             "Charging Station", "Charging"],
    "Контроллеры PlayStation" : ["VR2", "VR", "Подставка", "Док-Станция", "Док", "Станция", "FAT", "PRO", "Slim",
                     "Pulse", "Portal", "дисковод", "Drive", "DualShock", "Геймпад", "Disk", "Digital",
                    "Зарядная станция", "Charging Station", "Charging"],
    "PlayStation VR" : ["sense", "VR", "Подставка", "Док-Станция", "Док", "Станция", "FAT", "PRO", "Slim",
                     "Pulse", "Portal", "дисковод", "Drive", "DualShock", "Геймпад", "Disk", "Digital", "зарядка",
                        "Meta", "Quest", "Charging Station", "Charging"],
}

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ❇️ Список «сложных» брендов ❇️
COMPLEX_BRANDS = [
    "Apple Watch",
    "Apple Mac",
    "Apple Airpods",
    "Apple iPhone",
    "Apple iPad",
    "Apple Аксессуары",
    "Galaxy Buds",
    "Samsung Galaxy",
    "Стайлеры для волос Dyson",
    "Фены для волос Dyson",
    "Выпрямители для волос Dyson",
    "Пылесосы Dyson",
    "Системы очистки воздуха Dyson",
    "Сушилки для рук Dyson",
    "Аудиотехника Dyson",
    "Аксессуары Dyson",
    "Xiaomi",
    "OnePlus",
    "Google",
    "Realme",
    "Honor",
    "Doogee",
    "Infinix",
    "Tecno Mobile",
    "Яндекс",
    "JBL",
    "Beats",
    "Sony",
    "Marshall",
    "OnePlus Buds",
    "Redmi Buds",
    "Nothing Ear",
    "VK",
    "Аудио прочее",
    "Xbox",
    "PlayStation",
    "Meta Quest",
    "Valve Steam Deck",
    "Nintendo",
    "GoPro",
    "Insta360",
    "DJI Osmo"
]

#  Список слов паттернов для поиска в конкретном бренде
PATTERNS_FOR_COMPLEX_BRAND_SEARCH = {
    "Apple Watch" : ["AW", "apple watch"],
    "Apple Mac" : ["Apple MacBook", "MacBook Pro", "MacBook Air", "Mac Studio", "Mac Pro", "MacBook", "Mac",],
    "Apple Airpods" : ["Airpods"],
    "Apple iPhone" : [
        "iPhone",
        "11 Pro",
        "11 Pro Max",
        "12 Mini",
        "12 Pro",
        "12 Pro Max",
        "13 Mini",
        "13 Pro",
        "13 Pro Max",
        "14 Plus",
        "14 Pro",
        "14 Pro Max",
        "15 Plus",
        "15 Pro",
        "15 Pro Max",
        "16 Plus",
        "16 Pro",
        "16 Pro Max",
    ],
    "Apple iPad" : ["iPad"],
    "Apple Аксессуары" : ["Magic", "Pencil", "AirTag", "MagSafe"],
    "Galaxy Buds" : ["Galaxy Buds"],
    "Samsung Galaxy" : [
        "samsung",
        "A03", "A03", "A03s", "A04e", "A04", "A04s", "A05", "A05s", "A06", "A13", "A13", "A14", "A14", "A15", "A15",
        "A16", "A16", "A23", "A23", "A24", "A25", "A25", "A26", "A33", "A34", "A35", "A35", "A36", "A53",
        "A54", "A55", "A56", "A73",
        "M10", "M10s", "M11", "M12", "M13", "M13", "M14", "M20", "M21", "M22", "M23", "M23", "M30", "M30s", "M31", "M31s",
        "M32", "M33", "M34", "M40", "M42", "M50", "M51", "M52", "M53", "M54", "M55", "M55s",
        "S21", "S 21", "S21+", "S 21+", "S21 +", "S 21 +", "S21 plus", "S 21 plus", "S21plus",
        "S21 Ultra", "S21Ultra", "S21Ultra", "S 21Ultra", "S 21 Ultra",
        "S22", "S 22", "S22+", "S 22+", "S22 +", "S 22 +", "S22 plus", "S 22 plus", "S22plus",
        "S22 Ultra", "S22 Ultra", "S22Ultra", "S22Ultra", "S 22Ultra", "S 22 Ultra",
        "S23", "S 23", "S23+", "S 23+", "S23 +", "S 23 +", "S23 plus", "S 23 plus", "S23plus",
        "S23 Ultra", "S23 Ultra", "S23Ultra", "S23Ultra", "S 23Ultra", "S 23 Ultra",
        "S23FE", "S 23FE", "S23 FE", "S 23 FE", "S24+", "S 24+", "S24 +", "S 24 +", "S24 plus", "S 24 plus", "S24plus",
        "S24", "S 24", "S24 Ultra", "S24 Ultra", "S24Ultra", "S24Ultra", "S 24Ultra", "S 24 Ultra",
        "S24FE", "S 24FE", "S24 FE", "S 24 FE", "S25", "S 25",
        "S25+", "S25+", "S 25+", "S25 +", "S 25 +", "S25 plus", "S 25 plus", "S25plus",
        "S25 Ultra", "S25 Ultra", "S25Ultra", "S25Ultra", "S 25Ultra", "S 25 Ultra",
        "S25 Edge", "S25 Edge", "S25Edge",
        "Z Fold", "Z Flip", "Z Fold4", "Z Fold5", "Z Fold6", "Z Flip4", "Z Flip5", "Z Flip6"

    ],
    "Стайлеры для волос Dyson" : ["HS01", "HS05", "HS08"],
    "Фены для волос Dyson" : ["HD07", "HD08", "HD15", "HD16", "HD18"],
    "Выпрямители для волос Dyson" : ["HS03", "HS07", "HT01"],
    "Пылесосы Dyson" : [
        "V8", "V10", "V11", "V12", "V15", "Gen5", "G1", "V12s", "V15s",
        "Big Ball", "Ball", "Multi Floor", "Multi", "Floor", "Parquet",
        "Vis Nav", "Heurist"],
    "Системы очистки воздуха Dyson" : ["TP07", "TP08", "TP09", "BP03", "BP04", "PH03", "PH04",
        "HP07", "HP09", "HP10", "AM09", "AM10"],
    "Сушилки для рук Dyson" : ["HU02", "HU03", "AB09", "AB10", "AB11", "AB12", "AB13", "AB14", "WD04", "WD05", "WD06"],
    "Аксессуары Dyson" : ["расческа", "Paddle Brush", "чехол", "Travel Bag", "дорожные сумки", "сумки", "сумка", "бокс", "боксы",
                "дорожная", "дорожные","кейс", "Presentation Case", "Case", "кейсы", "подставка", "подставки"],
    "Redmi Buds" : ["Redmi Buds"],
    "OnePlus Buds" : ["OnePlus Buds"],
    "Xiaomi" : ["Xiaomi", "mi", "Redmi", "note", "poco", "Redmi Pad"],
    "OnePlus" : ["OnePlus"],
    "Google" : ["Pixel"],
    "Realme" : ["Realme"],
    "Honor" : ["Honor"],
    "Infinix" : ["Infinix"],
    "Doogee" : ["Doogee"],
    "Tecno Mobile" : ["Tecno Spark", "Tecno Camon", "Tecno Pova"],
    "Яндекс" : ["Яндекс"],
    "JBL" : ["JBL", "CLIP"],
    "Beats" : ["Beats"],
    "Sony" : ["Sony WH", "Sony WF"],
    "Marshall" : ["Marshall"],
    "Nothing Ear" : ["Nothing Ear"],
    "VK" : ["VK"],
    "Аудио прочее" : ["Sennheiser", "Bose", "QuietComfort", "Quiet Comfort", "B&W", "Bowers & Wilkins", "CMF",
    "Dyson Zone", "Dyson Zone™", "Air Purification", "Dyson OnTrac™", "Dyson OnTrac", "Dyson on trac", "Logitech",
    "Beyerdynamic", "Harman/Kardon", "Go play", "Go+play"
                      ],
    "Xbox" : ["Xbox"],
    "PlayStation" : ["PlayStation", "PS"],
    "Meta Quest" : ["Meta Quest"],
    "Valve Steam Deck" : ["Steam Deck"],
    "Nintendo" : ["Nintendo", "Switch"],
    "GoPro" : ["GoPro"],
    "Insta360" : ["Insta360", "Insta 360", "insta360°"],
    "DJI Osmo" : ["DJI Osmo"]
}

#Список обеденных brand
LIST_BRAND_GROUP = {
    "Apple" : ["Apple Аксессуары", "Apple Airpods", "Apple Watch", "Apple iPhone", "Apple iPad", "Apple Mac"],
    "Android" : ["Samsung Galaxy", "Xiaomi", "Google", "OnePlus", "Realme", "Honor", "Infinix", "Doogee", "Tecno Mobile"],
    "Dyson" : ["Аудиотехника Dyson", "Аксессуары Dyson", "Стайлеры для волос Dyson", "Фены для волос Dyson",
               "Выпрямители для волос Dyson", "Пылесосы Dyson", "Системы очистки воздуха Dyson",
               "Сушилки для рук Dyson"],
    "Аудио" : ["Яндекс", "JBL", "Beats", "Sony", "Marshall", "Galaxy Buds", "OnePlus Buds", "Redmi Buds", "Nothing Ear",
               "VK", "Аудио прочее"],
    "Консоли/VR" : ["PlayStation", "Xbox", "Meta Quest", "Steam Deck", "Nintendo"],
    "Фото и видео" : ["GoPro", "Insta360", "DJI Osmo"]
}

# Библиотека товаров
PRODUCT_LIBRARY = {
    #Apple:
    "Apple Аксессуары" : {
        "Magic Mouse" : {
            "aliases" : [
                "Magic Mouse",
            ],
            "attributes" : {
                "color" : {
                    "values" : ["Black", "White", "Silver", "Gray"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "White" : ["White"],
                        "Silver" : ["Silver"],
                        "Gray" : ["Gray", "Grey"]
                    },
                },
                "USB" : {
                    "values" : ["USB-C", "USB-A"],
                    "aliases" : {
                        "USB-C" : ["USB-C", "USB C"],
                        "USB-A" : ["USB-A", "USB A"]
                    },
                },
            },
        },
        "Magic Keyboard" : {
            "aliases" : [
                "Magic Keyboard",
            ],
            "attributes" : {
                "color" : {
                    "values" : ["Black", "White"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "White" : ["White"]
                    },
                },
                "iPad" : {
                    "values" : ["iPad Pro", "iPad Air"],
                    "aliases" : {
                        "iPad Pro" : ["iPad Pro", "Pro"],
                        "iPad Air" : ["iPad Air", "Air"]
                    },
                },
                "diagonal" : {
                    "values" : ["11", "12.9", "13"],
                    "aliases" : {
                        "11" : ["11"],
                        "12.9" : ["12.9", "12,9"],
                        "13" : ["13"],
                    },
                },
                "Numeric Keypad" : {
                    "values" : ["c Numeric Keypad"],
                    "aliases" : {
                        "c Numeric Keypad" : ["Numeric Keypad", "Numeric"]
                    },
                },
                "Touch ID" : {
                    "values" : ["c Touch ID"],
                    "aliases" : {
                        "c Touch ID" : ["Touch ID", "Touch"]
                    },
                },
            },
        },
        "Magic Trackpad" : {
            "aliases" : [
                "Magic Trackpad",
            ],
            "attributes" : {
                "color" : {
                    "values" : ["Black", "White"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "White" : ["White"]
                    },
                },
            },
        },
        "Pencil" : {
            "aliases" : [
                "Pencil",
            ],
            "attributes" : {
                "USB" : {
                    "values" : ["USB-C", "USB-A"],
                    "aliases" : {
                        "USB-C" : ["USB-C", "USB C"],
                        "USB-A" : ["USB-A", "USB A"]
                    },
                },
                "version" : {
                    "values" : ["2", "Pro"],
                    "aliases" : {
                        "2" : ["2"],
                        "Pro" : ["Pro"]
                    },
                },
            },
        },
        "AirTag" : {
            "aliases" : [
                "AirTag",
            ],
            "attributes" : {
                "Pack" : {
                    "values" : ["4 pack", "2 pack", "1 pack"],
                    "aliases" : {
                        "4 pack" : ["4 pack", "4"],
                        "2 pack" : ["2 pack", "2"],
                        "1 pack" : ["1 pack", "1"],
                    },
                },
            },
        },
        "Charger" : {
            "aliases" : [
                "MagSafe",
                "Magnetic Charger"
            ],
            "attributes" : {
                "version" : {
                    "values" : ["MagSafe Charger", "MagSafe Duo", "MagSafe 3", "Apple Watch Magnetic Charger USB-C"],
                    "aliases" : {
                        "MagSafe Charger" : ["MagSafe Charger"],
                        "MagSafe Duo" : ["MagSafe Duo"],
                        "MagSafe 3" : ["MagSafe 3"],
                        "Apple Watch Magnetic Charger USB-C" : ["Watch Magnetic Charger USB-C",
                                                                "Apple Watch Magnetic Charger USB C"]
                    },
                },
            },
        },
        "Apple TV 4K" : {
            "aliases" : [
                "Apple TV",
            ],
            "attributes" : {
                "SSD" : {
                    "values" : ["64GB Wi-Fi", "128GB Wi-Fi + Ethernet"],
                    "aliases" : {
                        "64GB Wi-Fi" : ["64"],
                        "128GB Wi-Fi + Ethernet" : ["128"]
                    },
                },
            },
        },
        "Наборы для AirPods" : {
            "aliases" : [
                "AirPods", "Air Pods"
            ],
            "attributes" : {
                "version" : {
                    "values" : ["2", "3", "Pro", "Pro 2", "4"],
                    "aliases" : {
                        "2" : ["2", "2nd", "2-nd", "2rd Gen"],
                        "3" : ["3", "3nd", "3-nd", "3rd Gen"],
                        "Pro" : ["Pro"],
                        "Pro 2" : ["Pro 2", "Pro 2nd", "Pro 2-nd"],
                        "4" : ["4", "4nd", "4-nd", "4rd Gen"],
                    },
                },
                "Pack" : {
                    "values" : ["левый наушник (L)", "правый наушник (R)", "зарядный футляр"],
                    "aliases" : {
                        "левый наушник (L)" : ["левый наушник", "левый", "левое", "L"],
                        "правый наушник (R)" : ["правый наушник", "правый", "правое", "R"],
                        "зарядный футляр" : ["зарядный футляр", "Box", "Кейс"],
                    },
                },
            },
        },
    },
    "Apple Airpods" : {
        "AirPods Max" : {
            "aliases" : [
                "AirPods Max",
            ],
            "attributes" : {
                "color" : {
                    "values" : ["Blue", "Black", "Green", "Pink", "Silver", "Midnight", "Starlight", "Purple",
                                "Orange"],
                    "aliases" : {
                        "Blue" : ["Blue"],
                        "Black" : ["Black"],
                        "Green" : ["Green"],
                        "Pink" : ["Pink"],
                        "Silver" : ["Silver"],
                        "Midnight" : ["Midnight"],  # 2024
                        "Starlight" : ["Starlight"],  # 2024
                        "Purple" : ["Purple"],  # 2024
                        "Orange" : ["Orange"]  # 2024
                    },
                },
                "years" : {
                    "values" : ["2022", "2024"],
                    "aliases" : {
                        "2022" : ["2022"],
                        "2024" : ["2024", "new"],
                    },
                },
            },
        },
        "AirPods" : {
            "aliases" : [
                "AirPods", "Air Pods"
            ],
            "attributes" : {
                "version" : {
                    "values" : ["2", "3", "Pro 2", "4"],
                    "aliases" : {
                        "2" : ["2", "2nd", "2-nd", "2rd Gen"],
                        "3" : ["3", "3nd", "3-nd", "3rd Gen"],
                        "Pro 2" : ["Pro 2", "Pro 2nd", "Pro 2-nd"],
                        "4" : ["4", "4nd", "4-nd", "4rd Gen"],
                    },
                },
                "ANC" : {
                    "values" : ["ANC"],
                    "aliases" : {
                        "ANC" : ["ANC", "ANK", "Active Noise Cancellation", "шумоподавлением"],
                    },
                },
                "case" : {
                    "values" : ["case MagSafe",
                                "case Lightning",
                                "case MagSafe (USB-C)",
                                "case MagSafe (Lightning)"],
                    "aliases" : {
                        "case MagSafe" : ["case MagSafe"],
                        "case Lightning" : ["case Lightning"],
                        "case MagSafe (USB-C)" : ["case MagSafe (USB-C)"],
                        "case MagSafe (Lightning)" : ["case MagSafe (Lightning)"],
                    },
                },
            },
        },
    },
    "Apple Watch" : {
        "AW SE 2" : {
            "aliases" : [
                "Watch SE",
                "Series SE 2",
                "aw se",
                "watch se 2",
                "watch se2",
                "aw se 2",
                "aw se2",
                "se 2",
                "se2",
                "aw se",
                "se"
            ],
            "attributes" : {
                "case_size" : {
                    "values" : ["40mm", "44mm"],
                    "aliases" : {
                        "40mm" : ["40mm", "40 мм", "40"],
                        "44mm" : ["44mm", "44 мм", "44"]
                    },
                },
                "year_release" : {
                    "values" : ["2022", "2023", "2024"],
                    "aliases" : {
                        "2022" : ["2022"],
                        "2023" : ["2023"],
                        "2024" : ["2024"]
                    },
                },
                "case_type" : {
                    "values" : [
                        "Starlight",
                        "Midnight",
                        "Silver",
                    ],
                    "aliases" : {
                        "Starlight" : [
                            "Starlight",
                            "Starlight aluminum"
                        ],
                        "Midnight" : [
                            "Midnight",
                            "Midnight aluminum"
                        ],
                        "Silver" : [
                            "silver",
                            "silver aluminum"
                        ],
                    }
                },
                "strap_type" : {
                    "values" : [
                        "Sport Band Denim",
                        "Sport Band Plum",
                        "Sport Band Lake Green",
                        "Sport Band Starlight",
                        "Sport Band Light Blush",
                        "Sport Band Stone Gray",
                        "Sport Band Black",
                        "Sport Band Pride Edition",
                        "Sport Band Black Unity",
                        "Sport Band Midnight",
                        "Sport Band",
                        "Sport Loop Blue Cloud",
                        "Sport Loop Lake Green",
                        "Sport Loop Plum",
                        "Sport Loop Ink",
                        "Sport Loop Black",
                        "Sport Loop Midnight",
                        "Sport Loop Ultramarine",
                        "Sport Loop Black Unity",
                        "Sport Loop",
                        "Natural Titanium Milanese Loop",
                        "Black Titanium Milanese Loop",
                        "Milanese Loop",
                        "Solo Loop Lake Green",
                        "Solo Loop Ultramarine",
                        "Solo Loop Star Fruit",
                        "Solo Loop Light Blush",
                        "Solo Loop Black",
                        "Solo Loop",
                        "Nike Sport Band Volt Splash",
                        "Nike Sport Band Cargo Khaki",
                        "Nike Sport Band Blue Flame",
                        "Nike Sport Band Magic Ember",
                        "Nike Sport Band Desert Stone",
                        "Nike Sport Band Midnight Sky",
                        "Nike Sport Band Pure Platinum",
                        "Nike Sport Band",
                        "Blue/Red Nike Sport Loop",
                        "Grey/Blue Nike Sport Loop",
                        "Black/Blue Nike Sport Loop",
                        "Green/Grey Nike Sport Loop",
                        "Starlight/Pink Nike Sport Loop",
                        "Nike Sport Loop",
                        "Braided Solo Loop Chartreuse",
                        "Braided Solo Loop Denim",
                        "Braided Solo Loop Magenta",
                        "Braided Solo Loop Midnight",
                        "Braided Solo Loop Lake Green",
                        "Braided Solo Loop Black Unity",
                        "Braided Solo Loop Pride Edition",
                        "Braided Solo Loop Beige",
                        "Braided Solo Loop"
                    ],
                    "aliases" : {
                        "Sport Band Denim" : [
                            "Sport Band Denim",
                            "Denim Sport Band",
                            "Denim SB",
                            "SB Denim",
                            "Denim"
                        ],
                        "Sport Band Plum" : [
                            "Sport Band Plum",
                            "Band Plum Sport",
                            "Plum Sport Band",
                            "Plum SB",
                            "SB Plum",
                            "Sport Plum"
                        ],
                        "Sport Band Lake Green" : [
                            "Lake Green Sport Band",
                            "Sport Band Lake Green",
                            "Green Sport Band",
                            "Sport Band Green",
                            "Green Band",
                            "Green SB",
                            "SB Green",
                            "Lake Green SB",
                            "SB Lake Green"
                        ],
                        "Sport Band Starlight" : [
                            "Sport Band Starlight",
                            "Starlight Sport Band",
                            "Starlight Band",
                            "Starlight SB",
                            "SB Starlight"
                        ],
                        "Sport Band Light Blush" : [
                            "Sport Band Light Blush",
                            "Light Blush Sport Band",
                            "Sport Band Light",
                            "Sport Band Blush",
                            "Light Blush SB",
                            "SB Light Blush",
                            "Light Blush",
                            "MWWH3",
                            "MWWU3",
                            "MWWJ3",
                            "U3LW",
                            "Blush",
                            "LB",
                            "LB SB"
                        ],
                        "Sport Band Stone Gray" : [
                            "Sport Band Stone Gray",
                            "Stone Gray Sport Band",
                            "Sport Band Stone",
                            "Sport Band Gray",
                            "Stone Gray SB",
                            "SB Stone Gray",
                            "Stone Gray",
                            "Gray SB",
                            "SB Gray",
                            "Gray"
                        ],
                        "Sport Band Black" : [
                            "Sport Band Black",
                            "Black Sport Band",
                            "Black Band",
                            "SB Black",
                            "Black SB",
                            "Q3LW",
                            "MWWE3",
                            "MWWP3",
                            "MWWF3"
                        ],
                        "Sport Band Pride Edition" : [
                            "Sport Band Pride Edition",
                            "Pride Edition Sport Band",
                            "Sport Band Pride",
                            "Sport Band Edition",
                            "Pride Edition",
                            "Pride SB",
                            "SB Pride",
                            "Pride"
                        ],
                        "Sport Band Black Unity" : [
                            "Sport Band Black Unity",
                            "Black Unity Sport Band",
                            "Sport Band Black",
                            "Sport Band Unity",
                            "Black Unity Band",
                            "Black Unity SB",
                            "SB Black Unity",
                            "Black Unity SB"
                        ],
                        "Sport Band Midnight" : [
                            "Sport Band Midnight",
                            "Midnight Sport Band",
                            "Midnight Band",
                            "Midnight SB",
                            "SB Midnight"
                        ],
                        "Sport Band" : [
                            "Sport Band",
                            "Sport",
                            "SB"
                        ],
                        "Sport Loop Blue Cloud" : [
                            "Sport Loop Blue Cloud",
                            "Blue Cloud Sport Loop",
                            "Sport Loop Blue",
                            "Blue Sport Loop",
                            "Blue Loop",
                            "Blue SL",
                            "SL Blue",
                            "Blue Cloud SL",
                            "SL Blue Cloud",
                            "Blue"
                        ],
                        "Sport Loop Lake Green" : [
                            "Sport Loop Lake Green",
                            "Lake Green Sport Loop",
                            "Sport Loop Green",
                            "Green Sport Loop",
                            "Green Loop",
                            "Lake Green SL",
                            "SL Lake Green",
                            "SL Green",
                            "Green SL"
                        ],
                        "Sport Loop Plum" : [
                            "Sport Loop Plum",
                            "Plum Sport Loop",
                            "Loop Plum",
                            "Plum Loop",
                            "SL Plum",
                            "Plum SL"
                        ],
                        "Sport Loop Ink" : [
                            "Sport Loop Ink",
                            "Ink Sport Loop",
                            "Ink Loop",
                            "Ink SL",
                            "SL Ink"
                        ],
                        "Sport Loop Black" : [
                            "Sport Loop Black",
                            "Black Sport Loop",
                            "Black Loop",
                            "Black SL",
                            "SL Black"
                        ],
                        "Sport Loop Midnight" : [
                            "Sport Loop Midnight",
                            "Midnight Loop",
                            "Midnight SL",
                            "SL Midnight"
                        ],
                        "Sport Loop Ultramarine" : [
                            "Sport Loop Ultramarine",
                            "Ultramarine Sport Loop",
                            "Ultramarine Loop",
                            "Ultramarine Sport",
                            "SL Ultramarine",
                            "Ultramarine SL"
                        ],
                        "Sport Loop Black Unity" : [
                            "Sport Loop Black Unity",
                            "Black Unity Sport Loop",
                            "Sport Loop Black",
                            "Sport Loop Unity",
                            "Black Sport Loop",
                            "Black Loop",
                            "SL Black Unity",
                            "Black Unity SL"
                        ],
                        "Sport Loop" : [
                            "Sport Loop",
                            "Loop",
                            "SL"
                        ],
                        "Natural Titanium Milanese Loop" : [
                            "Natural Titanium Milanese Loop",
                            "Natural Milanese Loop",
                            "Natural Milanese"
                        ],
                        "Black Titanium Milanese Loop" : [
                            "Black Titanium Milanese Loop",
                            "Black Milanese Loop",
                            "Black Milanese"
                        ],
                        "Milanese Loop" : [
                            "milanese loop",
                            "milanese",
                            "Mil LP"
                        ],
                        "Solo Loop Lake Green" : [
                            "Solo Loop Lake Green",
                            "Lake Green Solo Loop",
                            "Solo Loop Green",
                            "Green Solo Loop",
                        ],
                        "Solo Loop Ultramarine" : [
                            "Solo Loop Ultramarine",
                            "Ultramarine Solo Loop",
                        ],
                        "Solo Loop Star Fruit" : [
                            "Solo Loop Star Fruit",
                            "Star Fruit Solo Loop",
                            "Solo Loop Star",
                            "Solo Loop Fruit",
                            "Star Fruit Loop",
                            "SL Star Fruit",
                            "Star Fruit SL",
                            "SL Star",
                            "SL Fruit",
                            "SL Star Fruit",
                            "SL Star Fruit"
                            "Star Fruit Loop"
                        ],
                        "Solo Loop Light Blush" : [
                            "Solo Loop Light Blush",
                            "Light Blush Solo Loop",
                            "Solo Loop Light",
                            "Solo Loop Blush",
                            "SL Light Blush",
                            "Light Blush SL",
                            "SL Light",
                            "SL Blush",
                            "SL Light Blush",
                            "Light Blush SL"
                        ],
                        "Solo Loop Black" : [
                            "Loop Black Solo",
                            "Black Solo Loop",
                            "Black Solo",
                            "Solo Black"
                        ],
                        "Solo Loop" : [
                            "Solo Loop",
                            "Loop Solo",
                            "SL"
                        ],
                        "Nike Sport Band Volt Splash" : [
                            "Nike Sport Band Volt Splash",
                            "Volt Splash Nike Sport Band",
                            "Nike Band Volt Splash",
                            "Volt Splash Nike Sport",
                            "Nike Band Volt",
                            "Volt Splash Nike",
                            "Volt Nike",
                            "Nike Volt"
                        ],
                        "Nike Sport Band Cargo Khaki" : [
                            "Nike Sport Band Cargo Khaki",
                            "Cargo Khaki Nike Sport Band",
                            "Cargo Khaki Nike Sport",
                            "Nike Band Cargo Khaki",
                            "Cargo Khaki Nike",
                            "Cargo Nike",
                            "Khaki Nike",
                            "Nike Band Cargo",
                            "Nike Khaki",
                            "Nike Cargo"
                        ],
                        "Nike Sport Band Blue Flame" : [
                            "Nike Sport Band Blue Flame",
                            "Blue Flame Nike Sport Band",
                            "Nike Band Blue Flame",
                            "Blue Flame Nike Sport",
                            "Nike Band Blue",
                            "Blue Flame Nike",
                            "Nike Blue",
                            "Blue Nike"
                        ],
                        "Nike Sport Band Magic Ember" : [
                            "Nike Sport Band Magic Ember",
                            "Nike Band Magic Ember",
                            "Magic Ember Nike Sport",
                            "Nike Band Magic",
                            "Magic Ember Nike",
                            "Nike Magic",
                            "Magic Nike"
                        ],
                        "Nike Sport Band Desert Stone" : [
                            "Nike Sport Band Desert Stone",
                            "Nike Band Desert Stone",
                            "Desert Stone Nike",
                            "Nike Band Desert",
                            "Nike Desert",
                            "Desert Nike"
                        ],
                        "Nike Sport Band Midnight Sky" : [
                            "Nike Sport Band Midnight Sky",
                            "Midnight Sky Nike Sport Band"
                            "Nike Band Midnight Sky",
                            "Midnight Sky Nike Sport",
                            "Nike Band Midnight",
                            "Midnight Sky Nike",
                            "Nike Midnight",
                            "Midnight Nike"
                        ],
                        "Nike Sport Band Pure Platinum" : [
                            "Nike Sport Band Pure Platinum",
                            "Band Pure Platinum Nike Sport",
                            "Nike Band Pure Platinum",
                            "Pure Platinum Nike Band",
                            "Nike Band Pure",
                            "Nike Pure Platinum",
                            "Nike Pure",
                            "Pure Nike"
                        ],
                        "Nike Sport Band" : [
                            "Nike Sport Band",
                            "Nike Band",
                            "Nike Sport",
                            "Nike"
                        ],
                        "Blue/Red Nike Sport Loop" : [
                            "Blue/Red Nike Sport Loop",
                            "Blue/Red Sport Loop",
                            "Blue/Red Nike Loop",
                            "Blue/Red Nike"
                        ],
                        "Grey/Blue Nike Sport Loop" : [
                            "Grey/Blue Nike Sport Loop",
                            "Grey/Blue Sport Loop",
                            "Grey/Blue Nike Loop",
                            "Grey/Blue Nike"
                        ],
                        "Black/Blue Nike Sport Loop" : [
                            "Black/Blue Nike Sport Loop",
                            "Black/Blue Sport Loop",
                            "Black/Blue Nike Loop",
                            "Black/Blue Nike"
                        ],
                        "Green/Grey Nike Sport Loop" : [
                            "Green/Grey Nike Sport Loop",
                            "Green/Grey Sport Loop",
                            "Green/Grey Nike Loop",
                            "Green/Grey Nike"
                        ],
                        "Starlight/Pink Nike Sport Loop" : [
                            "Starlight/Pink Nike Sport Loop",
                            "Starlight/Pink Sport Loop",
                            "Starlight/Pink Nike Loop",
                            "Starlight/Pink Nike"
                        ],
                        "Nike Sport Loop" : [
                            "Nike Sport Loop",
                            "Nike Loop"
                        ],
                        "Braided Solo Loop Chartreuse" : [
                            "Braided Solo Loop Chartreuse",
                            "Chartreuse Braided Solo Loop",
                            "Chartreuse Braided SL",
                            "Braided Chartreuse",
                            "Braided SL Chartreuse",
                        ],
                        "Braided Solo Loop Denim" : [
                            "Braided Solo Loop Denim",
                            "Denim Braided Solo Loop",
                            "Denim Braided SL",
                            "Braided Denim",
                            "Braided SL Denim"
                        ],
                        "Braided Solo Loop Magenta" : [
                            "Braided Solo Loop Magenta",
                            "Magenta Braided Solo Loop",
                            "Magenta Braided SL",
                            "Braided Magenta",
                            "Braided SL Magenta"
                        ],
                        "Braided Solo Loop Midnight" : [
                            "Braided Solo Loop Midnight",
                            "Midnight Braided Solo Loop",
                            "Midnight Braided SL",
                            "Braided Midnight",
                            "Braided SL Midnight"
                        ],
                        "Braided Solo Loop Lake Green" : [
                            "Braided Solo Loop Lake Green",
                            "Lake Green Braided Solo Loop",
                            "Lake Green Braided SL",
                            "Braided Lake Green",
                            "Braided SL Lake Green",
                            "Braided Solo Loop Green",
                            "Green Braided Solo Loop",
                            "Green Braided SL",
                            "Braided Green",
                            "Braided SL Green",
                        ],
                        "Braided Solo Loop Black Unity" : [
                            "Braided Solo Loop Black Unity",
                            "Black Unity Braided Solo Loop",
                            "Black Unity Braided SL",
                            "Braided Black Unity",
                            "Braided SL Black Unity"
                        ],
                        "Braided Solo Loop Pride Edition" : [
                            "Braided Solo Loop Pride Edition",
                            "Pride Edition Braided Solo Loop",
                            "Pride Edition Braided SL",
                            "Braided Pride Edition",
                            "Braided SL Pride Edition"
                        ],
                        "Braided Solo Loop Beige" : [
                            "Braided Solo Loop Beige",
                            "Beige Braided Solo Loop",
                            "Beige Braided SL",
                            "Braided Beige",
                            "Braided SL Beige"
                        ],
                        "Braided Solo Loop" : [
                            "Braided Solo Loop",
                            "Solo Loop Braided",
                            "Braided SL",
                            "SL Braided"
                        ]
                    },
                },
                "strap_size" : {
                    "values" : ["S/M", "M/L", "S", "M", "L"],
                    "aliases" : {
                        "S/M" : ["s/m", "sm"],
                        "M/L" : ["m/l", "ml"],
                        "S" : ["s"],
                        "M" : ["m"],
                        "L" : ["l"]
                    }
                }
            },
        },
        "AW S8" : {
            "aliases" : [
                "watch series 8",
                "watch series8",
                "watch s8",
                "watch s 8",
                "aw series 8",
                "series 8",
                "aw s8",
                "aw 8",
                "s8",
                "s 8",
                "aw s 8"
            ],
            "attributes" : {
                "case_size" : {
                    "values" : ["41mm", "45mm"],
                    "aliases" : {
                        "41mm" : ["41mm", "41 мм", "41"],
                        "45mm" : ["45mm", "45 мм", "45"]
                    }
                },
                "case_type" : {
                    "values" : [
                        "Midnight",
                        "Silver",
                        "Starlight",
                        "RED",
                        "Silver Stainless",
                        "Gold Stainless",
                        "Graphite Stainless"
                    ],
                    "aliases" : {
                        "Silver Stainless" : [
                            "Silver Stainless",
                            "Silver steel",
                            "Silver Stainless steel"
                        ],
                        "Gold Stainless" : [
                            "gold Stainless",
                            "gold St",
                            "gold"
                        ],
                        "Graphite Stainless" : [
                            "Graphite Stainless",
                            "Graphite st",
                            "Graphite"
                        ],
                        "Midnight" : [
                            "Midnight",
                            "Midnight aluminum"
                        ],
                        "Silver" : [
                            "silver",
                            "silver aluminum"
                        ],
                        "Starlight" : [
                            "Starlight aluminum",
                            "Starlight"
                        ],
                        "Red" : [
                            "RED PRODUCT",
                            "RED"
                        ]
                    }
                },
                "strap_type" : {
                    "values" : [
                        "Sport Band Denim",
                        "Sport Band Plum",
                        "Sport Band Lake Green",
                        "Sport Band Starlight",
                        "Sport Band Light Blush",
                        "Sport Band Stone Gray",
                        "Sport Band Black",
                        "Sport Band Pride Edition",
                        "Sport Band Black Unity",
                        "Sport Band Midnight",
                        "Sport Band",
                        "Sport Loop Blue Cloud",
                        "Sport Loop Lake Green",
                        "Sport Loop Plum",
                        "Sport Loop Ink",
                        "Sport Loop Black",
                        "Sport Loop Midnight",
                        "Sport Loop Ultramarine",
                        "Sport Loop Black Unity",
                        "Sport Loop",
                        "Natural Titanium Milanese Loop",
                        "Black Titanium Milanese Loop",
                        "Milanese Loop",
                        "Solo Loop Lake Green",
                        "Solo Loop Ultramarine",
                        "Solo Loop Star Fruit",
                        "Solo Loop Light Blush",
                        "Solo Loop Black",
                        "Solo Loop",
                        "Nike Sport Band Volt Splash",
                        "Nike Sport Band Cargo Khaki",
                        "Nike Sport Band Blue Flame",
                        "Nike Sport Band Magic Ember",
                        "Nike Sport Band Desert Stone",
                        "Nike Sport Band Midnight Sky",
                        "Nike Sport Band Pure Platinum",
                        "Nike Sport Band",
                        "Blue/Red Nike Sport Loop",
                        "Grey/Blue Nike Sport Loop",
                        "Black/Blue Nike Sport Loop",
                        "Green/Grey Nike Sport Loop",
                        "Starlight/Pink Nike Sport Loop",
                        "Nike Sport Loop",
                        "Braided Solo Loop Chartreuse",
                        "Braided Solo Loop Denim",
                        "Braided Solo Loop Magenta",
                        "Braided Solo Loop Midnight",
                        "Braided Solo Loop Lake Green",
                        "Braided Solo Loop Black Unity",
                        "Braided Solo Loop Pride Edition",
                        "Braided Solo Loop Beige",
                        "Braided Solo Loop",
                        "Link Bracelet Natural",
                        "Link Bracelet Gold",
                        "Link Bracelet Slate",
                        "Link Bracelet"
                    ],
                    "aliases" : {
                        "Sport Band Denim" : [
                            "Sport Band Denim",
                            "Denim Sport Band",
                            "Denim SB",
                            "SB Denim",
                            "Denim"
                        ],
                        "Sport Band Plum" : [
                            "Sport Band Plum",
                            "Band Plum Sport",
                            "Plum Sport Band",
                            "Plum SB",
                            "SB Plum",
                            "Sport Plum"
                        ],
                        "Sport Band Lake Green" : [
                            "Lake Green Sport Band",
                            "Sport Band Lake Green",
                            "Green Sport Band",
                            "Sport Band Green",
                            "Green Band",
                            "Green SB",
                            "SB Green",
                            "Lake Green SB",
                            "SB Lake Green"
                        ],
                        "Sport Band Starlight" : [
                            "Sport Band Starlight",
                            "Starlight Sport Band",
                            "Starlight Band",
                            "Starlight SB",
                            "SB Starlight"
                        ],
                        "Sport Band Light Blush" : [
                            "Sport Band Light Blush",
                            "Light Blush Sport Band",
                            "Sport Band Light",
                            "Sport Band Blush",
                            "Light Blush SB",
                            "SB Light Blush",
                            "Light Blush",
                            "MWWH3",
                            "MWWU3",
                            "MWWJ3",
                            "U3LW",
                            "Blush",
                            "LB",
                            "LB SB"
                        ],
                        "Sport Band Stone Gray" : [
                            "Sport Band Stone Gray",
                            "Stone Gray Sport Band",
                            "Sport Band Stone",
                            "Sport Band Gray",
                            "Stone Gray SB",
                            "SB Stone Gray",
                            "Stone Gray",
                            "Gray SB",
                            "SB Gray",
                            "Gray",
                            "Grey"
                        ],
                        "Sport Band Black" : [
                            "Sport Band Black",
                            "Black Sport Band",
                            "Black Band",
                            "SB Black",
                            "Black SB",
                            "Q3LW",
                            "MWWE3",
                            "MWWP3",
                            "MWWF3"
                        ],
                        "Sport Band Pride Edition" : [
                            "Sport Band Pride Edition",
                            "Pride Edition Sport Band",
                            "Sport Band Pride",
                            "Sport Band Edition",
                            "Pride Edition",
                            "Pride SB",
                            "SB Pride",
                            "Pride"
                        ],
                        "Sport Band Black Unity" : [
                            "Sport Band Black Unity",
                            "Black Unity Sport Band",
                            "Sport Band Black",
                            "Sport Band Unity",
                            "Black Unity Band",
                            "Black Unity SB",
                            "SB Black Unity",
                            "Black Unity SB"
                        ],
                        "Sport Band Midnight" : [
                            "Sport Band Midnight",
                            "Midnight Sport Band",
                            "Midnight Band",
                            "Midnight SB",
                            "SB Midnight"
                        ],
                        "Sport Band" : [
                            "Sport Band",
                            "Sport",
                            "SB"
                        ],
                        "Sport Loop Blue Cloud" : [
                            "Sport Loop Blue Cloud",
                            "Blue Cloud Sport Loop",
                            "Sport Loop Blue",
                            "Blue Sport Loop",
                            "Blue Loop",
                            "Blue SL",
                            "SL Blue",
                            "Blue Cloud SL",
                            "SL Blue Cloud",
                            "Blue"
                        ],
                        "Sport Loop Lake Green" : [
                            "Sport Loop Lake Green",
                            "Lake Green Sport Loop",
                            "Sport Loop Green",
                            "Green Sport Loop",
                            "Green Loop",
                            "Lake Green SL",
                            "SL Lake Green",
                            "SL Green",
                            "Green SL"
                        ],
                        "Sport Loop Plum" : [
                            "Sport Loop Plum",
                            "Plum Sport Loop",
                            "Loop Plum",
                            "Plum Loop",
                            "SL Plum",
                            "Plum SL"
                        ],
                        "Sport Loop Ink" : [
                            "Sport Loop Ink",
                            "Ink Sport Loop",
                            "Ink Loop",
                            "Ink SL",
                            "SL Ink"
                        ],
                        "Sport Loop Black" : [
                            "Sport Loop Black",
                            "Black Sport Loop",
                            "Black Loop",
                            "Black SL",
                            "SL Black"
                        ],
                        "Sport Loop Midnight" : [
                            "Sport Loop Midnight",
                            "Midnight Sport Loop",
                            "Midnight Loop",
                            "Midnight SL",
                            "SL Midnight"
                        ],
                        "Sport Loop Ultramarine" : [
                            "Sport Loop Ultramarine",
                            "Ultramarine Sport Loop",
                            "Ultramarine Loop",
                            "Ultramarine Sport",
                            "SL Ultramarine",
                            "Ultramarine SL"
                        ],
                        "Sport Loop Black Unity" : [
                            "Sport Loop Black Unity",
                            "Black Unity Sport Loop",
                            "Sport Loop Black",
                            "Sport Loop Unity",
                            "Black Sport Loop",
                            "Black Loop",
                            "SL Black Unity",
                            "Black Unity SL"
                        ],
                        "Sport Loop" : [
                            "Sport Loop",
                            "Loop",
                            "SL"
                        ],
                        "Natural Titanium Milanese Loop" : [
                            "Natural Titanium Milanese Loop",
                            "Natural Milanese Loop",
                            "Natural Milanese"
                        ],
                        "Black Titanium Milanese Loop" : [
                            "Black Titanium Milanese Loop",
                            "Black Milanese Loop",
                            "Black Milanese"
                        ],
                        "Milanese Loop" : [
                            "milanese loop",
                            "milanese",
                            "Mil LP"
                        ],
                        "Solo Loop Lake Green" : [
                            "Solo Loop Lake Green",
                            "Lake Green Solo Loop",
                            "Solo Loop Green",
                            "Green Solo Loop",
                        ],
                        "Solo Loop Ultramarine" : [
                            "Solo Loop Ultramarine",
                            "Ultramarine Solo Loop",
                        ],
                        "Solo Loop Star Fruit" : [
                            "Solo Loop Star Fruit",
                            "Star Fruit Solo Loop",
                            "Solo Loop Star",
                            "Solo Loop Fruit",
                            "Star Fruit Loop",
                            "SL Star Fruit",
                            "Star Fruit SL",
                            "SL Star",
                            "SL Fruit",
                            "SL Star Fruit",
                            "SL Star Fruit"
                            "Star Fruit Loop"
                        ],
                        "Solo Loop Light Blush" : [
                            "Solo Loop Light Blush",
                            "Light Blush Solo Loop",
                            "Solo Loop Light",
                            "Solo Loop Blush",
                            "SL Light Blush",
                            "Light Blush SL",
                            "SL Light",
                            "SL Blush",
                            "SL Light Blush",
                            "Light Blush SL"
                        ],
                        "Solo Loop Black" : [
                            "Loop Black Solo",
                            "Black Solo Loop",
                            "Black Solo",
                            "Solo Black"
                        ],
                        "Solo Loop" : [
                            "Solo Loop",
                            "Loop Solo",
                            "SL"
                        ],
                        "Nike Sport Band Volt Splash" : [
                            "Nike Sport Band Volt Splash",
                            "Volt Splash Nike Sport Band",
                            "Nike Band Volt Splash",
                            "Volt Splash Nike Sport",
                            "Nike Band Volt",
                            "Volt Splash Nike",
                            "Volt Nike",
                            "Nike Volt"
                        ],
                        "Nike Sport Band Cargo Khaki" : [
                            "Nike Sport Band Cargo Khaki",
                            "Cargo Khaki Nike Sport Band",
                            "Cargo Khaki Nike Sport",
                            "Nike Band Cargo Khaki",
                            "Cargo Khaki Nike",
                            "Cargo Nike",
                            "Khaki Nike",
                            "Nike Band Cargo",
                            "Nike Khaki",
                            "Nike Cargo"
                        ],
                        "Nike Sport Band Blue Flame" : [
                            "Nike Sport Band Blue Flame",
                            "Blue Flame Nike Sport Band",
                            "Nike Band Blue Flame",
                            "Blue Flame Nike Sport",
                            "Nike Band Blue",
                            "Blue Flame Nike",
                            "Nike Blue",
                            "Blue Nike"
                        ],
                        "Nike Sport Band Magic Ember" : [
                            "Nike Sport Band Magic Ember",
                            "Nike Band Magic Ember",
                            "Magic Ember Nike Sport",
                            "Nike Band Magic",
                            "Magic Ember Nike",
                            "Nike Magic",
                            "Magic Nike"
                        ],
                        "Nike Sport Band Desert Stone" : [
                            "Nike Sport Band Desert Stone",
                            "Nike Band Desert Stone",
                            "Desert Stone Nike",
                            "Nike Band Desert",
                            "Nike Desert",
                            "Desert Nike"
                        ],
                        "Nike Sport Band Midnight Sky" : [
                            "Nike Sport Band Midnight Sky",
                            "Midnight Sky Nike Sport Band"
                            "Nike Band Midnight Sky",
                            "Midnight Sky Nike Sport",
                            "Nike Band Midnight",
                            "Midnight Sky Nike",
                            "Nike Midnight",
                            "Midnight Nike"
                        ],
                        "Nike Sport Band Pure Platinum" : [
                            "Nike Sport Band Pure Platinum",
                            "Band Pure Platinum Nike Sport",
                            "Nike Band Pure Platinum",
                            "Pure Platinum Nike Band",
                            "Nike Band Pure",
                            "Nike Pure Platinum",
                            "Nike Pure",
                            "Pure Nike"
                        ],
                        "Nike Sport Band" : [
                            "Nike Sport Band",
                            "Nike Band",
                            "Nike Sport",
                            "Nike"
                        ],
                        "Blue/Red Nike Sport Loop" : [
                            "Blue/Red Nike Sport Loop",
                            "Blue/Red Sport Loop",
                            "Blue/Red Nike Loop",
                            "Blue/Red Nike"
                        ],
                        "Grey/Blue Nike Sport Loop" : [
                            "Grey/Blue Nike Sport Loop",
                            "Grey/Blue Sport Loop",
                            "Grey/Blue Nike Loop",
                            "Grey/Blue Nike"
                        ],
                        "Black/Blue Nike Sport Loop" : [
                            "Black/Blue Nike Sport Loop",
                            "Black/Blue Sport Loop",
                            "Black/Blue Nike Loop",
                            "Black/Blue Nike"
                        ],
                        "Green/Grey Nike Sport Loop" : [
                            "Green/Grey Nike Sport Loop",
                            "Green/Grey Sport Loop",
                            "Green/Grey Nike Loop",
                            "Green/Grey Nike"
                        ],
                        "Starlight/Pink Nike Sport Loop" : [
                            "Starlight/Pink Nike Sport Loop",
                            "Starlight/Pink Sport Loop",
                            "Starlight/Pink Nike Loop",
                            "Starlight/Pink Nike"
                        ],
                        "Nike Sport Loop" : [
                            "Nike Sport Loop",
                            "Nike Loop"
                        ],
                        "Braided Solo Loop Chartreuse" : [
                            "Braided Solo Loop Chartreuse",
                            "Chartreuse Braided Solo Loop",
                            "Chartreuse Braided SL",
                            "Braided Chartreuse",
                            "Braided SL Chartreuse",
                        ],
                        "Braided Solo Loop Denim" : [
                            "Braided Solo Loop Denim",
                            "Denim Braided Solo Loop",
                            "Denim Braided SL",
                            "Braided Denim",
                            "Braided SL Denim"
                        ],
                        "Braided Solo Loop Magenta" : [
                            "Braided Solo Loop Magenta",
                            "Magenta Braided Solo Loop",
                            "Magenta Braided SL",
                            "Braided Magenta",
                            "Braided SL Magenta"
                        ],
                        "Braided Solo Loop Midnight" : [
                            "Braided Solo Loop Midnight",
                            "Midnight Braided Solo Loop",
                            "Midnight Braided SL",
                            "Braided Midnight",
                            "Braided SL Midnight"
                        ],
                        "Braided Solo Loop Lake Green" : [
                            "Braided Solo Loop Lake Green",
                            "Lake Green Braided Solo Loop",
                            "Lake Green Braided SL",
                            "Braided Lake Green",
                            "Braided SL Lake Green",
                            "Braided Solo Loop Green",
                            "Green Braided Solo Loop",
                            "Green Braided SL",
                            "Braided Green",
                            "Braided SL Green",
                        ],
                        "Braided Solo Loop Black Unity" : [
                            "Braided Solo Loop Black Unity",
                            "Black Unity Braided Solo Loop",
                            "Black Unity Braided SL",
                            "Braided Black Unity",
                            "Braided SL Black Unity"
                        ],
                        "Braided Solo Loop Pride Edition" : [
                            "Braided Solo Loop Pride Edition",
                            "Pride Edition Braided Solo Loop",
                            "Pride Edition Braided SL",
                            "Braided Pride Edition",
                            "Braided SL Pride Edition"
                        ],
                        "Braided Solo Loop Beige" : [
                            "Braided Solo Loop Beige",
                            "Beige Braided Solo Loop",
                            "Beige Braided SL",
                            "Braided Beige",
                            "Braided SL Beige"
                        ],
                        "Braided Solo Loop" : [
                            "Braided Solo Loop",
                            "Solo Loop Braided",
                            "Braided SL",
                            "SL Braided"
                        ],
                        "Link Bracelet Natural" : [
                            "Link Bracelet Natural",
                            "Natural Link Bracelet"
                            "Link Natural",
                            "Natural Link"
                        ],
                        "Link Bracelet Slate" : [
                            "Link Bracelet Slate",
                            "Slate Link Bracelet"
                            "Link Slate",
                            "Slate Link"
                        ],
                        "Link Bracelet Gold" : [
                            "Link Bracelet Gold",
                            "Gold Link Bracelet"
                            "Link Gold",
                            "Gold Link"
                        ],
                        "Link Bracelet" : [
                            "Link Bracelet",
                            "Link"
                        ]
                    },
                },
                "strap_size" : {
                    "values" : ["S/M", "M/L", "S", "M", "L"],
                    "aliases" : {
                        "S/M" : ["s/m", "sm"],
                        "M/L" : ["m/l", "ml"],
                        "S" : ["s"],
                        "M" : ["m"],
                        "L" : ["l"]
                    }
                }
            },
        },
        "AW S9" : {
            "aliases" : [
                "watch series 9",
                "watch series9",
                "watch s9",
                "watch s 9",
                "aw series 9",
                "series 9",
                "aw s9",
                "aw 9",
                "s9",
                "s 9",
                "aw s 9"
            ],
            "attributes" : {
                "case_size" : {
                    "values" : ["41mm", "45mm"],
                    "aliases" : {
                        "41mm" : ["41mm", "41 мм", "41"],
                        "45mm" : ["45mm", "45 мм", "45"]
                    }
                },
                "case_type" : {
                    "values" : [
                        "Midnight",
                        "Silver",
                        "Starlight",
                        "Pink",
                        "RED",
                        "Silver Stainless",
                        "Gold Stainless",
                        "Graphite Stainless",
                    ],
                    "aliases" : {
                        "Silver Stainless" : [
                            "Silver Stainless",
                            "Silver steel",
                            "Silver Stainless steel"
                        ],
                        "Gold Stainless" : [
                            "gold Stainless",
                            "gold St",
                            "gold"
                        ],
                        "Graphite Stainless" : [
                            "Graphite Stainless",
                            "Graphite st",
                            "Graphite"
                        ],
                        "Pink" : [
                            "Pink aluminum",
                            "Pink"
                        ],
                        "Midnight" : [
                            "Midnight",
                            "Midnight aluminum"
                        ],
                        "Silver" : [
                            "silver",
                            "silver aluminum"
                        ],
                        "Starlight" : [
                            "Starlight aluminum",
                            "Starlight"
                        ],
                        "Red" : [
                            "RED PRODUCT",
                            "RED"
                        ]
                    }
                },
                "strap_type" : {
                    "values" : [
                        "Sport Band Denim",
                        "Sport Band Plum",
                        "Sport Band Lake Green",
                        "Sport Band Starlight",
                        "Sport Band Light Blush",
                        "Sport Band Stone Gray",
                        "Sport Band Black",
                        "Sport Band Pride Edition",
                        "Sport Band Black Unity",
                        "Sport Band Midnight",
                        "Sport Band",
                        "Sport Loop Blue Cloud",
                        "Sport Loop Lake Green",
                        "Sport Loop Plum",
                        "Sport Loop Ink",
                        "Sport Loop Black",
                        "Sport Loop Midnight",
                        "Sport Loop Ultramarine",
                        "Sport Loop Black Unity",
                        "Sport Loop",
                        "Natural Titanium Milanese Loop",
                        "Black Titanium Milanese Loop",
                        "Milanese Loop",
                        "Solo Loop Lake Green",
                        "Solo Loop Ultramarine",
                        "Solo Loop Star Fruit",
                        "Solo Loop Light Blush",
                        "Solo Loop Black",
                        "Solo Loop",
                        "Nike Sport Band Volt Splash",
                        "Nike Sport Band Cargo Khaki",
                        "Nike Sport Band Blue Flame",
                        "Nike Sport Band Magic Ember",
                        "Nike Sport Band Desert Stone",
                        "Nike Sport Band Midnight Sky",
                        "Nike Sport Band Pure Platinum",
                        "Nike Sport Band",
                        "Blue/Red Nike Sport Loop",
                        "Grey/Blue Nike Sport Loop",
                        "Black/Blue Nike Sport Loop",
                        "Green/Grey Nike Sport Loop",
                        "Starlight/Pink Nike Sport Loop",
                        "Nike Sport Loop",
                        "Braided Solo Loop Chartreuse",
                        "Braided Solo Loop Denim",
                        "Braided Solo Loop Magenta",
                        "Braided Solo Loop Midnight",
                        "Braided Solo Loop Lake Green",
                        "Braided Solo Loop Black Unity",
                        "Braided Solo Loop Pride Edition",
                        "Braided Solo Loop Beige",
                        "Braided Solo Loop",
                        "Link Bracelet Natural",
                        "Link Bracelet Gold",
                        "Link Bracelet Slate",
                        "Link Bracelet"
                    ],
                    "aliases" : {
                        "Sport Band Denim" : [
                            "Sport Band Denim",
                            "Denim Sport Band",
                            "Denim SB",
                            "SB Denim",
                            "Denim"
                        ],
                        "Sport Band Plum" : [
                            "Sport Band Plum",
                            "Band Plum Sport",
                            "Plum Sport Band",
                            "Plum SB",
                            "SB Plum",
                            "Sport Plum"
                        ],
                        "Sport Band Lake Green" : [
                            "Lake Green Sport Band",
                            "Sport Band Lake Green",
                            "Green Sport Band",
                            "Sport Band Green",
                            "Green Band",
                            "Green SB",
                            "SB Green",
                            "Lake Green SB",
                            "SB Lake Green"
                        ],
                        "Sport Band Starlight" : [
                            "Sport Band Starlight",
                            "Starlight Sport Band",
                            "Starlight Band",
                            "Starlight SB",
                            "SB Starlight"
                        ],
                        "Sport Band Light Blush" : [
                            "Sport Band Light Blush",
                            "Light Blush Sport Band",
                            "Sport Band Light",
                            "Sport Band Blush",
                            "Light Blush SB",
                            "SB Light Blush",
                            "Light Blush",
                            "MWWH3",
                            "MWWU3",
                            "MWWJ3",
                            "U3LW",
                            "Blush",
                            "LB",
                            "LB SB"
                        ],
                        "Sport Band Stone Gray" : [
                            "Sport Band Stone Gray",
                            "Stone Gray Sport Band",
                            "Sport Band Stone",
                            "Sport Band Gray",
                            "Stone Gray SB",
                            "SB Stone Gray",
                            "Stone Gray",
                            "Gray SB",
                            "SB Gray",
                            "Gray",
                            "Grey"
                        ],
                        "Sport Band Black" : [
                            "Sport Band Black",
                            "Black Sport Band",
                            "Black Band",
                            "SB Black",
                            "Black SB",
                            "Q3LW",
                            "MWWE3",
                            "MWWP3",
                            "MWWF3"
                        ],
                        "Sport Band Pride Edition" : [
                            "Sport Band Pride Edition",
                            "Pride Edition Sport Band",
                            "Sport Band Pride",
                            "Sport Band Edition",
                            "Pride Edition",
                            "Pride SB",
                            "SB Pride",
                            "Pride"
                        ],
                        "Sport Band Black Unity" : [
                            "Sport Band Black Unity",
                            "Black Unity Sport Band",
                            "Sport Band Black",
                            "Sport Band Unity",
                            "Black Unity Band",
                            "Black Unity SB",
                            "SB Black Unity",
                            "Black Unity SB"
                        ],
                        "Sport Band Midnight" : [
                            "Sport Band Midnight",
                            "Midnight Sport Band",
                            "Midnight Band",
                            "Midnight SB",
                            "SB Midnight"
                        ],
                        "Sport Band" : [
                            "Sport Band",
                            "Sport",
                            "SB"
                        ],
                        "Sport Loop Blue Cloud" : [
                            "Sport Loop Blue Cloud",
                            "Blue Cloud Sport Loop",
                            "Sport Loop Blue",
                            "Blue Sport Loop",
                            "Blue Loop",
                            "Blue SL",
                            "SL Blue",
                            "Blue Cloud SL",
                            "SL Blue Cloud",
                            "Blue"
                        ],
                        "Sport Loop Lake Green" : [
                            "Sport Loop Lake Green",
                            "Lake Green Sport Loop",
                            "Sport Loop Green",
                            "Green Sport Loop",
                            "Green Loop",
                            "Lake Green SL",
                            "SL Lake Green",
                            "SL Green",
                            "Green SL"
                        ],
                        "Sport Loop Plum" : [
                            "Sport Loop Plum",
                            "Plum Sport Loop",
                            "Loop Plum",
                            "Plum Loop",
                            "SL Plum",
                            "Plum SL"
                        ],
                        "Sport Loop Ink" : [
                            "Sport Loop Ink",
                            "Ink Sport Loop",
                            "Ink Loop",
                            "Ink SL",
                            "SL Ink"
                        ],
                        "Sport Loop Black" : [
                            "Sport Loop Black",
                            "Black Sport Loop",
                            "Black Loop",
                            "Black SL",
                            "SL Black"
                        ],
                        "Sport Loop Midnight" : [
                            "Sport Loop Midnight",
                            "Midnight Sport Loop",
                            "Midnight Loop",
                            "Midnight SL",
                            "SL Midnight"
                        ],
                        "Sport Loop Ultramarine" : [
                            "Sport Loop Ultramarine",
                            "Ultramarine Sport Loop",
                            "Ultramarine Loop",
                            "Ultramarine Sport",
                            "SL Ultramarine",
                            "Ultramarine SL"
                        ],
                        "Sport Loop Black Unity" : [
                            "Sport Loop Black Unity",
                            "Black Unity Sport Loop",
                            "Sport Loop Black",
                            "Sport Loop Unity",
                            "Black Sport Loop",
                            "Black Loop",
                            "SL Black Unity",
                            "Black Unity SL"
                        ],
                        "Sport Loop" : [
                            "Sport Loop",
                            "Loop",
                            "SL"
                        ],
                        "Natural Titanium Milanese Loop" : [
                            "Natural Titanium Milanese Loop",
                            "Natural Milanese Loop",
                            "Natural Milanese"
                        ],
                        "Black Titanium Milanese Loop" : [
                            "Black Titanium Milanese Loop",
                            "Black Milanese Loop",
                            "Black Milanese"
                        ],
                        "Milanese Loop" : [
                            "milanese loop",
                            "milanese",
                            "Mil LP"
                        ],
                        "Solo Loop Lake Green" : [
                            "Solo Loop Lake Green",
                            "Lake Green Solo Loop",
                            "Solo Loop Green",
                            "Green Solo Loop",
                        ],
                        "Solo Loop Ultramarine" : [
                            "Solo Loop Ultramarine",
                            "Ultramarine Solo Loop",
                        ],
                        "Solo Loop Star Fruit" : [
                            "Solo Loop Star Fruit",
                            "Star Fruit Solo Loop",
                            "Solo Loop Star",
                            "Solo Loop Fruit",
                            "Star Fruit Loop",
                            "SL Star Fruit",
                            "Star Fruit SL",
                            "SL Star",
                            "SL Fruit",
                            "SL Star Fruit",
                            "SL Star Fruit"
                            "Star Fruit Loop"
                        ],
                        "Solo Loop Light Blush" : [
                            "Solo Loop Light Blush",
                            "Light Blush Solo Loop",
                            "Solo Loop Light",
                            "Solo Loop Blush",
                            "SL Light Blush",
                            "Light Blush SL",
                            "SL Light",
                            "SL Blush",
                            "SL Light Blush",
                            "Light Blush SL"
                        ],
                        "Solo Loop Black" : [
                            "Loop Black Solo",
                            "Black Solo Loop",
                            "Black Solo",
                            "Solo Black"
                        ],
                        "Solo Loop" : [
                            "Solo Loop",
                            "Loop Solo",
                            "SL"
                        ],
                        "Nike Sport Band Volt Splash" : [
                            "Nike Sport Band Volt Splash",
                            "Volt Splash Nike Sport Band",
                            "Nike Band Volt Splash",
                            "Volt Splash Nike Sport",
                            "Nike Band Volt",
                            "Volt Splash Nike",
                            "Volt Nike",
                            "Nike Volt"
                        ],
                        "Nike Sport Band Cargo Khaki" : [
                            "Nike Sport Band Cargo Khaki",
                            "Cargo Khaki Nike Sport Band",
                            "Cargo Khaki Nike Sport",
                            "Nike Band Cargo Khaki",
                            "Cargo Khaki Nike",
                            "Cargo Nike",
                            "Khaki Nike",
                            "Nike Band Cargo",
                            "Nike Khaki",
                            "Nike Cargo"
                        ],
                        "Nike Sport Band Blue Flame" : [
                            "Nike Sport Band Blue Flame",
                            "Blue Flame Nike Sport Band",
                            "Nike Band Blue Flame",
                            "Blue Flame Nike Sport",
                            "Nike Band Blue",
                            "Blue Flame Nike",
                            "Nike Blue",
                            "Blue Nike"
                        ],
                        "Nike Sport Band Magic Ember" : [
                            "Nike Sport Band Magic Ember",
                            "Nike Band Magic Ember",
                            "Magic Ember Nike Sport",
                            "Nike Band Magic",
                            "Magic Ember Nike",
                            "Nike Magic",
                            "Magic Nike"
                        ],
                        "Nike Sport Band Desert Stone" : [
                            "Nike Sport Band Desert Stone",
                            "Nike Band Desert Stone",
                            "Desert Stone Nike",
                            "Nike Band Desert",
                            "Nike Desert",
                            "Desert Nike"
                        ],
                        "Nike Sport Band Midnight Sky" : [
                            "Nike Sport Band Midnight Sky",
                            "Midnight Sky Nike Sport Band"
                            "Nike Band Midnight Sky",
                            "Midnight Sky Nike Sport",
                            "Nike Band Midnight",
                            "Midnight Sky Nike",
                            "Nike Midnight",
                            "Midnight Nike"
                        ],
                        "Nike Sport Band Pure Platinum" : [
                            "Nike Sport Band Pure Platinum",
                            "Band Pure Platinum Nike Sport",
                            "Nike Band Pure Platinum",
                            "Pure Platinum Nike Band",
                            "Nike Band Pure",
                            "Nike Pure Platinum",
                            "Nike Pure",
                            "Pure Nike"
                        ],
                        "Nike Sport Band" : [
                            "Nike Sport Band",
                            "Nike Band",
                            "Nike Sport",
                            "Nike"
                        ],
                        "Blue/Red Nike Sport Loop" : [
                            "Blue/Red Nike Sport Loop",
                            "Blue/Red Sport Loop",
                            "Blue/Red Nike Loop",
                            "Blue/Red Nike"
                        ],
                        "Grey/Blue Nike Sport Loop" : [
                            "Grey/Blue Nike Sport Loop",
                            "Grey/Blue Sport Loop",
                            "Grey/Blue Nike Loop",
                            "Grey/Blue Nike"
                        ],
                        "Black/Blue Nike Sport Loop" : [
                            "Black/Blue Nike Sport Loop",
                            "Black/Blue Sport Loop",
                            "Black/Blue Nike Loop",
                            "Black/Blue Nike"
                        ],
                        "Green/Grey Nike Sport Loop" : [
                            "Green/Grey Nike Sport Loop",
                            "Green/Grey Sport Loop",
                            "Green/Grey Nike Loop",
                            "Green/Grey Nike"
                        ],
                        "Starlight/Pink Nike Sport Loop" : [
                            "Starlight/Pink Nike Sport Loop",
                            "Starlight/Pink Sport Loop",
                            "Starlight/Pink Nike Loop",
                            "Starlight/Pink Nike"
                        ],
                        "Nike Sport Loop" : [
                            "Nike Sport Loop",
                            "Nike Loop"
                        ],
                        "Braided Solo Loop Chartreuse" : [
                            "Braided Solo Loop Chartreuse",
                            "Chartreuse Braided Solo Loop",
                            "Chartreuse Braided SL",
                            "Braided Chartreuse",
                            "Braided SL Chartreuse",
                        ],
                        "Braided Solo Loop Denim" : [
                            "Braided Solo Loop Denim",
                            "Denim Braided Solo Loop",
                            "Denim Braided SL",
                            "Braided Denim",
                            "Braided SL Denim"
                        ],
                        "Braided Solo Loop Magenta" : [
                            "Braided Solo Loop Magenta",
                            "Magenta Braided Solo Loop",
                            "Magenta Braided SL",
                            "Braided Magenta",
                            "Braided SL Magenta"
                        ],
                        "Braided Solo Loop Midnight" : [
                            "Braided Solo Loop Midnight",
                            "Midnight Braided Solo Loop",
                            "Midnight Braided SL",
                            "Braided Midnight",
                            "Braided SL Midnight"
                        ],
                        "Braided Solo Loop Lake Green" : [
                            "Braided Solo Loop Lake Green",
                            "Lake Green Braided Solo Loop",
                            "Lake Green Braided SL",
                            "Braided Lake Green",
                            "Braided SL Lake Green",
                            "Braided Solo Loop Green",
                            "Green Braided Solo Loop",
                            "Green Braided SL",
                            "Braided Green",
                            "Braided SL Green",
                        ],
                        "Braided Solo Loop Black Unity" : [
                            "Braided Solo Loop Black Unity",
                            "Black Unity Braided Solo Loop",
                            "Black Unity Braided SL",
                            "Braided Black Unity",
                            "Braided SL Black Unity"
                        ],
                        "Braided Solo Loop Pride Edition" : [
                            "Braided Solo Loop Pride Edition",
                            "Pride Edition Braided Solo Loop",
                            "Pride Edition Braided SL",
                            "Braided Pride Edition",
                            "Braided SL Pride Edition"
                        ],
                        "Braided Solo Loop Beige" : [
                            "Braided Solo Loop Beige",
                            "Beige Braided Solo Loop",
                            "Beige Braided SL",
                            "Braided Beige",
                            "Braided SL Beige"
                        ],
                        "Braided Solo Loop" : [
                            "Braided Solo Loop",
                            "Solo Loop Braided",
                            "Braided SL",
                            "SL Braided"
                        ],
                        "Link Bracelet Natural" : [
                            "Link Bracelet Natural",
                            "Natural Link Bracelet"
                            "Link Natural",
                            "Natural Link"
                        ],
                        "Link Bracelet Slate" : [
                            "Link Bracelet Slate",
                            "Slate Link Bracelet"
                            "Link Slate",
                            "Slate Link"
                        ],
                        "Link Bracelet Gold" : [
                            "Link Bracelet Gold",
                            "Gold Link Bracelet"
                            "Link Gold",
                            "Gold Link"
                        ],
                        "Link Bracelet" : [
                            "Link Bracelet",
                            "Link"
                        ]
                    },
                },
                "strap_size" : {
                    "values" : ["S/M", "M/L", "S", "M", "L"],
                    "aliases" : {
                        "S/M" : ["s/m", "sm"],
                        "M/L" : ["m/l", "ml"],
                        "S" : ["s"],
                        "M" : ["m"],
                        "L" : ["l"]
                    }
                }
            },
        },
        "AW S10" : {
            "aliases" : [
                "watch series 10",
                "watch series10",
                "watch s10",
                "watch s 10",
                "aw series 10",
                "series 10",
                "aw s10",
                "aw 10",
                "s10",
                "s 10",
                "aw s 10",
                "10"
            ],
            "attributes" : {
                "case_size" : {
                    "values" : ["42mm", "46mm"],
                    "aliases" : {
                        "42mm" : ["42mm", "42 мм", "42"],
                        "46mm" : ["46mm", "46 мм", "46"]
                    }
                },
                "case_type" : {
                    "values" : [
                        "Jet Black",
                        "Rose Gold",
                        "Silver",
                        "Slate Titanium",
                        "Gold Titanium",
                        "Natural Titanium",
                        "Silver Titanium Hermes"
                    ],
                    "aliases" : {
                        "Slate Titanium" : [
                            "slate titanium",
                            "slate ti",
                            "slate"
                        ],
                        "Gold Titanium" : [
                            "gold titanium",
                            "gold ti",
                            "gold"
                        ],
                        "Natural Titanium" : [
                            "natural titanium",
                            "natural ti",
                            "natural"
                        ],
                        "Silver Titanium Hermes" : [
                            "Silver Titanium Hermes",
                            "Silver Ti Hermes",
                            "Silver Hermes",
                            "Hermes"
                        ],
                        "Jet Black" : [
                            "jet black",
                            "black",
                            "jet black aluminum",
                            "black aluminum"
                        ],
                        "Rose Gold" : [
                            "rose",
                            "rose gold",
                            "rose gold aluminum"
                        ],
                        "Silver" : [
                            "silver",
                            "silver aluminum"
                        ]
                    }
                },
                "strap_type" : {
                    "values" : [
                        "Sport Band Denim",
                        "Sport Band Plum",
                        "Sport Band Lake Green",
                        "Sport Band Starlight",
                        "Sport Band Light Blush",
                        "Sport Band Stone Gray",
                        "Sport Band Black",
                        "Sport Band Pride Edition",
                        "Sport Band Black Unity",
                        "Sport Band Midnight",
                        "Sport Band",
                        "Sport Loop Blue Cloud",
                        "Sport Loop Lake Green",
                        "Sport Loop Plum",
                        "Sport Loop Ink",
                        "Sport Loop Black",
                        "Sport Loop Midnight",
                        "Sport Loop Ultramarine",
                        "Sport Loop Black Unity",
                        "Sport Loop",
                        "Natural Titanium Milanese Loop",
                        "Black Titanium Milanese Loop",
                        "Milanese Loop",
                        "Solo Loop Lake Green",
                        "Solo Loop Ultramarine",
                        "Solo Loop Star Fruit",
                        "Solo Loop Light Blush",
                        "Solo Loop Black",
                        "Solo Loop",
                        "Nike Sport Band Volt Splash",
                        "Nike Sport Band Cargo Khaki",
                        "Nike Sport Band Blue Flame",
                        "Nike Sport Band Magic Ember",
                        "Nike Sport Band Desert Stone",
                        "Nike Sport Band Midnight Sky",
                        "Nike Sport Band Pure Platinum",
                        "Nike Sport Band",
                        "Blue/Red Nike Sport Loop",
                        "Grey/Blue Nike Sport Loop",
                        "Black/Blue Nike Sport Loop",
                        "Green/Grey Nike Sport Loop",
                        "Starlight/Pink Nike Sport Loop",
                        "Nike Sport Loop",
                        "Braided Solo Loop Chartreuse",
                        "Braided Solo Loop Denim",
                        "Braided Solo Loop Magenta",
                        "Braided Solo Loop Midnight",
                        "Braided Solo Loop Lake Green",
                        "Braided Solo Loop Black Unity",
                        "Braided Solo Loop Pride Edition",
                        "Braided Solo Loop Beige",
                        "Braided Solo Loop",
                        "Link Bracelet Natural",
                        "Link Bracelet Gold",
                        "Link Bracelet Slate",
                        "Link Bracelet"
                    ],
                    "aliases" : {
                        "Sport Band Denim" : [
                            "Sport Band Denim",
                            "Denim Sport Band",
                            "Denim SB",
                            "SB Denim",
                            "Denim"
                        ],
                        "Sport Band Plum" : [
                            "Sport Band Plum",
                            "Band Plum Sport",
                            "Plum Sport Band",
                            "Plum SB",
                            "SB Plum",
                            "Sport Plum"
                        ],
                        "Sport Band Lake Green" : [
                            "Lake Green Sport Band",
                            "Sport Band Lake Green",
                            "Green Sport Band",
                            "Sport Band Green",
                            "Green Band",
                            "Green SB",
                            "SB Green",
                            "Lake Green SB",
                            "SB Lake Green"
                        ],
                        "Sport Band Starlight" : [
                            "Sport Band Starlight",
                            "Starlight Sport Band",
                            "Starlight Band",
                            "Starlight SB",
                            "SB Starlight",
                            "Starlight"
                        ],
                        "Sport Band Light Blush" : [
                            "Sport Band Light Blush",
                            "Light Blush Sport Band",
                            "Sport Band Light",
                            "Sport Band Blush",
                            "Light Blush SB",
                            "SB Light Blush",
                            "Light Blush",
                            "AI LB SB"
                            "MWWH3",
                            "MWWU3",
                            "MWWJ3",
                            "U3LW",
                            "Blush",
                            "LB",
                            "LB SB"
                        ],
                        "Sport Band Stone Gray" : [
                            "Sport Band Stone Gray",
                            "Stone Gray Sport Band",
                            "Sport Band Stone",
                            "Sport Band Gray",
                            "Stone Gray SB",
                            "SB Stone Gray",
                            "Stone Gray",
                            "Gray SB",
                            "SB Gray",
                            "Gray",
                            "Grey"
                        ],
                        "Sport Band Black" : [
                            "Sport Band Black",
                            "Black Sport Band",
                            "Black Band",
                            "SB Black",
                            "Black SB",
                            "Q3LW",
                            "MWWE3",
                            "MWWP3",
                            "MWWF3"
                        ],
                        "Sport Band Pride Edition" : [
                            "Sport Band Pride Edition",
                            "Pride Edition Sport Band",
                            "Sport Band Pride",
                            "Sport Band Edition",
                            "Pride Edition",
                            "Pride SB",
                            "SB Pride",
                            "Pride"
                        ],
                        "Sport Band Black Unity" : [
                            "Sport Band Black Unity",
                            "Black Unity Sport Band",
                            "Sport Band Black",
                            "Sport Band Unity",
                            "Black Unity Band",
                            "Black Unity SB",
                            "SB Black Unity",
                            "Black Unity SB"
                        ],
                        "Sport Band Midnight" : [
                            "Sport Band Midnight",
                            "Midnight Sport Band",
                            "Midnight Band",
                            "Midnight SB",
                            "SB Midnight"
                        ],
                        "Sport Band" : [
                            "Sport Band",
                            "Sport",
                            "SB"
                        ],
                        "Sport Loop Blue Cloud" : [
                            "Sport Loop Blue Cloud",
                            "Blue Cloud Sport Loop",
                            "Sport Loop Blue",
                            "Blue Sport Loop",
                            "Blue Loop",
                            "Blue SL",
                            "SL Blue",
                            "Blue Cloud SL",
                            "SL Blue Cloud",
                            "Blue"
                        ],
                        "Sport Loop Lake Green" : [
                            "Sport Loop Lake Green",
                            "Lake Green Sport Loop",
                            "Sport Loop Green",
                            "Green Sport Loop",
                            "Green Loop",
                            "Lake Green SL",
                            "SL Lake Green",
                            "SL Green",
                            "Green SL"
                        ],
                        "Sport Loop Plum" : [
                            "Sport Loop Plum",
                            "Plum Sport Loop",
                            "Loop Plum",
                            "Plum Loop",
                            "SL Plum",
                            "Plum SL"
                        ],
                        "Sport Loop Ink" : [
                            "Sport Loop Ink",
                            "Ink Sport Loop",
                            "Ink Loop",
                            "Ink SL",
                            "SL Ink"
                        ],
                        "Sport Loop Black" : [
                            "Sport Loop Black",
                            "Black Sport Loop",
                            "Black Loop",
                            "Black SL",
                            "SL Black"
                        ],
                        "Sport Loop Midnight" : [
                            "Sport Loop Midnight",
                            "Midnight Sport Loop",
                            "Midnight Loop",
                            "Midnight SL",
                            "SL Midnight"
                        ],
                        "Sport Loop Ultramarine" : [
                            "Sport Loop Ultramarine",
                            "Ultramarine Sport Loop",
                            "Ultramarine Loop",
                            "Ultramarine Sport",
                            "SL Ultramarine",
                            "Ultramarine SL"
                        ],
                        "Sport Loop Black Unity" : [
                            "Sport Loop Black Unity",
                            "Black Unity Sport Loop",
                            "Sport Loop Black",
                            "Sport Loop Unity",
                            "Black Sport Loop",
                            "Black Loop",
                            "SL Black Unity",
                            "Black Unity SL"
                        ],
                        "Sport Loop" : [
                            "Sport Loop",
                            "Loop",
                            "SL"
                        ],
                        "Natural Titanium Milanese Loop" : [
                            "Natural Titanium Milanese Loop",
                            "Natural Milanese Loop",
                            "Natural Milanese"
                        ],
                        "Black Titanium Milanese Loop" : [
                            "Black Titanium Milanese Loop",
                            "Black Milanese Loop",
                            "Black Milanese"
                        ],
                        "Milanese Loop" : [
                            "milanese loop",
                            "milanese",
                            "Mil LP"
                        ],
                        "Solo Loop Lake Green" : [
                            "Solo Loop Lake Green",
                            "Lake Green Solo Loop",
                            "Solo Loop Green",
                            "Green Solo Loop",
                        ],
                        "Solo Loop Ultramarine" : [
                            "Solo Loop Ultramarine",
                            "Ultramarine Solo Loop",
                        ],
                        "Solo Loop Star Fruit" : [
                            "Solo Loop Star Fruit",
                            "Star Fruit Solo Loop",
                            "Solo Loop Star",
                            "Solo Loop Fruit",
                            "Star Fruit Loop",
                            "SL Star Fruit",
                            "Star Fruit SL",
                            "SL Star",
                            "SL Fruit",
                            "SL Star Fruit",
                            "SL Star Fruit"
                            "Star Fruit Loop"
                        ],
                        "Solo Loop Light Blush" : [
                            "Solo Loop Light Blush",
                            "Light Blush Solo Loop",
                            "Solo Loop Light",
                            "Solo Loop Blush",
                            "SL Light Blush",
                            "Light Blush SL",
                            "SL Light",
                            "SL Blush",
                            "SL Light Blush",
                            "Light Blush SL"
                        ],
                        "Solo Loop Black" : [
                            "Loop Black Solo",
                            "Black Solo Loop",
                            "Black Solo",
                            "Solo Black"
                        ],
                        "Solo Loop" : [
                            "Solo Loop",
                            "Loop Solo",
                            "SL"
                        ],
                        "Nike Sport Band Volt Splash" : [
                            "Nike Sport Band Volt Splash",
                            "Volt Splash Nike Sport Band",
                            "Nike Band Volt Splash",
                            "Volt Splash Nike Sport",
                            "Nike Band Volt",
                            "Volt Splash Nike",
                            "Volt Nike",
                            "Nike Volt"
                        ],
                        "Nike Sport Band Cargo Khaki" : [
                            "Nike Sport Band Cargo Khaki",
                            "Cargo Khaki Nike Sport Band",
                            "Cargo Khaki Nike Sport",
                            "Nike Band Cargo Khaki",
                            "Cargo Khaki Nike",
                            "Cargo Nike",
                            "Khaki Nike",
                            "Nike Band Cargo",
                            "Nike Khaki",
                            "Nike Cargo"
                        ],
                        "Nike Sport Band Blue Flame" : [
                            "Nike Sport Band Blue Flame",
                            "Blue Flame Nike Sport Band",
                            "Nike Band Blue Flame",
                            "Blue Flame Nike Sport",
                            "Nike Band Blue",
                            "Blue Flame Nike",
                            "Nike Blue",
                            "Blue Nike"
                        ],
                        "Nike Sport Band Magic Ember" : [
                            "Nike Sport Band Magic Ember",
                            "Nike Band Magic Ember",
                            "Magic Ember Nike Sport",
                            "Nike Band Magic",
                            "Magic Ember Nike",
                            "Nike Magic",
                            "Magic Nike"
                        ],
                        "Nike Sport Band Desert Stone" : [
                            "Nike Sport Band Desert Stone",
                            "Nike Band Desert Stone",
                            "Desert Stone Nike",
                            "Nike Band Desert",
                            "Nike Desert",
                            "Desert Nike"
                        ],
                        "Nike Sport Band Midnight Sky" : [
                            "Nike Sport Band Midnight Sky",
                            "Midnight Sky Nike Sport Band"
                            "Nike Band Midnight Sky",
                            "Midnight Sky Nike Sport",
                            "Nike Band Midnight",
                            "Midnight Sky Nike",
                            "Nike Midnight",
                            "Midnight Nike"
                        ],
                        "Nike Sport Band Pure Platinum" : [
                            "Nike Sport Band Pure Platinum",
                            "Band Pure Platinum Nike Sport",
                            "Nike Band Pure Platinum",
                            "Pure Platinum Nike Band",
                            "Nike Band Pure",
                            "Nike Pure Platinum",
                            "Nike Pure",
                            "Pure Nike"
                        ],
                        "Nike Sport Band" : [
                            "Nike Sport Band",
                            "Nike Band",
                            "Nike Sport",
                            "Nike"
                        ],
                        "Blue/Red Nike Sport Loop" : [
                            "Blue/Red Nike Sport Loop",
                            "Blue/Red Sport Loop",
                            "Blue/Red Nike Loop",
                            "Blue/Red Nike"
                        ],
                        "Grey/Blue Nike Sport Loop" : [
                            "Grey/Blue Nike Sport Loop",
                            "Grey/Blue Sport Loop",
                            "Grey/Blue Nike Loop",
                            "Grey/Blue Nike"
                        ],
                        "Black/Blue Nike Sport Loop" : [
                            "Black/Blue Nike Sport Loop",
                            "Black/Blue Sport Loop",
                            "Black/Blue Nike Loop",
                            "Black/Blue Nike"
                        ],
                        "Green/Grey Nike Sport Loop" : [
                            "Green/Grey Nike Sport Loop",
                            "Green/Grey Sport Loop",
                            "Green/Grey Nike Loop",
                            "Green/Grey Nike"
                        ],
                        "Starlight/Pink Nike Sport Loop" : [
                            "Starlight/Pink Nike Sport Loop",
                            "Starlight/Pink Sport Loop",
                            "Starlight/Pink Nike Loop",
                            "Starlight/Pink Nike"
                        ],
                        "Nike Sport Loop" : [
                            "Nike Sport Loop",
                            "Nike Loop"
                        ],
                        "Braided Solo Loop Chartreuse" : [
                            "Braided Solo Loop Chartreuse",
                            "Chartreuse Braided Solo Loop",
                            "Chartreuse Braided SL",
                            "Braided Chartreuse",
                            "Braided SL Chartreuse",
                        ],
                        "Braided Solo Loop Denim" : [
                            "Braided Solo Loop Denim",
                            "Denim Braided Solo Loop",
                            "Denim Braided SL",
                            "Braided Denim",
                            "Braided SL Denim"
                        ],
                        "Braided Solo Loop Magenta" : [
                            "Braided Solo Loop Magenta",
                            "Magenta Braided Solo Loop",
                            "Magenta Braided SL",
                            "Braided Magenta",
                            "Braided SL Magenta"
                        ],
                        "Braided Solo Loop Midnight" : [
                            "Braided Solo Loop Midnight",
                            "Midnight Braided Solo Loop",
                            "Midnight Braided SL",
                            "Braided Midnight",
                            "Braided SL Midnight"
                        ],
                        "Braided Solo Loop Lake Green" : [
                            "Braided Solo Loop Lake Green",
                            "Lake Green Braided Solo Loop",
                            "Lake Green Braided SL",
                            "Braided Lake Green",
                            "Braided SL Lake Green",
                            "Braided Solo Loop Green",
                            "Green Braided Solo Loop",
                            "Green Braided SL",
                            "Braided Green",
                            "Braided SL Green",
                        ],
                        "Braided Solo Loop Black Unity" : [
                            "Braided Solo Loop Black Unity",
                            "Black Unity Braided Solo Loop",
                            "Black Unity Braided SL",
                            "Braided Black Unity",
                            "Braided SL Black Unity"
                        ],
                        "Braided Solo Loop Pride Edition" : [
                            "Braided Solo Loop Pride Edition",
                            "Pride Edition Braided Solo Loop",
                            "Pride Edition Braided SL",
                            "Braided Pride Edition",
                            "Braided SL Pride Edition"
                        ],
                        "Braided Solo Loop Beige" : [
                            "Braided Solo Loop Beige",
                            "Beige Braided Solo Loop",
                            "Beige Braided SL",
                            "Braided Beige",
                            "Braided SL Beige"
                        ],
                        "Braided Solo Loop" : [
                            "Braided Solo Loop",
                            "Solo Loop Braided",
                            "Braided SL",
                            "SL Braided"
                        ],
                        "Link Bracelet Natural" : [
                            "Link Bracelet Natural",
                            "Natural Link Bracelet"
                            "Link Natural",
                            "Natural Link"
                        ],
                        "Link Bracelet Slate" : [
                            "Link Bracelet Slate",
                            "Slate Link Bracelet"
                            "Link Slate",
                            "Slate Link"
                        ],
                        "Link Bracelet Gold" : [
                            "Link Bracelet Gold",
                            "Gold Link Bracelet"
                            "Link Gold",
                            "Gold Link"
                        ],
                        "Link Bracelet" : [
                            "Link Bracelet",
                            "Link"
                        ]
                    },
                },
                "strap_size" : {
                    "values" : ["S/M", "M/L", "S", "M", "L"],
                    "aliases" : {
                        "S/M" : ["s/m", "sm"],
                        "M/L" : ["m/l", "ml"],
                        "S" : ["s"],
                        "M" : ["m"],
                        "L" : ["l"]
                    }
                }
            },
        },
        "AW Ultra 2" : {
            "aliases" : [
                "AW Ultra 2",
                "watch Ultra2",
                "watch Ultra 2",
                "Ultra2",
                "Ultra 2"
            ],
            "attributes" : {
                "case_type" : {
                    "values" : [
                        "Natural Ti",
                        "Black Ti",
                        "Titanium"
                    ],
                    "aliases" : {
                        "Natural Ti" : [
                            "Natural Titanium",
                            "Natural",
                            "Natural Ti"
                        ],
                        "Black Ti" : [
                            "Black Titanium",
                            "Black",
                            "Black Ti"
                        ],
                        "Titanium" : ["Default"]
                    },
                },
                "year_release" : {
                    "values" : [
                        "2023",
                        "2024"
                    ],
                    "aliases" : {
                        "2023" : [
                            "2023",
                        ],
                        "2024" : [
                            "2024"
                        ]
                    }
                },
                "strap_type" : {
                    "values" : [
                        "Alpine Loop Tan",
                        "Alpine Loop Navy",
                        "Alpine Loop Dark Green",
                        "Alpine Loop Olive",
                        "Alpine Loop Indigo",
                        "Alpine Loop Blue",
                        "Alpine Loop",
                        "Trail Loop Green",
                        "Trail Loop Blue",
                        "Trail Loop Black",
                        "Trail Loop Orange/Beige",
                        "Trail Loop Green/Gray",
                        "Trail Loop Blue/Black",
                        "Trail Loop",
                        "Ocean Band Navy",
                        "Ocean Band Black",
                        "Ocean Band Ice Blue",
                        "Ocean Band White",
                        "Ocean Band Orange",
                        "Ocean Band Blue",
                        "Ocean Band",
                        "Milanese Loop Natural",
                        "Titanium Milanese Loop Black",
                        "Milanese Loop"
                    ],
                    "aliases" : {
                        "Alpine Loop Tan" : [
                            "Alpine Loop Tan",
                            "Loop Tan Alpine",
                            "Tan Alpine Loop",
                            "Tan Alpine",
                            "Alpine Tan",
                            "AL Tan",
                            "Tan AL"
                        ],
                        "Alpine Loop Navy" : [
                            "Alpine Loop Navy",
                            "Loop Navy Alpine",
                            "Navy Alpine Loop",
                            "Alpine Navy",
                            "Navy Alpine",
                            "AL Navy",
                            "Navy AL"
                        ],
                        "Alpine Loop Dark Green" : [
                            "Alpine Loop Dark Green",
                            "Loop Dark Green Alpine",
                            "Dark Green Alpine Loop",
                            "Alpine Loop Green",
                            "Alpine Dark Green",
                            "AL Dark Green",
                            "AL Green",
                            "Green AL",
                            "Dark Green AL"
                        ],
                        "Alpine Loop Olive" : [
                            "Alpine Loop Olive",
                            "Loop Olive Alpine",
                            "Olive Alpine Loop",
                            "Olive Alpine",
                            "Alpine Olive",
                            "AL Olive",
                            "Olive AL"
                        ],
                        "Alpine Loop Indigo" : [
                            "Alpine Loop Indigo",
                            "Loop Indigo Alpine",
                            "Indigo Alpine Loop",
                            "Indigo Alpine",
                            "Alpine Indigo",
                            "AL Indigo",
                            "Indigo AL"
                        ],
                        "Alpine Loop Blue" : [
                            "Alpine Loop Blue",
                            "Loop Blue Alpine",
                            "Blue Alpine Loop",
                            "Blue Alpine",
                            "Alpine Blue",
                            "AL Blue",
                            "Blue AL"
                        ],
                        "Alpine Loop" : [
                            "Alpine Loop",
                            "AL"
                        ],
                        "Trail Loop Green" : [
                            "Trail Loop Green",
                            "Loop Green Trail",
                            "Green Trail Loop",
                            "Trail Green",
                            "TL Green",
                            "Green TL"
                        ],
                        "Trail Loop Blue" : [
                            "Trail Loop Blue",
                            "Loop Blue Trail",
                            "Blue Trail Loop",
                            "Trail Blue",
                            "Loop Blue",
                            "Blue TL",
                            "TL Blue"
                        ],
                        "Trail Loop Black" : [
                            "Trail Loop Black",
                            "Loop Black Trail",
                            "Black Trail Loop",
                            "Trail Black",
                            "Loop Black",
                            "Black TL",
                            "TL Black"
                        ],
                        "Trail Loop Orange/Beige" : [
                            "Trail Loop Orange/Beige",
                            "Orange/Beige Trail Loop",
                            "Orange/Beige Trail",
                            "Trail Orange/Beige",
                            "TL Orange/Beige",
                            "Orange/Beige TL",
                            "Orange/Beige"
                        ],
                        "Trail Loop Green/Gray" : [
                            "Trail Loop Green/Gray",
                            "Green/Gray Trail Loop",
                            "Trail Green/Gray",
                            "Green/Gray Trail",
                            "TL Green/Gray",
                            "Green/Gray TL",
                            "Green/Gray"
                        ],
                        "Trail Loop Blue/Black" : [
                            "Trail Loop Blue/Black",
                            "Blue/Black Trail Loop",
                            "Trail Blue/Black",
                            "Blue/Black Trail",
                            "Blue/Black",
                            "TL Blue/Black",
                            "Blue/Black TL"
                        ],
                        "Trail Loop" : [
                            "Trail Loop",
                            "TL"
                        ],
                        "Ocean Band Navy" : [
                            "Ocean Band Navy",
                            "Band Navy Ocean",
                            "Navy Ocean Band",
                            "Ocean Navy",
                            "Band Navy",
                            "Navy"
                        ],
                        "Ocean Band Black" : [
                            "Ocean Band Black",
                            "Band Black Ocean",
                            "Black Ocean Band",
                            "Ocean Black",
                            "Band Black",
                        ],
                        "Ocean Band Ice Blue" : [
                            "Ocean Band Ice Blue",
                            "Band Ice Blue Ocean",
                            "Ice Blue Ocean Band",
                            "Ocean Ice Blue",
                            "Band Ice Blue",
                            "Ice Blue"
                        ],
                        "Ocean Band White" : [
                            "Ocean Band White",
                            "Band White Ocean",
                            "White Ocean Band",
                            "Ocean White",
                            "Band White",
                        ],
                        "Ocean Band Orange" : [
                            "Ocean Band Orange",
                            "Band Orange Ocean",
                            "Orange Ocean Band",
                            "Ocean Orange",
                            "Band Orange",
                        ],
                        "Ocean Band Blue" : [
                            "Ocean Band Blue",
                            "Blue Ocean Band",
                            "Blue Band",
                            "Blue"
                        ],
                        "Ocean Band" : [
                            "Ocean Band"
                        ],
                        "Milanese Loop Natural" : [
                            "Natural Titanium Milanese Loop",
                            "Natural Milanese Loop",
                            "Natural Milanese"
                        ],
                        "Milanese Loop Black" : [
                            "Black Titanium Milanese Loop",
                            "Black Milanese Loop",
                            "Black Milanese"
                        ],
                        "Milanese Loop" : [
                            "milanese loop",
                            "milanese",
                            "Mil LP"
                        ],
                    },
                },
                "strap_size" : {
                    "values" : ["S/M", "M/L", "S", "M", "L"],
                    "aliases" : {
                        "S/M" : ["s/m", "sm"],
                        "M/L" : ["m/l", "ml"],
                        "S" : ["s"],
                        "M" : ["m"],
                        "L" : ["l"]
                    }
                },
            },
        },
    },
    "Apple iPhone": {
        "iPhone 11" : {
            "aliases" : ["iPhone 11", "11"],
            "attributes" : {
                "SSD" : {
                    "values" : ["64", "128", "256"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"]
                    },
                },
                "color" : {
                    "values" : ["Black", "White", "Red", "Green", "Yellow", "Purple"],
                    "aliases" : {
                        "Black" : ["Midnight", "Black"],
                        "White" : ["Starlight", "White"],
                        "Red" : ["Red"],
                        "Green" : ["Green"],
                        "Yellow" : ["Yellow"],
                        "Purple" : ["Purple"]
                    },
                },
            },
        },
        "iPhone 11 Pro" : {
            "aliases" : ["iPhone 11 Pro", "11 Pro"],
            "attributes" : {
                "SSD" : {
                    "values" : ["64", "256", "512"],
                    "aliases" : {
                        "128" : ["64"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Midnight Green", "Gold", "Silver", "Pacific Blue"],
                    "aliases" : {
                        "Midnight Green" : ["Midnight Green", "Midnight", "Green", "Black"],
                        "Gold" : ["Gold"],
                        "Silver" : ["Silver"],
                        "Space Gray" : ["Space Gray", "Grey"]
                    },
                },
            },
        },
        "iPhone 11 Pro Max" : {
            "aliases" : ["iPhone 11 Pro Max", "11 Pro Max", "11 Max"],
            "attributes" : {
                "SSD" : {
                    "values" : ["64", "256", "512"],
                    "aliases" : {
                        "128" : ["64"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Midnight Green", "Gold", "Silver", "Pacific Blue"],
                    "aliases" : {
                        "Midnight Green" : ["Midnight Green", "Midnight", "Green", "Black"],
                        "Gold" : ["Gold"],
                        "Silver" : ["Silver"],
                        "Space Gray" : ["Space Gray", "Gray", "Grey"]
                    },
                },
            },
        },
        "iPhone SE 2" : {
            "aliases" : ["iPhone SE 2", "SE 2 2020", "SE 2020", "SE 2"], # "SE 2 2020", "SE 2020",
            "attributes" : {
                "SSD" : {
                    "values" : ["64", "128", "256"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                    },
                },
                "color" : {
                    "values" : ["Midnight", "Starlight", "Red"],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Starlight" : ["Starlight", "White"],
                        "Red" : ["Red"]
                    },
                },
            },
        },
        "iPhone 12" : {
            "aliases" : ["iPhone 12", "12"],
            "attributes" : {
                "SSD" : {
                    "values" : ["64", "128", "256"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"]
                    },
                },
                "color" : {
                    "values" : ["Midnight", "Starlight", "Red", "Green", "Blue", "Purple"],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Starlight" : ["Starlight", "White"],
                        "Red" : ["Red"],
                        "Green" : ["Green"],
                        "Blue" : ["Blue"],
                        "Purple" : ["Purple"]
                    },
                },
            },
        },
        "iPhone 12 Mini" : {
            "aliases" : ["iPhone 12 Mini", "12 Mini"],
            "attributes" : {
                "SSD" : {
                    "values" : ["64", "128", "256"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"]
                    },
                },
                "color" : {
                    "values" : ["Midnight", "Starlight", "Red", "Green", "Blue", "Purple"],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Starlight" : ["Starlight", "White"],
                        "Red" : ["Red"],
                        "Green" : ["Green"],
                        "Blue" : ["Blue"],
                        "Purple" : ["Purple"]
                    },
                },
            },
        },
        "iPhone 12 Pro" : {
            "aliases" : ["iPhone 12 Pro", "12 Pro"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Graphite", "Gold", "Silver", "Pacific Blue"],
                    "aliases" : {
                        "Graphite" : ["Graphite", "Black"],
                        "Gold" : ["Gold"],
                        "Silver" : ["Silver"],
                        "Pacific Blue" : ["Blue"]
                    },
                },
            },
        },
        "iPhone 12 Pro Max" : {
            "aliases" : ["iPhone 12 Pro Max", "12 Pro Max", "12 Max"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Graphite", "Gold", "Silver", "Pacific Blue"],
                    "aliases" : {
                        "Graphite" : ["Graphite", "Black"],
                        "Gold" : ["Gold"],
                        "Silver" : ["Silver"],
                        "Pacific Blue" : ["Blue"]
                    },
                },
            },
        },
        "iPhone 13" : {
            "aliases" : ["iPhone 13", "13"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Midnight", "Starlight", "Red", "Green", "Blue", "Pink"],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Starlight" : ["Starlight", "White"],
                        "Red" : ["Red"],
                        "Green" : ["Green"],
                        "Blue" : ["Blue"],
                        "Pink" : ["Pink"]
                    },
                },
            },
        },
        "iPhone 13 Mini" : {
            "aliases" : ["iPhone 13 Mini", "13 Mini"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Midnight", "Starlight", "Red", "Green", "Blue", "Pink"],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Starlight" : ["Starlight", "White"],
                        "Red" : ["Red"],
                        "Green" : ["Green"],
                        "Blue" : ["Blue"],
                        "Pink" : ["Pink"]
                    },
                },
            },
        },
        "iPhone 13 Pro" : {
            "aliases" : ["iPhone 13 Pro", "13 Pro"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512", "1TB"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "values" : ["Graphite", "Gold", "Alpine Green", "Silver", "Sierra Blue"],
                    "aliases" : {
                        "Graphite" : ["Graphite", "Black"],
                        "Gold" : ["Gold"],
                        "Silver" : ["Silver"],
                        "Alpine Green" : ["Green"],
                        "Sierra Blue" : ["Blue"]
                    },
                },
            },
        },
        "iPhone 13 Pro Max" : {
            "aliases" : ["iPhone 13 Pro Max", "13 Pro Max", "13 Max"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512", "1TB"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "values" : ["Graphite", "Gold", "Alpine Green", "Silver", "Sierra Blue"],
                    "aliases" : {
                        "Graphite" : ["Graphite", "Black"],
                        "Gold" : ["Gold"],
                        "Silver" : ["Silver"],
                        "Alpine Green" : ["Green"],
                        "Sierra Blue" : ["Blue"]
                    },
                },
            },
        },
        "iPhone SE 3" : {
            "aliases" : ["iPhone SE 3", "SE 3"],
            "attributes" : {
                "SSD" : {
                    "values" : ["64", "128", "256"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"]
                    },
                },
                "color" : {
                    "values" : ["Midnight", "Starlight", "Red"],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Starlight" : ["Starlight", "White"],
                        "Red" : ["Red"]
                    },
                },
            },
        },
        "iPhone 14" : {
            "aliases" : ["iPhone 14", "14"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Midnight", "Starlight", "Blue", "Red", "Purple", "Yellow"],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Starlight" : ["Starlight", "White"],
                        "Blue" : ["Blue"],
                        "Red" : ["Red"],
                        "Purple" : ["Purple"],
                        "Yellow" : ["Yellow"]
                    },
                },
            },
        },
        "iPhone 14 Plus" : {
            "aliases" : ["iPhone 14 plus", "14 plus"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Midnight", "Starlight", "Blue", "Red", "Purple", "Yellow"],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Starlight" : ["Starlight", "White"],
                        "Blue" : ["Blue"],
                        "Red" : ["Red"],
                        "Purple" : ["Purple"],
                        "Yellow" : ["Yellow"]
                    },
                },
            },
        },
        "iPhone 14 Pro" : {
            "aliases" : ["iPhone 14 Pro", "14 Pro"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512", "1TB"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Gold", "Silver", "Purple"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "Gold" : ["Gold"],
                        "Silver" : ["Silver"],
                        "Purple" : ["Purple"],
                    },
                },
            },
        },
        "iPhone 14 Pro Max" : {
            "aliases" : ["iPhone 14 Pro Max", "14 Pro Max", "14 Max"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512", "1TB"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Gold", "Silver", "Purple"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "Gold" : ["Gold"],
                        "Silver" : ["Silver"],
                        "Purple" : ["Purple"],
                    },
                },
            },
        },
        "iPhone 15" : {
            "aliases" : ["iPhone 15", "15"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Pink", "Blue", "Green", "Yellow"],
                    "aliases" : {
                        "Black" : ["Black", "Midnight"],
                        "Pink" : ["Pink"],
                        "Blue" : ["Blue"],
                        "Green" : ["Green"],
                        "Yellow" : ["Yellow"],
                    },
                },
            },
        },
        "iPhone 15 Plus" : {
            "aliases" : ["iPhone 15 plus", "15 plus"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                    },
                },
                "color" : {
                    "values" : ["Black", "Pink", "Blue", "Green", "Yellow"],
                    "aliases" : {
                        "Black" : ["Black", "Midnight"],
                        "Pink" : ["Pink"],
                        "Blue" : ["Blue"],
                        "Green" : ["Green"],
                        "Yellow" : ["Yellow"],
                    },
                },
            },
        },
        "iPhone 15 Pro" : {
            "aliases" : ["iPhone 15 Pro", "15 Pro"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512", "1TB"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Blue", "Natural", "White"],
                    "aliases" : {
                        "Black" : ["Black", "Midnight"],
                        "Blue" : ["Blue"],
                        "Natural" : ["Natural"],
                        "White" : ["White"],
                    },
                },
            },
        },
        "iPhone 15 Pro Max" : {
            "aliases" : ["iPhone 15 Pro Max", "iPhone 15 ProMax", "15 Pro Max", "15 ProMax", "15 Max"],
            "attributes" : {
                "SSD" : {
                    "values" : ["256", "512", "1TB"],
                    "aliases" : {
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Blue", "Natural", "White"],
                    "aliases" : {
                        "Black" : ["Black", "Midnight"],
                        "Blue" : ["Blue"],
                        "Natural" : ["Natural"],
                        "White" : ["White"],
                    },
                },
            },
        },
        "iPhone 16E" : {
            "aliases" : ["iPhone 16E", "16E", "iPhone 16 E", "16E"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Pink", "Ultramarine", "Teal", "White"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "Pink" : ["Pink"],
                        "Ultramarine" : ["Ultramarine"],
                        "Teal" : ["Teal"],
                        "White" : ["White"],
                    },
                },
            },
        },
        "iPhone 16": {
            "aliases" : ["iPhone 16", "16"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Pink", "Ultramarine", "Teal", "White"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "Pink" : ["Pink"],
                        "Ultramarine" : ["Ultramarine"],
                        "Teal" : ["Teal"],
                        "White" : ["White"],
                    },
                },
            },
        },
        "iPhone 16 Plus": {
            "aliases" : ["iPhone 16 plus", "16 plus"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                    },
                },
                "color" : {
                    "values" : ["Black", "Pink", "Ultramarine", "Teal", "White"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "Pink" : ["Pink"],
                        "Ultramarine" : ["Ultramarine"],
                        "Teal" : ["Teal"],
                        "White" : ["White"],
                    },
                },
            },
        },
        "iPhone 16 Pro": {
            "aliases" : ["iPhone 16 Pro", "16 Pro"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512", "1TB"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Desert", "Natural", "White"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "Desert" : ["Desert"],
                        "Natural" : ["Natural"],
                        "White" : ["White"],
                    },
                },
            },
        },
        "iPhone 16 Pro Max": {
            "aliases" : ["iPhone 16 Pro Max", "iPhone 16 ProMax", "16 Pro Max", "16 ProMax", "16 Max"],
            "attributes" : {
                "SSD" : {
                    "values" : ["128", "256", "512", "1TB"],
                    "aliases" : {
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "values" : ["Black", "Desert", "Natural", "White"],
                    "aliases" : {
                        "Black" : ["Black"],
                        "Desert" : ["Desert"],
                        "Natural" : ["Natural"],
                        "White" : ["White"],
                    },
                },
            },
        },
    },
    "Apple Mac" : {
        "MacBook Air" : {
            "aliases" : [
                "MacBook Air",
                "Mac Book Air",
                "Air", #>>> спец алиасы
                "MGN63",
                "MLY33",
                "MLY13",
                "MC7U4",
                "MC7V4",
                "MC7W4",
                "MC7X4",
                "MC8J4",
                "MC8M4",
                "MC8Q4",
                "MRYQ3",
                "MRYV3",
                "MRYT3",
                "MRYN3",
                "MC9E4",
                "MC9F4",
                "MC9D4",
                "MGND3",
                "MC9G4",
                "MLY43",
                "MRXN3",
                "MRXV3",
                "MRXQ3",
                "MRXT3",
                "MRXP3",
                "MRXW3",
                "MRXR3",
                "MRXU3",
                "MXCR3",
                "MXCT3",
                "MXCV3",
                "MXCU3",
                "MC8N4",
                "MC8P4",
                "MLXX3",
                "MLY03",
                "MLY23",
                "MLXW3",
                "Z1BR000L3",
                "Z1BP000LW",
                "MC9L4",
                "MXD33",
                "MXD23",
                "MXD13",
                "MRYU3",
                "MRYR3",
                "MRYP3",
                "MRYM3",
                "MQKX3",
                "MQKV3",
                "MQKT3",
                "MQKQ3",
                "MQKR3LL/A",
                "MQKP3",
                "Z1BV000SC",
                "Z1BV000RL",
                "Z1BV000Q8",
                "Z1BV0006S",
                "Z1BV0006P",
                "Z1BV0006K",
                "Z1BR000L5",
                "Z1BR000KD",
                "Z1BP000QF",
                "Z1BP000MD",
                "Z1BP000LM",
                "Z1BP0006M",
                "Z1BD000MJ",
                "Z1BD000MG",
                "Z1BC0017C",
                "Z1BC0015S",
                "Z1BB000MG",
                "Z1BB000M6",
                "Z1BB000M5",
                "Z1BA0017J",
                "Z1B9000N0",
                "Z1B9000MT",
                "Z1B80015Z",
                "Z1B7000MG",
                "Z1B7000MD",
                "Z1B60019P",
                "MC8H4",
                "MC8G4",
                "Z16000190",
                "Z16100074",
                "Z1600040U",
                "Z1600040T",
                "Z1600040S",
                "Z1600040R",
                "Z1600040Q",
                "Z1600040P",
                "Z1600040N",
                "Z1600040M",
                "Z1600040L",
                "Z1600040J",
                "Z160000B1",
                "Z160000AU",
                "Z15Z0005L",
                "Z15Z0005K",
                "Z15Z00028",
                "Z15Y002N6",
                "Z15Y002N5",
                "Z15Y002N4",
                "Z15Y002N3",
                "Z15Y002N2",
                "Z15Y002N1",
                "Z15Y002N0",
                "Z15Y002MY",
                "Z15Y000B3",
                "Z15Y0000B",
                "Z15X0005M",
                "Z15X0000D",
                "Z15W002B6",
                "Z15W002B5",
                "Z15W002B4",
                "Z15W002B3",
                "Z15W002B2",
                "Z15W002B1",
                "Z15W002B0",
                "Z15W002AZ",
                "Z15W002AY",
                "Z15W002AW",
                "Z15W002AR",
                "Z15T0000F",
                "Z15S002L3",
                "Z15S002L2",
                "Z15S002L1",
                "Z15S002L0",
                "Z15S002KZ",
                "Z15S002KY",
                "Z15S002KX",
                "Z15S002KV",
                "Z15S002KT",
                "Z15S002KS",
                "Z15S00112",
                "Z15S000V9",
                "MN703",
                "MLXY3",
                "Z127000NL",
                "Z12A000P5",
                "Z12700036",
                "MGN93ZE/A/R1",
                "MGN93",
                "MC9K4",
                "Z18T000PR",
                "Z18T000PT",
                "Z18U2",
                "Z18S000Q7",
                "Z18R000XA",
                "Z18L000Y0",
                "Z18P0006L",
                "Z18UO",
                "Z18T000PQ",
                "Z1BP000LV",
                "Z1BC00148",
                "Z1B9000MY",
                "Z1B7000P2",
                "Z1B7000N3",
                "MC9J4",
                "MC8K4",
                "Z1BT000L8",
                "Z1BT000L2",
                "Z1BT000KB",
                "Z1BR000LF",
                "MC9H4",
                "Z15S000CT",
                "Z15S002KW",
                "Z15W000BB",
                "Z15Y000B2",
                "Z1600040F",
                "Z18T000PP",
                "Z18L000PR",
                "MQKW3",
                "MQKR3",
                "MQKU3",
                "MGNE3",
                "Z124000FK",
                "MXD43",
                "MW133",
                "MC6U4",
                "MC6A4",
                "MW1G3",
                "MW1J3",
                "MW1M3",
                "MC7C4",
                "MW133",
                "MC6U4",
                "MC6A4",
                "MW1G3",
                "MW1L3",
                "MW1J3",
                "MW1M3",
                "MC7C4",
                "MC6T4",
                "MW0W3",
                "MW0Y3",
                "MW123",
                "MW0X3",
                "MW103",
                "MC6V4",
                "MC654",
                "MC6C4",
                "MC7A4",
                "MW1H3",
                "MW1K3",

            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["13”", "15”"],
                    "aliases" : {
                    "13”" : ["13”", "13", "13-inch", "13 inch", "13,6"],
                    "15”" : ["15”", "15", "15-inch", "15 inch", "15,3"],
                    },
                },
                "chip" : {
                    "values" : [
                    "M1",
                    "M1 Pro",
                    "M1 Max",
                    "M2 Pro",
                    "M2 Max",
                    "M2",
                    "M3 Pro",
                    "M3 Max",
                    "M3"
                ],
                    "aliases" : {
                    "M1 Pro" : ["M1 Pro"],
                    "M1 Max" : ["M1 Max"],
                    "M1" : ["M1"],
                    "M2 Pro" : ["M2 Pro"],
                    "M2 Max" : ["M2 Max"],
                    "M2" : ["M2"],
                    "M3 Pro" : ["M3 Pro"],
                    "M3 Max" : ["M3 Max"],
                    "M3" : ["M3"],
                    "M4 Pro" : ["M4 Pro"],
                    "M4 Max" : ["M4 Max"],
                    "M4" : ["M4"]
                    },
                },
                "RAM" : {
                    "values" : [
                        "8",
                        "16",
                        "18",
                        "24",
                        "32",
                        "36",
                        "48",
                        "64",
                        "128"
                    ],
                    "aliases" : {
                        "8" : ["8GB", "8 GB", "8ГБ", "8 ГБ", "8"],
                        "16" : ["16GB", "16 GB", "16ГБ", "16 ГБ", "16"],
                        "18" : ["18GB", "18 GB", "18ГБ", "18 ГБ", "18"],
                        "24" : ["24GB", "24 GB", "24ГБ", "24 ГБ", "24"],
                        "32" : ["32GB", "32 GB", "32ГБ", "32 ГБ", "32"],
                        "36" : ["36GB", "36 GB", "36ГБ", "36 ГБ", "36"],
                        "48" : ["48GB", "48 GB", "48ГБ", "48 ГБ", "48"],
                        "64" : ["64GB", "64 GB", "64ГБ", "64 ГБ", "64"],
                        "128" : ["128GB", "128 GB", "128ГБ", "128 ГБ", "128"],
                    },
                },
                "SSD" : {
                    "values" : [
                        "256",
                        "512",
                        "1TB",
                        "2TB"
                    ],
                    "aliases" : {
                        "256" : ["256 GB", "256GB", "256 ГБ", "256ГБ", "256"],
                        "512" : ["512 GB", "512GB", "512 ГБ", "512ГБ", "512"],
                        "1TB" : ["1024 GB", "1024GB", "1024 ГБ", "1024ГБ", "1TB", "1 TB"],
                        "2TB" : ["2048 GB", "2048GB", "2048 ГБ", "2048ГБ", "2TB", "2 TB"]
                    },
                },
                "color" : {
                    "values" : [
                        "Midnight",
                        "Silver",
                        "Space Gray",
                        "Starlight",
                        "Gold"
                    ],
                    "aliases" : {
                        "Midnight" : ["Midnight", "Black"],
                        "Silver" : ["Silver"],
                        "Space Gray" : ["Space Gray", "Gray", "SpaceGray", "Grey"],
                        "Starlight" : ["Starlight", "Starlit"],
                        "Gold" : ["Gold"],
                        "Sky Blue" : ["Sky Blue"]
                    },
                },
                "custom" : {
                    "values" : ["кастомный"],
                    "aliases" : {
                        "кастомный" : ["кастомный"],
                    },
            },
            },
        },
        "MacBook Pro" : {
            "aliases" : [
                "MacBook Pro",
                "Mac Book Pro",
                "Pro",
                "MRX43", # спец. алиасы >>>
                "MX2J3",
                "MW2W3",
                "MX2Z3",
                "MX2N3",
                "MUW73",
                "MX303",
                "MX314",
                "MPHE3",
                "MRW43",
                "MUW63",
                "MCX14",
                "MX2F3",
                "MX2K3",
                "MX2Y3",
                "MRW13",
                "MRX33",
                "MRX63",
                "MK193",
                "MRX73",
                "MW2U3",
                "MX2E3",
                "MX2G3",
                "MRW73",
                "Z1FW0000T",
                "Z1FW0000S",
                "Z1FS0000T",
                "Z1FS0000Q",
                "Z1FS0000P",
                "Z1FS0000M",
                "Z1AF001AL",
                "Z1AF001AF",
                "Z1FG0000V",
                "Z1FG0000R",
                "Z1FG0000N",
                "Z1FG0000L",
                "Z1FG0000K",
                "Z1FD0000L",
                "MW2V3",
                "MCX04",
                "Z1AU002AC",
                "MTL83",
                "MMQX3",
                "MKH53",
                "MX2T3",
                "Z1FW0000R",
                "Z1FW0000P",
                "Z1FW0000N",
                "Z1FW0000M",
                "Z1FV00006",
                "Z1FS0000R",
                "Z1FR00003",
                "MX2W3",
                "MX2V3",
                "Z1AH00174",
                "Z1AF0019Y",
                "Z1AF0019W",
                "MRW63",
                "Z1CM0000J",
                "Z1CM0000G",
                "Z1AG00002",
                "Z1AF001VB",
                "Z1AF001V9",
                "Z1AF001V7",
                "Z1AF001V3",
                "Z1AF001S7",
                "Z1760005S",
                "Z1740017J",
                "MNWD3",
                "MNWC3",
                "MNW93",
                "MNW83",
                "Z177000NE",
                "Z177000E9",
                "Z1760005V",
                "MNWE3",
                "MNWA3",
                "Z14Y001M4",
                "Z14V0023L",
                "Z14V00234",
                "Z14V0008Z",
                "MK1F3",
                "MK1E3",
                "MK183",
                "Z14Y0026L",
                "Z14Y001M6",
                "Z14Y001JD",
                "Z14Y0008W",
                "Z14Y0008M",
                "Z14V0028J",
                "Z14V0027K",
                "Z14V0027J",
                "Z14V0024F",
                "Z14V0023R",
                "Z14V001XN",
                "Z14V00092",
                "Z14V00090",
                "Z14V0008V",
                "MMQW3",
                "MK233",
                "MK1A3",
                "Z14Y001T7",
                "Z14Y001PA",
                "Z14Y0008J",
                "Z14X002DY",
                "Z14X000HQ",
                "Z1FF0000B",
                "Z1FE00012",
                "Z1FE0000E",
                "Z1FB00014",
                "MX2H3",
                "Z1FG0000S",
                "Z1FG0000P",
                "Z1FG0000C",
                "Z1FD0000T",
                "Z1FD0000S",
                "Z1FD0000Q",
                "MW2X3",
                "Z1CM000ZQ",
                "Z1C800047",
                "Z1AU0000M",
                "Z1CM000UW",
                "Z1AY001JB",
                "Z1AW0000W",
                "Z1AW0000U",
                "Z1AW0000S",
                "Z1AU002M9",
                "Z1AJ0019D",
                "Z1AJ0018V",
                "MXE03",
                "MRX83",
                "MRX53",
                "Z1C80001D",
                "MTL73",
                "MR7K3",
                "MR7J3",
                "Z17G002HT",
                "Z17G000NA",
                "MPHJ3",
                "MPHH3",
                "MPHG3",
                "MPHF3",
                "Z17K002UN",
                "Z17K002UM",
                "Z17J00165",
                "Z17G003AN",
                "Z17G002KJ",
                "Z17G001BC",
                "MPHK3",
                "Z15G00460",
                "MKGT3",
                "MKGR3",
                "MKGQ3",
                "MKGP3",
                "Z15J004WS",
                "Z15J0030H",
                "Z15J000DJ",
                "Z15G007C6",
                "Z15G0047Q",
                "Z15G0045J",
                "Z15G000DV",
                "Z15G000DT",
                "Z15G000DR",
                "MK1H3",
                "Z16U00025",
                "Z16R000UA",
                "Z16R0005J",
                "MNEQ3",
                "MNEP3",
                "MNEJ3/LL",
                "MNEJ3",
                "MNEH3",
                "G16S6",
                "Z11F0002Z",
                "MYDC2",
                "MYD92",
                "MYD82",
                "MRW23",
                "MX2X3"
            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["13”", "14”", "16”"],
                    "aliases" : {
                        "13”" : ["13”", "13", "13-inch", "13 inch"],
                        "14”" : ["14”", "14", "14-inch", "14 inch"],
                        "16”" : ["16”", "16", "16-inch", "16 inch"]
                    },
                },
                "chip" : {
                    "values" : [
                        "M1",
                        "M1 Pro",
                        "M1 Max",
                        "M2 Pro",
                        "M2 Max",
                        "M2",
                        "M3 Pro",
                        "M3 Max",
                        "M3",
                        "M4 Pro",
                        "M4 Max",
                        "M4"
                        ],
                    "aliases" : {
                        "M1 Pro" : ["M1 Pro"],
                        "M1 Max" : ["M1 Max"],
                        "M1" : ["M1"],
                        "M2 Pro" : ["M2 Pro"],
                        "M2 Max" : ["M2 Max"],
                        "M2" : ["M2"],
                        "M3 Pro" : ["M3 Pro"],
                        "M3 Max" : ["M3 Max"],
                        "M3" : ["M3"],
                        "M4 Pro" : ["M4 Pro"],
                        "M4 Max" : ["M4 Max"],
                        "M4" : ["M4"]
                    },
                },
                "RAM" : {
                    "values" : [
                        "8",
                        "16",
                        "18",
                        "24",
                        "32",
                        "36",
                        "48",
                        "64",
                        "128"
                    ],
                    "aliases" : {
                        "8" : ["8GB", "8 GB", "8ГБ", "8 ГБ", "8"],
                        "16" : ["16GB", "16 GB", "16ГБ", "16 ГБ", "16"],
                        "18" : ["18GB", "18 GB", "18ГБ", "18 ГБ", "18"],
                        "24" : ["24GB", "24 GB", "24ГБ", "24 ГБ", "24"],
                        "32" : ["32GB", "32 GB", "32ГБ", "32 ГБ", "32"],
                        "36" : ["36GB", "36 GB", "36ГБ", "36 ГБ", "36"],
                        "48" : ["48GB", "48 GB", "48ГБ", "48 ГБ", "48"],
                        "64" : ["64GB", "64 GB", "64ГБ", "64 ГБ", "64"],
                        "128" : ["128GB", "128 GB", "128ГБ", "128 ГБ", "128"],
                    },
                },
                "SSD" : {
                    "values" : [
                        "512",
                        "1TB",
                        "2TB",
                        "4TB"
                    ],
                    "aliases" : {
                        "512" : ["512 GB", "512GB", "512 ГБ", "512ГБ", "512"],
                        "1TB" : ["1024 GB", "1024GB", "1024 ГБ", "1024ГБ", "1TB", "1 TB"],
                        "2TB" : ["2048 GB", "2048GB", "2048 ГБ", "2048ГБ", "2TB", "2 TB"],
                        "4TB" : ["4TB"]
                    },
                },
                "color" : {
                    "values" : [
                        "Space Black",
                        "Silver",
                        "Space Gray"
                    ],
                    "aliases" : {
                        "Space Black" : ["Space Black", "SpaceBlack", "Black"],
                        "Silver" : ["Silver"],
                        "Space Gray" : ["Space Gray", "SpaceGray", "Midnight", "Gray", "Grey"]
                    },
                },
                "custom" : {
                    "values" : ["кастомный"],
                    "aliases" : {
                        "кастомный" : ["кастомный"],
                    },
                },
                "glass" : {
                    "values" : ["Nano-texture glass"],
                    "aliases" : {
                        "Nano-texture glass" : ["Nano-texture glass", "Nano"],
                    },
                },
            },
        },
        "iMac" : {
            "aliases" : [
                "24",
                "27",
                "iMac",
                "Mac",
                "MWUY3",
                "MWUW3",
                "MWV83",
                "MWV43",
                "MWV63",
                "MWUF3",
                "MWUC3",
                "MWV03",
                "MWUX3",
                "MWV93",
                "MWV53",
                "MWV73",
                "MWV33",
                "MWUV3",
                "MD2Q4",
                "MD2P4",
                "MD2W4",
                "MD2U4",
                "MD2V4",
                "MD2T4",
                "MCR24",
                "MQRJ3",
                "MQR93",
                "MQRD3",
                "MQRC3",
                "MQRP3",
                "MQRK3",
                "MQRU3",
                "MQRR3",
                "Z1K80000L",
                "Z1K50000M",
                "Z1K50000L",
                "Z1K30000M",
                "Z1K30000L",
                "Z1K300003",
                "Z1K10000L",
                "Z1K100003",
                "Z1EQ00003",
                "Z1EN00003",
                "Z1EJ00003",
                "Z19R001DF",
                "Z19L00033",
                "Z19K0019C",
                "Z19J0001L",
                "Z19H001LZ",
                "Z19H0011L",
                "Z19D0023H",
                "MGPL3",
                "MGPK3",
                "MGPH3",
                "Z1K70000L",
                "Z1EU00003",
                "MWV13",
                "MD3H4",
                "Z19S000YC",
                "Z19S00043",
                "Z19S00033",
                "Z19R001KO",
                "Z19Q0001M",
                "Z19Q0001G",
                "Z19L001B7",
                "Z19L001AY",
                "Z19L00101",
                "Z19L000ZA",
                "Z19L000ER",
                "Z19L00036",
                "Z19L00034",
                "Z19L0001N",
                "Z19K002CN",
                "Z19K0001V",
                "Z19K0001T",
                "Z19H0001W",
                "Z19H0001V",
                "Z19H0001P",
                "Z19G000Z8",
                "Z19F001HV",
                "Z19E001CL",
                "Z19E000ZY",
                "Z19E000ZC",
                "Z19E000Y4",
                "Z19E000Y3",
                "Z19E00036",
                "Z19E00034",
                "Z19E00033",
                "Z19D0023E",
                "Z19D001KC",
                "Z19D0015E",
                "Z19D0012Y",
                "Z19D0012G",
                "Z19D0001U",
                "Z19D0001P",
                "Z197000HL",
                "Z1970004P",
                "Z195001А1",
                "Z195001LZ",
                "Z1950004S",
                "Z1950004R",
                "Z19500025",
                "Z19500023",
                "Z1950001Z",
                "MR7E3",
                "MQRX3",
                "MQRT3",
                "MQRQ3",
                "MQRN3",
                "MQRL3",
                "MQRA3",
                "MQR83",
                "MGTF3",
                "MJV83",
                "MJV93",
                "MJVA3",
                "MGPC3",
                "MGPM3",
                "Z12SIMAC01",
                "Z130IMAC01",
                "Z132IMAC01",
                "MGPD3",
                "MGPJ3",
                "MGPN3",
                "Z12TIMAC01",
                "Z131IMAC01",
                "Z133IMAC01",
                "Z12Q003AY",
                "MGPP3",
                "MGPR3",
                "MWUE3",
                "MWUG3",
                "MWUU3",
                "Z1K1000ES",
                "Z19D001G5",
                "Z19K001QC",
                "Z1330024S",
                "Z13300107",
                "Z131002M1",
                "Z131002LK",
                "Z131002LG",
                "Z131002LF",
                "Z131002LE",
                "Z1310027W",
                "Z1310006P",
                "Z1310005F",
                "Z130002B8",
                "Z130002A7",
                "Z130002A6",
                "Z130000NR",
                "Z1300007H",
                "Z12X003SJ",
                "Z12X003SH",
                "Z12X003SG",
                "Z12X003HR",
                "Z12X0036C",
                "Z12X002BC",
                "Z12X000TA",
                "Z12X0006P",
                "Z12X0005F",
                "Z12W0036V",
                "Z12W001E5",
                "Z12W000LS",
                "Z12W0007H",
                "Z12W00064",
                "Z12V002WN",
                "Z12V002WM",
                "Z12V002VH",
                "Z12V002VG",
                "Z12V002VF",
                "Z12V0006P",
                "Z12U002EP",
                "Z12U002EN",
                "Z12U0007H",
                "Z12T002HK",
                "Z12T002HJ",
                "Z12T000W0",
                "Z12R003QE",
                "Z12R003QD",
                "Z12R003QC",
                "Z12R003QB",
                "Z12R002N8",
                "Z12R0006P",
                "Z12R0005F",
                "Z12Q0034M",
                "Z12Q0034K",
                "Z12Q001SB",
                "Z12Q000V6",
                "Z12Q000BV",
                "Z12Q0007H",
                "Z12Q00064",
                "Z1970004R",
                "Z12X000LY",
                "Z12V001CW",
                "Z12V000QK",
                "MXWT2A",
                "MXWU2A",
                "MXWV2",
                "MHJY3L"
            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["24”", "27”"],
                    "aliases" : {
                        "24”" : ["24”", "24", "24-inch", "24 inch"],
                        "27”" : ["27”", "27", "27-inch", "27 inch"],
                    },
                },
                "chip" : {
                    "values" : [
                        "M1",
                        "M1 Pro",
                        "M1 Max",
                        "M2 Pro",
                        "M2 Max",
                        "M2",
                        "M3 Pro",
                        "M3 Max",
                        "M3",
                        "M4 Pro",
                        "M4 Max",
                        "M4"
                    ],
                    "aliases" : {
                        "M1 Pro" : ["M1 Pro"],
                        "M1 Max" : ["M1 Max"],
                        "M1" : ["M1"],
                        "M2 Pro" : ["M2 Pro"],
                        "M2 Max" : ["M2 Max"],
                        "M2" : ["M2"],
                        "M3 Pro" : ["M3 Pro"],
                        "M3 Max" : ["M3 Max"],
                        "M3" : ["M3"],
                        "M4 Pro" : ["M4 Pro"],
                        "M4 Max" : ["M4 Max"],
                        "M4" : ["M4"]
                    },
                },
                "RAM" : {
                    "values" : [
                        "8",
                        "16",
                        "18",
                        "24",
                        "32",
                        "36",
                        "48",
                        "64",
                        "128"
                    ],
                    "aliases" : {
                        "8" : ["8GB", "8 GB", "8ГБ", "8 ГБ", "8"],
                        "16" : ["16GB", "16 GB", "16ГБ", "16 ГБ", "16"],
                        "18" : ["18GB", "18 GB", "18ГБ", "18 ГБ", "18"],
                        "24" : ["24GB", "24 GB", "24ГБ", "24 ГБ", "24"],
                        "32" : ["32GB", "32 GB", "32ГБ", "32 ГБ", "32"],
                        "36" : ["36GB", "36 GB", "36ГБ", "36 ГБ", "36"],
                        "48" : ["48GB", "48 GB", "48ГБ", "48 ГБ", "48"],
                        "64" : ["64GB", "64 GB", "64ГБ", "64 ГБ", "64"],
                        "128" : ["128GB", "128 GB", "128ГБ", "128 ГБ", "128"],
                    },
                },
                "SSD" : {
                    "values" : [
                        "256",
                        "512",
                        "1TB",
                        "2TB"
                    ],
                    "aliases" : {
                        "256" : ["256 GB", "256GB", "256 ГБ", "256ГБ", "256"],
                        "512" : ["512 GB", "512GB", "512 ГБ", "512ГБ", "512"],
                        "1TB" : ["1024 GB", "1024GB", "1024 ГБ", "1024ГБ", "1TB", "1 TB"],
                        "2TB" : ["2048 GB", "2048GB", "2048 ГБ", "2048ГБ", "2TB", "2 TB"]
                    },
                },
                "color" : {
                    "values" : [
                        "Silver",
                        "Blue",
                        "Purple",
                        "Pink",
                        "Orange",
                        "Yellow",
                        "Green"
                    ],
                    "aliases" : {
                        "Silver" : ["Silver"],
                        "Blue" : ["Blue"],
                        "Purple" : ["Purple"],
                        "Pink" : ["Pink"],
                        "Orange" : ["Orange"],
                        "Yellow" : ["Yellow"],
                        "Green" : ["Green"]
                    },
                },
                "custom" : {
                    "values" : ["кастомный"],
                    "aliases" : {
                        "кастомный" : ["кастомный"],
                    },
                },
            },
        },
        "Mac Mini" : {
            "aliases" : [
                "iMac mini",
                "Mac mini"
            ],
            "attributes" : {
                "chip" : {
                    "values" : [
                        "M1",
                        "M1 Pro",
                        "M1 Max",
                        "M2 Pro",
                        "M2 Max",
                        "M2",
                        "M3 Pro",
                        "M3 Max",
                        "M3",
                        "M4 Pro",
                        "M4 Max",
                        "M4"
                    ],
                    "aliases" : {
                        "M1 Pro" : ["M1 Pro"],
                        "M1 Max" : ["M1 Max"],
                        "M1" : ["M1"],
                        "M2 Pro" : ["M2 Pro"],
                        "M2 Max" : ["M2 Max"],
                        "M2" : ["M2"],
                        "M3 Pro" : ["M3 Pro"],
                        "M3 Max" : ["M3 Max"],
                        "M3" : ["M3"],
                        "M4 Pro" : ["M4 Pro"],
                        "M4 Max" : ["M4 Max"],
                        "M4" : ["M4"]
                    },
                },
                "RAM" : {
                    "values" : [
                        "8",
                        "16",
                        "18",
                        "24",
                        "32",
                        "36",
                        "48",
                        "64",
                        "128"
                    ],
                    "aliases" : {
                        "16" : ["16GB", "16 GB", "16ГБ", "16 ГБ", "16"],
                        "18" : ["18GB", "18 GB", "18ГБ", "18 ГБ", "18"],
                        "24" : ["24GB", "24 GB", "24ГБ", "24 ГБ", "24"],
                        "32" : ["32GB", "32 GB", "32ГБ", "32 ГБ", "32"],
                        "36" : ["36GB", "36 GB", "36ГБ", "36 ГБ", "36"],
                        "48" : ["48GB", "48 GB", "48ГБ", "48 ГБ", "48"],
                        "64" : ["64GB", "64 GB", "64ГБ", "64 ГБ", "64"],
                        "128" : ["128GB", "128 GB", "128ГБ", "128 ГБ", "128"],
                    },
                },
                "SSD" : {
                    "values" : [
                        "256"
                        "512",
                        "1TB",
                        "2TB"
                    ],
                    "aliases" : {
                        "256" : ["256 GB", "256GB", "256 ГБ", "256ГБ", "256"],
                        "512" : ["512 GB", "512GB", "512 ГБ", "512ГБ", "512"],
                        "1TB" : ["1024 GB", "1024GB", "1024 ГБ", "1024ГБ", "1TB", "1 TB"],
                        "2TB" : ["2048 GB", "2048GB", "2048 ГБ", "2048ГБ", "2TB", "2 TB"]
                    },
                },
                "custom" : {
                    "values" : ["кастомный"],
                    "aliases" : {
                        "кастомный" : ["кастомный"],
                    },
                },
            },
        },
        "Mac Studio" : {
            "aliases" : [
                "iMac Studio",
                "Mac Studio",
                "Z14K0000V",
                "Z140004T",
                "Z14K0000Q",
                "MJMW3",
                "MJMV3",
                "MQH63",
                "MQH73"
            ],
            "attributes" : {
                "chip" : {
                    "values" : [
                        "M1",
                        "M1 Pro",
                        "M1 Max",
                        "M2 Pro",
                        "M2 Max",
                        "M2",
                        "M3 Pro",
                        "M3 Max",
                        "M3",
                        "M4 Pro",
                        "M4 Max",
                        "M4"
                    ],
                    "aliases" : {
                        "M1 Max" : ["M1 Max"],
                        "M1 Ultra" : ["M1 Ultra"],
                        "M2 Max" : ["M2 Max"],
                        "M2 Ultra" : ["M2 Ultra"],
                    },
                },
                "RAM" : {
                    "values" : [
                        "18",
                        "32",
                        "48",
                        "64",
                        "128"
                    ],
                    "aliases" : {
                        "18" : ["18GB", "18 GB", "18ГБ", "18 ГБ", "18"],
                        "32" : ["32GB", "32 GB", "32ГБ", "32 ГБ", "32"],
                        "36" : ["36GB", "36 GB", "36ГБ", "36 ГБ", "36"],
                        "48" : ["48GB", "48 GB", "48ГБ", "48 ГБ", "48"],
                        "64" : ["64GB", "64 GB", "64ГБ", "64 ГБ", "64"],
                        "128" : ["128GB", "128 GB", "128ГБ", "128 ГБ", "128"],
                    },
                },
                "SSD" : {
                    "values" : [
                        "256",
                        "512",
                        "1TB",
                        "2TB"
                    ],
                    "aliases" : {
                        "256" : ["256 GB", "256GB", "256 ГБ", "256ГБ", "256"],
                        "512" : ["512 GB", "512GB", "512 ГБ", "512ГБ", "512"],
                        "1TB" : ["1024 GB", "1024GB", "1024 ГБ", "1024ГБ", "1TB", "1 TB"],
                        "2TB" : ["2048 GB", "2048GB", "2048 ГБ", "2048ГБ", "2TB", "2 TB"]
                    },
                },
                "custom" : {
                    "values" : ["кастомный"],
                    "aliases" : {
                        "кастомный" : ["кастомный"],
                    },
                },
            },
        },
        "Mac Pro" :  {
            "aliases" : [
                "iMac Pro",
                "Mac Pro"
            ],
            "attributes" : {
                "chip" : {
                    "values" : [
                        "M1",
                        "M1 Pro",
                        "M1 Max",
                        "M2 Pro",
                        "M2 Max",
                        "M2",
                        "M3 Pro",
                        "M3 Max",
                        "M3",
                        "M4 Pro",
                        "M4 Max",
                        "M4"
                    ],
                    "aliases" : {
                        "M1 Max" : ["M1 Max"],
                        "M1 Ultra" : ["M1 Ultra"],
                        "M2 Max" : ["M2 Max"],
                        "M2 Ultra" : ["M2 Ultra"],
                    },
                },
                "RAM" : {
                    "values" : [
                        "64",
                        "128",
                        "192"
                    ],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "192" : ["192"],
                    },
                },
                "SSD" : {
                    "values" : [
                        "1TB",
                        "2TB",
                        "4TB",
                        "8TB"
                    ],
                    "aliases" : {
                        "1TB" : ["1024 GB", "1024GB", "1024 ГБ", "1024ГБ", "1TB", "1 TB"],
                        "2TB" : ["2048 GB", "2048GB", "2048 ГБ", "2048ГБ", "2TB", "2 TB"],
                        "4TB" : ["4096 GB", "4096GB", "4096 ГБ", "4096ГБ", "4TB", "4 TB"],
                        "8TB" : ["8192 GB", "8192GB", "8192 ГБ", "8192ГБ", "8TB", "8 TB"]
                    },
                },
            },
        },
        "5K Retina Display" : {
            "aliases" : [
                "Studio Display",
            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["27”"],
                    "aliases" : {
                        "27”" : ["27”", "27", "27-inch", "27 inch"],
                    },
                },
            },
        },
        "Pro Display XDR" : {
            "aliases" : [
                "Pro Display XDR",
                "Pro Display"
            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["32”"],
                    "aliases" : {
                        "32”" : ["32”", "32", "32-inch", "32 inch"],
                    },
                },
            },
        },
    },
    "Apple iPad" : {
        "iPad" : {
            "aliases" : [
                "iPad",
                "10",
                "9"
            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["10", "9"],
                    "aliases" : {
                        "10" : ["10", "10th", "10.9-inch", "10.9"],
                        "9" : ["9", "9th", "10.2-inch", "10.2"],
                        "11" : ["11"]
                    },
                },
                "SSD" : {
                    "values" : ["64GB", "256GB"],
                    "aliases" : {
                        "128GB" : ["128"],
                        "64GB" : ["64"],
                        "256GB" : ["256"]
                    },
                },
                "color" : {
                    "values" : ["Silver", "Pink", "Blue", "Yellow", "Space Gray"],
                    "aliases" : {
                        "Silver" : ["Silver"],
                        "Pink" : ["Pink"],
                        "Blue" : ["Blue"],
                        "Yellow" : ["Yellow"],
                        "Space Gray" : ["Space Gray", "Gray", "Grey"]
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "Cellular" : {
                    "values" : ["+ Cellular"],
                    "aliases" : {
                        "+ Cellular" : ["Cellular", "LTE", "5G"]
                    },
                },
            },
        },
        "iPad Mini" : {
            "aliases" : [
                "iPad Mini",
                "Mini",
            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["6", "7"],
                    "aliases" : {
                        "6" : ["6"],
                        "7" : ["7"]
                    },
                },
                "SSD" : {
                    "values" : ["64GB", "128GB", "256GB", "512GB"],
                    "aliases" : {
                        "64GB" : ["64"],
                        "128GB" : ["128"],
                        "256GB" : ["256"],
                        "512GB" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Blue", "Purple", "Starlight", "Pink", "Space Gray"],
                    "aliases" : {
                        "Blue" : ["Blue"],
                        "Purple" : ["Purple"],
                        "Starlight" : ["Starlight", "Starlit"],
                        "Pink" : ["Pink"],
                        "Space Gray" : ["Space Gray", "Gray", "Grey"]
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "Cellular" : {
                    "values" : ["+ Cellular"],
                    "aliases" : {
                        "+ Cellular" : ["Cellular", "LTE", "5G"]
                    },
                },
            },
        },
        "iPad Air" : {
            "aliases" : [
                "iPad Air",
                "Air",
            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["11", "13", "4", "5"],
                    "aliases" : {
                        "4" : ["4"],
                        "5" : ["5"],
                        "11”" : ["11”", "11", "11-inch", "11 inch"],
                        "12.9”" : ["12.9”", "12.9", "12.9-inch", "12.9 inch", "12,9”", "12,9", "12,9-inch",
                                   "12,9 inch"],
                        "13”" : ["13", "13”", "13-inch", "13 inch"]
                    },
                },
                "SSD" : {
                    "values" : ["64GB", "128GB", "256GB", "512GB"],
                    "aliases" : {
                        "64GB" : ["64"],
                        "128GB" : ["128"],
                        "256GB" : ["256"],
                        "512GB" : ["512"]
                    },
                },
                "color" : {
                    "values" : ["Blue", "Purple", "Starlight", "Space Gray"],
                    "aliases" : {
                        "Blue" : ["Blue"],
                        "Purple" : ["Purple"],
                        "Starlight" : ["Starlight"],
                        "Space Gray" : ["Space Gray", "Gray", "Grey"],
                        "Black" : "Black"
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "Cellular" : {
                    "values" : ["+ Cellular"],
                    "aliases" : {
                        "+ Cellular" : ["Cellular", "LTE", "5G"]
                    },
                },
                "chip" : {
                    "values" : [
                        "M2"
                    ],
                    "aliases" : {
                        "M2" : ["M2"],
                        "M3" : ["M3"],
                        "M4" : ["M4"]
                    },
                },
            },
        },
        "iPad Pro" : {
            "aliases" : [
                "iPad Pro",
                "Pro",
            ],
            "attributes" : {
                "diagonal" : {
                    "values" : ["11", "13", "4", "5"],
                    "aliases" : {
                        "4" : ["4"],
                        "5" : ["5"],
                        "11”" : ["11”", "11", "11-inch", "11 inch"],
                        "12.9”" : ["12.9”", "12.9", "12.9-inch", "12.9 inch", "12,9”", "12,9", "12,9-inch", "12,9 inch"],
                        "13”" : ["13", "13”", "13-inch", "13 inch"]
                    },
                },
                "SSD" : {
                    "values" : ["128GB", "256GB", "512GB", "1TB", "2TB"],
                    "aliases" : {
                        "128GB" : ["128"],
                        "256GB" : ["256"],
                        "512GB" : ["512"],
                        "1TB" : ["1TB"],
                        "2TB" : ["2TB"]
                    },
                },
                "color" : {
                    "values" : ["Silver", "Space Black", "Starlight", "Gray"],
                    "aliases" : {
                        "Silver" : ["Silver"],
                        "Space Black" : ["Space Black", "Black"],
                        "Starlight" : ["Starlight"],
                        "Gray" : ["Gray", "Grey"]
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "Cellular" : {
                    "values" : ["+ Cellular"],
                    "aliases" : {
                        "+ Cellular" : ["Cellular", "LTE", "5G"]
                    },
                },
                "chip" : {
                    "values" : ["M2", "M4"],
                    "aliases" : {
                        "M2" : ["M2"],
                        "M4" : ["M4"]
                    },
                },
                "glass" : {
                    "values" : ["Standard Glass", "Nano-texture Glass"],
                    "aliases" : {
                        "Standard Glass" : ["Standard Glass", "Standard"],
                        "Nano-texture Glass" : ["Nano-texture Glass", "Nano-Glass", "Nano"]
                    },
                },
            },
        },
    },

    #Android:
    "Samsung Galaxy" : {
        "Galaxy Watch" : {
            "aliases" : [
                "Galaxy Watch", "Galaxy Series", "Galaxy Ultra", "Watch Ultra", "Galaxy Fit"
            ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "5" : ["Galaxy Series 5", "Watch5", "Watch 5", "Series 5"],
                        "5 Pro" : ["Galaxy Series 5 Pro", "Watch5 Pro", "Watch 5 Pro", "Series 5 Pro"],
                        "6 Classic" : ["Galaxy Series 6 Classic", "Series 6 Classic", "Watch 6 Classic",
                                       "Watch6 Classic", "6 Classic"],
                        "6" : ["Galaxy Series 6", "Watch6", "Watch 6", "Series 6"],
                        "7" : ["Galaxy Series 7", "Watch7", "Watch 7", "Series 7"],
                        "Ultra" : ["Galaxy Ultra", "Watch Ultra"],
                        "FE" : ["Watch FE"],
                        "Fit 3" : ["Galaxy Fit 3", "Fit 3", "Fit3"]
                    },
                },
                "case_size" : {
                    "aliases" : {
                        "40mm" : ["40mm", "40 мм", "40"],
                        "43mm" : ["43mm", "43 мм", "43"],
                        "44mm" : ["44mm", "44 мм", "44"],
                        "45mm" : ["45mm", "45 мм", "45"],
                        "47mm" : ["47mm", "47 мм", "47"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black"],
                        "Silver" : ["Silver"],
                        "Cream" : ["Cream"],
                        "Green" : ["Green"],
                        "Grey" : ["Grey", "Gray"],
                        "White" : ["White"],
                        "Sapphire" : ["Sapphire"],
                        "Pink Gold" : ["Pink Gold"],
                        "Black Titanium" : ["Black Titanium"],
                        "Grey Titanium" : ["Grey Titanium"],
                    },
                },
            },
        },
        "Galaxy A": {
            "aliases" : ["A03", "A03", "A03s", "A04e", "A04", "A04s", "A05", "A05s",
                        "A06", "A13", "A13", "A14", "A14", "A15", "A15",
                        "A16", "A16", "A23", "A23", "A24", "A25", "A25", "A26",
                        "A33", "A34", "A35", "A35", "A36", "A53",
                        "A54", "A55", "A56", "A73"],
            "attributes" : {
                "model": {
                    "values": [
                        "A03 Core", "A03", "A03s", "A04e", "A04", "A04s", "A05", "A05s",
                        "A06", "A13", "A13 5G", "A14", "A14 5G", "A15", "A15 5G",
                        "A16", "A16 5G", "A23", "A23 5G", "A24", "A25", "A25 5G", "A26",
                        "A33 5G", "A34 5G", "A35", "A35 5G", "A36", "A53 5G",
                        "A54 5G", "A55 5G", "A56", "A73 5G"
                    ],
                    "aliases": {
                        "A03 Core": ["A03"],
                        "A03": ["A03"],
                        "A03s": ["A03s"],
                        "A04e": ["A04e"],
                        "A04": ["A04"],
                        "A04s": ["A04s"],
                        "A05s" : ["A05s"],
                        "A05": ["A05"],
                        "A06": ["A06"],
                        "A13": ["A13"],
                        "A13 5G": ["A13 5G"],
                        "A14": ["A14"],
                        "A14 5G": ["A14"],
                        "A15": ["A15"],
                        "A15 5G": ["A15 5G"],
                        "A16": ["A16"],
                        "A16 5G": ["A16 5G"],
                        "A23": ["A23"],
                        "A23 5G": ["A23 5G"],
                        "A24": ["A24"],
                        "A25": ["A25"],
                        "A25 5G": ["A25 5G"],
                        "A26": ["A26"],
                        "A33 5G": ["A33"],
                        "A34 5G": ["A34"],
                        "A35": ["A35"],
                        "A35 5G": ["A35 5G"],
                        "A36": ["A36"],
                        "A53 5G": ["A53"],
                        "A54 5G": ["A54"],
                        "A55 5G": ["A55"],
                        "A56": ["A56"],
                        "A73 5G": ["A73"]
                    },
                },
                "RAM" : {
                    "values" : ["4", "6", "8", "12"],
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"]
                    },
                },
                "SSD" : {
                    "values" : ["64", "128", "256", "512"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Blue Black" : ["Blue Black", "BlueBlack"],
                        "Light Gray" : ["Light Gray", "Lightgray"],
                        "Black" : ["Black"],
                        "Red" : ["Red"],
                        "White" : ["White"],
                        "Copper" : ["Copper"],
                        "Light Green" : ["Light Green", "LightGreen"],
                        "Light Blue" : ["Light Blue", "LightBlue"],
                        "Ice Blue" : ["Ice Blue", "IceBlue"],
                        "Green" : ["Green"],
                        "Blue" : ["Blue"],
                        "Silver" : ["Silver"],
                        "Violet" : ["Violet",],
                        "Peach" : ["Peach"],
                        "Lavender" : ["Lavender"],
                        "Yellow" : ["Yellow"],
                        "Gray" : ["Gray", "Grey"],
                        "Mint" : ["Mint"],
                        "Graphite" : ["Graphite"],
                        "Lime" : ["Lime"],
                        "Lemon" : ["Lemon"],
                        "Navy" : ["Navy"],
                        "Lilac" : ["Lilac"],
                        "Gold" : ["Gold"],
                        "Olive" : ["Olive"],
                        "Pink" : ["Pink"]
                    },
                },
            },
        },
        "Galaxy M" : {
            "aliases" : ["M10", "M10s", "M11", "M12", "M13", "M13", "M14",
                        "M20", "M21", "M22", "M23", "M23", "M30", "M30s", "M31", "M31s",
                        "M32", "M33", "M34", "M40", "M42", "M50", "M51",
                        "M52", "M53", "M54", "M55", "M55s"],
            "attributes" : {
                "model" : {
                    "values" : [
                        "M10", "M10s", "M11", "M12", "M13", "M13 5G", "M14 5G",
                        "M20", "M21", "M22", "M23", "M23 5G", "M30", "M30s", "M31", "M31s",
                        "M32", "M32 Prime", "M33 5G", "M34 5G", "M40", "M42 5G", "M50", "M51",
                        "M52 5G", "M53 5G", "M54 5G", "M55 5G", "M55s"
                    ],
                    "aliases" : {
                            "M10": ["M10"],
                            "M10s": ["M10s"],
                            "M11": ["M11"],
                            "M12": ["M12"],
                            "M13": ["M13"],
                            "M13 5G": ["M13"],
                            "M14 5G": ["M14"],
                            "M20": ["M20"],
                            "M21": ["M21"],
                            "M22": ["M22"],
                            "M23": ["M23"],
                            "M23 5G": ["M23"],
                            "M30": ["M30"],
                            "M30s": ["M30s"],
                            "M31": ["M31"],
                            "M31s": ["M31s"],
                            "M32": ["M32"],
                            "M32 Prime": ["M32 Prime"],
                            "M33 5G": ["M33"],
                            "M34 5G": ["M34"],
                            "M40": ["M40"],
                            "M42 5G": ["M42"],
                            "M50": ["M50"],
                            "M51": ["M51"],
                            "M52 5G": ["M52"],
                            "M53 5G": ["M53"],
                            "M54 5G": ["M54"],
                            "M55 5G": ["M55"],
                            "M55s": ["M55s"]
                    },
                },
                "RAM" : {
                    "values" : ["4", "6", "8", "12"],
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"]
                    },
                },
                "SSD" : {
                    "values" : ["64", "128", "256", "512"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"]
                    },
                },
                "color" : {
                    "values" : [
                        "Blue",
                        "Dark Grey",
                        "Stone Blue",
                        "Piano Black",
                        "Metallic Blue",
                        "Black",
                        "Violet",
                        "Green",
                        "Aqua Green",
                        "Midnight Blue",
                        "Stardust Brown",
                        "Icy Silver",
                        "Berry Blue",
                        "Smoky Teal",
                        "Charcoal Black",
                        "Ocean Blue",
                        "Raven Black",
                        "Light Blue",
                        "White",
                        "Deep Green",
                        "Orange Copper",
                        "Gradation Black",
                        "Gradation Blue",
                        "Opal Black",
                        "Sapphire Blue",
                        "Pearl White",
                        "Red",
                        "Mirage Black",
                        "Mirage Blue",
                        "Deep Ocean Blue",
                        "Mystique Green",
                        "Emerald Brown",
                        "Prism Silver",
                        "Waterfall Blue",
                        "Seawater Blue",
                        "Cocktail Orange",
                        "Prism Dot Black",
                        "Prism Dot Gray",
                        "Celestial Black",
                        "Electric Blue",
                        "Icy Blue",
                        "Blazing Black",
                        "Brown",
                        "Dark Blue",
                        "Light Green"
                    ],
                    "aliases" : {
                        "Blue" : ["Blue"],
                        "Dark Grey" : ["Dark Grey"],
                        "Stone Blue" : ["Stone Blue"],
                        "Piano Black" : ["Piano Black"],
                        "Metallic Blue" : ["Metallic Blue"],
                        "Black" : ["Black"],
                        "Violet" : ["Violet"],
                        "Green" : ["Green"],
                        "Aqua Green" : ["Aqua Green"],
                        "Midnight Blue" : ["Midnight Blue"],
                        "Stardust Brown" : ["Stardust Brown"],
                        "Icy Silver" : ["Icy Silver"],
                        "Berry Blue" : ["Berry Blue"],
                        "Smoky Teal" : ["Smoky Teal"],
                        "Charcoal Black" : ["Charcoal Black"],
                        "Ocean Blue" : ["Ocean Blue"],
                        "Raven Black" : ["Raven Black"],
                        "Light Blue" : ["Light Blue"],
                        "White" : ["White"],
                        "Deep Green" : ["Deep Green"],
                        "Orange Copper" : ["Orange Copper"],
                        "Gradation Black" : ["Gradation Black"],
                        "Gradation Blue" : ["Gradation Blue"],
                        "Opal Black" : ["Opal Black"],
                        "Sapphire Blue" : ["Sapphire Blue"],
                        "Pearl White" : ["Pearl White"],
                        "Red" : ["Red"],
                        "Mirage Black" : ["Mirage Black"],
                        "Mirage Blue" : ["Mirage Blue"],
                        "Deep Ocean Blue" : ["Deep Ocean Blue"],
                        "Mystique Green" : ["Mystique Green"],
                        "Emerald Brown" : ["Emerald Brown"],
                        "Prism Silver" : ["Prism Silver"],
                        "Waterfall Blue" : ["Waterfall Blue"],
                        "Seawater Blue" : ["Seawater Blue"],
                        "Cocktail Orange" : ["Cocktail Orange"],
                        "Prism Dot Black" : ["Prism Dot Black"],
                        "Prism Dot Gray" : ["Prism Dot Gray"],
                        "Celestial Black" : ["Celestial Black"],
                        "Electric Blue" : ["Electric Blue"],
                        "Icy Blue" : ["Icy Blue"],
                        "Blazing Black" : ["Blazing Black"],
                        "Brown" : ["Brown"],
                        "Dark Blue" : ["Dark Blue"],
                        "Light Green" : ["Light Green"]
                    },
                },
            },
        },
        "Galaxy S" : {
            "aliases" : [
                "S21", "S 21",
                "S21+", "S 21+", "S21 +", "S 21 +", "S21 plus", "S 21 plus", "S21plus",
                "S21 Ultra", "S21Ultra", "S21Ultra", "S 21Ultra", "S 21 Ultra",
                "S21FE", "S 21FE", "S21 FE", "S 21 FE",
                "S22", "S 22",
                "S22+", "S 22+", "S22 +", "S 22 +", "S22 plus", "S 22 plus", "S22plus",
                "S22 Ultra", "S22 Ultra", "S22Ultra", "S22Ultra", "S 22Ultra", "S 22 Ultra",
                "S23", "S 23",
                "S23+", "S 23+", "S23 +", "S 23 +", "S23 plus", "S 23 plus", "S23plus",
                "S23 Ultra", "S23 Ultra", "S23Ultra", "S23Ultra", "S 23Ultra", "S 23 Ultra",
                "S23FE", "S 23FE", "S23 FE", "S 23 FE",
                "S24+", "S 24+", "S24 +", "S 24 +", "S24 plus", "S 24 plus", "S24plus",
                "S24", "S 24",
                "S24 Ultra", "S24 Ultra", "S24Ultra", "S24Ultra", "S 24Ultra", "S 24 Ultra",
                "S24FE", "S 24FE", "S24 FE", "S 24 FE",
                "S25", "S 25",
                "S25+", "S25+", "S 25+", "S25 +", "S 25 +", "S25 plus", "S 25 plus", "S25plus",
                "S25 Ultra", "S25 Ultra", "S25Ultra", "S25Ultra", "S 25Ultra", "S 25 Ultra",
                "S25 Edge", "S25 Edge", "S25Edge"
            ],
            "attributes" : {
                "model" : {
                    "values" : [
                            "S21", "S 21",
                            "S21+", "S 21+", "S21 +", "S 21 +", "S21 plus", "S 21 plus", "S21plus",
                            "S21FE", "S 21FE", "S21 FE", "S 21 FE",
                            "S21 Ultra", "S21Ultra", "S21Ultra", "S 21Ultra", "S 21 Ultra",
                            "S22", "S 22",
                            "S22FE", "S 22FE", "S22 FE", "S 22 FE",
                            "S22+", "S 22+", "S22 +", "S 22 +", "S22 plus", "S 22 plus", "S22plus",
                            "S22 Ultra", "S22 Ultra", "S22Ultra", "S22Ultra", "S 22Ultra", "S 22 Ultra",
                            "S23", "S 23",
                            "S23+", "S 23+", "S23 +", "S 23 +", "S23 plus", "S 23 plus", "S23plus",
                            "S23 Ultra", "S23 Ultra", "S23Ultra", "S23Ultra", "S 23Ultra", "S 23 Ultra",
                            "S23FE", "S 23FE", "S23 FE", "S 23 FE",
                            "S24+", "S 24+", "S24 +", "S 24 +", "S24 plus", "S 24 plus", "S24plus",
                            "S24", "S 24",
                            "S24 Ultra", "S24 Ultra", "S24Ultra", "S24Ultra", "S 24Ultra", "S 24 Ultra",
                            "S24FE", "S 24FE", "S24 FE", "S 24 FE",
                            "S25", "S 25",
                            "S25+", "S25+", "S 25+", "S25 +", "S 25 +", "S25 plus", "S 25 plus", "S25plus",
                            "S25 Ultra", "S25 Ultra", "S25Ultra", "S25Ultra", "S 25Ultra", "S 25 Ultra",
                            "S25 Edge", "S25 Edge", "S25Edge"
                    ],
                    "aliases" : {
                        "S21" : ["S21", "S 21"],
                        "S21+" : ["S21+", "S 21+", "S21 +", "S 21 +", "S21 plus", "S 21 plus", "S21plus"],
                        "S21 FE" : ["S21FE", "S 21FE", "S21 FE", "S 21 FE",],
                        "S21 Ultra" : ["S21 Ultra", "S21Ultra", "S21Ultra", "S 21Ultra", "S 21 Ultra", ],
                        "S22" : ["S22", "S 22"],
                        "S22 FE" : ["S22FE", "S 22FE", "S22 FE", "S 22 FE"],
                        "S22+" : ["S22+", "S 22+", "S22 +",  "S 22 +", "S22 plus", "S 22 plus", "S22plus"],
                        "S22 Ultra" : ["S22 Ultra", "S22Ultra", "S22Ultra", "S 22Ultra", "S 22 Ultra",],
                        "S23" : ["S23", "S 23"],
                        "S23+" : ["S23+", "S 23+", "S23 +",  "S 23 +", "S23 plus", "S 23 plus", "S23plus"],
                        "S23 Ultra" : ["S23 Ultra", "S23Ultra", "S23Ultra", "S 23Ultra", "S 23 Ultra",],
                        "S23 FE" : ["S23FE", "S 23FE", "S23 FE", "S 23 FE"],
                        "S24+" : ["S24+", "S 24+", "S24 +",  "S 24 +", "S24 plus", "S 24 plus", "S24plus"],
                        "S24" : ["S24", "S 24"],
                        "S24 Ultra" : ["S24 Ultra", "S24Ultra", "S24Ultra", "S 24Ultra", "S 24 Ultra",],
                        "S24 FE" : ["S24FE", "S 24FE", "S24 FE", "S 24 FE"],
                        "S25" : ["S25", "S 25"],
                        "S25+" : ["S25+", "S 25+", "S25 +",  "S 25 +", "S25 plus", "S 25 plus", "S25plus"],
                        "S25 Ultra" : ["S25 Ultra", "S25Ultra", "S25Ultra", "S 25Ultra", "S 25 Ultra",],
                        "S25 Edge" : ["S25 Edge", "S25Edge"]
                    },
                },
                "RAM" : {
                    "values" : ["4", "6", "8", "12", "16"],
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"]
                    },
                },
                "SSD" : {
                    "values" : ["64", "128", "256", "512", "1TB"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
        "Galaxy Z" : {
            "aliases" : [
                "Z Fold", "Z Flip",
                "Z Fold 4", "Z Flip 4", "Z Fold 5", "Z Flip 5", "Z Fold 6", "Z Flip 6",
                "Z Fold4", "Z Fold5", "Z Fold6", "Z Flip4", "Z Flip5", "Z Flip6"
            ],
            "attributes" : {
                "model" : {
                    "values" : [
                        "Z Fold 4", "Z Flip 4", "Z Fold 5", "Z Flip 5", "Z Fold 6", "Z Flip 6",
                    ],
                    "aliases" : {
                        "Z Fold 4" : ["Z Fold 4", "Z Fold4"],
                        "Z Flip 4" : ["Z Flip 4", "Z Flip4"],
                        "Z Fold 5" : ["Z Fold 5", "Z Fold5"],
                        "Z Flip 5" : ["Z Flip 5", "Z Flip5"],
                        "Z Fold 6" : ["Z Fold 6", "Z Fold6"],
                        "Z Flip 6" : ["Z Flip 6", "Z Flip6"],
                    },
                },
                "RAM" : {
                    "values" : ["4", "6", "8", "12", "16"],
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"]
                    },
                },
                "SSD" : {
                    "values" : ["64", "128", "256", "512", "1TB"],
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
        "Galaxy Tab" : {
            "aliases" : [
                "Galaxy Tab",
                "Tab",
            ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "A9" : ["A9", "A 9"],
                        "A9+" : ["A9+", "A 9+"]
                    },
                },
                "diagonal" : {
                    "aliases" : {
                        "8.7”" : ["8.7"],
                        "11”" : ["11", "11.0"]
                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4", "4+"],
                        "8" : ["8", "8+"],
                        "16" : ["16", "16+"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Silver" : ["Silver"],
                        "Graphite" : ["Graphite"],
                        "Navy" : ["Navy"],
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "LTE" : {
                    "aliases" : {
                        "LTE" : ["Cellular", "LTE", "5G"]
                    },
                },
            },
        },
    },
    "Xiaomi" : {
        "Xiaomi Watch" : {
            "aliases" : [
                "Redmi Watch", "Smart Band", "Xiaomi Watch"
            ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "Xiaomi Redmi Watch 4" : ["Redmi Watch 4"],
                        "Xiaomi Redmi Watch 5" : ["Redmi Watch 5"],
                        "Xiaomi Redmi Watch 5 Active" : ["Redmi Watch 5 Active"],
                        "Xiaomi Redmi Watch 5 Lite" : ["Redmi Watch 5 Lite"],
                        "Xiaomi Smart Band 9" : ["Xiaomi Smart Band 9", "Smart Band 9"],
                        "Xiaomi Smart Band 9 Pro" : ["Xiaomi Smart Band 9 Pro", "Smart Band 9 Pro"],
                        "Xiaomi Smart Band 9 Active" : ["Xiaomi Smart Band 9 Active", "Smart Band 9 Active"],
                        "Xiaomi Watch 2" : ["Xiaomi Watch 2"],
                        "Xiaomi Watch 2 Pro" : ["Xiaomi Watch 2 Pro"],
                        "Xiaomi Watch S2" : ["Xiaomi Watch S2", "Xiaomi Watch S 2"],
                        "Xiaomi Watch 3" : ["Xiaomi Watch 3"],
                        "Xiaomi Watch 3 Pro" : ["Xiaomi Watch 3 Pro"],
                        "Xiaomi Watch S3" : ["Xiaomi Watch S3", "Xiaomi Watch S 3"],
                    },
                },
            },
        },
        "Xiaomi" : {
            "aliases" : ["12 Lite", "12Lite",
                "12",
                "12T",
                "12T Pro", "12TPro",
                "12 Pro", "12Pro",
                "12S",
                "12S Pro", "12SPro",
                "12S Ultra", "12SUltra",
                "13",
                "13 Pro",
                "MIX Fold 2", "MIX Fold2", "Fold2", "Fold 2",
                "13 Lite", "13Lite",
                "Civi 3", "Civi3",
                "13T",
                "13T Pro", "13TPro",
                "13 Ultra", "13Ultra",
                "14",
                "14 Pro", "14Pro",
                "MIX Fold 3", "MIX Fold3", "Fold3", "Fold 3",
                "14 Civi", "14Civi",
                "Civi 4 Pro", "Civi4Pro", "Civi 4Pro", "Civi4 Pro",
                "14T", "14T Pro", "14TPro",
                "14 Ultra", "14 Ultra",
                "15",
                "15 Pro", "15Pro",
                "MIX Fold 4",
                "15 Ultra", "15Ultra"],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "12" : ["12"],
                        "12 Lite" : ["12 Lite", "12Lite"],
                        "12T" : ["12T"],
                        "12T Pro" : ["12T Pro", "12TPro"],
                        "12 Pro" : ["12 Pro", "12Pro"],
                        "12S" : ["12S"],
                        "12S Pro" : ["12S Pro", "12SPro"],
                        "12S Ultra" : ["12S Ultra", "12SUltra"],
                        "13" : ["13"],
                        "13 Pro" : ["13 Pro"],
                        "MIX Fold 2" : ["MIX Fold 2", "MIX Fold2", "Fold2", "Fold 2"],
                        "13 Lite" : ["13 Lite", "13Lite"],
                        "Civi 3" : ["Civi 3", "Civi3"],
                        "13T" : ["13T"],
                        "13T Pro" : ["13T Pro", "13TPro"],
                        "13 Ultra" : ["13 Ultra", "13Ultra"],
                        "14" : ["14"],
                        "14 Pro" : ["14 Pro", "14Pro"],
                        "MIX Fold 3" : ["MIX Fold 3", "MIX Fold3", "Fold3", "Fold 3"],
                        "14 Civi" : ["14 Civi", "14Civi"],
                        "Civi 4 Pro" : ["Civi 4 Pro", "Civi4Pro", "Civi 4Pro", "Civi4 Pro"],
                        "14 Ultra" : ["14 Ultra", "14 Ultra"],
                        "15": ["15"],
                        "15 Pro": ["15 Pro", "15Pro"],
                        "MIX Fold 4": ["MIX Fold 4"],
                        "14T" : ["14T"],
                        "14T Pro" : ["14T Pro", "14TPro"],
                        "15 Ultra" : ["15 Ultra", "15Ultra"]
                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
        "Xiaomi Pad" : {
            "aliases" : [
                "Xiaomi Pad", "mi pad"
            ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "Pad 5" : ["Pad 5"],
                        "Pad 5 Pro" : ["Pad 5 Pro"],
                        "Pad 6" : ["Pad 6"],
                        "Pad 6S Pro" : ["Pad 6S Pro"],
                        "Pad 7" : ["Pad 7"],
                        "Pad 7 Pro" : ["Pad 7 Pro"],

                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Gray" : ["Gray", "Grey"],
                        "Green" : ["Green"],
                        "Purple" : ["Purple"],
                        "Silver" : ["Silver"],
                        "Blue" : ["Blue"],
                        "Black" : ["black"],
                        "Gold" : ["Gold"]
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "+ 5G" : {
                    "aliases" : {
                        "+ 5G" : ["Cellular", "LTE", "5G", "sim"]
                    },
                },
            },
        },
        "Redmi" : {
            "aliases" : [
                "A1",
                "12",
                "12C",
                "Note 12",
                "Note 12 Pro",
                "Note 12 Pro+",
                "A2",
                "A2",
                "Note 12 Turbo",
                "13",
                "13C",
                "Note 13",
                "Note 13 Pro",
                "Note 13 Pro+",
                "A3",
                "14C",
                "Note 14",
                "Note 14 Pro",
                "Note 14 Pro+",
                "K80",
                "K80 Pro"
                ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "A1 4G" : ["A1"],
                        "12 4G" : ["12","12 4G"],
                        "12 5G" : ["12 5G"],
                        "12C 4G" : ["12C"],
                        "Note 12 4G" : ["Note 12", "Note 12 4G"],
                        "Note 12 5G" : ["Note 12 5G"],
                        "Note 12 Pro 5G" : ["Note 12 Pro"],
                        "Note 12 Pro+ 5G" : ["Note 12 Pro+", "Note 12 Pro plus"],
                        "A2 4G" : ["A2"],
                        "A2+ 4G" : ["A2"],
                        "Note 12 Turbo 5G" : ["Note 12 Turbo"],
                        "13 4G" : ["13", "13 4G"],
                        "13 5G" : ["13"],
                        "13C 4G" : ["13C"],
                        "Note 13 4G" : ["Note 13 4G", "Note 13"],
                        "Note 13 5G" : ["Note 13 5G"],
                        "Note 13 Pro 4G" : ["Note 13 Pro", "Note 13 Pro 4G"],
                        "Note 13 Pro 5G" : ["Note 13 Pro 5G"],
                        "Note 13 Pro+ 5G" : ["Note 13 Pro+", "Note 13 Pro +", "Note 13 Pro plus"],
                        "A3 4G" : ["A3"],
                        "14C 4G" : ["14C"],
                        "Note 14 4G" : ["Note 14 4G", "Note 14"],
                        "Note 14 5G" : ["Note 14 5G"],
                        "Note 14 Pro 4G" : ["Note 14 Pro 4G", "Note 14 Pro"],
                        "Note 14 Pro 5G" : ["Note 14 Pro 5G"],
                        "Note 14 Pro+ 5G" : ["Note 14 Pro+", "Note 14 Pro+ ", "Note 14 Pro plus"],
                        "K80 5G" : ["K80"],
                        "K80 Pro 5G" : ["K80 Pro"],
                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"]
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
        "Redmi Pad" : {
            "aliases" : [
                "Redmi Pad",
            ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "Pad SE" : ["PAD SE", "SE"],
                        "Pad Pro" : ["Pad Pro"],
                        "Pad" : ["Pad"],

                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"]
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Gray" : ["Gray", "Grey"],
                        "Green" : ["Green"],
                        "Purple" : ["Purple"],
                        "Silver" : ["Silver"],
                        "Blue" : ["Blue"]
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "+ 5G" : {
                    "aliases" : {
                        "+ 5G" : ["Cellular", "LTE", "5G", "sim"]
                    },
                },
            },
        },
        "Poco" : {
            "aliases" : ["C40", "C50", "C55", "C65", "C61", "C75",
                "M4 Pro", "M5", "M5s", "M6", "M6 Pro", "M7 Pro",
                "X4 Pro", "X4 GT", "X5","X5 Pro","X6","X6 Pro","X7", "X7 Pro",
                "F4","F4 GT","F5","F6","F6 Pro","F7","F7 Pro"
                ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "C40" : ["C40"],
                        "C50" : ["C50"],
                        "C55" : ["C55"],
                        "C65" : ["C65"],
                        "C61" : ["C61"],
                        "C75" : ["C75"],
                        "C75 5G" : ["C75 5G"],
                        "M4 Pro": ["M4 Pro"],
                        "M4 Pro 5G": ["M4 Pro 5G"],
                        "M5": ["M5"],
                        "M5s": ["M5s"],
                        "M6": ["M6"],
                        "M6 Pro 5G": ["M6 Pro"],
                        "M7 Pro 5G": ["M7 Pro"],
                        "X4 Pro 5G": ["X4 Pro"],
                        "X4 GT 5G": ["X4 GT"],
                        "X5 5G": ["X5"],
                        "X5 Pro 5G": ["X5 Pro"],
                        "X6 5G": ["X6"],
                        "X6 Pro 5G": ["X6 Pro"],
                        "X7 5G": ["X7"],
                        "X7 Pro 5G" : ["X7 Pro"],
                        "F4 5G": ["F4"],
                        "F4 GT 5G": ["F4 GT"],
                        "F5 5G": ["F5"],
                        "F5 Pro 5G": ["F5 Pro"],
                        "F6 5G": ["F6"],
                        "F6 Pro 5G": ["F6 Pro"],
                        "F7 5G": ["F7"],
                        "F7 Pro 5G": ["F7 Pro"],

                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
        "Poco Pad" : {
            "aliases" : [
                "Poco Pad",
            ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "Pad" : ["Pad"],

                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"]
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Gray" : ["Gray", "Grey"],
                        "Green" : ["Green"],
                        "Purple" : ["Purple"],
                        "Silver" : ["Silver"],
                        "Blue" : ["Blue"]
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "+ 5G" : {
                    "aliases" : {
                        "+ 5G" : ["Cellular", "LTE", "5G", "sim"]
                    },
                },
            },
        },
    },
    "Google" : {
        "Pixel" : {
            "aliases" : ["Pixel", "Google"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Pixel 7" : ["Pixel 7"],
                        "Pixel 7 Pro" : ["Pixel 7 Pro", "7 Pro"],
                        "Pixel 8" : ["Pixel 8"],
                        "Pixel 8a" : ["Pixel 8a", "Pixel 8 a"],
                        "Pixel 8 Pro" : ["Pixel 8 Pro", "Pixel 8Pro", "Pixel Pro 8"],
                        "Pixel 9" : ["Pixel 9"],
                        "Pixel 9 Pro XL" : ["Pixel 9 Pro XL", "9 Pro XL"],
                        "Pixel Fold" : ["Pixel Fold"]
                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
        "Pixel Watch" : {
            "aliases" : ["Pixel", "Google"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Pixel Watch" : ["Pixel Watch"],
                        "Pixel Watch 2" : ["Pixel Watch 2", "Pixel Watch2"],
                        "Pixel Watch 3" : ["Pixel Watch 3", "Pixel Watch3"],
                    },
                },
                "case_size" : {
                    "aliases" : {
                        "40mm" : ["40mm", "40 мм", "40"],
                        "41mm" : ["41mm", "41 мм", "41"],
                        "43mm" : ["43mm", "43 мм", "43"],
                        "44mm" : ["44mm", "44 мм", "44"],
                        "45mm" : ["45mm", "45 мм", "45"],
                        "47mm" : ["47mm", "47 мм", "47"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Matte Black" : ["Matte Black", "Black"],
                        "Polished Silver" : ["Polished Silver", "Silver"],
                        "Champagne Gold" : ["Champagne Gold", "Gold"],
                    },
                },
            },
        },
    },
    "OnePlus" : {
        "OnePlus Watch" : {
            "aliases" : [
                "OnePlus Watch"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "OnePlus Watch 2" : ["OnePlus Watch 2"],
                        "OnePlus Watch 2R" : ["OnePlus Watch 2R"],
                        "OnePlus Watch 3" : ["OnePlus Watch 3"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black"],
                        "White" : ["White"],
                        "Yellow" : ["Yellow"],
                        "Blue" : ["Blue"],
                        "Green" : ["Green"],
                        "Gray" : ["Gray"]
                    },
                },
            },
        },
        "OnePlus" : {
            "aliases" : ["OnePlus", "OnePlus 12", "OnePlus 13", "OnePlus 13r"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "OnePlus 12" : ["OnePlus 12"],
                        "OnePlus 13R" : ["OnePlus 13R", "OnePlus 13R"],
                        "OnePlus 13" : ["OnePlus 13"],
                        "OnePlus Nord 4": ["OnePlus Nord 4", "OnePlus Nord4",]
                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
        "OnePlus Pad" : {
            "aliases" : [
                "OnePlus Pad",
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "OnePlus Pad" : ["OnePlus Pad"],
                        "OnePlus Pad 2" : ["OnePlus Pad 2", "OnePlus Pad2"],
                        "OnePlus Pad Pro" : ["OnePlus Pad Pro"],
                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Gray" : ["Gray", "Grey"],
                        "Green" : ["Green"],
                        "Purple" : ["Purple"],
                        "Silver" : ["Silver"],
                        "Blue" : ["Blue"],
                        "White" : ["White"],
                        "Black" : ["Black"]
                    },
                },
                "Wi-Fi" : {
                    "values" : ["Wi-Fi"],
                    "aliases" : {
                        "Wi-Fi" : ["Wi-Fi", "Wi Fi", "WiFi"]
                    },
                },
                "+ LTE" : {
                    "aliases" : {
                        "+ LTE" : ["Cellular", "LTE", "5G", "sim"]
                    },
                },
            },
        },
    },
    "Realme" : {
        "Realme" : {
            "aliases" : ["Realme"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Realme 12 5G" : ["Realme 12"],
                        "Realme 12 Pro 5G": ["Realme 12 Pro"],
                        "Realme 12 Pro+ 5G": ["Realme 12 Pro+"],
                        "Realme 13 5G": ["Realme 13"],
                        "Realme 13+ 5G": ["Realme 13+"],
                        "Realme 13 Pro 5G": ["Realme 13 Pro"],
                        "Realme 13 Pro+ 5G": ["Realme 13 Pro+"],
                        "Realme GT 6T": ["Realme GT 6T", "GT6T"],
                        "Realme GT 6": ["Realme GT 6", "GT6"],

                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
    },
    "Honor" : {
        "Honor" : {
            "aliases" : ["Honor"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Honor 200" : ["Honor 200"],
                        "Honor 200 Lite" : ["Honor 200 Lite", "200 Lite"],
                        "Honor Magic V3" : ["Honor Magic V3", "Magic V3"],
                        "Honor Magic 6 Pro" : ["Honor Magic 6 Pro", "Magic 6 Pro"],
                        "Honor X9c" : ["X9c", "X 9c"],
                        "Honor X8c" : ["X8c", "X 8c"],
                        "Honor X7b" : ["X7b", "X 7b"],
                        "Honor X6a" : ["X6a", "X6a"],
                        "Honor Magic 7 Pro" : ["Magic 7 Pro"],
                        "Honor Magic 7 Lite" : ["Magic 7 Lite"],
                        "Honor X7c" : ["X7c", "X 7c"],
                        "Honor X6b" : ["X6b", "X 6b"],

                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
    },
    "Infinix" : {
        "Infinix" : {
            "aliases" : ["Infinix"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Infinix Hot 50 Pro" : ["Infinix Hot 50 Pro"],
                        "Infinix Hot 50 Pro+" : ["Infinix Hot 50 Pro+", "Infinix Hot 50 Pro +", "Infinix Hot 50 Pro plus"],
                        "Infinix Note 50 Pro+ 5G" : ["Infinix Note 50 Pro+ 5G", "Infinix Note 50 Pro+", "Infinix Note 50 Pro plus"],
                        "Infinix GT 20 Pro" : ["Infinix GT 20 Pro", "Infinix GT20 Pro"],
                        "Infinix Smart 9" : ["Infinix Smart 9"]
                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
    },
    "Doogee" : {
        "Doogee" : {
            "aliases" : ["Doogee"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Doogee V Max Plus" : ["V Max Plus", "VMax Plus"],
                        "Doogee V40 Pro" : ["V 40 Pro", "V40 Pro"],
                        "Doogee S200" : ["S200", "S 200"],
                        "Doogee Smini" : ["Smini", "S mini"],
                        "Doogee R10" : ["R10", "R 10"],
                    },
                },
                "RAM" : {
                    "aliases" : {
                        "4" : ["4"],
                        "6" : ["6"],
                        "8" : ["8"],
                        "12" : ["12"],
                        "16" : ["16"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64" : ["64"],
                        "128" : ["128"],
                        "256" : ["256"],
                        "512" : ["512"],
                        "1TB" : ["1TB"]
                    },
                },
            },
        },
    },
    "Tecno Mobile": {
        "Tecno Mobile": {
            "aliases": ["Tecno Spark", "Tecno Camon", "Tecno Pova"],
            "attributes": {
                "model": {
                    "aliases": {
                        "Tecno Spark Go 1": ["Tecno Spark Go 1", "Tecno Spark Go 2024"],
                        "Tecno Spark 30C": ["Tecno Spark 30C"],
                        "Tecno Spark 30 Pro": ["Tecno Spark 30 Pro"],
                        "Tecno Camon 30 Pro": ["Tecno Camon 30 Pro"],
                        "Tecno Camon 30S": ["Tecno Camon 30S"],
                        "Tecno Pova 6 Neo": ["Tecno Pova 6 Neo"]
                    }
                },
                "RAM": {
                    "aliases": {
                        "4": ["4GB", "4 GB"],
                        "6": ["6GB", "6 GB"],
                        "8": ["8GB", "8 GB"],
                        "12": ["12GB", "12 GB"],
                        "16": ["16GB", "16 GB"]
                    }
                },
                "SSD": {
                    "aliases": {
                        "64": ["64GB", "64 GB"],
                        "128": ["128GB", "128 GB"],
                        "256": ["256GB", "256 GB"],
                        "512": ["512GB", "512 GB"],
                        "1TB": ["1TB"]
                    }
                },
                "color": {
                    "aliases": {
                        "Black": ["Black"],
                        "White": ["White"],
                        "Gold": ["Gold"],
                        "Green": ["Green"],
                        "Silver": ["Silver"],
                        "Blue": ["Blue"],
                        "Violet": ["Violet"],
                        "Gray" : ["Gray"]
                    }
                }
            }
        }
    },

    #Дайсон:
    "Аксессуары Dyson" : {
        "Аксессуары Dyson" : {
            "aliases" : ["расческа", "Paddle Brush", "Bag", "чехол", "Travel Bag", "дорожные сумки", "сумки", "сумка",
                         "дорожная", "дорожные", "кейс", "Presentation Case", "Case", "кейсы",
                         "подставка", "подставки", "бокс", "боксы"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Расческа Dyson Paddle Brush" : ["расческа", "Paddle Brush"],
                        "Чехол Dyson Travel Bag" : [
                            "чехол", "Travel Bag", "Bag", "дорожные сумки", "сумки", "сумка",
                            "дорожная", "дорожные"],
                        "Кейс Dyson Presentation" : ["кейс", "Presentation Case", "Case", "кейсы", "бокс", "боксы"],
                        "Подставка для" : ["подставка", "подставки"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Pale Rose" : ["Pale Rose"],
                        "Nickel/Black" : ["Nickel/Black"],
                        "Blue/Cooper" : ["Blue/Cooper"],
                    },
                },
            },
        },
    },
    "Стайлеры для волос Dyson": {
        "Dyson Airwrap HS01" : {
            "aliases" : [
                "HS01", "HS 01"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Black/Purple",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Black/Purple" : ["Black/Purple", "Black Purple"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz", "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Blue/Topaz", "Vincia blue /Topaz", "Vincia blue / Topaz",
                                              "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia Nickel", "Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
            },
        },
        "Dyson Airwrap HS05" : {
            "aliases" : [
                "HS05", "HS 05"
            ],
            "attributes" : {
                "complete" : {
                    "values" : ["Long"],
                    "aliases" : {
                        "Long" : ["Long"]
                    },
                },
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Black/Purple",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper", "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink", "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Black/Purple" : ["Black/Purple", "Black Purple"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue", "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz", "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz", "Vincia blue / Topaz", "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose", "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia Nickel", "Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
                "diffuse" : {
                    "values" : ["с насадкой Diffuse"],
                    "aliases" : {
                        "с насадкой Diffuse" : [
                            "Diffuse", "насадка", "насадкой",
                            "гребнем", "гребнь", "диффузором", "диффузор"]
                    },
                },
            },
        },
        "Dyson Airwrap i.d.™ HS08" : {
            "aliases" : [
                "HS08", "HS 08"
            ],
            "attributes" : {
                "color" : {
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper", "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink", "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Black/Purple" : ["Black/Purple", "Black Purple"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue", "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz", "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz", "Vincia blue / Topaz", "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz", "Vinca Blue"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose", "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia Nickel", "Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"],
                        "Jasper Plum" : ["Jasper Plum", "Jasper"]
                    },
                },
                "dryer" : {
                    "values" : ["(Straight+Wavy)", "(Curly+Coily)"],
                    "aliases" : {
                        "(Straight+Wavy)" : ["Straight+Wavy", "Strait+Wavy", "Straight", "Strait", "Wavy"],
                        "(Curly+Coily)" : ["Curly+Coily", "Curly", "Coily", "Diffuse",
                                           "Diffuse", "насадка", "насадкой",
                                           "гребнем", "гребнь", "диффузором", "диффузор"
                                           ],
                    },
                },
            },
        },
    },
    "Фены для волос Dyson" : {
        "Dyson Supersonic HD07" : {
            "aliases" : [
                "HD07", "HD 07"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Iron/Fuchsia",
                        "Anthrazit/Fuchsia",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz", "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz", "Vincia blue / Topaz",
                                              "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia /Nickel", "Fuchsia/ Nickel", "Fuchsia Nickel"],
                        "Iron/Fuchsia" : ["Iron/Fuchsia", "Iron /Fuchsia", "Iron/ Fuchsia", "Iron Fuchsia"],
                        "Anthrazit/Fuchsia" : ["Anthrazit/Fuchsia", "Anthrazit /Fuchsia", "Anthrazit/ Fuchsia", "Anthrazit Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
                "case" : {
                    "values" : [
                        "с кейсом",
                    ],
                    "aliases" : {
                        "с кейсом" : ["кейсом"],
                    },
                },
            },
        },
        "Dyson Supersonic HD08" : {
            "aliases" : [
                "HD08", "HD 08"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Iron/Fuchsia",
                        "Anthrazit/Fuchsia",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz", "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz", "Vincia blue / Topaz",
                                              "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia /Nickel", "Fuchsia/ Nickel", "Fuchsia Nickel"],
                        "Iron/Fuchsia" : ["Iron/Fuchsia", "Iron /Fuchsia", "Iron/ Fuchsia", "Iron Fuchsia"],
                        "Anthrazit/Fuchsia" : ["Anthrazit/Fuchsia", "Anthrazit /Fuchsia", "Anthrazit/ Fuchsia",
                                               "Anthrazit Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
                "case" : {
                    "values" : [
                        "с кейсом",
                    ],
                    "aliases" : {
                        "с кейсом" : ["кейсом"],
                    },
                },
            },
        },
        "Dyson Supersonic HD15" : {
            "aliases" : [
                "HD15", "HD 15"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Iron/Fuchsia",
                        "Anthrazit/Fuchsia",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz", "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz", "Vincia blue / Topaz",
                                              "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia /Nickel", "Fuchsia/ Nickel", "Fuchsia Nickel"],
                        "Iron/Fuchsia" : ["Iron/Fuchsia", "Iron /Fuchsia", "Iron/ Fuchsia", "Iron Fuchsia"],
                        "Anthrazit/Fuchsia" : ["Anthrazit/Fuchsia", "Anthrazit /Fuchsia", "Anthrazit/ Fuchsia",
                                               "Anthrazit Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
                "case" : {
                    "values" : [
                        "с кейсом",
                    ],
                    "aliases" : {
                        "с кейсом" : ["кейсом"],
                    },
                },
            },
        },
        "Dyson Supersonic HD16 Nural™" : {
            "aliases" : [
                "HD16", "HD 16"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Iron/Fuchsia",
                        "Anthrazit/Fuchsia",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Topaz", "Ceramic Patina", "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz", "Vincia blue / Topaz",
                                              "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia /Nickel", "Fuchsia/ Nickel", "Fuchsia Nickel"],
                        "Iron/Fuchsia" : ["Iron/Fuchsia", "Iron /Fuchsia", "Iron/ Fuchsia", "Iron Fuchsia"],
                        "Anthrazit/Fuchsia" : ["Anthrazit/Fuchsia", "Anthrazit /Fuchsia", "Anthrazit/ Fuchsia",
                                               "Anthrazit Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
                "case" : {
                    "values" : [
                        "с кейсом",
                    ],
                    "aliases" : {
                        "с кейсом" : ["кейсом"],
                    },
                },
            },
        },
        "Dyson Supersonic HD18 r™ Professional" : {
            "aliases" : [
                "HD18", "HD 18", "Supersonic R Professional"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Iron/Fuchsia",
                        "Anthrazit/Fuchsia",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Topaz", "Ceramic Patina",
                                                  "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz",
                                              "Vincia blue / Topaz",
                                              "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia /Nickel", "Fuchsia/ Nickel", "Fuchsia Nickel"],
                        "Iron/Fuchsia" : ["Iron/Fuchsia", "Iron /Fuchsia", "Iron/ Fuchsia", "Iron Fuchsia"],
                        "Anthrazit/Fuchsia" : ["Anthrazit/Fuchsia", "Anthrazit /Fuchsia", "Anthrazit/ Fuchsia",
                                               "Anthrazit Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
                "case" : {
                    "values" : [
                        "с кейсом",
                    ],
                    "aliases" : {
                        "с кейсом" : ["кейсом"],
                    },
                },
            },
        },
    },
    "Выпрямители для волос Dyson" : {
        "Dyson Corrale HS03" : {
            "aliases" : [
                "HS03", "HS 03"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Black/Purple",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Black/Purple" : ["Black/Purple", "Black Purple"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz",
                                                  "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz",
                                              "Vincia blue / Topaz", "blue /Topaz", "blue/ Topaz", "blue/ Topaz",
                                              "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia Nickel", "Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
            },
        },
        "Dyson Corrale HS07" : {
            "aliases" : [
                "HS07", "HS 07"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Black/Purple",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Black/Purple" : ["Black/Purple", "Black Purple"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz",
                                                  "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz",
                                              "Vincia blue / Topaz",
                                              "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia Nickel", "Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
            },
        },
        "Dyson AirStrait HT01" : {
            "aliases" : [
                "HT01", "HT 01"
            ],
            "attributes" : {
                "color" : {
                    "values" : [
                        "Nickel/Copper",
                        "Prussian Blue/Rich Copper",
                        "Prussian Blue/Copper",
                        "Strawberry Bronze/Blush Pink",
                        "Black/Purple",
                        "Blue/Copper",
                        "Blue/Blush",
                        "Ceramic Patina/Topaz",
                        "Vinca Blue/Topaz",
                        "Vinca Blue/Rose",
                        "Velvet Red/Gold",
                        "Sakura Rose Gold",
                        "Fuchsia/Nickel",
                        "Ceramic Pop",
                        "Black Onyx/Gold",
                        "Blush Blue",
                        "Ceramic Pink/Rose Gold"
                    ],
                    "aliases" : {
                        "Nickel/Copper" : ["Nickel/Copper", "Nickel / Copper", "Nickel Copper", "Nickel"],
                        "Prussian Blue/Rich Copper" : ["Prussian Blue/Rich Copper", "Prussian Blue Rich Copper",
                                                       "Rich Copper"],
                        "Prussian Blue/Copper" : ["Prussian Blue/Copper", "Prussian Blue Copper", "Prussian Blue"],
                        "Strawberry Bronze/Blush Pink" : ["Strawberry Bronze/Blush Pink",
                                                          "Strawberry Bronze Blush Pink", "Strawberry", "Bronze"],
                        "Black/Purple" : ["Black/Purple", "Black Purple"],
                        "Blue/Copper" : ["Blue/Copper", "Blue Copper", "Blue/Cooper", "Blue Cooper"],
                        "Blue/Blush" : ["Blue/Blush", "Blush/Blue", "Blue Blush", "Blush Blue", "blash blue",
                                        "Blue blash"],
                        "Ceramic Patina/Topaz" : ["Ceramic Patina/Topaz", "Ceramic Patina", "Ceramic Topaz",
                                                  "Patina/Topaz", "Patina Topaz"],
                        "Vinca Blue/Topaz" : ["Vinca Blue/Topaz", "Vincia blue /Topaz", "Blue/Topaz",
                                              "Vincia blue / Topaz",
                                              "blue /Topaz", "blue/ Topaz", "blue/ Topaz", "blue Topaz"],
                        "Vinca Blue/Rose" : ["Vinca Blue/Rose", "Vincia blue /rose", "Vincia blue / rose", "blue /rose",
                                             "blue/ rose", "blue/ rose", "blue rose"],
                        "Velvet Red/Gold" : ["Velvet Red/Gold", "Velvet Red Gold", "Red/Gold", "Red Gold", "Velvet"],
                        "Sakura Rose Gold" : ["Sakura Rose Gold", "Rose Gold", "Rose/Gold", "Sakura"],
                        "Fuchsia/Nickel" : ["Fuchsia/Nickel", "Fuchsia Nickel", "Fuchsia"],
                        "Ceramic Pop" : ["Ceramic Pop", "Pop"],
                        "Black Onyx/Gold" : ["Black Onyx/Gold", "Gold Onyx", "Gold"],
                        "Ceramic Pink/Rose Gold" : ["Ceramic Pink/Rose Gold", "Ceramic Pink", "Pink/Rose", "Pink Rose"]
                    },
                },
                "case" : {
                    "values" : [
                        "с кейсом",
                    ],
                    "aliases" : {
                        "с кейсом" : ["кейсом"],
                    },
                },
            },
        },
    },
    "Пылесосы Dyson" : {
        "Пылесосы Dyson" : {
            "aliases" : [
                "V8", "V10", "V11", "V 8", "V 10", "V 11", "V12", "V 12", "V15", "V 15",
                "Gen5", "Gen 5", "Gen5detect", "5detect",
            ],
            "attributes" : {
                "version" : {
                    "values" : [
                        "V8", "V10", "V11", "V 8", "V 10", "V 11", "V12", "V 12", "V15", "V 15",
                        "Gen5", "Gen 5", "Gen5detect", "5detect",
                    ],
                    "aliases" : {
                        "V8" : ["V8", "V 8"],
                        "V10" : ["V10", "V 10"],
                        "V11" : ["V11", "V 11"],
                        "V12" : ["V12", "V 12"],
                        "V15" : ["V15", "V 15"],
                        "Gen5" : ["Gen5", "Gen 5"],
                    },
                },
                "complete" : {
                    "values" : [
                        "Absolute",
                        "Animal"
                        "Animal+",
                        "Motorhead",
                    ],
                    "aliases" : {
                        "Absolute" : ["Absolute"],
                        "Animal" : ["Animal"],
                        "Animal+" : ["Animal+", "Animal +", "Animal plus"],
                        "Motorhead" : ["Motorhead"],
                    },
                },
                "color" : {
                    "values" : [
                        "Silver/Nickel",
                    ],
                    "aliases" : {
                        "Silver/Nickel" : ["Silver/Nickel"],
                    },
                },
            },
        },
        "Пылесосы с влажной уборкой Dyson" : {
            "aliases" : ["G1", "WashG1", "G1Wash", "V15s", "V 15s", "V 15 s", "V12s", "V 12s", "V 12 s"
                         ],
            "attributes" : {
                "version" : {
                    "values" : [
                        "G1", "V15s", "V12s",
                    ],
                    "aliases" : {
                        "G1" : ["G1", "WashG1", "G1Wash"],
                        "V12s Detect" : ["V12s", "V 12s", "V 12 s"],
                        "V15s Detect" : ["V15s", "V 15s", "V 15 s"]
                    },
                },
                "complete" : {
                    "values" : [
                        "Absolute",
                        "Animal",
                        "Animal+",
                        "Motorhead",
                    ],
                    "aliases" : {
                        "Absolute" : ["Absolute"],
                        "Animal" : ["Animal"],
                        "Animal+" : ["Animal+", "Animal +", "Animal plus"],
                        "Motorhead" : ["Motorhead"],
                    },
                },
                "color" : {
                    "values" : [
                        "Silver/Nickel",
                    ],
                    "aliases" : {
                        "Silver/Nickel" : ["Silver/Nickel"],
                    },
                },
            },
        },
        "Проводные пылесосы Dyson" : {
            "aliases" : ["Big Ball", "Ball", "Multi Floor", "Multi", "Floor", "Parquet"],
            "attributes" : {
                "version" : {
                    "values" : [
                        "Big Ball",
                    ],
                    "aliases" : {
                        "Big Ball" : ["Big Ball", "Big", "Ball"],
                    },
                },
                "complete" : {
                    "values" : [
                        "Cinetic™ Absolute 2",
                        "Multi Floor 2",
                        "Parquet 2",
                    ],
                    "aliases" : {
                        "Cinetic™ Absolute 2" : ["Cinetic™ Absolute 2", "Cinetic™", "Cinetic", "Absolute"],
                        "Multi Floor 2" : ["Multi Floor 2", "Multi", "Floor"],
                        "Parquet 2" : ["Parquet 2", "Parquet"],
                    },
                },
            },
        },
        "Робот-пылесосы Dyson" : {
            "aliases" : ["360 Heurist", "Heurist", "360 Vis Nav", "Vis Nav", "Vis", "Nav", "Navi", "Nava", "360"],
            "attributes" : {
                "version" : {
                    "values" : [
                        "360",
                    ],
                    "aliases" : {
                        "360" : ["360"],
                    },
                },
                "complete" : {
                    "values" : [
                        "Heurist",
                        "Vis Nav"
                    ],
                    "aliases" : {
                        "Heurist" : ["Heurist"],
                        "Vis Nav" : ["Vis Nav", "VisNav", "VisNava", "VisNavi", "Navi", "Nava", "Nav"],
                    },
                },
            },
        },
    },
    "Системы очистки воздуха Dyson" : {
        "Очистители воздуха Dyson" : {
            "aliases" : ["TP07", "TP08", "TP09", "TP 07", "TP 08", "TP 09", "BP03", "BP04", "BP 04"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "TP07 Purifier Cool™" : ["TP07", "TP 07"],
                        "TP08 Pure Cool™" : ["TP08", "TP 08"],
                        "TP09 Purifier Cool Formaldehyde™" : ["TP09", "TP 09"],
                        "BP03 Purifier Big+Quiet Formaldehyde™" : ["BP03", "BP 03"],
                        "BP04 Purifier Big+Quiet Formaldehyde™" : ["BP04", "BP 04"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black/Nickel" : ["Black/Nickel", "Black"], #TP07
                        "White/Silver" : ["White/Silver", "Silver"], #TP08 и TP07
                        "Nickel/Gold" : ["Nickel/Gold"], #TP09
                        "White/Gold" : ["White/Gold"], #TP09
                    },
                },
            },
        },
        "Очистители-увлажнители воздуха Dyson" : {
            "aliases" : ["PH03", "PH 03", "PH04", "PH 04"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "PH03 Purifier Humidify+Cool™" : ["PH03", "PH 03"],
                        "PH04 Purifier Humidify+Cool Formaldehyde™" : ["PH04", "PH 04"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black/Nickel" : ["Black/Nickel",],
                        "White/Silver" : ["White/Silver",],
                        "Nickel/Gold" : ["Nickel/Gold"],
                        "White/Gold" : ["White/Gold"],
                    },
                },
            },
        },
        "Очистители-обогреватели воздуха Dyson" : {
            "aliases" : ["HP07", "HP 07", "HP09", "HP 09", "HP10", "HP 10"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "HP07 Purifier Hot+Cool™" : ["HP07", "HP 07"],
                        "HP09 Purifier Hot+Cool Formaldehyde™" : ["HP09", "HP 09"],
                        "HP10 Purifier Hot+Cool™ Gen1" : ["HP10", "HP 10"]

                    },
                },
                "color" : {
                    "aliases" : {
                        "Black/Nickel" : ["Black/Nickel",],
                        "White/Silver" : ["White/Silver",],
                        "Nickel/Gold" : ["Nickel/Gold"],
                        "White/Gold" : ["White/Gold"],
                    },
                },
            },
        },
        "Беслопастные вентиляторы и увлажнители Dyson" : {
            "aliases" : ["AM9", "AM 9", "AM10", "AM 10"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "AM09 Hot+Cool™" : ["AM09", "AM 09"],
                        "AM10 Humidifier" : ["AM10", "AM 10"]

                    },
                },
                "color" : {
                    "aliases" : {
                        "Black/Nickel" : ["Black/Nickel",],
                        "White/Silver" : ["White/Silver",],
                        "Nickel/Gold" : ["Nickel/Gold"],
                        "White/Gold" : ["White/Gold"],
                    },
                },
            },
        },
    },
    "Сушилки для рук Dyson" : {
        "Настенные сушилки Dyson" : {
            "aliases" : ["HU01", "HU02", "HU03", "AB09", "AB10", "AB11", "AB12", "AB14"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Dyson Airblade™ dB Hand Dryer (HU01)" : ["HU01"],
                        "Dyson Airblade™ V Hand Dryer (HU02)" : ["HU02"],
                        "Dyson Airblade™ 9kJ Hand Dryer (HU03)" : ["HU03"],
                        "Dyson Airblade™ Tap Short Hand Dryer (AB09)" : ["AB09"],
                        "Dyson Airblade™ Tap Long Hand Dryer (AB10)" : ["AB10"],
                        "Dyson Airblade™ Tap Wall Hand Dryer (AB11)" : ["AB11"],
                        "Dyson Airblade™ V Hand Dryer (AB12)" : ["AB12"],
                        "Dyson Airblade™ dB Hand Dryer (AB14)" : ["AB14"],
                    },
                },
            },
        },
        "Сушилки интегрированные в смеситель Dyson" : {
            "aliases" : ["WD04", "WD05", "WD06"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Dyson Airblade™ Wash+Dry Short Hand Dryer (WD04)" : ["WD04"],
                        "Dyson Airblade™ Wash+Dry Tall Hand Dryer (WD05)" : ["WD05"],
                        "Dyson Airblade™ Wash+Dry Wall Hand Dryer (WD06)" : ["WD06"],
                    },
                },
            },
        },
    },

    #Аудио
    "Яндекс" : {
        "Яндекс станция" : {
            "aliases" : [
                "Яндекс", "Яндекс.Станция"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Яндекс.Станция Лайт" : ["Яндекс.Станция Лайт", "Станция Лайт", "Лайт"],
                        "Яндекс.Станция Лайт 2" : ["Яндекс.Станция Лайт 2", "Станция Лайт 2", "Лайт 2", "Лайт2"],
                        "Яндекс.Мини 2" : ["Яндекс Мини 2", "Яндекс Мини", "мини 2"],
                        "Яндекс.Мини 2 (без часов)" : ["Яндекс.Мини 2 (без часов)", "Яндекс Мини 2 без часов", "Яндекс Мини без часов", "Мини 2 без"],
                        "Яндекс.Мини 3" : ["Яндекс.Мини 3", "Яндекс Мини 3", "Мини 3"],
                        "Яндекс.Станция Миди" : ["Яндекс.Станция Миди", "Станция Миди", "Яндекс Миди"],
                        "Яндекс.Станция 2" : ["Яндекс.Станция 2", "Станция 2"],
                        "Яндекс.Станция Макс с ZigBee" : ["Макс ZigBee", "ZigBee"],
                        "Яндекс.Станция Дуо Макс" : ["Яндекс.Станция Дуо Макс", "Дуо Макс", "Дуо"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black"],
                        "Yellow" : ["Yellow"],
                        "Red" : ["Red", "Raspberry", "crimson"],
                        "Beige" : ["Beige"],
                        "Turquoise" : ["Turquoise"],
                        "White" : ["White"],
                        "Green" : ["Green"],
                        "Blue" : ["Blue"],
                        "Pink" : ["Pink"],
                        "Purple" : ["Purple", "violet", "luel"],
                        "Coral" : ["coral"],
                        "Gray" : ["gray", "grey"],
                        "Orange" : ["Orange"],
                        "Silver" : ["Silver"],
                        "Cooper" : ["Cooper"],
                        "Mint" : ["Mint"]

                    },
                },
            },
        },
    },
    "JBL" : {
        "Акустические системы JBL" : {
            "aliases" : [
                "JBL Go", "JBL Clip", "JBL Charge", "JBL Xtreme", "Clip", "JBL PartyBox", "Partybox", "JBL JR POP",
                "JBL Boombox", "PartyBox", "JBL Pulse", "JBL Wind", "JBL Tuner", "Boombox"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "JBL Go 3" : [
                            "JBL Go 3",
                            "JBL Go-3"
                        ],
                        "JBL Go 4" : [
                            "JBL Go 4",
                            "JBL Go-4"
                        ],
                        "JBL Clip 4" : [
                            "JBL Clip 4",
                            "Clip 4",
                            "JBL Clip-4",
                            "Clip-4"
                        ],
                        "JBL Clip 5" : [
                            "JBL Clip 5",
                            "Clip 5",
                            "JBL Clip-5",
                            "Clip-5"
                        ],
                        "JBL Flip 5" : [
                            "JBL Flip 5",
                            "JBL Flip-5"
                        ],
                        "JBL Flip 6" : [
                            "JBL Flip 6",
                            "JBL Flip-6"
                        ],
                        "JBL Charge 4" : [
                            "JBL Charge 4",
                            "JBL Charge-4"
                        ],
                        "JBL Charge 5" : [
                            "JBL Charge 5",
                            "JBL Charge-5"
                        ],
                        "JBL Xtreme 3" : [
                            "JBL Xtreme 3",
                            "JBL Xtreme-3"
                        ],
                        "JBL Xtreme 4" : [
                            "JBL Xtreme 4",
                            "JBL Xtreme-4"
                        ],
                        "JBL Boombox 2" : [
                            "JBL Boombox 2",
                            "Boombox 2",
                            "JBL Boombox-2",
                            "Boombox-2"
                        ],
                        "JBL Boombox 3" : [
                            "JBL Boombox 3",
                            "Boombox 3",
                            "JBL Boombox-3",
                            "Boombox-3"
                        ],
                        "JBL Boombox 3 Wi-Fi" : [
                            "JBL Boombox 3 Wi-Fi",
                            "Boombox 3 Wi-Fi",
                            "Boombox Wi-Fi",
                            "Boombox WiFi",
                            "JBL Boombox-3 Wi-Fi",
                            "Boombox-3 Wi-Fi"
                        ],
                        "JBL PartyBox 1000" : [
                            "JBL Partybox 1000",
                            "Partybox 1000",
                            "JBL Partybox-1000",
                            "Partybox-1000"
                        ],
                        "JBL PartyBox 710" : [
                            "JBL Partybox 710",
                            "Partybox 710",
                            "JBL Partybox-710",
                            "Partybox-710"
                        ],
                        "JBL PartyBox 520" : [
                            "JBL Partybox 520",
                            "Partybox 520",
                            "JBL Partybox-520",
                            "Partybox-520"
                        ],
                        "JBL PartyBox 310" : [
                            "JBL Partybox 310",
                            "Partybox 310",
                            "JBL Partybox-310",
                            "Partybox-310"
                        ],
                        "JBL PartyBox 320" : [
                            "JBL Partybox 320",
                            "Partybox 320",
                            "JBL Partybox-320",
                            "Partybox-320"
                        ],
                        "JBL PartyBox 110" : [
                            "JBL Partybox 110",
                            "Partybox 110",
                            "JBL Partybox-110",
                            "Partybox-110"
                        ],
                        "JBL PartyBox 120" : [
                            "JBL Partybox 120",
                            "Partybox 120",
                            "JBL Partybox-120",
                            "Partybox-120"
                        ],
                        "JBL PartyBox Encore" : [
                            "JBL Partybox Encore",
                            "Partybox Encore"
                        ],
                        "JBL PartyBox Encore Essential" : [
                            "JBL Partybox Encore Essential",
                            "Partybox Encore Essential"
                        ],
                        "JBL PartyBox Encore 2" : [
                            "JBL Partybox Encore 2",
                            "Partybox Encore 2",
                            "JBL Partybox Encore-2",
                            "Partybox Encore-2"
                        ],
                        "JBL PartyBox On-The-Go" : [
                            "JBL Partybox On-The-Go",
                            "Partybox On-The-Go",
                            "Partybox On The Go",
                            "Partybox OnTheGo",
                            "Partybox OTG"
                        ],
                        "JBL PartyBox Ultimate" : ["JBL PartyBox Ultimate", "Partybox Ultimate"],
                        "JBL Pulse 4" : [
                            "JBL Pulse 4",
                            "JBL Pulse-4"
                        ],
                        "JBL Pulse 5" : [
                            "JBL Pulse 5",
                            "JBL Pulse-5"
                        ],
                        "JBL Wind 3" : [
                            "JBL Wind 3",
                            "JBL Wind-3"
                        ],
                        "JBL Wind 3 Slim" : [
                            "JBL Wind 3 Slim",
                            "JBL Wind 3S",
                            "JBL Wind-3 Slim",
                            "JBL Wind-3S"
                        ],
                        "JBL JR POP" : ["JBL JR POP"],
                        "JBL Tuner FM" : ["JBL Tuner FM"],
                        "JBL Tuner XL" : ["JBL Tuner XL"],
                        "JBL Tuner 2" : ["JBL Tuner 2"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Blue/Pink" : ["Blue/Pink", "Blue Pink", "Pink Blue"],
                        "Blue/Red" : ["blue/red", "blue red", "red blue"],
                        "Light Blue" : ["Light Blue"],
                        "Blue Pink" : ["Blue Pink"],
                        "Black Orange" : ["Black Orange"],
                        "Ocean Blue" : ["Ocean Blue"],
                        "Sand" : ["Sand"],
                        "Forest" : ["Forest"],
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Squad" : ["Squad", "Camouflage", "🪲"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                    },
                },
            },
        },
        "Наушники JBL" : {
            "aliases" : [
                "JBL Tune", "JBL Live", "JBL Wave", "JBL Tune Buds", "JBL Buds Tune", "JBL Wave Flex", "JBL Flex Wave",
                "JBL Wave Beam", "JBL Wave Beam", "JBL Beam Tune", "JBL JR", "JBL T100", "JBL 100", "JBL T110", "JBL 110",

            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "JBL Tune 130NC TWS" : ["JBL Tune 130NC TWS", "JBL Tune 130"],
                        "JBL Tune 230NC TWS" : ["JBL Tune 230NC TWS", "JBL Tune 230"],
                        "JBL Tune 205" : ["JBL Tune 205"],
                        "JBL Tune 215BT" : ["JBL Tune 215BT", "JBL Tune 215"],
                        "JBL Tune 510BT" : ["JBL Tune 510BT", "JBL Tune 510"],
                        "JBL Tune 520BT" : ["JBL Tune 520BT", "JBL Tune 520"],
                        "JBL Tune 720BT" : ["JBL Tune 720BT", "JBL Tune 720"],
                        "JBL Tune 670NC" : ["JBL Tune 670NC", "JBL Tune 670 NC"],
                        "JBL Tune 760NC" : ["JBL Tune 760NC", "JBL Tune 760 NC"],
                        "JBL Tune 770NC" : ["JBL Tune 770NC", "JBL Tune 770 NC"],
                        "JBL Live 670NC" : ["JBL Live 670NC", "JBL Live 670"],
                        "JBL Live 770NC" : ["JBL Live 770NC", "JBL Live 770"],
                        "JBL Live Beam 3" : ["JBL Live Beam 3", "JBL Live Beam3"],
                        "JBL Live Flex 3" : ["JBL Live Flex 3", "JBL Live Flex3"],
                        "JBL Tune Flex" : ["JBL Tune Flex"],
                        "JBL Tune Flex 2" : ["JBL Tune Flex 2", "JBL Tune Flex2"],
                        "JBL Tune Beam" : ["JBL Tune Beam", "JBL Beam Tune"],
                        "JBL Tune Beam 2" : ["JBL Tune Beam 2", "JBL Tune Beam2"],
                        "JBL Tune Buds" : ["JBL Tune Buds", "JBL Buds Tune"],
                        "JBL Wave Flex" : ["JBL Wave Flex", "JBL Flex Wave"],
                        "JBL Wave Beam" : ["JBL Wave Beam", "JBL Wave Beam"],
                        "JBL Wave Buds" : ["Jbl wave buds"],
                        "JBL Wave Buds 2" : ["JBL Wave Buds 2"],
                        "JBL Wave 200TWS" : ["JBL Wave 200TWS", "JBL Wave 200"],
                        "JBL Wave 300TWS" : ["JBL Wave 300TWS", "JBL Wave 300"],
                        "JBL JR 300" : ["JBL JR 300"],
                        "JBL JR 300BT" : ["JBL JR 300BT"],
                        "JBL JR 310" : ["JBL JR 300"],
                        "JBL JR 310BT" : ["JBL JR 310BT"],
                        "JBL JR 460NC" : ["JBL JR 460NC", "JBL JR 460"],
                        "JBL T110" : ["JBL T100", "JBL 100"],
                        "JBL T100" : ["JBL T110", "JBL 110"],

                    },
                },
                "color" : {
                    "aliases" : {
                        "Blue/Pink" : ["Blue/Pink", "Blue Pink", "Pink Blue"],
                        "Blue/Red" : ["blue/red", "blue red", "red blue"],
                        "Light Blue" : ["Light Blue"],
                        "Blue Pink" : ["Blue Pink"],
                        "Black Orange" : ["Black Orange"],
                        "Ocean Blue" : ["Ocean Blue"],
                        "Sand" : ["Sand"],
                        "Forest" : ["Forest"],
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Squad" : ["Squad", "Camouflage", "🪲"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"]
                    },
                },
            },
        },
        "Аудиооборудование JBL" : {
            "aliases" : [
                "Микрофоны JBL", "микрофон"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Микрофоны JBL PartyBox Wireless Mic (2 шт)" : ["JBL PartyBox Wireless Mic", "Микрофоны JBL Partybox"],
                        "Микрофоны JBL Wireless Set (2 шт)" : ["JBL Wireless Set", "Микрофоны JBL SET"],
                        "Микрофон JBL PBM100 Wired Mic" : ["JBL PBM100 Wired", "JBL PBM100"],
                        "Микрофон JBL Quantum Stream" : ["JBL Quantum Stream"]
                    },
                },
            },
        },
    },
    "Beats" : {
        "Накладные и полноразмерные наушники Beats" : {
            "aliases" : ["Beats Solo 3", "Beats Solo 4", "Beats Solo Pro", "Beats Studio Pro", "Beats EP", "Beats Studio 3",
                         "Beats Pro"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Beats Solo 3" : ["Beats Solo 3"],
                        "Beats Solo 4" : ["Beats Solo 4"],
                        "Beats Solo Pro" : ["Beats Solo Pro"],
                        "Beats EP" : ["Beats EP"],
                        "Beats Studio Pro" : ["Beats Studio Pro"],
                        "Beats Studio 3" : ["Beats Studio 3"],
                        "Beats Pro" : ["Beats Pro"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "⚫️", "🖤"],
                        "Matte Black" : ["Matte Black"],
                        "Champagne Gold" : ["Champagne Gold"],
                        "Black/Gold" : ["black/gold"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "Cream" : ["Cream", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Navy" : ["Navy", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Sand" : ["🩶"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Kim Kardashian Dune" : ["Cardashyan Dune", "Kardashian Dune"],
                        "Kim Kardashian" : ["Kim Kardashian", "Kardashian", "Cardashyan"],
                        "Earth" : ["Earth"],
                        "Moon" : ["Moon"]
                    },
                },
            },
        },
        "Внутриканальные наушники Beats" : {
            "aliases" : ["Beats Studio Buds", "Beats Fit Pro", "Beats Flex"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Beats Studio Buds" : ["Beats Studio Buds"],
                        "Beats Studio Buds +" : ["Beats Studio Buds +", "Beats Studio Buds+", "Beats Studio Buds plus"],
                        "Beats Fit Pro" : ["Beats Fit Pro"],
                        "Beats Flex" : ["Beats Flex"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "⚫️", "🖤"],
                        "Matte Black" : ["Matte Black"],
                        "Champagne Gold" : ["Champagne Gold"],
                        "Black/Gold" : ["black/gold"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "Cream" : ["Cream", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Navy" : ["Navy", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Kim Kardashian Dune" : ["Cardashyan Dune", "Kardashian Dune"],
                        "Kim Kardashian" : ["Kim Kardashian", "Kardashian", "Cardashyan"],
                        "Earth" : ["Earth"],
                        "Moon" : ["Moon"]
                    },
                },
            },
        },
        "Акустические системы Beats" : {
            "aliases" : ["Beats Pill"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Beats Pill" : ["Beats Pill"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "⚫️", "🖤"],
                        "Matte Black" : ["Matte Black"],
                        "Champagne Gold" : ["Champagne Gold"],
                        "Black/Gold" : ["black/gold"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "Cream" : ["Cream", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Navy" : ["Navy", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Kim Kardashian Dune" : ["Cardashyan Dune", "Kardashian Dune"],
                        "Kim Kardashian" : ["Kim Kardashian", "Kardashian", "Cardashyan"],
                        "Earth" : ["Earth"],
                        "Moon" : ["Moon"]
                    },
                },
            },
        },
    },
    "Sony" : {
        "Наушники Sony WH" : {
            "aliases" : [
                "Sony WH", "ULT900"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Sony WH-ULT900" : ["Sony WH-ULT900", "Sony ULT900", "Sony WH -ULT900", "Sony WH- ULT900",
                                            "Sony WH - ULT900"],
                        "Sony WH-CH500" : ["Sony WH-CH500", "Sony WH -CH500", "Sony WH- CH500", "Sony WH - CH500"],
                        "Sony WH-CH510" : ["Sony WH-CH510", "Sony WH -CH510", "Sony WH- CH510", "Sony WH - CH510"],
                        "Sony WH-CH520" : ["Sony WH-CH520", "Sony WH -CH520", "Sony WH- CH520", "Sony WH - CH520"],
                        "Sony WH-C700N" : ["Sony WH-CH700N", "Sony WH-CH700", "Sony WH -CH700N", "Sony WH- CH700N",
                                           "Sony WH - CH700N", "Sony WH -CH700", "Sony WH- CH700", "Sony WH - CH700"],
                        "Sony WH-CH720N" : ["Sony WH-CH720N", "Sony WH-CH720", "Sony WH -CH720N", "Sony WH- CH720N",
                                            "Sony WH - CH720N", "Sony WH -CH720", "Sony WH- CH720", "Sony WH - CH720"],
                        "Sony WH-1000XM4" : ["Sony WH-1000XM4", "Sony WH -1000XM4", "Sony WH- 1000XM4",
                                             "Sony WH - 1000XM4"],
                        "Sony WH-1000XM5" : ["Sony WH-1000XM5", "Sony WH -1000XM5", "Sony WH- 1000XM5",
                                             "Sony WH - 1000XM5"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Наушники Sony WF" : {
            "aliases" : [
                "Sony WF"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Sony WF-1000XM5" : ["Sony WF-1000XM5", "Sony WF -1000XM5", "Sony WF- 1000XM5",
                                             "Sony WF - 1000XM5"],
                        "Sony WF-C500" : ["Sony WF-C500", "Sony WF -C500", "Sony WF- C500", "Sony WF - C500"],
                        "Sony WF-C510" : ["Sony WF-C510", "Sony WF -C510", "Sony WF- C510", "Sony WF - C510"],
                        "Sony WF-C700N" : ["Sony WF-C700N", "Sony WF-C700", "Sony WF -C700N", "Sony WF- C700N",
                                           "Sony WF - C700N", "Sony WF -C700", "Sony WF- C700", "Sony WF - C700"],
                        "Sony WF-C720N" : ["Sony WF-C720N", "Sony WF-C720", "Sony WF -C720N", "Sony WF- C720N",
                                           "Sony WF - C720N", "Sony WF -C720", "Sony WF- C720", "Sony WF - C720"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "Silver" : ["Silver", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
    },
    "Marshall" : {
        "Акустические системы Marshall" : {
            "aliases" : ["Marshall Acton", "Marshall Stanmore", "Marshall Woburn", "Marshall Kilburn",
                         "Marshall Stockwell", "Marshall Tufton", "Marshall Emberton", "Marshall Willen",
                         "Marshall Middleton", "Acton", "Stanmore"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Marshall Acton II" : ["Marshall Acton II", "Marshall Acton 2"],
                        "Marshall Acton III" : ["Marshall Acton III", "Marshall Acton 3", "Acton 3"],
                        "Marshall Stanmore II" : ["Marshall Stanmore II", "Marshall Stanmore 2", "Stanmore 2"],
                        "Marshall Stanmore III" : ["Marshall Stanmore III", "Marshall Stanmore 3", "Stanmore 3"],
                        "Marshall Woburn II" : ["Marshall Woburn II", "Marshall Woburn 2"],
                        "Marshall Woburn III" : ["Marshall Woburn III", "Marshall Woburn 3"],
                        "Marshall Kilburn II" : ["Marshall Kilburn II", "Marshall Kilburn 2"],
                        "Marshall Kilburn III" : ["Marshall Kilburn III", "Marshall Kilburn 3"],
                        "Marshall Stockwell II" : ["Marshall Stockwell II", "Marshall Stockwell 2"],
                        "Marshall Stockwell III" : ["Marshall Stockwell III", "Marshall Stockwell 3"],
                        "Marshall Tufton" : ["Marshall Tufton"],
                        "Marshall Emberton I" : ["Marshall Emberton I", "Marshall Emberton 1", "Marshall Emberton"],
                        "Marshall Emberton II" : ["Marshall Emberton II", "Marshall Emberton 2"],
                        "Marshall Emberton III" : ["Marshall Emberton III", "Marshall Emberton 3"],
                        "Marshall Willen I" : ["Marshall Willen I", "Marshall Willen 1", "Marshall Willen"],
                        "Marshall Willen II" : ["Marshall Willen II", "Marshall Willen 2"],
                        "Marshall Middleton" : ["Marshall Middleton"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "Cream" : ["Cream", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"]
                    },
                },
            },
        },
        "Наушники Marshall" : {
            "aliases" : ["Marshall Major", "Marshall Minor", "Marshall Monitor", "Marshall Mode", "Marshall Motif", "Major"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Marshall Major IV" : ["Marshall Major IV", "Marshall Major 4", "Major 4"],
                        "Marshall Major V" : ["Marshall Major V", "Marshall Major 5", "Major 5"],
                        "Marshall Minor III" : ["Marshall Minor III", "Marshall Minor 3", "Minor 3"],
                        "Marshall Minor IV" : ["Marshall Minor IV", "Marshall Minor 4", "Minor 4"],
                        "Marshall Monitor II A.N.C." : ["Marshall Monitor II", "Marshall Monitor 2", "Monitor 2"],
                        "Marshall Monitor III A.N.C." : ["Marshall Monitor III", "Marshall Monitor 3", "Monitor 3"],
                        "Marshall Mode II" : ["Marshall Mode II", "Marshall Mode 2", "Mode 2"],
                        "Marshall Mode III" : ["Marshall Mode III", "Marshall Mode 3", "Mode 3"],
                        "Marshall Motif II A.N.C." : ["Marshall Motif II", "Marshall Motif 2", "Motif 2"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "Cream" : ["Cream", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"]
                    },
                },
            },
        },
    },
    "Galaxy Buds" : {
        "Наушники Galaxy Buds" : {
            "aliases" : [
                "Galaxy Buds", "Galaxy Buds2", "Galaxy Buds3"
            ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "Buds FE" : ["Galaxy Buds FE", "Buds FE"],
                        "Buds 2" : ["Galaxy Buds 2", "Buds 2", "Buds2"],
                        "Buds 2 Pro" : ["Galaxy Buds 2 Pro", "Buds 2 Pro", "Buds2 Pro"],
                        "Buds 3" : ["Galaxy Buds 3", "Buds 3", "Buds3"],
                        "Buds 3 Pro" : ["Galaxy Buds 3 Pro", "Buds 3 Pro", "Buds3 Pro"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Silver" : ["Silver"],
                        "White" : ["White"],
                        "Graphite" : ["Graphite"],
                        "Lavender" : ["Lavender"],
                        "Olive" : ["Olive"],
                        "Purple" : ["Purple"],
                    },
                },
            },
        },
    },
    "OnePlus Buds" : {
        "Наушники OnePlus Buds" : {
            "aliases" : [
                "OnePlus Buds",
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "OnePlus Buds 3" : ["OnePlus Buds 3", "Buds 3"],
                        "OnePlus Buds Pro 2" : ["OnePlus Buds Pro 2", "Buds Pro 2"],
                        "OnePlus Buds Pro 3" : ["OnePlus Buds Pro 3", "Buds Pro 3"],
                        "OnePlus Nord Buds 2" : ["OnePlus Nord Buds 2", "Nord Buds 2"],
                        "OnePlus Nord Buds 3 Pro" : ["OnePlus Nord Buds 3 Pro", "Nord Buds 3 Pro"],
                    },
                },
            },
        },
    },
    "Redmi Buds" : {
        "Наушники Redmi Buds" : {
            "aliases" : [
                "Redmi Buds",
            ],
            "attributes" : {
                "model" : {
                    "aliases" : {
                        "5 Pro" : ["Buds 5 Pro"],
                        "6 Pro" : ["Buds 6 Pro"],
                        "6 Play" : ["Buds 6 Play"],
                        "6 Lite" : ["Buds 6 Lite"],
                        "6 Active" : ["Buds 6 Active"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black"],
                        "White" : ["White"],
                        "Green" : ["Green"],
                        "Blue" : ["Blue"],
                        "Pink" : ["Pink"],
                        "Purple" : ["Purple"]

                    },
                },
            },
        },
    },
    "Nothing Ear" : {
        "Наушники Nothing Ear" : {
            "aliases" : [
                "Nothing Ear"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Nothing Ear (2)" : ["Nothing Ear (2)"],
                        "Nothing Ear (3)" : ["Nothing Ear (3) B171", "Nothing Ear (3)", "Nothing Ear 2024 b171", "b171"],
                        "Nothing Ear (stick)" : ["Nothing Ear (stick)"],
                        "Nothing Ear (a)" : ["Nothing Ear (a)", "Nothing Ear a", "B162"],
                        "Nothing Ear (open)" : ["Nothing Ear (open)", "Nothing ear open 2024", "open"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black"],
                        "White" : ["White"],
                        "Yellow" : ["Yellow"],
                    },
                },
            },
        },
    },
    "VK" : {
        "Умные колонки VK" : {
            "aliases" : [
                "VK"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "VK Капсула" : ["VK Капсула"],
                        "VK Капсула Мини" : ["VK Капсула Мини", "VK Капсула mini", "VK Мини", "VK mini"],
                        "VK Капсула Нео" : ["VK Капсула Нео", "VK Нео", "VK Капсула neo", "VK neo"],
                        "VK Капсула Про" : ["VK Капсула Про", "VK Про", "VK Капсула Pro", "VK Pro"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"]
                    },
                },
            },
        },
    },
    "Аудио прочее" : {
        "Наушники Sennheiser" : {
            "aliases" : [
                "Sennheiser"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Sennheiser HD 505" : ["Sennheiser HD 505", "Sennheiser HD505"],
                        "Sennheiser Momentum True Wireless 4" : ["Sennheiser Momentum True Wireless 4", "Sennheiser true momentum 4",
                                                                 "Sennheiser Momentum True 4", "Sennheiser Momentum 4"],
                        "Sennheiser Accentum True Wireless" : ["Sennheiser Accentum True Wireless", "Sennheiser Accentum True",
                                                               "Sennheiser True Accentum"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Наушники Bose" : {
            "aliases" : [
                "Bose", "QuietComfort", "Quiet Comfort", "Open-Ear", "OpenEar", "Open Ear"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "QuietComfort" : ["QuietComfort", "Quiet Comfort"],
                        "QuietComfort Ultra" : ["QuietComfort Ultra", "Quiet Comfort Ultra"],
                        "QuietComfort Ultra Earbuds" : ["QuietComfort Ultra Earbuds", "Quiet Comfort Ultra Earbuds"],
                        "QuietComfort SC" : ["QuietComfort SC", "Quiet Comfort SC"],
                        "Open-Ear Earbuds" : ["Open-Ear Earbuds", "OpenEar Earbuds", "Open Ear Earbuds"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Наушники B&W" : {
            "aliases" : [
                "B&W", "Bowers & Wilkins"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Bowers & Wilkins Pi7" : ["Bowers & Wilkins Pi7"],
                        "Bowers & Wilkins Px7 S2" : ["Bowers & Wilkins Px7 S2"],
                        "Bowers & Wilkins Px7 S2e" : ["Bowers & Wilkins Px7 S2e"],
                        "Bowers & Wilkins Px8" : ["Bowers & Wilkins Px8"],
                        "Bowers & Wilkins Pi7 S2" : ["Bowers & Wilkins Pi7 S2"],
                        "Bowers & Wilkins Pi8" : ["Bowers & Wilkins Pi8"],

                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Наушники CMF" : {
            "aliases" : [
                "CMF", "CMF buds"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "CMF Buds" : ["CMF Buds"],
                        "CMF Buds Pro" : ["CMF Buds Pro"],
                        "CMF Buds Pro 2" : ["CMF Buds Pro 2"],

                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Наушники Dyson" : {
            "aliases" : ["Ean5025155055748", "Ean5025155055755", "Dyson Zone", "Dyson Zone™", "Air Purification",
                         "Dyson OnTrac™", "Dyson OnTrac", "Dyson on trac"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Dyson Zone™ Air Purification" : ["Ean5025155055748", "Ean5025155055755", "Dyson Zone",
                                                          "Dyson Zone™", "Air Purification"],
                        "Dyson OnTrac™ Noise Cancelling Headphones" : ["Dyson OnTrac™", "Dyson OnTrac", "Dyson on trac"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Наушники Logitech" : {
            "aliases" : ["Logitech"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Logitech G Pro X Wireless:" : ["Logitech G Pro X Wireless:", "Logitech G Pro X", "Logitech GPro X"],
                        "Logitech G733 Lightspeed" : ["Logitech G733 Lightspeed", "Logitech G733"],
                        "Logitech G435" : ["Logitech G435"],
                        "Logitech G433" : ["Logitech G433"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Наушники Beyerdynamic" : {
            "aliases" : ["Beyerdynamic", "Aventho 300"],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "DT 770 PRO 32 Ом": ["DT 770 PRO 32 Ом", "32 ом dt770", "DT 770 PRO", "DT770 PRO"],
                        "DT 770 PRO 80 Ом": ["DT 770 PRO 80 Ом", "80 ом dt770", "DT 770 PRO", "DT770 PRO"],
                        "DT 770 PRO 250 Ом": ["DT 770 PRO 250 Ом", "250 ом dt770", "DT 770 PRO", "DT770 PRO"],
                        "Aventho 300" : ["Aventho 300"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Акустические системы B&W" : {
            "aliases" : [
                "Bowers & Wilkins Zeppelin"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Bowers & Wilkins Zeppelin" : ["Bowers & Wilkins Zeppelin"],

                    },
                },
                "color" : {
                    "aliases" : {
                        "Midnight Grey" : ["Midnight Grey"],
                        "Pearl Grey" : ["Pearl Grey"],
                        "Solar Gold" : ["Solar Gold"],
                        "Space Grey" : ["Space Grey"],
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
        "Акустические системы Harman/Kardon" : {
            "aliases" : [
                "Harman/Kardon", "Go play", "Go+play", "Aura Studio", "Onyx Studio", "Luna"
            ],
            "attributes" : {
                "version" : {
                    "aliases" : {
                        "Go+Play Mini 2" : ["Go+Play Mini 2", "Go+Play Mini2", "Go Play Mini 2", "Go Play Mini2"],
                        "Go+Play Mini 3" : ["Go+Play Mini 3", "Go+Play Mini3", "Go Play Mini 3", "Go Play Mini3"],
                        "Aura Studio 4" : ["Aura Studio 4"],
                        "Aura Studio 3" : ["Aura Studio 3"],
                        "Onyx Studio 7" : ["Onyx Studio 7"],
                        "Onyx Studio 8" : ["Onyx Studio 8"],
                        "Onyx Studio 9" : ["Onyx Studio 9"],
                        "Luna" : ["Luna"]
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black/Gold" : ["Black/Gold"],
                        "Black" : ["Black", "⚫️", "🖤"],
                        "Yellow" : ["Yellow", "💛", "🟡"],
                        "Red" : ["Red", "❤️", "🔴"],
                        "White" : ["White", "⚪️", "🤍"],
                        "Green" : ["Green", "💚", "🟢"],
                        "Blue" : ["Blue", "🔵", "💙"],
                        "Pink" : ["Pink", "💖"],
                        "Purple" : ["Purple", "💜", "🟣"],
                        "Orange" : ["Orange", "🟠", "🍊"],
                        "Brown" : ["Brown", "🤎", "🟤"],
                        "Teal" : ["Teal"],
                        "Mint" : ["Mint"],
                        "Gray" : ["Gray", "grey"],
                        "Beige" : ["beige"]
                    },
                },
            },
        },
    },

    #Консоли/VR
    "Xbox" : {
        "Контроллеры Xbox" : {
            "aliases" : [
                "Xbox Controller", "Xbox Контроллеры"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "Xbox" : ["Xbox"],
                    },
                },
                "version" : {
                    "aliases" : {
                        "Controller" : ["Controller", "Контроллеры"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Carbon Black" : ["Black", "⚫️", "🖤"],
                        "Robot White" : ["White", "⚪️", "🤍"],
                        "Shock Blue" : ["Shock Blue", "Blue"],
                        "Pulse Red" : ["Pulse Red", "Red"],
                        "Electric Volt" : ["Electric Volt", "Volt"],
                        "Deep Pink" : ["Deep Pink", "Pink"],
                        "Velocity Green" : ["Velocity Green", "Green"],
                        "Astral Purple" : ["Astral Purple", "Purple"],
                        "Daystrike Camo" : ["Daystrike Camo", "Daystrike"],
                        "Mineral Camo" : ["Mineral Camo", "Camo"],
                        "Aqua Shift" : ["Aqua Shift", "Aqua"],
                        "Lunar Shift" : ["Lunar Shift", "Lunar"],
                        "Stellar Shift" : ["Stellar Shift", "Stellar"],
                        "Stormcloud Vapor" : ["Stormcloud Vapor", "Stormcloud"],
                    },
                },
            },
        },
        "Консоли Xbox" : {
            "aliases" : [
                "Xbox"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "Xbox" : ["Xbox"],
                    },
                },
                "version" : {
                    "aliases" : {
                        "Series X" : ["Series X"],
                        "Series S" : ["Series S"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black", "⚫️", "🖤"],
                        "White" : ["White", "⚪️", "🤍"],
                    },
                },
            },
        },
    },
    "PlayStation" : {
        "Аксессуары PlayStation" : {
            "aliases" : [
                "Sony Pulse", "Sony Elite", "Sony Explore", "Pulse 3D", "Док-Станция для геймпадов",
                "Зарядка для джойстиков",
                "Зарядка", "Зарядная станция", "подставка", "Дисковод", "Disc Drive", "Portal", "Headset"
            ],
            "attributes" : {
                "acs" : {
                    "aliases" : {
                        "Наушники Sony Pulse 3D" : ["Sony Pulse", "Pulse 3D", "PS 5 Headset",
                                                    "PULSE 3D Wireless Headset"],
                        "Наушники Sony Elite" : ["Sony Elite", "Headset Elite", "PULSE Elite Wireless Headset"],
                        "Наушники Sony Explore" : ["Sony Explore", "Headset Explore", "PULSE Explore Wireless Earbuds"],
                        "Зарядная станция DualSense" : ["Док-Станция для геймпадов", "Зарядка для джойстиков",
                                                        "Зарядка",
                                                        "Зарядная станция", "Charging Station"],
                        "Вертикальная подставка для" : ["подставка"],
                        "Дисковод для" : ["Дисковод", "Disc Drive"],
                        "PlayStation Portal" : ["PS PORTAL", "PlayStation Portal", "PS5 Portal", "PS 5 Portal",
                                                "PS Portal"]
                    },
                },
                "colors" : {
                    "aliases" : {
                        "White" : ["White", "⚪️"],
                        "Black" : ["Black", "⚫️"],
                        "Camouflage" : ["Camouflage", "камуфляжная", "камуфляжный", "камуфляж", "Кафуляж"],
                        "PS5" : ["PlayStation 5, ""PS5", "PS 5", "twin"],
                    },
                },
            },
        },
        "Контроллеры PlayStation" : {
            "aliases" : [
                "DualSense", "Dualsence"
            ],
            "attributes" : {
                "dualsense" : {
                    "aliases" : {
                        "DualSense" : ["DualSense", "DualSense™", "Dualsence",],
                    },
                },
                "consoles" : {
                    "aliases" : {
                        "PS5" : ["PS 5", "PS5"],
                    },
                },
                "colors" : {
                    "aliases" : {
                        "White" : ["White", "⚪️"],
                        "Midnight Black" : ["Midnight Black", "Black", "⚫️"],
                        "Starlight Blue" : ["Starlight Blue", "Blue", "🔵"],
                        "Nova Pink" : ["Nova Pink", "Pink", "💖"],
                        "Cosmic Red" : ["Cosmic Red", "Red", "🔴"],
                        "Astro Bot Limited Edition" : ["Astro Bot Limited Edition", "Astro Bot"],
                        "Camo Gray" : ["Camo Gray", "Gray", "Camo"],
                        "Purple" : ["Purple", "💜"],
                        "Cobalt Blue" : ["Cobalt Blue", "Cobalt", "💙"],
                        "Silver" : ["Silver"],
                        "Chrome Pearl" : ["Chrome Pearl", "Pearl"],
                        "Chrome Indigo" : ["Chrome Indigo", "Indigo"],
                        "Volcanic red" : ["Volcanic red"],
                        "Chroma Tea" : ["Chroma Tea"],
                        "Sterling Silver" : ["Sterling Silver"],
                        "Edge" : ["Edge"]
                    },
                },
            },
        },
        "PlayStation VR" : {
            "aliases" : [
                "VR2"
            ],
            "attributes" : {
                "vr" : {
                    "aliases" : {
                        "PlayStation VR2" : ["VR2"],
                    },
                },
                "game" : {
                    "aliases" : {
                        "+ Horizon " : ["Horizon"],
                    },
                },
            },
        },
        "Консоли PlayStation" : {
            "aliases" : [
                "PlayStation", "PS"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "PlayStation" : ["PlayStation", "PS"],
                    },
                },
                "number" : {
                    "aliases" : {
                        "5" : ["5"],
                    },
                },
                "version" : {
                    "aliases" : {
                        "FAT" : ["FAT"],
                        "PRO" : ["PRO"],
                        "Slim" : ["Slim"],
                    },
                },
                "drive" : {
                    "aliases" : {
                        "Disk" : ["Disk"],
                        "Digital Edition" : ["Digital Edition", "Digital"],
                    },
                },
            },
        },
    },
    "Meta Quest" : {
        "Meta Quest" : {
            "aliases" : [
                "Meta Quest"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "Meta Quest 2" : ["Meta Quest 2"],
                        "Meta Quest 3" : ["Meta Quest 3"],
                        "Meta Quest 3S" : ["Meta Quest 3S"],
                        "Meta Quest Pro" : ["Meta Quest Pro"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "128GB" : ["128 GB", "128GB", "128 ГБ", "128ГБ", "128"],
                        "256GB" : ["256 GB", "256GB", "256 ГБ", "256ГБ", "256"],
                        "512GB" : ["512 GB", "512GB", "512 ГБ", "512ГБ", "512"],
                        "1TB" : ["1024 GB", "1024GB", "1024 ГБ", "1024ГБ", "1TB", "1 TB"],
                        "2TB" : ["2048 GB", "2048GB", "2048 ГБ", "2048ГБ", "2TB", "2 TB"],
                    },
                },
                "game" : {
                    "aliases" : {
                        "+ Batman" : ["Batman", "+Batman"],
                        "+ Asgard’s Wrath 2" : ["Asgard", "Asgards", "+Asgard", "+Asgards"],
                    },
                },
            },
        },
    },
    "Valve Steam Deck" : {
        "Steam Deck" : {
            "aliases" : [
                "Steam Deck"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "Steam Deck" : ["Steam Deck"],
                    },
                },
                "oled" : {
                    "aliases" : {
                        "OLED" : ["oled"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "64GB" : ["64 GB", "64GB", "64 ГБ", "64ГБ", "64"],
                        "128GB" : ["128 GB", "128GB", "128 ГБ", "128ГБ", "128"],
                        "256GB" : ["256 GB", "256GB", "256 ГБ", "256ГБ", "256"],
                        "512GB" : ["512 GB", "512GB", "512 ГБ", "512ГБ", "512"],
                        "1TB" : ["1024 GB", "1024GB", "1024 ГБ", "1024ГБ", "1TB", "1 TB"],
                        "2TB" : ["2048 GB", "2048GB", "2048 ГБ", "2048ГБ", "2TB", "2 TB"],
                    },
                },
            },
        },
    },
    "Nintendo" : {
        "Nintendo Switch" : {
            "aliases" : [
                "Switch", "Nintendo"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "Nintendo Switch" : ["Switch", "Nintendo"],
                    },
                },
                "version" : {
                    "aliases" : {
                        "OLED" : ["oled"],
                        "Lite" : ["Lite"],
                    },
                },
                "color" : {
                    "aliases" : {
                        "Yellow" : ["Yellow", "💛"],
                        "Black" : ["⚫️", "🖤", "Black"],
                        "Blue" : ["🔵", "Blue"],
                        "Pink" : ["💖", "Pink"],
                        "Splatoon 3" : ["Splatoon 3"],
                        "Mario" : ["Mario"],
                        "Neon" : ["Neon"],
                        "White" : ["White", "⚪️", "🤍"],
                        "POKEMON" : ["POKEMON"],
                        "ZELDA" : ["ZELDA"],
                        "Special" : ["Special"],
                        "Diablo" : ["Diablo"],
                        "Monster Hunter" : ["Monster Hunter"],
                        "Fortnite" : ["Fortnite"],
                        "Turquoise" : ["Turquoise", "бирюза"],
                        "Coral" : ["Coral"]
                    },
                },
            },
        },
    },

    #Фото и видео
    "GoPro" : {
        "Экшн-камера GoPro" : {
            "aliases" : [
                "GoPro", "Go Pro"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "GoPro" : ["GoPro", "Go Pro"],
                    },
                },
                "version" : {
                    "aliases" : {
                        "HERO12" : ["12", "HERO12", "HERO 12"],
                        "HERO13" : ["13", "HERO13", "HERO 13"],
                        "4K" : ["4K"],
                    },
                },
                "add" : {
                    "aliases" : {
                        "Creator Edition" : ["Creator Edition"],
                        "Accessory Bundle" : ["Accessory Bundle"],
                        "with 64 SD" : ["with 64 SD", "with 64 SD Card"]

                    },
                },
            },
        },
        "Аксессуары GoPro" : {
            "aliases" : [
                "GoPro Army", "Removable Instrument Mount"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "GoPro Army" : ["GoPro Army"],
                        "GoPro Removable" : ["Removable"]
                    },
                },
                "add" : {
                    "aliases" : {
                        "2.0 (3-Way Refresh)" : ["2.0 (3-Way Refresh)", "2.0 (3-Way Refresh)", "2.0"],
                        "Instrument Mount" : ["Instrument Mount"]
                    },
                },
            },
        },
    },
    "Insta360" : {
        "Экшн-камера Insta360" : {
            "aliases" : [
                "Insta360", "Insta 360", "insta360°"
            ],
            "attributes" : {
                "insta" : {
                    "aliases" : {
                        "Insta360" : ["Insta360", "Insta 360", "insta360°"],
                    },
                },
                "version" : {
                    "aliases" : {
                        "X4" : ["X4"],
                        "X3" : ["X3 "],
                        "ONE X2" : ["ONE X2"],
                        "ONE RS " : ["ONE RS "],
                        "GO 3" : ["GO 3"],
                        "GO 3S" : ["GO 3S"],
                        "Ace Pro" : ["Ace Pro"],
                        "Ace Pro 2" : ["Ace Pro 2"],
                    },
                },
                "SSD" : {
                    "aliases" : {
                        "32" : ["32GB"],
                        "64" : ["64GB"],
                        "128" : ["128GB"],

                    },
                },
                "color" : {
                    "aliases" : {
                        "Black" : ["Black"],
                        "White" : ["White"],
                    },
                },
                "add" : {
                    "aliases" : {
                        "Adventure Bundle" : ["Adventure Bundle", "Adventure Action Camera"],
                        "Creator Kit" : ["Creator Kit"],
                        "Vlog Kit" : ["Vlog Kit"],
                        "Motorcycle Kit" : ["Motorcycle Kit"],
                        "Bike Bundle" : ["Bike Bundle"],
                        "Snow Bundle" : ["Snow Bundle"],
                        "Ski Kit" : ["Ski Kit"],
                        "Professional Kit" : ["Professional Kit"],
                        "1-Inch Bundle" : ["1-Inch Bundle"],
                        "Stand Alone" : ["Stand Alone"],
                        "Base Kit" : ["Base Kit"],
                        "2 АКБ" : ["2 АКБ"]
                    },
                },
            },
        },
        "Аксессуары Insta360" : {
            "aliases" : [
                "Selfie Stick", "Mini 2 in 1 Tripod", "Flow Pro Gray", "Flow Pro White", "Flow White", "Flow Gray",
                "Flow 2 Pro White", "Flow 2 Pro Gray", "Flow Pro 2 White", "Flow Pro 2 Gray", "Mini 2-in-1 Tripod + Selfie Stick",
                "Extended Edition Selfie Stick 300 см", "Extended Edition Selfie Stick 500 см", "Bullet Time Cord",
                "Bullet Time Handle + Tripod", "Helmet Mount Bundle", "Chest Strap Mount", "Back Bar Mount",
                "Suction Cup Car Mount", "Clamp Mount", "Handlebar Mount", "All-purpose Tripod",
                "Invisible Cold Shoe", "Quick Reader", "Mount Adapter Bundle", "Charging Hub",
                "Additional Battery Base", "Boosted Battery Base", "Power Selfie Stick", "Fast Charging Hub for GO 3/3S",
                "Mic Adapter", "Directional Mic", "Cold Shoe Adapter", "External Mic Mount", "Magnetic Light Mod",
                "Lens Guards", "Sticky Lens Guards", "Dive Case", "Carrying Case", "Travel Case",
                "Screen Protector", "GPS Action Remote", "AI-powered Smart Remote", "Magnetic Pendant", "Quick Release Mount"
            ],
            "attributes" : {
                "insta" : {
                    "aliases" : {
                        "Insta360" : ["Insta360", "Insta 360", "insta360°"],
                    },
                },
                "accessories": {
                    "aliases": {
                        "Invisible Selfie Stick 70 см": [
                            "Invisible Selfie Stick 70cm",
                            "Invisible Selfie Stick 70 cm",
                            "Invisible Selfie Stick 70см",
                            "Invisible Selfie Stick 70 см"
                        ],
                        "Invisible Selfie Stick 85 см": [
                            "Invisible Selfie Stick 85cm",
                            "Invisible Selfie Stick 85 cm",
                            "Invisible Selfie Stick 85см",
                            "Invisible Selfie Stick 85 см"
                        ],
                        "Invisible Selfie Stick 114 см": [
                            "Invisible Selfie Stick 114cm",
                            "Invisible Selfie Stick 114 cm",
                            "Invisible Selfie Stick 114см",
                            "Invisible Selfie Stick 114 см"
                        ],
                        "Invisible Selfie Stick 120 см": [
                            "Invisible Selfie Stick 120cm",
                            "Invisible Selfie Stick 120 cm",
                            "Invisible Selfie Stick 120см",
                            "Invisible Selfie Stick 120 см"
                        ],
                        "Invisible Selfie Stick 300 см": [
                            "Invisible Selfie Stick 300cm",
                            "Invisible Selfie Stick 300 cm",
                            "Invisible Selfie Stick 300см",
                            "Invisible Selfie Stick 300 см"
                        ],
                        "Invisible Selfie Stick 500 см": [
                            "Invisible Selfie Stick 500cm",
                            "Invisible Selfie Stick 500 cm",
                            "Invisible Selfie Stick 500см",
                            "Invisible Selfie Stick 500 см"
                        ],
                        "Mini 2-in-1 Tripod + Selfie Stick": [
                            "Mini 2-in-1 Tripod + Selfie Stick",
                            "Selfie Stick Mini 2 in 1 Tripod",
                            "Mini 2-in-1 Tripod"
                        ],
                        "Extended Edition Selfie Stick 300 см": [
                            "Extended Edition Selfie Stick 300cm",
                            "Extended Edition Selfie Stick 300 cm",
                            "Extended Selfie Stick 300cm",
                            "Extended Selfie Stick 300 см"
                        ],
                        "Extended Edition Selfie Stick 500 см": [
                            "Extended Edition Selfie Stick 500cm",
                            "Extended Edition Selfie Stick 500 cm",
                            "Extended Selfie Stick 500cm",
                            "Extended Selfie Stick 500 см"
                        ],
                        "Flow Pro Gray" : ["Flow Pro Gray"],
                        "Flow Pro White" : ["Flow Pro White"],
                        "Flow White" : ["Flow White"],
                        "Flow Gray" : ["Flow Gray"],
                        "Flow 2 Pro White": ["Flow 2 Pro White"],
                        "Flow 2 Pro Gray": ["Flow 2 Pro Gray"],
                        "Flow Pro 2 White": ["Flow Pro 2 White"],
                        "Flow Pro 2 Gray": ["Flow Pro 2 Gray"],
                        "Bullet Time Cord": [
                            "Bullet Time Cord"
                        ],
                        "Bullet Time Handle + Tripod": [
                            "Bullet Time Handle + Tripod"
                        ],
                        "Helmet Mount Bundle": [
                            "Helmet Mount Bundle"
                        ],
                        "Chest Strap Mount": [
                            "Chest Strap Mount"
                        ],
                        "Back Bar Mount": [
                            "Back Bar Mount"
                        ],
                        "Suction Cup Car Mount": [
                            "Suction Cup Car Mount"
                        ],
                        "Clamp Mount": [
                            "Clamp Mount"
                        ],
                        "Handlebar Mount": [
                            "Handlebar Mount"
                        ],
                        "All-purpose Tripod": [
                            "All-purpose Tripod",
                            "All purpose Tripod"
                        ],
                        "Invisible Cold Shoe": [
                            "Invisible Cold Shoe"
                        ],
                        "Quick Reader": [
                            "Quick Reader"
                        ],
                        "Mount Adapter Bundle": [
                            "Mount Adapter Bundle"
                        ],
                        "Charging Hub": [
                            "Charging Hub"
                        ],
                        "Additional Battery Base": [
                            "Additional Battery Base"
                        ],
                        "Boosted Battery Base": [
                            "Boosted Battery Base"
                        ],
                        "Power Selfie Stick": [
                            "Power Selfie Stick"
                        ],
                        "Fast Charging Hub for GO 3/3S": [
                            "Fast Charging Hub for GO 3/3S"
                        ],
                        "Mic Adapter": [
                            "Mic Adapter"
                        ],
                        "Directional Mic": [
                            "Directional Mic"
                        ],
                        "Cold Shoe Adapter": [
                            "Cold Shoe Adapter"
                        ],
                        "External Mic Mount": [
                            "External Mic Mount"
                        ],
                        "Magnetic Light Mod": [
                            "Magnetic Light Mod"
                        ],
                        "Lens Guards": [
                            "Lens Guards"
                        ],
                        "Sticky Lens Guards": [
                            "Sticky Lens Guards"
                        ],
                        "Dive Case": [
                            "Dive Case"
                        ],
                        "Carrying Case": [
                            "Carrying Case"
                        ],
                        "Travel Case": [
                            "Travel Case"
                        ],
                        "Screen Protector": [
                            "Screen Protector"
                        ],
                        "GPS Action Remote": [
                            "GPS Action Remote"
                        ],
                        "AI-powered Smart Remote": [
                            "AI-powered Smart Remote"
                        ],
                        "Magnetic Pendant": [
                            "Magnetic Pendant"
                        ],
                        "Quick Release Mount": [
                            "Quick Release Mount"
                        ]
                    },
                },
            },
        },
    },
    "DJI Osmo" : {
        "Экшн-камера DJI Osmo" : {
            "aliases" : [
                "DJI Osmo Action", "DJI Osmo Pocket"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "DJI Osmo Pocket" : ["DJI Osmo Pocket"],
                        "DJI Osmo Action" : ["DJI Osmo Action"]
                    },
                },
                "version" : {
                    "aliases" : {
                        "3" : ["3"],
                        "4" : ["4 "],
                        "5 Pro" : ["5 Pro"]
                    },
                },
                "add" : {
                    "aliases" : {
                        "Standard Combo" : ["Standard"],
                        "Creator Combo" : ["Creator"],
                        "Adventure Combo" : ["Adventure"],
                        "Vlog Combo" : ["Vlog"]
                    },
                },
            },
        },
        "Стабилизаторы DJI Osmo" : {
            "aliases" : [
                "DJI Osmo Mobile"
            ],
            "attributes" : {
                "console" : {
                    "aliases" : {
                        "DJI Osmo Mobile 6" : ["DJI Osmo Mobile 6"],
                        "DJI Osmo Mobile SE" : ["DJI Osmo Mobile SE"],
                        "DJI Osmo Mobile 7" : ["DJI Osmo Mobile 7"],
                        "DJI Osmo Mobile 7P" : ["DJI Osmo Mobile 7P"]
                    },
                },
            },
        },
    },
}

