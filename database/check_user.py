from database.database_users import get_db_connection

def check_user(name: str, password: str):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()
        if row:
            stored_password = row[0]
            return stored_password == password  
        return False
    except Exception as e:
        print(f"❌ Ошибка при проверке пользователя {name}: {e}")
        return False
    finally:
        conn.close()
            