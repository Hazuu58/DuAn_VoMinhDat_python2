import mysql.connector
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import create_connection
def delete_category( category_id):
    """
    Hàm xóa 1 danh mục khỏi bảng category dựa trên category_id.
    """
    query = "DELETE FROM category WHERE category_id = %s"
    try:
        connection = create_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute(query, (category_id,))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"✅ Đã xóa danh mục có ID = {category_id}")
        else:
            print(f"⚠️ Không tìm thấy danh mục có ID = {category_id}")
    except Error as e:
        print(f"❌ Lỗi khi xóa danh mục: {e}")
