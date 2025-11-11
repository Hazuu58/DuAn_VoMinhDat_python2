import tkinter as tk
from tkinter import ttk, messagebox
from ketnoidb.ketnoi_mysql import create_connection
from datetime import datetime

# ========================== 🗂️ HÀM XỬ LÝ DỮ LIỆU ==========================

def load_data():
    """ Load toàn bộ dữ liệu danh mục từ CSDL lên TreeView"""
    for item in tree.get_children():
        tree.delete(item)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM category")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)
        conn.close()

def add_category():
    """ Thêm danh mục mới vào CSDL"""
    name = entry_name.get().strip()
    desc = entry_desc.get().strip()
    if name == "":
        messagebox.showwarning("⚠️ Cảnh báo", "Tên danh mục không được để trống!")
        return
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO category (category_name, description, created_at) VALUES (%s, %s, %s)",
            (name, desc, datetime.now())
        )
        conn.commit()
        conn.close()
        load_data()
        clear_inputs()
        messagebox.showinfo("✅ Thành công", "Đã thêm danh mục mới!")

def delete_category():
    """ Xóa danh mục đang chọn"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn danh mục để xóa!")
        return
    item = tree.item(selected[0])
    category_id = item["values"][0]
    if not messagebox.askyesno("❓ Xác nhận", "Bạn có chắc muốn xóa danh mục này?"):
        return
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
        conn.commit()
        conn.close()
        load_data()
        messagebox.showinfo("✅ Thành công", "Đã xóa danh mục!")

def update_category():
    """ Cập nhật thông tin danh mục đã chọn"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn danh mục để sửa!")
        return
    item = tree.item(selected[0])
    category_id = item["values"][0]
    name = entry_name.get().strip()
    desc = entry_desc.get().strip()
    if name == "":
        messagebox.showwarning("⚠️ Cảnh báo", "Tên danh mục không được để trống!")
        return
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE category 
            SET category_name = %s, description = %s 
            WHERE category_id = %s
        """, (name, desc, category_id))
        conn.commit()
        conn.close()
        load_data()
        clear_inputs()
        messagebox.showinfo("✅ Thành công", "Đã cập nhật danh mục!")

def on_select(event):
    """ Khi chọn một dòng trên bảng thì hiển thị thông tin lên ô nhập"""
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        values = item["values"]
        entry_name.delete(0, tk.END)
        entry_name.insert(0, values[1])
        entry_desc.delete(0, tk.END)
        entry_desc.insert(0, values[2])

def clear_inputs():
    """ Xóa các ô nhập và bỏ chọn trên bảng"""
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    tree.selection_remove(tree.selection())

# ========================== 🎨 GIAO DIỆN CHÍNH ==========================

root = tk.Tk()
root.title("📂 Quản lý Danh mục")
root.geometry("750x500")
root.configure(bg="#f9fafb")
root.resizable(False, False)

#  Tiêu đề chính
lbl_title = tk.Label(
    root,
    text="🗃️ QUẢN LÝ DANH MỤC SẢN PHẨM",
    font=("Segoe UI", 16, "bold"),
    bg="#f9fafb",
    fg="#0d6efd"
)
lbl_title.pack(pady=10)

#  Frame nhập liệu
frame_input = tk.LabelFrame(
    root, text="Thông tin danh mục", padx=10, pady=10,
    bg="#f9fafb", fg="#333", font=("Segoe UI", 10, "bold")
)
frame_input.pack(fill="x", padx=15, pady=10)

tk.Label(frame_input, text="Tên danh mục:", bg="#f9fafb", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(frame_input, width=45, font=("Segoe UI", 10))
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Mô tả:", bg="#f9fafb", font=("Segoe UI", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_desc = tk.Entry(frame_input, width=45, font=("Segoe UI", 10))
entry_desc.grid(row=1, column=1, padx=5, pady=5)

#  Frame nút chức năng
frame_btn = tk.Frame(root, bg="#f9fafb")
frame_btn.pack(fill="x", padx=10, pady=5)

style_btn = {
    "font": ("Segoe UI", 10, "bold"),
    "width": 13,
    "height": 1,
    "relief": "groove",
    "cursor": "hand2"
}

btn_add = tk.Button(frame_btn, text="➕ Thêm", bg="#198754", fg="white", command=add_category, **style_btn)
btn_add.pack(side="left", padx=5)

btn_update = tk.Button(frame_btn, text="✏️ Sửa", bg="#0d6efd", fg="white", command=update_category, **style_btn)
btn_update.pack(side="left", padx=5)

btn_delete = tk.Button(frame_btn, text="🗑️ Xóa", bg="#dc3545", fg="white", command=delete_category, **style_btn)
btn_delete.pack(side="left", padx=5)

btn_clear = tk.Button(frame_btn, text="🧹 Làm mới", bg="#6c757d", fg="white", command=clear_inputs, **style_btn)
btn_clear.pack(side="left", padx=5)

#  Bảng hiển thị dữ liệu
frame_table = tk.Frame(root, bg="#f9fafb")
frame_table.pack(fill="both", expand=True, padx=15, pady=10)

columns = ("ID", "Tên danh mục", "Mô tả", "Ngày tạo")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)

#  Thiết lập tiêu đề bảng
style = ttk.Style()
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#0d6efd", foreground="black")
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

for col in columns:
    tree.heading(col, text=col, anchor="center")
tree.column("ID", width=50, anchor="center")
tree.column("Tên danh mục", width=180)
tree.column("Mô tả", width=300)
tree.column("Ngày tạo", width=150, anchor="center")

#  Thanh cuộn
scrollbar_y = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar_y.set)
scrollbar_y.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", on_select)

#  Load dữ liệu ban đầu
load_data()

root.mainloop()
