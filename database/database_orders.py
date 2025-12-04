import sqlite3
from pathlib import Path

DB_PATH = Path("orders.db")


def init_orders_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_price INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('в сборке', 'готов')),
            payment TEXT NOT NULL CHECK(payment IN ('наличные', 'карта')),
            products TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn