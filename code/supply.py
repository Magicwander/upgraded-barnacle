import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database setup
def init_db():
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    contact TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    item_name TEXT,
                    quantity INTEGER,
                    supplier_id INTEGER,
                    FOREIGN KEY(supplier_id) REFERENCES suppliers(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS purchase_orders (
                    id INTEGER PRIMARY KEY,
                    item_name TEXT,
                    quantity INTEGER,
                    supplier_id INTEGER,
                    FOREIGN KEY(supplier_id) REFERENCES suppliers(id))''')
    conn.commit()
    conn.close()

# CRUD operations
def add_supplier(name, contact):
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("INSERT INTO suppliers (name, contact) VALUES (?, ?)", (name, contact))
    conn.commit()
    conn.close()

def add_inventory(item_name, quantity, supplier_id):
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (item_name, quantity, supplier_id) VALUES (?, ?, ?)", (item_name, quantity, supplier_id))
    conn.commit()
    conn.close()

def add_purchase_order(item_name, quantity, supplier_id):
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("INSERT INTO purchase_orders (item_name, quantity, supplier_id) VALUES (?, ?, ?)", (item_name, quantity, supplier_id))
    conn.commit()
    conn.close()

def get_suppliers():
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("SELECT * FROM suppliers")
    suppliers = c.fetchall()
    conn.close()
    return suppliers

def get_inventory():
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    inventory = c.fetchall()
    conn.close()
    return inventory

def get_purchase_orders():
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("SELECT * FROM purchase_orders")
    orders = c.fetchall()
    conn.close()
    return orders

def delete_supplier(supplier_id):
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
    conn.commit()
    conn.close()

def delete_inventory(item_id):
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

def delete_purchase_order(order_id):
    conn = sqlite3.connect('supply_chain.db')
    c = conn.cursor()
    c.execute("DELETE FROM purchase_orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

# GUI setup
class SupplyChainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Supply Chain Management System")

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.supplier_tab = ttk.Frame(self.tab_control)
        self.inventory_tab = ttk.Frame(self.tab_control)
        self.purchase_order_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.supplier_tab, text='Suppliers')
        self.tab_control.add(self.inventory_tab, text='Inventory')
        self.tab_control.add(self.purchase_order_tab, text='Purchase Orders')

        self.tab_control.pack(expand=1, fill='both')

        self.create_supplier_tab()
        self.create_inventory_tab()
        self.create_purchase_order_tab()

    def create_supplier_tab(self):
        tk.Label(self.supplier_tab, text="Supplier Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.supplier_tab, text="Contact").grid(row=1, column=0, padx=10, pady=5)

        self.supplier_name = tk.Entry(self.supplier_tab)
        self.supplier_contact = tk.Entry(self.supplier_tab)

        self.supplier_name.grid(row=0, column=1, padx=10, pady=5)
        self.supplier_contact.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.supplier_tab, text='Add Supplier', command=self.add_supplier).grid(row=2, column=0, columnspan=2, pady=10)

        self.supplier_list = tk.Listbox(self.supplier_tab, width=50)
        self.supplier_list.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.supplier_tab, text='Delete Supplier', command=self.delete_supplier).grid(row=4, column=0, columnspan=2, pady=10)

        self.load_suppliers()

    def create_inventory_tab(self):
        tk.Label(self.inventory_tab, text="Item Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.inventory_tab, text="Quantity").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.inventory_tab, text="Supplier ID").grid(row=2, column=0, padx=10, pady=5)

        self.item_name = tk.Entry(self.inventory_tab)
        self.quantity = tk.Entry(self.inventory_tab)
        self.supplier_id = tk.Entry(self.inventory_tab)

        self.item_name.grid(row=0, column=1, padx=10, pady=5)
        self.quantity.grid(row=1, column=1, padx=10, pady=5)
        self.supplier_id.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.inventory_tab, text='Add Inventory', command=self.add_inventory).grid(row=3, column=0, columnspan=2, pady=10)

        self.inventory_list = tk.Listbox(self.inventory_tab, width=50)
        self.inventory_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.inventory_tab, text='Delete Inventory', command=self.delete_inventory).grid(row=5, column=0, columnspan=2, pady=10)

        self.load_inventory()

    def create_purchase_order_tab(self):
        tk.Label(self.purchase_order_tab, text="Item Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.purchase_order_tab, text="Quantity").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.purchase_order_tab, text="Supplier ID").grid(row=2, column=0, padx=10, pady=5)

        self.po_item_name = tk.Entry(self.purchase_order_tab)
        self.po_quantity = tk.Entry(self.purchase_order_tab)
        self.po_supplier_id = tk.Entry(self.purchase_order_tab)

        self.po_item_name.grid(row=0, column=1, padx=10, pady=5)
        self.po_quantity.grid(row=1, column=1, padx=10, pady=5)
        self.po_supplier_id.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.purchase_order_tab, text='Add Purchase Order', command=self.add_purchase_order).grid(row=3, column=0, columnspan=2, pady=10)

        self.po_list = tk.Listbox(self.purchase_order_tab, width=50)
        self.po_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.purchase_order_tab, text='Delete Purchase Order', command=self.delete_purchase_order).grid(row=5, column=0, columnspan=2, pady=10)

        self.load_purchase_orders()

    def add_supplier(self):
        name = self.supplier_name.get()
        contact = self.supplier_contact.get()
        if name and contact:
            add_supplier(name, contact)
            self.load_suppliers()
            messagebox.showinfo("Success", "Supplier added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide both name and contact")

    def add_inventory(self):
        item_name = self.item_name.get()
        quantity = self.quantity.get()
        supplier_id = self.supplier_id.get()
        if item_name and quantity and supplier_id:
            add_inventory(item_name, quantity, supplier_id)
            self.load_inventory()
            messagebox.showinfo("Success", "Inventory added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide item name, quantity, and supplier ID")

    def add_purchase_order(self):
        item_name = self.po_item_name.get()
        quantity = self.po_quantity.get()
        supplier_id = self.po_supplier_id.get()
        if item_name and quantity and supplier_id:
            add_purchase_order(item_name, quantity, supplier_id)
            self.load_purchase_orders()
            messagebox.showinfo("Success", "Purchase order added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide item name, quantity, and supplier ID")

    def load_suppliers(self):
        self.supplier_list.delete(0, tk.END)
        suppliers = get_suppliers()
        for supplier in suppliers:
            self.supplier_list.insert(tk.END, f"{supplier[0]}: {supplier[1]} - {supplier[2]}")

    def load_inventory(self):
        self.inventory_list.delete(0, tk.END)
        inventory = get_inventory()
        for item in inventory:
            self.inventory_list.insert(tk.END, f"{item[0]}: {item[1]} - {item[2]} - Supplier ID: {item[3]}")

    def load_purchase_orders(self):
        self.po_list.delete(0, tk.END)
        orders = get_purchase_orders()
        for order in orders:
            self.po_list.insert(tk.END, f"{order[0]}: {order[1]} - {order[2]} - Supplier ID: {order[3]}")

    def delete_supplier(self):
        selected_index = self.supplier_list.curselection()
        if selected_index:
            supplier_id = self.supplier_list.get(selected_index).split(':')[0]
            delete_supplier(supplier_id)
            self.load_suppliers()
            messagebox.showinfo("Success", "Supplier deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a supplier to delete")

    def delete_inventory(self):
        selected_index = self.inventory_list.curselection()
        if selected_index:
            item_id = self.inventory_list.get(selected_index).split(':')[0]
            delete_inventory(item_id)
            self.load_inventory()
            messagebox.showinfo("Success", "Inventory item deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select an inventory item to delete")

    def delete_purchase_order(self):
        selected_index = self.po_list.curselection()
        if selected_index:
            order_id = self.po_list.get(selected_index).split(':')[0]
            delete_purchase_order(order_id)
            self.load_purchase_orders()
            messagebox.showinfo("Success", "Purchase order deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a purchase order to delete")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = SupplyChainApp(root)
    root.mainloop()
