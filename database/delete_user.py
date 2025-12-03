from database.database_users import get_db_connection

def delete_user(name: str) -> bool:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM users WHERE name = ?", (name,))
        if not cursor.fetchone():
            print(f"ℹ️ Пользователь '{name}' не найден — удаление не требуется.")
            return False

        cursor.execute("DELETE FROM users WHERE name = ?", (name,))
        conn.commit()

        print(f"✅ Пользователь '{name}' успешно удалён.")
        return True

    except Exception as e:
        print(f"❌ Ошибка при удалении пользователя '{name}': {e}")
        return False
    finally:
        conn.close()