import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import create_connection


def load_data():
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
    name = entry_name.get()
    desc = entry_desc.get()
    if name == "":
        messagebox.showwarning("Cảnh báo", "Tên danh mục không được để trống!")
        return
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO category (category_name, description) VALUES (%s, %s)", (name, desc))
        conn.commit()
        conn.close()
        load_data()
        clear_inputs()
        messagebox.showinfo("Thành công", "Đã thêm danh mục mới!")

def delete_category():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn danh mục để xóa!")
        return
    item = tree.item(selected[0])
    category_id = item["values"][0]
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
        conn.commit()
        conn.close()
        load_data()
        messagebox.showinfo("Thành công", "Đã xóa danh mục!")

def update_category():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn danh mục để sửa!")
        return
    item = tree.item(selected[0])
    category_id = item["values"][0]
    name = entry_name.get()
    desc = entry_desc.get()
    if name == "":
        messagebox.showwarning("Cảnh báo", "Tên danh mục không được để trống!")
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
        messagebox.showinfo("Thành công", "Đã cập nhật danh mục!")
def on_select(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        values = item["values"]
        entry_name.delete(0, tk.END)
        entry_name.insert(0, values[1])
        entry_desc.delete(0, tk.END)
        entry_desc.insert(0, values[2])

def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    tree.selection_remove(tree.selection())
# ==================== GIAO DIỆN CHÍNH ====================
root = tk.Tk()
root.title("Quản lý Danh mục")
root.geometry("700x450")
root.resizable(False, False)

# Frame nhập liệu
frame_input = tk.LabelFrame(root, text="Thông tin danh mục", padx=10, pady=10)
frame_input.pack(fill="x", padx=10, pady=10)

tk.Label(frame_input, text="Tên danh mục:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(frame_input, width=40)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Mô tả:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_desc = tk.Entry(frame_input, width=40)
entry_desc.grid(row=1, column=1, padx=5, pady=5)

# Nút chức năng
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=10, pady=5)

btn_add = tk.Button(frame_btn, text="➕ Thêm", width=12, command=add_category)
btn_add.pack(side="left", padx=5)

btn_update = tk.Button(frame_btn, text="✏️ Sửa", width=12, command=update_category)
btn_update.pack(side="left", padx=5)

btn_delete = tk.Button(frame_btn, text="🗑️ Xóa", width=12, command=delete_category)
btn_delete.pack(side="left", padx=5)

btn_clear = tk.Button(frame_btn, text="🧹 Làm mới", width=12, command=clear_inputs)
btn_clear.pack(side="left", padx=5)

# Bảng hiển thị dữ liệu
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Tên danh mục", "Mô tả", "Ngày tạo")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
tree.column("ID", width=50, anchor="center")
tree.column("Tên danh mục", width=200)
tree.column("Mô tả", width=300)
tree.column("Ngày tạo", width=130, anchor="center")
tree.bind("<<TreeviewSelect>>", on_select)
tree.pack(fill="both", expand=True)

load_data()

root.mainloop()