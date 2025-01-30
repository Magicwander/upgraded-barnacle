import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime
import hashlib

# Database setup
conn = sqlite3.connect('online_shop.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                price REAL,
                stock INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS cart (
                cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(product_id) REFERENCES products(product_id))''')
c.execute('''CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_amount REAL,
                order_date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id))''')
c.execute('''CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY(order_id) REFERENCES orders(order_id),
                FOREIGN KEY(product_id) REFERENCES products(product_id))''')
conn.commit()

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def login_user():
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = hash_password(password)
    c.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    if user:
        messagebox.showinfo("Success", "Login successful!")
        return user[0]
    else:
        messagebox.showerror("Error", "Invalid username or password!")
        return None

def add_product():
    name = product_name_entry.get()
    description = product_description_entry.get()
    price = float(product_price_entry.get())
    stock = int(product_stock_entry.get())
    c.execute("INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)", (name, description, price, stock))
    conn.commit()
    messagebox.showinfo("Success", "Product added successfully!")

def view_products():
    c.execute("SELECT product_id, name, description, price, stock FROM products")
    products = c.fetchall()
    product_info = "Products:\n"
    for product in products:
        product_info += f"Product ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Stock: {product[4]}\n"
    messagebox.showinfo("Products", product_info)

def delete_product():
    product_id = int(product_id_entry.get())
    c.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    conn.commit()
    messagebox.showinfo("Success", "Product deleted successfully!")

def add_to_cart(user_id):
    product_id = int(product_id_entry.get())
    quantity = int(quantity_entry.get())
    c.execute("SELECT stock FROM products WHERE product_id = ?", (product_id,))
    stock = c.fetchone()[0]
    if stock >= quantity:
        c.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, quantity))
        c.execute("UPDATE products SET stock = stock - ? WHERE product_id = ?", (quantity, product_id))
        conn.commit()
        messagebox.showinfo("Success", "Item added to cart successfully!")
    else:
        messagebox.showerror("Error", "Insufficient stock!")

def view_cart(user_id):
    c.execute("SELECT c.product_id, p.name, p.price, c.quantity FROM cart c JOIN products p ON c.product_id = p.product_id WHERE c.user_id = ?", (user_id,))
    cart_items = c.fetchall()
    cart_info = "Your Cart:\n"
    total_amount = 0
    for item in cart_items:
        cart_info += f"Product ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Quantity: {item[3]}\n"
        total_amount += item[2] * item[3]
    cart_info += f"Total Amount: {total_amount}"
    messagebox.showinfo("Cart", cart_info)

def update_cart(user_id):
    product_id = int(product_id_entry.get())
    quantity = int(quantity_entry.get())
    c.execute("UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?", (quantity, user_id, product_id))
    conn.commit()
    messagebox.showinfo("Success", "Cart updated successfully!")

def place_order(user_id):
    c.execute("SELECT c.product_id, p.price, c.quantity FROM cart c JOIN products p ON c.product_id = p.product_id WHERE c.user_id = ?", (user_id,))
    cart_items = c.fetchall()
    total_amount = 0
    for item in cart_items:
        total_amount += item[1] * item[2]
    c.execute("INSERT INTO orders (user_id, total_amount, order_date) VALUES (?, ?, ?)", (user_id, total_amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    order_id = c.lastrowid
    for item in cart_items:
        c.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", (order_id, item[0], item[2], item[1]))
    c.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    messagebox.showinfo("Success", "Order placed successfully!")

def view_order_history(user_id):
    c.execute("SELECT o.order_id, o.total_amount, o.order_date FROM orders o WHERE o.user_id = ?", (user_id,))
    orders = c.fetchall()
    order_info = "Your Orders:\n"
    for order in orders:
        order_info += f"Order ID: {order[0]}, Total Amount: {order[1]}, Order Date: {order[2]}\n"
    messagebox.showinfo("Orders", order_info)

# GUI setup
root = tk.Tk()
root.title("Online Shopping Cart System")

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", foreground="black")
style.configure("TLabel", padding=6, background="#eee", foreground="black")
style.configure("TEntry", padding=6, relief="flat", background="white", foreground="black")

def main_menu(user_id=None):
    for widget in root.winfo_children():
        widget.destroy()

    if user_id:
        tk.Label(root, text=f"Welcome, User ID: {user_id}", font=("Helvetica", 16)).pack(pady=10)

        notebook = ttk.Notebook(root)
        notebook.pack(expand=1, fill="both")

        product_tab = ttk.Frame(notebook)
        cart_tab = ttk.Frame(notebook)
        order_tab = ttk.Frame(notebook)

        notebook.add(product_tab, text="Product Management")
        notebook.add(cart_tab, text="Shopping Cart")
        notebook.add(order_tab, text="Order Management")

        # Product Management Tab
        tk.Label(product_tab, text="Add Product", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(product_tab, text="Product Name").pack()
        global product_name_entry
        product_name_entry = tk.Entry(product_tab)
        product_name_entry.pack()
        tk.Label(product_tab, text="Description").pack()
        global product_description_entry
        product_description_entry = tk.Entry(product_tab)
        product_description_entry.pack()
        tk.Label(product_tab, text="Price").pack()
        global product_price_entry
        product_price_entry = tk.Entry(product_tab)
        product_price_entry.pack()
        tk.Label(product_tab, text="Stock").pack()
        global product_stock_entry
        product_stock_entry = tk.Entry(product_tab)
        product_stock_entry.pack()
        add_product_button = tk.Button(product_tab, text="Add Product", command=add_product)
        add_product_button.pack(pady=10)

        view_products_button = tk.Button(product_tab, text="View Products", command=view_products)
        view_products_button.pack(pady=10)

        tk.Label(product_tab, text="Delete Product", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(product_tab, text="Product ID").pack()
        global product_id_entry
        product_id_entry = tk.Entry(product_tab)
        product_id_entry.pack()
        delete_product_button = tk.Button(product_tab, text="Delete Product", command=delete_product)
        delete_product_button.pack(pady=10)

        # Shopping Cart Tab
        tk.Label(cart_tab, text="Add to Cart", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(cart_tab, text="Product ID").pack()
        global cart_product_id_entry
        cart_product_id_entry = tk.Entry(cart_tab)
        cart_product_id_entry.pack()
        tk.Label(cart_tab, text="Quantity").pack()
        global quantity_entry
        quantity_entry = tk.Entry(cart_tab)
        quantity_entry.pack()
        add_to_cart_button = tk.Button(cart_tab, text="Add to Cart", command=lambda: add_to_cart(user_id))
        add_to_cart_button.pack(pady=10)

        view_cart_button = tk.Button(cart_tab, text="View Cart", command=lambda: view_cart(user_id))
        view_cart_button.pack(pady=10)

        tk.Label(cart_tab, text="Update Cart", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(cart_tab, text="Product ID").pack()
        global update_product_id_entry
        update_product_id_entry = tk.Entry(cart_tab)
        update_product_id_entry.pack()
        tk.Label(cart_tab, text="Quantity").pack()
        global update_quantity_entry
        update_quantity_entry = tk.Entry(cart_tab)
        update_quantity_entry.pack()
        update_cart_button = tk.Button(cart_tab, text="Update Cart", command=lambda: update_cart(user_id))
        update_cart_button.pack(pady=10)

        # Order Management Tab
        place_order_button = tk.Button(order_tab, text="Place Order", command=lambda: place_order(user_id))
        place_order_button.pack(pady=10)

        view_order_history_button = tk.Button(order_tab, text="View Order History", command=lambda: view_order_history(user_id))
        view_order_history_button.pack(pady=10)

        logout_button = tk.Button(root, text="Logout", command=main_menu)
        logout_button.pack(pady=10)
    else:
        tk.Label(root, text="Online Shopping Cart System", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(root, text="Username").pack()
        global username_entry
        username_entry = tk.Entry(root)
        username_entry.pack()

        tk.Label(root, text="Password").pack()
        global password_entry
        password_entry = tk.Entry(root, show='*')
        password_entry.pack()

        tk.Label(root, text="Email").pack()
        global email_entry
        email_entry = tk.Entry(root)
        email_entry.pack()

        register_button = tk.Button(root, text="Register", command=register_user)
        register_button.pack(pady=10)

        login_button = tk.Button(root, text="Login", command=lambda: main_menu(login_user()))
        login_button.pack(pady=10)

main_menu()

root.mainloop()

# Close the database connection
conn.close()
