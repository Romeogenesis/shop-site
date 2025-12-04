from database.database_users import get_db_connection

def add_user(name: str, password: str, role: str) -> bool:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE name = ?", (name,))
            if cursor.fetchone():
                return False
            cursor.execute(
                "INSERT INTO users (name, password, role) VALUES (?, ?, ?)",
                (name, password, role)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Ошибка при добавлении пользователя: {e}")
            return False
        finally:
            conn.close()