import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Hàm tạo kết nối đến MySQL Database.
    Trả về đối tượng connection nếu thành công, None nếu thất bại.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="qlthuocankhang"
        )
        print("✅ Kết nối MySQL thành công!")
    except Error as e:
        print(f"❌ Lỗi khi kết nối MySQL: {e}")
    return connection
