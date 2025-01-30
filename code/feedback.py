import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('feedback.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_name TEXT NOT NULL,
                feedback_text TEXT NOT NULL,
                submission_date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id))''')

conn.commit()

# GUI setup
root = tk.Tk()
root.title("Product Feedback Management System")
root.geometry("800x600")

# Styles
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", foreground="#000")
style.configure("TLabel", padding=6, background="#fff", foreground="#000")
style.configure("TFrame", padding=6, background="#fff")

# Global variables
current_user = None
current_role = None

# Functions
def register_user():
    username = register_username_entry.get()
    password = register_password_entry.get()
    role = register_role_var.get()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    messagebox.showinfo("Success", "User registered successfully")
    clear_entries()

def login_user():
    global current_user, current_role
    username = login_username_entry.get()
    password = login_password_entry.get()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    if user:
        current_user = user[0]
        current_role = user[3]
        messagebox.showinfo("Success", "Login successful")
        show_main_menu()
    else:
        messagebox.showerror("Error", "Invalid username or password")
    clear_entries()

def submit_feedback():
    product_name = feedback_product_entry.get()
    feedback_text = feedback_text_entry.get()
    submission_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO feedback (user_id, product_name, feedback_text, submission_date) VALUES (?, ?, ?, ?)",
              (current_user, product_name, feedback_text, submission_date))
    conn.commit()
    messagebox.showinfo("Success", "Feedback submitted successfully")
    clear_entries()

def view_feedback():
    feedback_text.delete(1.0, tk.END)
    c.execute("SELECT * FROM feedback")
    feedback_data = c.fetchall()
    for row in feedback_data:
        feedback_text.insert(tk.END, f"ID: {row[0]}, User ID: {row[1]}, Product: {row[2]}, Feedback: {row[3]}, Date: {row[4]}\n")

def update_feedback():
    feedback_id = int(update_feedback_id_entry.get())
    feedback_text = update_feedback_text_entry.get()
    c.execute("UPDATE feedback SET feedback_text = ? WHERE feedback_id = ?", (feedback_text, feedback_id))
    conn.commit()
    messagebox.showinfo("Success", "Feedback updated successfully")
    clear_entries()

def delete_feedback():
    feedback_id = int(delete_feedback_id_entry.get())
    c.execute("DELETE FROM feedback WHERE feedback_id = ?", (feedback_id,))
    conn.commit()
    messagebox.showinfo("Success", "Feedback deleted successfully")
    clear_entries()

def generate_report():
    report_text.delete(1.0, tk.END)
    c.execute("SELECT product_name, COUNT(*) FROM feedback GROUP BY product_name")
    report_data = c.fetchall()
    for row in report_data:
        report_text.insert(tk.END, f"Product: {row[0]}, Feedback Count: {row[1]}\n")

def clear_entries():
    register_username_entry.delete(0, tk.END)
    register_password_entry.delete(0, tk.END)
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)
    feedback_product_entry.delete(0, tk.END)
    feedback_text_entry.delete(0, tk.END)
    update_feedback_id_entry.delete(0, tk.END)
    update_feedback_text_entry.delete(0, tk.END)
    delete_feedback_id_entry.delete(0, tk.END)

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    if current_role == "admin":
        admin_menu()
    else:
        user_menu()

def user_menu():
    ttk.Label(root, text="Submit Feedback").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(root, text="Product Name").grid(row=1, column=0, padx=5, pady=5)
    global feedback_product_entry
    feedback_product_entry = ttk.Entry(root)
    feedback_product_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(root, text="Feedback").grid(row=2, column=0, padx=5, pady=5)
    global feedback_text_entry
    feedback_text_entry = ttk.Entry(root)
    feedback_text_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(root, text="Submit Feedback", command=submit_feedback).grid(row=3, column=0, columnspan=2, pady=5)

def admin_menu():
    ttk.Label(root, text="Admin Menu").grid(row=0, column=0, padx=10, pady=10)

    ttk.Button(root, text="View Feedback", command=view_feedback).grid(row=1, column=0, pady=5)
    ttk.Button(root, text="Update Feedback", command=lambda: show_update_feedback_menu()).grid(row=2, column=0, pady=5)
    ttk.Button(root, text="Delete Feedback", command=lambda: show_delete_feedback_menu()).grid(row=3, column=0, pady=5)
    ttk.Button(root, text="Generate Report", command=generate_report).grid(row=4, column=0, pady=5)

    global report_text
    report_text = tk.Text(root, height=10, width=50)
    report_text.grid(row=5, column=0, columnspan=2, pady=5)

def show_update_feedback_menu():
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="Update Feedback").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(root, text="Feedback ID").grid(row=1, column=0, padx=5, pady=5)
    global update_feedback_id_entry
    update_feedback_id_entry = ttk.Entry(root)
    update_feedback_id_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(root, text="New Feedback").grid(row=2, column=0, padx=5, pady=5)
    global update_feedback_text_entry
    update_feedback_text_entry = ttk.Entry(root)
    update_feedback_text_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(root, text="Update Feedback", command=update_feedback).grid(row=3, column=0, columnspan=2, pady=5)
    ttk.Button(root, text="Back to Admin Menu", command=admin_menu).grid(row=4, column=0, columnspan=2, pady=5)

def show_delete_feedback_menu():
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="Delete Feedback").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(root, text="Feedback ID").grid(row=1, column=0, padx=5, pady=5)
    global delete_feedback_id_entry
    delete_feedback_id_entry = ttk.Entry(root)
    delete_feedback_id_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(root, text="Delete Feedback", command=delete_feedback).grid(row=2, column=0, columnspan=2, pady=5)
    ttk.Button(root, text="Back to Admin Menu", command=admin_menu).grid(row=3, column=0, columnspan=2, pady=5)

# Initial Login/Register Frame
ttk.Label(root, text="Register").grid(row=0, column=0, padx=10, pady=10)
ttk.Label(root, text="Username").grid(row=1, column=0, padx=5, pady=5)
register_username_entry = ttk.Entry(root)
register_username_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Password").grid(row=2, column=0, padx=5, pady=5)
register_password_entry = ttk.Entry(root, show="*")
register_password_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(root, text="Role").grid(row=3, column=0, padx=5, pady=5)
register_role_var = tk.StringVar(value="user")
ttk.OptionMenu(root, register_role_var, "user", "admin").grid(row=3, column=1, padx=5, pady=5)

ttk.Button(root, text="Register", command=register_user).grid(row=4, column=0, columnspan=2, pady=5)

ttk.Label(root, text="Login").grid(row=5, column=0, padx=10, pady=10)
ttk.Label(root, text="Username").grid(row=6, column=0, padx=5, pady=5)
login_username_entry = ttk.Entry(root)
login_username_entry.grid(row=6, column=1, padx=5, pady=5)

ttk.Label(root, text="Password").grid(row=7, column=0, padx=5, pady=5)
login_password_entry = ttk.Entry(root, show="*")
login_password_entry.grid(row=7, column=1, padx=5, pady=5)

ttk.Button(root, text="Login", command=login_user).grid(row=8, column=0, columnspan=2, pady=5)

root.mainloop()

# Close the database connection
conn.close()
