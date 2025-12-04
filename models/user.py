# user.py
import sqlite3
from pathlib import Path
from typing import Optional, List

DB_PATH = Path("orders.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class User:
    def __init__(self):
        pass

    def _get_connection(self):
        return get_db_connection()

    # ===== ВРЕМЕННЫЙ ЗАКАЗ (в памяти или можно хранить в сессии) =====
    # В реальном проекте — в сессии Flask (`session['cart']`)
    # Здесь для простоты — через методы, но можно легко переделать под хранение в БД как "draft"

    def _parse_products(self, products_str: str) -> List[str]:
        """Преобразует строку 'Товар1, Товар2' → ['Товар1', 'Товар2']"""
        return [p.strip() for p in products_str.split(",") if p.strip()]

    def _format_products(self, products: List[str]) -> str:
        """Преобразует ['Товар1', 'Товар2'] → 'Товар1, Товар2'"""
        return ", ".join(products)

    # ===== ФУНКЦИИ РАБОТЫ С ЗАКАЗОМ =====

    def get_order(self, order_id: int) -> Optional[dict]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "id": row["id"],
                "total_price": row["total_price"],
                "status": row["status"],
                "payment": row["payment"],  
                "products": self._parse_products(row["products"])
            }
        except Exception as e:
            print(f"❌ Ошибка получения заказа {order_id}: {e}")
            return None
        finally:
            conn.close()

    def add_product_to_order(self, order_id: int, product_name: str) -> bool:
        """Добавить товар в существующий заказ"""
        order = self.get_order(order_id)
        if not order:
            return False

        products = order["products"]
        products.append(product_name)

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET products = ? WHERE id = ?",
                (self._format_products(products), order_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Ошибка добавления товара в заказ {order_id}: {e}")
            return False
        finally:
            conn.close()

    def remove_product_from_order(self, order_id: int, product_name: str) -> bool:
        """Удалить товар из заказа (первое вхождение)"""
        order = self.get_order(order_id)
        if not order:
            return False

        products = order["products"]
        if product_name not in products:
            return False

        products.remove(product_name)  # удаляет первое вхождение

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET products = ? WHERE id = ?",
                (self._format_products(products), order_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Ошибка удаления товара из заказа {order_id}: {e}")
            return False
        finally:
            conn.close()

    def set_payment_method(self, order_id: int, method: str) -> bool:
        if method not in ("наличные", "карта"):
            return False

        # Прямое обновление — без парсинга
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET payment = ? WHERE id = ?",
                (method, order_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Ошибка установки способа оплаты для заказа {order_id}: {e}")
            return False
        finally:
            conn.close()

    def create_order(self, total_price: int, product_names: List[str]) -> int:
        if not product_names:
            raise ValueError("Нельзя создать заказ без товаров")

        products_str = self._format_products(product_names)

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (total_price, status, payment, products) VALUES (?, ?, ?, ?)",
                (total_price, "в сборке", "наличные", products_str)  
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ Ошибка создания заказа: {e}")
            raise
        finally:
            conn.close()
    
    def get_all_products(self) -> list[dict]:
        """Получить список всех товаров (для выбора при добавлении)"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # Подключаемся к БД товаров (предполагаем, что файл рядом)
            cursor.execute("ATTACH DATABASE 'products.db' AS products_db")
            cursor.execute("SELECT id, product_name, price FROM products_db.products")
            rows = cursor.fetchall()
            return [
                {"id": r[0], "name": r[1], "price": r[2]}
                for r in rows
            ]
        except Exception as e:
            print(f"❌ Ошибка получения товаров: {e}")
            return []
        finally:
            conn.close()