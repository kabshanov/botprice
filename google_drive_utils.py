import os
import io
import socket
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# Файл с учетными данными (скачанный JSON из Google Cloud)
CREDENTIALS_FILE = "credentials.json"  # Убедись, что этот файл в .gitignore

# ID файлов API-ключей на Google Drive
FILE_IDS = {
    "dev" : "17wmkEx_aomeLuSoUXzhy96Rt5VRi26Pv",  # ID api_key_dev.txt
    "prod" : "1ZXRLIXgZgNEFRrW8JKuGJAPWv4Vz2Pg8"  # ID api_key_prod.txt
}


def detect_environment() :
    """Определяет, где запущен код: локально или на сервере."""
    if os.getenv("BOT_ENV") == "production" :
        return "prod"
    if os.getenv("BOT_ENV") == "development" :
        return "dev"

    # Проверяем имя хоста (можно изменить под свой сервер)
    hostname = socket.gethostname()
    if "server" in hostname or "prod" in hostname :
        return "prod"
    else :
        return "dev"


def download_api_key(env) :
    """Загружает API-ключ из Google Drive."""
    try :
        # Авторизация
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/drive"]
        )
        service = build("drive", "v3", credentials=creds)

        file_id = FILE_IDS[env]
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while not done :
            _, done = downloader.next_chunk()

        # Читаем API-ключ
        api_key = file_stream.getvalue().decode("utf-8").strip()
        return api_key

    except Exception as e :
        print(f"❌ Ошибка загрузки API-ключа: {e}")
        return None


# Определяем среду (локально или на сервере)
ENV = detect_environment()
print(f"🌍 Определенная среда: {ENV}")

# Загружаем нужный API-ключ
API_TOKEN = download_api_key(ENV)

if not API_TOKEN :
    print("❌ Ошибка! Не удалось загрузить API-ключ.")
    exit(1)

print("✅ API-ключ загружен успешно.")
