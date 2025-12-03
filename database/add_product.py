from database.database_products import get_db_connection

def add_product(product_name: str, price: int):
    conn = get_db_connection()
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
        