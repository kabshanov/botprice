# db_utils.py

import pymysql
import os
import json  # для хранения списков в JSON
import datetime

# Конфигурация подключения к MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "bestprice_user",
    "password": "your_secure_password",
    "database": "bestprice",
    "charset": "utf8mb4"
}


def get_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        # print("✅ Подключение к MySQL успешно!")
        return conn
    except pymysql.MySQLError as err:
        print(f"❌ Ошибка подключения к MySQL: {err}")
        return None


# Для быстрой ручной проверки подключения
if __name__ == "__main__":
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("Результат запроса:", cursor.fetchone())
        connection.close()


# ---------------------------------------------------------------------------
# ИНИЦИАЛИЗАЦИЯ БАЗЫ
# ---------------------------------------------------------------------------

def init_db():
    """Создаём все необходимые таблицы, если их ещё нет."""
    conn = get_connection()
    if not conn:
        return

    c = conn.cursor()

    # 1) Текущий срез товаров пользователя
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user_products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            line TEXT,
            brand TEXT,
            country TEXT,
            product_name TEXT,
            model_group TEXT,
            price INT,
            supplier TEXT,
            comment TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    # 2) Настройки прайс‑листа
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id BIGINT PRIMARY KEY,
            num_columns INT,
            columns_names TEXT,
            prices_gradation TEXT,
            output_format TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    # 3) Статистика активности пользователей
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS bot_users (
            user_id BIGINT PRIMARY KEY,
            username VARCHAR(255),
            first_activity DATETIME,
            last_activity DATETIME,
            total_actions INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    # 4) НОВАЯ ТАБЛИЦА: история цен пользователя (пишем каждую цену как факт)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS price_history_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            product_name TEXT NOT NULL,
            model_group TEXT,
            price INT NOT NULL,
            country TEXT,
            supplier TEXT,
            comment TEXT,
            line TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    # --- На случай, если user_id был INT в старой схеме
    for tbl in ("user_products", "bot_users", "price_history_users"):
        try:
            c.execute(f"ALTER TABLE {tbl} MODIFY user_id BIGINT")
        except pymysql.MySQLError:
            # Если тип уже BIGINT или нет прав — тихо пропускаем
            pass

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# ТАБЛИЦЫ: user_products + price_history_users
# ---------------------------------------------------------------------------

def add_price_history_record(
    user_id: int,
    product_name: str,
    model_group: str,
    price: int,
    country: str,
    supplier: str,
    comment: str,
    line: str,
):
    """Фиксируем цену в таблице price_history_users."""
    conn = get_connection()
    if not conn:
        return

    c = conn.cursor()
    c.execute(
        """
        INSERT INTO price_history_users
        (user_id, product_name, model_group, price, country, supplier, comment, line)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            product_name,
            model_group,
            price,
            country,
            supplier,
            comment,
            line,
        ),
    )
    conn.commit()
    conn.close()


def add_product(
    user_id: int,
    line: str,
    brand: str,
    country: str,
    product_name: str,
    model_group: str,
    price: int,
    supplier: str,
    comment: str,
):
    """Добавляем запись в user_products **и** пишем историю в price_history_users."""
    conn = get_connection()
    if not conn:
        return

    c = conn.cursor()
    c.execute(
        """
        INSERT INTO user_products
        (user_id, line, brand, country, product_name, model_group, price, supplier, comment)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            line,
            brand,
            country,
            product_name,
            model_group,
            price,
            supplier,
            comment,
        ),
    )
    conn.commit()
    conn.close()

    # — Записываем историю (несинхронно с основным соединением, чтобы не держать курсор открытым)
    add_price_history_record(
        user_id=user_id,
        product_name=product_name,
        model_group=model_group,
        price=price,
        country=country,
        supplier=supplier,
        comment=comment,
        line=line,
    )


# ---------------------------------------------------------------------------
# CRUD‑функции user_products
# ---------------------------------------------------------------------------

def get_all_products(user_id: int):
    """Возвращает все товары пользователя в виде списка словарей."""
    conn = get_connection()
    if not conn:
        return []

    c = conn.cursor()
    c.execute(
        """
        SELECT line, brand, country, product_name, model_group, price, supplier, comment
        FROM user_products
        WHERE user_id = %s
        """,
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()

    return [
        {
            "line": line,
            "brand": brand,
            "country": country,
            "product_name": product_name,
            "model_group": model_group,
            "price": price,
            "supplier": supplier,
            "comment": comment,
        }
        for line, brand, country, product_name, model_group, price, supplier, comment in rows
    ]


def clear_user_data(user_id: int):
    conn = get_connection()
    if not conn:
        return
    c = conn.cursor()
    c.execute("DELETE FROM user_products WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# НАСТРОЙКИ ПРАЙС‑ЛИСТА
# ---------------------------------------------------------------------------

def get_user_settings(user_id: int) -> dict | None:
    conn = get_connection()
    if not conn:
        return None
    c = conn.cursor()
    c.execute(
        """
        SELECT num_columns, columns_names, prices_gradation, output_format
        FROM user_settings
        WHERE user_id = %s
        """,
        (user_id,),
    )
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    num_columns, columns_names_json, prices_gradation_json, output_format = row
    columns_names = json.loads(columns_names_json) if columns_names_json else []
    prices_gradation = json.loads(prices_gradation_json) if prices_gradation_json else []

    return {
        "num_columns": num_columns,
        "columns_names": columns_names,
        "prices_gradation": prices_gradation,
        "output_format": output_format,
    }


def save_user_settings(
    user_id: int,
    num_columns: int | None = None,
    columns_names: list[str] | None = None,
    prices_gradation: list | None = None,
    output_format: str | None = None,
):
    current = get_user_settings(user_id) or {
        "num_columns": None,
        "columns_names": [],
        "prices_gradation": [],
        "output_format": None,
    }

    if num_columns is not None:
        current["num_columns"] = num_columns
    if columns_names is not None:
        current["columns_names"] = columns_names
    if prices_gradation is not None:
        current["prices_gradation"] = prices_gradation
    if output_format is not None:
        current["output_format"] = output_format

    columns_json = json.dumps(current["columns_names"]) if current["columns_names"] else None
    gradation_json = json.dumps(current["prices_gradation"]) if current["prices_gradation"] else None

    conn = get_connection()
    if not conn:
        return
    c = conn.cursor()

    # INSERT … ON DUPLICATE KEY UPDATE — лаконично и безопасно
    c.execute(
        """
        INSERT INTO user_settings (user_id, num_columns, columns_names, prices_gradation, output_format)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            num_columns = VALUES(num_columns),
            columns_names = VALUES(columns_names),
            prices_gradation = VALUES(prices_gradation),
            output_format = VALUES(output_format)
        """,
        (
            user_id,
            current["num_columns"],
            columns_json,
            gradation_json,
            current["output_format"],
        ),
    )
    conn.commit()
    conn.close()


def clear_user_settings(user_id: int):
    conn = get_connection()
    if not conn:
        return
    c = conn.cursor()
    c.execute("DELETE FROM user_settings WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# СТАТИСТИКА ПОЛЬЗОВАТЕЛЕЙ (bot_users)
# ---------------------------------------------------------------------------

def track_user_activity(user_id: int, username: str):
    conn = get_connection()
    if not conn:
        return
    c = conn.cursor()

    c.execute("SELECT total_actions FROM bot_users WHERE user_id = %s", (user_id,))
    row = c.fetchone()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if row:
        total = row[0] if row[0] else 0
        c.execute(
            """
            UPDATE bot_users SET
                username = %s,
                last_activity = %s,
                total_actions = %s
            WHERE user_id = %s
            """,
            (username, now, total + 1, user_id),
        )
    else:
        c.execute(
            """
            INSERT INTO bot_users (user_id, username, first_activity, last_activity, total_actions)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, username, now, now, 1),
        )

    conn.commit()
    conn.close()


def get_all_bot_users() -> list[dict]:
    conn = get_connection()
    if not conn:
        return []
    c = conn.cursor()
    c.execute(
        """
        SELECT user_id, username, first_activity, last_activity, total_actions
        FROM bot_users
        """,
    )
    rows = c.fetchall()
    conn.close()

    return [
        {
            "user_id": user_id,
            "username": username,
            "first_activity": first_activity,
            "last_activity": last_activity,
            "total_actions": total_actions,
        }
        for user_id, username, first_activity, last_activity, total_actions in rows
    ]
