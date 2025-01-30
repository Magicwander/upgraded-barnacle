import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database setup
def init_db():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS menu (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    price REAL,
                    category TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    table_number INTEGER,
                    item_id INTEGER,
                    quantity INTEGER,
                    FOREIGN KEY(item_id) REFERENCES menu(id))''')
    conn.commit()
    conn.close()

# CRUD operations
def add_menu_item(name, price, category):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("INSERT INTO menu (name, price, category) VALUES (?, ?, ?)", (name, price, category))
    conn.commit()
    conn.close()

def add_order(table_number, item_id, quantity):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (table_number, item_id, quantity) VALUES (?, ?, ?)", (table_number, item_id, quantity))
    conn.commit()
    conn.close()

def get_menu_items():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("SELECT * FROM menu")
    menu_items = c.fetchall()
    conn.close()
    return menu_items

def get_orders():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    orders = c.fetchall()
    conn.close()
    return orders

def delete_menu_item(item_id):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("DELETE FROM menu WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

# GUI setup
class RestaurantOrderingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Ordering System")

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.menu_tab = ttk.Frame(self.tab_control)
        self.order_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.menu_tab, text='Menu')
        self.tab_control.add(self.order_tab, text='Orders')

        self.tab_control.pack(expand=1, fill='both')

        self.create_menu_tab()
        self.create_order_tab()

    def create_menu_tab(self):
        tk.Label(self.menu_tab, text="Item Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.menu_tab, text="Price").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.menu_tab, text="Category").grid(row=2, column=0, padx=10, pady=5)

        self.menu_item_name = tk.Entry(self.menu_tab)
        self.menu_item_price = tk.Entry(self.menu_tab)
        self.menu_item_category = tk.Entry(self.menu_tab)

        self.menu_item_name.grid(row=0, column=1, padx=10, pady=5)
        self.menu_item_price.grid(row=1, column=1, padx=10, pady=5)
        self.menu_item_category.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.menu_tab, text='Add Menu Item', command=self.add_menu_item).grid(row=3, column=0, columnspan=2, pady=10)

        self.menu_list = tk.Listbox(self.menu_tab, width=50)
        self.menu_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.menu_tab, text='Delete Menu Item', command=self.delete_menu_item).grid(row=5, column=0, columnspan=2, pady=10)

        self.load_menu_items()

    def create_order_tab(self):
        tk.Label(self.order_tab, text="Table Number").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.order_tab, text="Item ID").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.order_tab, text="Quantity").grid(row=2, column=0, padx=10, pady=5)

        self.order_table_number = tk.Entry(self.order_tab)
        self.order_item_id = tk.Entry(self.order_tab)
        self.order_quantity = tk.Entry(self.order_tab)

        self.order_table_number.grid(row=0, column=1, padx=10, pady=5)
        self.order_item_id.grid(row=1, column=1, padx=10, pady=5)
        self.order_quantity.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.order_tab, text='Add Order', command=self.add_order).grid(row=3, column=0, columnspan=2, pady=10)

        self.order_list = tk.Listbox(self.order_tab, width=50)
        self.order_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.order_tab, text='Delete Order', command=self.delete_order).grid(row=5, column=0, columnspan=2, pady=10)

        self.load_orders()

    def add_menu_item(self):
        name = self.menu_item_name.get()
        price = self.menu_item_price.get()
        category = self.menu_item_category.get()
        if name and price and category:
            add_menu_item(name, price, category)
            self.load_menu_items()
            messagebox.showinfo("Success", "Menu item added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide all menu item details")

    def add_order(self):
        table_number = self.order_table_number.get()
        item_id = self.order_item_id.get()
        quantity = self.order_quantity.get()
        if table_number and item_id and quantity:
            add_order(table_number, item_id, quantity)
            self.load_orders()
            messagebox.showinfo("Success", "Order added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide all order details")

    def load_menu_items(self):
        self.menu_list.delete(0, tk.END)
        menu_items = get_menu_items()
        for item in menu_items:
            self.menu_list.insert(tk.END, f"{item[0]}: {item[1]} - ${item[2]} - {item[3]}")

    def load_orders(self):
        self.order_list.delete(0, tk.END)
        orders = get_orders()
        for order in orders:
            self.order_list.insert(tk.END, f"{order[0]}: Table {order[1]}, Item ID: {order[2]}, Quantity: {order[3]}")

    def delete_menu_item(self):
        selected_index = self.menu_list.curselection()
        if selected_index:
            item_id = self.menu_list.get(selected_index).split(':')[0]
            delete_menu_item(item_id)
            self.load_menu_items()
            messagebox.showinfo("Success", "Menu item deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a menu item to delete")

    def delete_order(self):
        selected_index = self.order_list.curselection()
        if selected_index:
            order_id = self.order_list.get(selected_index).split(':')[0]
            delete_order(order_id)
            self.load_orders()
            messagebox.showinfo("Success", "Order deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select an order to delete")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = RestaurantOrderingApp(root)
    root.mainloop()
