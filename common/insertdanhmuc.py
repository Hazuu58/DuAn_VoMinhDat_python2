import mysql.connector
from mysql.connector import Error

from ketnoidb.ketnoi_mysql import create_connection
def insert_category( category_name, description):
    """
    Hàm thêm 1 danh mục mới vào bảng category.
    """
    query = """
        INSERT INTO category (category_name, description)
        VALUES (%s, %s)
    """
    try:
        connection = create_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute(query, (category_name, description))
        connection.commit()
        print("✅ Thêm danh mục thành công!")
    except Error as e:
        print(f"❌ Lỗi khi thêm danh mục: {e}")
