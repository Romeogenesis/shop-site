from database.database import get_db_connection

def add_user(name: str, password: str, role: str):
    conn = get_db_connection()
    try: 
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, password, role) VALUES (?, ?, ?)",
            (name, password, role)
        )
        conn.commit()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()
        