#!/usr/bin/env python3
import os
import datetime
import subprocess

# Для загрузки в Google Диск
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# MySQL конфигурация для создания дампа
MYSQL_HOST = "localhost"
MYSQL_USER = "bestprice_user"
MYSQL_PASSWORD = "SECRET"
MYSQL_DATABASE = "bestprice"

# Директория для временного хранения дампа базы данных
BACKUP_DIR = "/tmp"

# Путь к JSON-файлу сервисного аккаунта Google
SERVICE_ACCOUNT_FILE = '/root/botprice/credentials/google_service_account.json'

# ID папки в Google Диске, куда загружаем файл
DRIVE_FOLDER_ID = '1w8tYDcUbgXgS1_Yc4O4KatfLwHS3fl5d'

# Список прав (scopes) — для полного доступа к Диску
SCOPES = ['https://www.googleapis.com/auth/drive']


def backup_mysql_database() :
    """
    Создаёт дамп (backup) базы данных MySQL и сохраняет его во временную директорию.
    Возвращает путь к файлу дампа или None, если произошла ошибка.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"bestprice_backup_{timestamp}.sql"
    backup_filepath = os.path.join(BACKUP_DIR, backup_filename)

    # Формируем команду для создания дампа базы данных
    dump_command = f"mysqldump -h {MYSQL_HOST} -u {MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE}"

    try :
        with open(backup_filepath, "w") as outfile :
            result = subprocess.run(dump_command, shell=True, stdout=outfile, stderr=subprocess.PIPE)
        if result.returncode != 0 :
            error_message = result.stderr.decode().strip()
            print(
                f"[ERROR] Не удалось создать дамп базы данных. Код ошибки: {result.returncode}. Ошибка: {error_message}")
            return None
        print(f"[OK] Дамп базы данных создан: {backup_filepath}")
        return backup_filepath
    except Exception as e :
        print(f"[ERROR] Exception при создании дампа базы данных: {e}")
        return None


def upload_to_google_drive(local_file_path, drive_folder_id) :
    """
    Загружает локальный файл (local_file_path) в Google Диск
    в папку с ID = drive_folder_id.
    Возвращает ID загруженного файла или None при ошибке.
    """

    # Создаём credentials из JSON-файла сервисного аккаунта
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    # Создаём клиент для Google Drive API (v3)
    drive_service = build('drive', 'v3', credentials=credentials)

    # Формируем имя файла для хранения на Google Диске (с датой и временем)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    drive_filename = f"bestprice_backup_{timestamp}.sql"

    # Метаданные файла: имя на Google Диске и папка
    file_metadata = {
        'name' : drive_filename,
        'parents' : [drive_folder_id]
    }

    # Готовим сам файл к загрузке
    media = MediaFileUpload(local_file_path, resumable=True)

    try :
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = uploaded_file.get('id')
        print(f"[OK] Файл '{drive_filename}' загружен на Google Диск (ID: {file_id})")
        return file_id

    except Exception as e :
        print(f"[ERROR] Не удалось загрузить файл '{local_file_path}' в Google Диск: {e}")
        return None


def main() :
    # Создаём дамп базы данных MySQL
    backup_file = backup_mysql_database()
    if not backup_file or not os.path.exists(backup_file) :
        print(f"[ERROR] Файл дампа базы данных не найден.")
        return

    # Загружаем дамп на Google Диск
    uploaded_file_id = upload_to_google_drive(backup_file, DRIVE_FOLDER_ID)

    # После успешной загрузки можно удалить локальный дамп
    if uploaded_file_id :
        try :
            os.remove(backup_file)
            print(f"[OK] Локальный файл дампа удалён: {backup_file}")
        except Exception as e :
            print(f"[WARNING] Не удалось удалить локальный файл дампа: {e}")


if __name__ == '__main__' :
    main()
