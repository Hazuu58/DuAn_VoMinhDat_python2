import mysql.connector
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import create_connection
def update_category( category_id, new_name, new_description):
    """
    Hàm cập nhật tên và mô tả danh mục dựa trên category_id.
    """
    query = """
        UPDATE category
        SET category_name = %s,
            description = %s
        WHERE category_id = %s
    """
    try:
        connection = create_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute(query, (new_name, new_description, category_id))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"✅ Đã cập nhật danh mục có ID = {category_id}")
        else:
            print(f"⚠️ Không tìm thấy danh mục có ID = {category_id}")
    except Error as e:
        print(f"❌ Lỗi khi cập nhật danh mục: {e}")
