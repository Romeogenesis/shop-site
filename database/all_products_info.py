from database.database_products import get_db_connection

def get_all_products() -> list[dict] | None:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, product_name, price FROM products ORDER BY id")
        rows = cursor.fetchall()
        
        products = [
            {"id": row[0], "product_name": row[1], "price": row[2]}
            for row in rows
        ]
        
        print(f"✅ Получено {len(products)} товаров.")
        return products

    except Exception as e:
        print(f"❌ Ошибка при получении списка товаров: {e}")
        return None
    finally:
        conn.close()