from common.insertdanhmuc import insert_category
while True:
    ten = input("Nhập vào tên danh mục")
    mota = input("Nhập vào mô tả")
    insert_category(ten,mota)
    con = input("Tiếp tục: Y, Thoát: ký tự bất kỳ")
    if con != "Y":
        break