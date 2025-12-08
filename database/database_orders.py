import sqlite3
from pathlib import Path

ORDERS_DB_PATH = Path("orders.db")
USERS_DB_PATH = Path("user.db")

def init_orders_db():
    conn = sqlite3.connect(ORDERS_DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_price INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('в сборке', 'готов')),
            payment TEXT NOT NULL CHECK(payment IN ('наличные', 'карта')),
            products TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(ORDERS_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

