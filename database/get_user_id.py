from database.database_users import get_db_connection

def get_user_id(username: str) -> str | None:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE name = ?", (username,))
        row = cursor.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"❌ Ошибка при получении id: {e}")
        return None
    finally:
        conn.close()