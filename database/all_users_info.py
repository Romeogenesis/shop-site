from database.database_users import get_db_connection

def get_all_users() -> list[dict] | None:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, role FROM users ORDER BY id")
        rows = cursor.fetchall()
        
        users = [
            {"id": row[0], "name": row[1], "role": row[2]}
            for row in rows
        ]
        
        print(f"✅ Получено {len(users)} пользователей.")
        return users

    except Exception as e:
        print(f"❌ Ошибка при получении списка пользователей: {e}")
        return None
    finally:
        conn.close()