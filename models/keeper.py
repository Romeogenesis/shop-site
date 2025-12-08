# keeper.py
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict
from database.database_orders import get_db_connection


class Keeper:
    def __init__(self):
        pass

    def _get_connection(self):
        return get_db_connection()

    def get_all_orders(self, status_filter: Optional[str] = None) -> List[Dict]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if status_filter:
                cursor.execute("SELECT * FROM orders WHERE status = ?", (status_filter,))
            else:
                cursor.execute("SELECT * FROM orders ORDER BY id DESC")
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "total_price": row["total_price"],
                    "status": row["status"],
                    "payment": row["payment"],
                    "products": [p.strip() for p in row["products"].split(",") if p.strip()]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"❌ Ошибка получения заказов: {e}")
            return []
        finally:
            conn.close()

    def update_order_status(self, order_id: int, new_status: str) -> bool:
        if new_status not in ("в сборке", "готов"):
            return False

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                (new_status, order_id)
            )
            conn.commit()
            return cursor.rowcount > 0  
        except Exception as e:
            print(f"❌ Ошибка обновления статуса заказа {order_id}: {e}")
            return False
        finally:
            conn.close()