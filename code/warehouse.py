import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY, product_name TEXT, quantity INTEGER, location TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS deliveries
                 (id INTEGER PRIMARY KEY, product_name TEXT, quantity INTEGER, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shipments
                 (id INTEGER PRIMARY KEY, product_name TEXT, quantity INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

# Add a new product to the inventory
def add_product():
    product_name = entry_product_name.get()
    quantity = entry_quantity.get()
    location = entry_location.get()
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (product_name, quantity, location) VALUES (?, ?, ?)",
              (product_name, quantity, location))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Product added successfully!")
    clear_entries()
    view_inventory()

# Update product quantity
def update_product():
    product_name = entry_product_name.get()
    quantity = entry_quantity.get()
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("UPDATE inventory SET quantity = ? WHERE product_name = ?", (quantity, product_name))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Product updated successfully!")
    clear_entries()
    view_inventory()

# Delete a product from the inventory
def delete_product():
    product_name = entry_product_name.get()
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE product_name = ?", (product_name,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Product deleted successfully!")
    clear_entries()
    view_inventory()

# Search for a product by name
def search_product():
    product_name = entry_product_name.get()
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE product_name = ?", (product_name,))
    rows = c.fetchall()
    conn.close()
    if rows:
        messagebox.showinfo("Product Found", f"Product: {rows[0][1]}, Quantity: {rows[0][2]}, Location: {rows[0][3]}")
    else:
        messagebox.showinfo("Product Not Found", "No product found with the given name.")

# Track a delivery
def track_delivery():
    product_name = entry_product_name.get()
    quantity = entry_quantity.get()
    date = entry_date.get()
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("INSERT INTO deliveries (product_name, quantity, date) VALUES (?, ?, ?)",
              (product_name, quantity, date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Delivery tracked successfully!")
    clear_entries()
    view_deliveries()

# Track a shipment
def track_shipment():
    product_name = entry_product_name.get()
    quantity = entry_quantity.get()
    date = entry_date.get()
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("INSERT INTO shipments (product_name, quantity, date) VALUES (?, ?, ?)",
              (product_name, quantity, date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Shipment tracked successfully!")
    clear_entries()
    view_shipments()

# Generate a report on stock levels
def generate_report():
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    conn.close()
    report = "Stock Levels Report:\n"
    for row in rows:
        report += f"ID: {row[0]}, Product: {row[1]}, Quantity: {row[2]}, Location: {row[3]}\n"
    messagebox.showinfo("Report", report)

# View inventory in a table
def view_inventory():
    for i in tree_inventory.get_children():
        tree_inventory.delete(i)
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_inventory.insert("", "end", values=row)

# View deliveries in a table
def view_deliveries():
    for i in tree_deliveries.get_children():
        tree_deliveries.delete(i)
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("SELECT * FROM deliveries")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_deliveries.insert("", "end", values=row)

# View shipments in a table
def view_shipments():
    for i in tree_shipments.get_children():
        tree_shipments.delete(i)
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("SELECT * FROM shipments")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_shipments.insert("", "end", values=row)

# Clear entry fields
def clear_entries():
    entry_product_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_location.delete(0, tk.END)
    entry_date.delete(0, tk.END)

# Create the main application window
root = tk.Tk()
root.title("Warehouse Management System")

# Initialize the database
init_db()

# Create and place widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Product Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_product_name = ttk.Entry(frame)
entry_product_name.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_quantity = ttk.Entry(frame)
entry_quantity.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Location:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_location = ttk.Entry(frame)
entry_location.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=5)
entry_date = ttk.Entry(frame)
entry_date.grid(row=3, column=1, pady=5)

ttk.Button(frame, text="Add Product", command=add_product).grid(row=4, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Update Product", command=update_product).grid(row=5, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Delete Product", command=delete_product).grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Search Product", command=search_product).grid(row=7, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Track Delivery", command=track_delivery).grid(row=8, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Track Shipment", command=track_shipment).grid(row=9, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Generate Report", command=generate_report).grid(row=10, column=0, columnspan=2, pady=5)

# Create treeviews for displaying tables
tree_inventory = ttk.Treeview(frame, columns=("ID", "Product Name", "Quantity", "Location"), show='headings')
tree_inventory.heading("ID", text="ID")
tree_inventory.heading("Product Name", text="Product Name")
tree_inventory.heading("Quantity", text="Quantity")
tree_inventory.heading("Location", text="Location")
tree_inventory.grid(row=11, column=0, columnspan=2, pady=5)

tree_deliveries = ttk.Treeview(frame, columns=("ID", "Product Name", "Quantity", "Date"), show='headings')
tree_deliveries.heading("ID", text="ID")
tree_deliveries.heading("Product Name", text="Product Name")
tree_deliveries.heading("Quantity", text="Quantity")
tree_deliveries.heading("Date", text="Date")
tree_deliveries.grid(row=12, column=0, columnspan=2, pady=5)

tree_shipments = ttk.Treeview(frame, columns=("ID", "Product Name", "Quantity", "Date"), show='headings')
tree_shipments.heading("ID", text="ID")
tree_shipments.heading("Product Name", text="Product Name")
tree_shipments.heading("Quantity", text="Quantity")
tree_shipments.heading("Date", text="Date")
tree_shipments.grid(row=13, column=0, columnspan=2, pady=5)

# View initial data
view_inventory()
view_deliveries()
view_shipments()

# Run the application
root.mainloop()
