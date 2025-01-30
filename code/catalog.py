import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('product_catalog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL,
                    quantity INTEGER)''')
    conn.commit()
    conn.close()

# Add a product
def add_product(name, description, price, quantity):
    conn = sqlite3.connect('product_catalog.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)",
              (name, description, price, quantity))
    conn.commit()
    conn.close()

# Update a product
def update_product(product_id, name, description, price, quantity):
    conn = sqlite3.connect('product_catalog.db')
    c = conn.cursor()
    c.execute("UPDATE products SET name = ?, description = ?, price = ?, quantity = ? WHERE id = ?",
              (name, description, price, quantity, product_id))
    conn.commit()
    conn.close()

# Delete a product
def delete_product(product_id):
    conn = sqlite3.connect('product_catalog.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# Get all products
def get_all_products():
    conn = sqlite3.connect('product_catalog.db')
    c = conn.cursor()
    c.execute("SELECT id, name, description, price, quantity FROM products")
    products = c.fetchall()
    conn.close()
    return products

# Tkinter GUI
class ProductCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Catalog System")

        self.product_id = tk.IntVar()
        self.product_name = tk.StringVar()
        self.product_description = tk.StringVar()
        self.product_price = tk.DoubleVar()
        self.product_quantity = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill="both")

        # Add Product Tab
        add_product_tab = ttk.Frame(notebook)
        notebook.add(add_product_tab, text='Add Product')

        tk.Label(add_product_tab, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(add_product_tab, textvariable=self.product_name).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(add_product_tab, text="Description:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(add_product_tab, textvariable=self.product_description).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(add_product_tab, text="Price:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(add_product_tab, textvariable=self.product_price).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(add_product_tab, text="Quantity:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(add_product_tab, textvariable=self.product_quantity).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(add_product_tab, text="Add Product", command=self.add_product).grid(row=4, column=1, padx=10, pady=10)

        # Update Product Tab
        update_product_tab = ttk.Frame(notebook)
        notebook.add(update_product_tab, text='Update Product')

        tk.Label(update_product_tab, text="Product ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(update_product_tab, textvariable=self.product_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(update_product_tab, text="Name:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(update_product_tab, textvariable=self.product_name).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(update_product_tab, text="Description:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(update_product_tab, textvariable=self.product_description).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(update_product_tab, text="Price:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(update_product_tab, textvariable=self.product_price).grid(row=3, column=1, padx=10, pady=10)
        tk.Label(update_product_tab, text="Quantity:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(update_product_tab, textvariable=self.product_quantity).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(update_product_tab, text="Update Product", command=self.update_product).grid(row=5, column=1, padx=10, pady=10)

        # Delete Product Tab
        delete_product_tab = ttk.Frame(notebook)
        notebook.add(delete_product_tab, text='Delete Product')

        tk.Label(delete_product_tab, text="Product ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(delete_product_tab, textvariable=self.product_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(delete_product_tab, text="Delete Product", command=self.delete_product).grid(row=1, column=1, padx=10, pady=10)

        # View All Products Tab
        view_products_tab = ttk.Frame(notebook)
        notebook.add(view_products_tab, text='View All Products')

        self.products_list = tk.Listbox(view_products_tab, width=100)
        self.products_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_products_tab, text="Refresh", command=self.refresh_products).grid(row=1, column=0, padx=10, pady=10)

        self.refresh_products()

    def add_product(self):
        name = self.product_name.get()
        description = self.product_description.get()
        price = self.product_price.get()
        quantity = self.product_quantity.get()
        if name and description and price and quantity:
            add_product(name, description, price, quantity)
            messagebox.showinfo("Success", "Product added successfully.")
            self.refresh_products()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def update_product(self):
        product_id = self.product_id.get()
        name = self.product_name.get()
        description = self.product_description.get()
        price = self.product_price.get()
        quantity = self.product_quantity.get()
        if product_id and name and description and price and quantity:
            update_product(product_id, name, description, price, quantity)
            messagebox.showinfo("Success", "Product updated successfully.")
            self.refresh_products()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def delete_product(self):
        product_id = self.product_id.get()
        if product_id:
            delete_product(product_id)
            messagebox.showinfo("Success", "Product deleted successfully.")
            self.refresh_products()
        else:
            messagebox.showwarning("Input error", "Please enter a product ID.")

    def refresh_products(self):
        self.products_list.delete(0, tk.END)
        products = get_all_products()
        for product in products:
            self.products_list.insert(tk.END, f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Quantity: {product[4]}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = ProductCatalogApp(root)
    root.mainloop()
