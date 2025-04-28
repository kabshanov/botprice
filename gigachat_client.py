# gigachat_client.py
import time
import uuid
import requests

from gigachat_config import (
    GIGACHAT_AUTH_KEY,
    GIGACHAT_SCOPE,
    GIGACHAT_TOKEN_URL,
    GIGACHAT_API_BASE_URL,
)

# Кэш токена, чтобы не запрашивать его при каждом обращении
_token_cache: dict[str, float | str | None] = {
    "access_token": None,
    "expires_at": 0.0,
}


def get_access_token() -> str:
    """
    Получает (и кэширует) access-token GigaChat.
    При каждом вызове проверяет, не истёк ли текущий.
    """
    now_ms = time.time() * 1000
    if _token_cache["access_token"] and now_ms < _token_cache["expires_at"] - 30_000:
        return _token_cache["access_token"]  # type: ignore

    headers = {
        "Authorization": GIGACHAT_AUTH_KEY,
        "Content-Type":  "application/x-www-form-urlencoded",
        "Accept":        "application/json",
        "RqUID":         str(uuid.uuid4()),
    }
    data = {"scope": GIGACHAT_SCOPE}

    resp = requests.post(GIGACHAT_TOKEN_URL, headers=headers, data=data, verify=False)
    resp.raise_for_status()
    obj = resp.json()

    _token_cache.update(
        {
            "access_token": obj["access_token"],
            "expires_at":   obj["expires_at"],  # миллисекунды от эпохи
        }
    )
    return obj["access_token"]


def chat_completion(model: str, messages: list[dict]) -> str:
    """
    Обёртка над POST /chat/completions.
    `messages` — список dict’ов в формате OpenAI/GigaChat API.
    Возвращает content из первого choice.
    """
    token = get_access_token()
    url = f"{GIGACHAT_API_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    }
    payload = {"model": model, "messages": messages}

    resp = requests.post(url, json=payload, headers=headers, verify=False)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ——— System-prompt по умолчанию ———
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        # ───────── 1. Общая роль ─────────
        "Ты — форматировщик прайс-листов.\n"
        "Ниже я передам *Эталон* — это единственный пример того, "
        "как пользователь хочет видеть готовый прайс-лист.\n\n"

        # ───────── 2. Что нужно сделать ─────────
        "Твоя задача — внимательно изучить Эталон, извлечь из него правила визуального оформления и "
        "потом применить эти правила к *НовомуСообщению* (сырым ценам), не теряя данных и не добавляя лишнего.\n\n"

        # 2.1 Какие именно правила надо вытащить
        "Извлеки и запомни (внутренне, без вывода) всё, что касается:\n"
        "• порядка и названий блоков/заголовков;\n"
        "• наличия/отсутствия общих заголовков категорий, брендов;\n"
        "• символа-маркера (▪️, •, эмодзи, др.);\n"
        "• мест, где стоят пустые строки;\n"
        "• логики группировки (объём памяти, Dual sim/eSim/LTE, год, модель и т.д.);\n"
        "• порядка полей в строке (модель → объём → цвет → атрибуты → цена → флаг страны);\n"
        "• сортировки внутри групп (объём ↑, цвет A→Z, и пр.).\n\n"

        # 2.2 Как работать с НовымСообщением
        "Когда получишь НовоеСообщение, преврати его в готовый прайс строго по этим правилам. "
        "Если там встретятся новые модели/объёмы/атрибуты — логично вставь их в уже существующие группы, "
        "соблюдая найденный порядок.\n\n"

        # ───────── 3. ЖЁСТКИЕ ПРАВИЛА-ОГРАНИЧЕНИЯ ─────────
        "ДОПОЛНИТЕЛЬНЫЕ ЖЁСТКИЕ ПРАВИЛА:\n"
        "• Не используй Markdown-разметку ( #, *, _, —, -, +, цифры-точки ). Выводи только plain-text.\n"
        "• Сохраняй символы-маркеры и тире ровно такими, как в Эталоне (например, «▪️» и «–»).\n"
        "• Не добавляй символ валюты, если его нет в Эталоне. Не меняй формат чисел (точки↔запятые, пробелы-разделители).\n"
        "• Пустые строки ставь **только** в тех местах, где они есть в Эталоне.\n"
        "• Заголовок под-группы выводи один раз; при следующих строках той же под-группы не дублируй его.\n"
        "• Сохраняй все эмодзи-флаги, кавычки (\" vs ”), дюймовые символы и любые спец-знаки как есть.\n"
        "• Не выводи ничего, кроме конечного текста прайс-листа (никаких объяснений, описаний правил и т.п.).\n\n"

        # ───────── 4. Универсальность ─────────
        "Правила должны работать для любых товарных категорий: смартфоны, планшеты, ноутбуки, часы, аудио и др.\n"
        "Если в Эталоне нет общего заголовка-категории — не добавляй его, даже если он встречается в НовомСообщении.\n"
    ),
}



# ——— Мини-самотест ———
if __name__ == "__main__":
    raw_text = """
APPLE IPHONE
iPhone 16 Pro
16 Pro 128 Black – 83.400 🇦🇪
16 Pro 128 Desert – 81.300 🇦🇪
16 Pro 128 Desert Dual sim – 81.100 🇨🇳
16 Pro 128 Black eSim – 75.100 🇺🇸
"""
    dialog = [SYSTEM_PROMPT, {"role": "user", "content": raw_text}]
    print(chat_completion("GigaChat-Pro", dialog))
