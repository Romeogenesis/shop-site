from database.database_products import get_db_connection

def delete_product(product_name: str) -> bool:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM products WHERE product_name = ?", (product_name,))
        if not cursor.fetchone():
            print(f"ℹ️ Товар '{product_name}' не найден — удаление не требуется.")
            return False

        cursor.execute("DELETE FROM products WHERE product_name = ?", (product_name,))
        conn.commit()

        print(f"✅ Товар '{product_name}' успешно удалён.")
        return True

    except Exception as e:
        print(f"❌ Ошибка при удалении товара '{product_name}': {e}")
        return False
    finally:
        conn.close()