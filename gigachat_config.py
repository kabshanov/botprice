# gigachat_config.py
import os

# ——— Ваш Authorization Key из SberStudio ———
GIGACHAT_AUTH_KEY = os.getenv(
    "GIGACHAT_AUTH_KEY",
    "Basic SECRET"
)

# ——— Scope (GIGACHAT_API_PERS,  B2B или CORP) ———
GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

# ——— URL для получения токена и самого API ———
GIGACHAT_TOKEN_URL    = os.getenv("GIGACHAT_TOKEN_URL",
                                  "https://ngw.devices.sberbank.ru:9443/api/v2/oauth")
GIGACHAT_API_BASE_URL = os.getenv("GIGACHAT_API_BASE_URL",
                                  "https://gigachat.devices.sberbank.ru/api/v1")
