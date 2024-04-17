import tkinter as tk
from tkinter import ttk

import sqlite3

# Создадим базу данных
def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    order_details TEXT NOT NULL,
    status TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

# Добавим содержимое базы данных
def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
                (customer_name_entry.get(), order_details_entry.get()))
    conn.commit()
    conn.close()
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
#     После каждого добавления заказа также строчку надо будет очищать
    view_orders()

# Создадим функцию, которая будет отображать содержимое базы данных в таблице приложения

def view_orders():
    # этот цикл for будет очищать строки таблицы для ввода новых данных, чтобы информация не повторялась
    for i in tree.get_children():
        tree.delete(i)
    #     здесь цикл заканчивается
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()



app = tk.Tk()
app.title("Система управления заказами")

# Поле для ввода, чтобы ввести Имя

tk.Label(app, text="Имя клиента").pack()
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

# Поле для ввода, чтобы ввести Детали заказа

tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()

# Устанавливаем кнопку для добавления заказа и прикрепляем к ней функцию

add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# Создадим таблицу

columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")
for column in columns:
    tree.heading(column, text=column)
tree.pack()

init_db()
view_orders()
app.mainloop()
