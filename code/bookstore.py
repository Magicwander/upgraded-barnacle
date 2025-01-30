import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime
import hashlib

# Database setup
conn = sqlite3.connect('bookstore.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT,
                role TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                genre TEXT,
                price REAL,
                stock INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                quantity INTEGER,
                order_date TEXT,
                status TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(book_id) REFERENCES books(book_id))''')
conn.commit()

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    role = role_entry.get()
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)", (username, hashed_password, email, role))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def login_user():
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = hash_password(password)
    c.execute("SELECT user_id, role FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    if user:
        messagebox.showinfo("Success", "Login successful!")
        return user
    else:
        messagebox.showerror("Error", "Invalid username or password!")
        return None

def add_book():
    title = book_title_entry.get()
    author = book_author_entry.get()
    genre = book_genre_entry.get()
    price = float(book_price_entry.get())
    stock = int(book_stock_entry.get())
    c.execute("INSERT INTO books (title, author, genre, price, stock) VALUES (?, ?, ?, ?, ?)", (title, author, genre, price, stock))
    conn.commit()
    messagebox.showinfo("Success", "Book added successfully!")

def view_books():
    c.execute("SELECT book_id, title, author, genre, price, stock FROM books")
    books = c.fetchall()
    book_info = "Books:\n"
    for book in books:
        book_info += f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Price: {book[4]}, Stock: {book[5]}\n"
    messagebox.showinfo("Books", book_info)

def update_book():
    book_id = int(book_id_entry.get())
    stock = int(book_stock_entry.get())
    c.execute("UPDATE books SET stock = ? WHERE book_id = ?", (stock, book_id))
    conn.commit()
    messagebox.showinfo("Success", "Book stock updated successfully!")

def delete_book():
    book_id = int(book_id_entry.get())
    c.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    conn.commit()
    messagebox.showinfo("Success", "Book deleted successfully!")

def place_order(user_id):
    book_id = int(book_id_entry.get())
    quantity = int(quantity_entry.get())
    c.execute("SELECT stock FROM books WHERE book_id = ?", (book_id,))
    stock = c.fetchone()[0]
    if stock >= quantity:
        c.execute("INSERT INTO orders (user_id, book_id, quantity, order_date, status) VALUES (?, ?, ?, ?, ?)",
                  (user_id, book_id, quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Pending'))
        c.execute("UPDATE books SET stock = stock - ? WHERE book_id = ?", (quantity, book_id))
        conn.commit()
        messagebox.showinfo("Success", "Order placed successfully!")
    else:
        messagebox.showerror("Error", "Insufficient stock!")

def view_order_history(user_id):
    c.execute("SELECT o.order_id, b.title, o.quantity, o.order_date, o.status FROM orders o JOIN books b ON o.book_id = b.book_id WHERE o.user_id = ?", (user_id,))
    orders = c.fetchall()
    order_info = "Your Orders:\n"
    for order in orders:
        order_info += f"Order ID: {order[0]}, Book Title: {order[1]}, Quantity: {order[2]}, Order Date: {order[3]}, Status: {order[4]}\n"
    messagebox.showinfo("Orders", order_info)

def update_order_status():
    order_id = int(order_id_entry.get())
    status = status_entry.get()
    c.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id))
    conn.commit()
    messagebox.showinfo("Success", "Order status updated successfully!")

def admin_panel():
    admin_password = simpledialog.askstring("Admin Panel", "Enter admin password:", show='*')
    if admin_password == "admin123":  # Replace with a secure method to check admin credentials
        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Panel")

        def view_users():
            c.execute("SELECT user_id, username, email, role FROM users")
            users = c.fetchall()
            user_info = "Users:\n"
            for user in users:
                user_info += f"User ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}\n"
            messagebox.showinfo("Users", user_info)

        def delete_user():
            user_id = simpledialog.askinteger("Delete User", "Enter user ID to delete:")
            c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()
            messagebox.showinfo("Success", "User deleted successfully!")

        def generate_report():
            c.execute("SELECT b.book_id, b.title, SUM(o.quantity) FROM books b LEFT JOIN orders o ON b.book_id = o.book_id GROUP BY b.book_id")
            report = c.fetchall()
            report_info = "Sales Report:\n"
            for row in report:
                report_info += f"Book ID: {row[0]}, Book Title: {row[1]}, Total Quantity Sold: {row[2]}\n"
            messagebox.showinfo("Report", report_info)

        view_users_button = tk.Button(admin_window, text="View Users", command=view_users)
        view_users_button.pack()

        delete_user_button = tk.Button(admin_window, text="Delete User", command=delete_user)
        delete_user_button.pack()

        generate_report_button = tk.Button(admin_window, text="Generate Report", command=generate_report)
        generate_report_button.pack()
    else:
        messagebox.showerror("Error", "Invalid admin password!")

# GUI setup
root = tk.Tk()
root.title("Bookstore Management System")

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", foreground="black")
style.configure("TLabel", padding=6, background="#eee", foreground="black")
style.configure("TEntry", padding=6, relief="flat", background="white", foreground="black")

def main_menu(user_info=None):
    for widget in root.winfo_children():
        widget.destroy()

    if user_info:
        user_id, role = user_info
        tk.Label(root, text=f"Welcome, User ID: {user_id} (Role: {role})", font=("Helvetica", 16)).pack(pady=10)

        notebook = ttk.Notebook(root)
        notebook.pack(expand=1, fill="both")

        book_tab = ttk.Frame(notebook)
        order_tab = ttk.Frame(notebook)
        admin_tab = ttk.Frame(notebook)

        notebook.add(book_tab, text="Book Management")
        notebook.add(order_tab, text="Order Management")
        if role == "admin":
            notebook.add(admin_tab, text="Admin Panel")

        # Book Management Tab
        tk.Label(book_tab, text="Add Book", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(book_tab, text="Title").pack()
        global book_title_entry
        book_title_entry = tk.Entry(book_tab)
        book_title_entry.pack()
        tk.Label(book_tab, text="Author").pack()
        global book_author_entry
        book_author_entry = tk.Entry(book_tab)
        book_author_entry.pack()
        tk.Label(book_tab, text="Genre").pack()
        global book_genre_entry
        book_genre_entry = tk.Entry(book_tab)
        book_genre_entry.pack()
        tk.Label(book_tab, text="Price").pack()
        global book_price_entry
        book_price_entry = tk.Entry(book_tab)
        book_price_entry.pack()
        tk.Label(book_tab, text="Stock").pack()
        global book_stock_entry
        book_stock_entry = tk.Entry(book_tab)
        book_stock_entry.pack()
        add_book_button = tk.Button(book_tab, text="Add Book", command=add_book)
        add_book_button.pack(pady=10)

        view_books_button = tk.Button(book_tab, text="View Books", command=view_books)
        view_books_button.pack(pady=10)

        tk.Label(book_tab, text="Update Book Stock", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(book_tab, text="Book ID").pack()
        global update_book_id_entry
        update_book_id_entry = tk.Entry(book_tab)
        update_book_id_entry.pack()
        tk.Label(book_tab, text="Stock").pack()
        global update_book_stock_entry
        update_book_stock_entry = tk.Entry(book_tab)
        update_book_stock_entry.pack()
        update_book_button = tk.Button(book_tab, text="Update Book Stock", command=update_book)
        update_book_button.pack(pady=10)

        tk.Label(book_tab, text="Delete Book", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(book_tab, text="Book ID").pack()
        global delete_book_id_entry
        delete_book_id_entry = tk.Entry(book_tab)
        delete_book_id_entry.pack()
        delete_book_button = tk.Button(book_tab, text="Delete Book", command=delete_book)
        delete_book_button.pack(pady=10)

        # Order Management Tab
        tk.Label(order_tab, text="Place Order", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(order_tab, text="Book ID").pack()
        global order_book_id_entry
        order_book_id_entry = tk.Entry(order_tab)
        order_book_id_entry.pack()
        tk.Label(order_tab, text="Quantity").pack()
        global order_quantity_entry
        order_quantity_entry = tk.Entry(order_tab)
        order_quantity_entry.pack()
        place_order_button = tk.Button(order_tab, text="Place Order", command=lambda: place_order(user_id))
        place_order_button.pack(pady=10)

        view_order_history_button = tk.Button(order_tab, text="View Order History", command=lambda: view_order_history(user_id))
        view_order_history_button.pack(pady=10)

        tk.Label(order_tab, text="Update Order Status", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(order_tab, text="Order ID").pack()
        global order_id_entry
        order_id_entry = tk.Entry(order_tab)
        order_id_entry.pack()
        tk.Label(order_tab, text="Status").pack()
        global status_entry
        status_entry = tk.Entry(order_tab)
        status_entry.pack()
        update_order_status_button = tk.Button(order_tab, text="Update Order Status", command=update_order_status)
        update_order_status_button.pack(pady=10)

        # Admin Panel Tab
        if role == "admin":
            admin_button = tk.Button(admin_tab, text="Admin Panel", command=admin_panel)
            admin_button.pack(pady=10)

        logout_button = tk.Button(root, text="Logout", command=main_menu)
        logout_button.pack(pady=10)
    else:
        tk.Label(root, text="Bookstore Management System", font=("Helvetica", 16)).pack(pady=10)

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

        tk.Label(root, text="Role").pack()
        global role_entry
        role_entry = tk.Entry(root)
        role_entry.pack()

        register_button = tk.Button(root, text="Register", command=register_user)
        register_button.pack(pady=10)

        login_button = tk.Button(root, text="Login", command=lambda: main_menu(login_user()))
        login_button.pack(pady=10)

main_menu()

root.mainloop()

# Close the database connection
conn.close()
