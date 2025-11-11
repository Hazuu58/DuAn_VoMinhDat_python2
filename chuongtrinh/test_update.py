from common.updatedanhmuc import update_category

while True:
    ma = input("Nhập mã danh mục cần sửa")
    ten = input("Nhập vào tên danh mục mới")
    mota = input("Nhập vào mô tả mới")
    update_category(ma,ten,mota)
    con = input("Tiếp tục: Y, Thoát: ký tự bất kỳ")
    if con != "Y":
        break