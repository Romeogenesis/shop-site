# admin.py
from database.database_users import get_db_connection


class Admin:
    def __init__(self):
        pass

    def _get_connection(self):
        """Внутренний метод для получения соединения (единая точка доступа)"""
        return get_db_connection()


    def add_user(self, name: str, password: str, role: str) -> bool:
        conn = self._get_connection()
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

    def delete_user(self, name: str) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE name = ?", (name,))
            if not cursor.fetchone():
                return False
            cursor.execute("DELETE FROM users WHERE name = ?", (name,))
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Ошибка при удалении пользователя '{name}': {e}")
            return False
        finally:
            conn.close()

    def get_all_users(self) -> list[dict] | None:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, role FROM users ORDER BY id")
            rows = cursor.fetchall()
            return [
                {"id": r[0], "name": r[1], "role": r[2]}
                for r in rows
            ]
        except Exception as e:
            print(f"❌ Ошибка при получении списка пользователей: {e}")
            return None
        finally:
            conn.close()

    # ========================
    # УПРАВЛЕНИЕ ТОВАРАМИ
    # ========================

    def add_product(self, product_name: str, price: int) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM products WHERE product_name = ?", (product_name,))
            if cursor.fetchone():
                return False
            cursor.execute(
                "INSERT INTO products (product_name, price) VALUES (?, ?)",
                (product_name, price)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Ошибка при добавлении товара: {e}")
            return False
        finally:
            conn.close()

    def delete_product(self, product_name: str) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM products WHERE product_name = ?", (product_name,))
            if not cursor.fetchone():
                return False
            cursor.execute("DELETE FROM products WHERE product_name = ?", (product_name,))
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Ошибка при удалении товара '{product_name}': {e}")
            return False
        finally:
            conn.close()

    def get_all_products(self) -> list[dict] | None:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, product_name, price FROM products ORDER BY id")
            rows = cursor.fetchall()
            return [
                {"id": r[0], "product_name": r[1], "price": r[2]}
                for r in rows
            ]
        except Exception as e:
            print(f"❌ Ошибка при получении списка товаров: {e}")
            return None
        finally:
            conn.close()