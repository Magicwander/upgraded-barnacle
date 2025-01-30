import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('delivery_tracking.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deliveries (
            delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_name TEXT,
            delivery_date TEXT,
            status TEXT,
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a product
def add_product():
    name = product_name_entry.get()
    description = product_description_entry.get()
    conn = sqlite3.connect('delivery_tracking.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Product added successfully!")
    clear_entries()

# Function to track a delivery
def track_delivery():
    product_id = track_product_id_entry.get()
    customer_name = track_customer_name_entry.get()
    delivery_date = track_delivery_date_entry.get()
    status = "In Transit"
    conn = sqlite3.connect('delivery_tracking.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO deliveries (product_id, customer_name, delivery_date, status) VALUES (?, ?, ?, ?)',
                   (product_id, customer_name, delivery_date, status))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Delivery tracked successfully!")
    clear_entries()

# Function to update delivery status
def update_delivery_status():
    delivery_id = update_delivery_id_entry.get()
    status = update_status_entry.get()
    conn = sqlite3.connect('delivery_tracking.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE deliveries SET status=? WHERE delivery_id=?', (status, delivery_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Delivery status updated successfully!")
    clear_entries()

# Function to view delivery reports
def view_delivery_reports():
    conn = sqlite3.connect('delivery_tracking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM deliveries')
    deliveries = cursor.fetchall()
    conn.close()
    report = ""
    for delivery in deliveries:
        report += f"Delivery ID: {delivery[0]}, Product ID: {delivery[1]}, Customer: {delivery[2]}, Date: {delivery[3]}, Status: {delivery[4]}\n"
    messagebox.showinfo("Delivery Reports", report)

# Function to clear entries
def clear_entries():
    product_name_entry.delete(0, tk.END)
    product_description_entry.delete(0, tk.END)
    track_product_id_entry.delete(0, tk.END)
    track_customer_name_entry.delete(0, tk.END)
    track_delivery_date_entry.delete(0, tk.END)
    update_delivery_id_entry.delete(0, tk.END)
    update_status_entry.delete(0, tk.END)

# Initialize the database
init_db()

# Create the main window
root = tk.Tk()
root.title("Product Delivery Tracking System")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create frames for each tab
add_product_frame = ttk.Frame(notebook)
track_delivery_frame = ttk.Frame(notebook)
update_status_frame = ttk.Frame(notebook)
view_reports_frame = ttk.Frame(notebook)

notebook.add(add_product_frame, text='Add Product')
notebook.add(track_delivery_frame, text='Track Delivery')
notebook.add(update_status_frame, text='Update Status')
notebook.add(view_reports_frame, text='View Reports')

# Add Product Frame
tk.Label(add_product_frame, text="Product Name:").grid(row=0, column=0, padx=10, pady=10)
product_name_entry = tk.Entry(add_product_frame)
product_name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(add_product_frame, text="Description:").grid(row=1, column=0, padx=10, pady=10)
product_description_entry = tk.Entry(add_product_frame)
product_description_entry.grid(row=1, column=1, padx=10, pady=10)

add_product_button = tk.Button(add_product_frame, text="Add Product", command=add_product)
add_product_button.grid(row=2, column=0, columnspan=2, pady=10)

# Track Delivery Frame
tk.Label(track_delivery_frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=10)
track_product_id_entry = tk.Entry(track_delivery_frame)
track_product_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(track_delivery_frame, text="Customer Name:").grid(row=1, column=0, padx=10, pady=10)
track_customer_name_entry = tk.Entry(track_delivery_frame)
track_customer_name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(track_delivery_frame, text="Delivery Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
track_delivery_date_entry = tk.Entry(track_delivery_frame)
track_delivery_date_entry.grid(row=2, column=1, padx=10, pady=10)

track_delivery_button = tk.Button(track_delivery_frame, text="Track Delivery", command=track_delivery)
track_delivery_button.grid(row=3, column=0, columnspan=2, pady=10)

# Update Status Frame
tk.Label(update_status_frame, text="Delivery ID:").grid(row=0, column=0, padx=10, pady=10)
update_delivery_id_entry = tk.Entry(update_status_frame)
update_delivery_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(update_status_frame, text="Status:").grid(row=1, column=0, padx=10, pady=10)
update_status_entry = tk.Entry(update_status_frame)
update_status_entry.grid(row=1, column=1, padx=10, pady=10)

update_status_button = tk.Button(update_status_frame, text="Update Status", command=update_delivery_status)
update_status_button.grid(row=2, column=0, columnspan=2, pady=10)

# View Reports Frame
view_reports_button = tk.Button(view_reports_frame, text="View Delivery Reports", command=view_delivery_reports)
view_reports_button.grid(row=0, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
