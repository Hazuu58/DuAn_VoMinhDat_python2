import mysql.connector
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import create_connection
def get_all_categories():
    """
    Hàm lấy toàn bộ danh sách danh mục từ bảng category.
    Trả về list các tuple (category_id, category_name, description, created_at)
    """
    query = "SELECT * FROM category"
    try:
        connection = create_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()   # Lấy toàn bộ dữ liệu
        if result:
            print("✅ Danh sách danh mục:")
            for row in result:
                print(row)
        else:
            print("⚠️ Chưa có danh mục nào trong cơ sở dữ liệu.")
        return result
    except Error as e:
        print(f"❌ Lỗi khi lấy danh sách danh mục: {e}")
        return []
