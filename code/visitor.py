import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('visitor_management.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS visitors (
                visitor_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                purpose TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS visits (
                visit_id INTEGER PRIMARY KEY,
                visitor_id INTEGER,
                check_in_time TEXT,
                check_out_time TEXT,
                FOREIGN KEY(visitor_id) REFERENCES visitors(visitor_id))''')

conn.commit()

# GUI setup
root = tk.Tk()
root.title("Visitor Management System")
root.geometry("800x600")

# Styles
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", foreground="#000")
style.configure("TLabel", padding=6, background="#fff", foreground="#000")
style.configure("TFrame", padding=6, background="#fff")

# Functions
def register_visitor():
    name = visitor_name_entry.get()
    contact = visitor_contact_entry.get()
    purpose = visitor_purpose_entry.get()
    c.execute("INSERT INTO visitors (name, contact, purpose) VALUES (?, ?, ?)", (name, contact, purpose))
    conn.commit()
    messagebox.showinfo("Success", "Visitor registered successfully")
    clear_entries()

def check_in_visitor():
    visitor_id = int(check_in_visitor_id_entry.get())
    check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO visits (visitor_id, check_in_time) VALUES (?, ?)", (visitor_id, check_in_time))
    conn.commit()
    messagebox.showinfo("Success", "Visitor checked in successfully")
    clear_entries()

def check_out_visitor():
    visit_id = int(check_out_visit_id_entry.get())
    check_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("UPDATE visits SET check_out_time = ? WHERE visit_id = ?", (check_out_time, visit_id))
    conn.commit()
    messagebox.showinfo("Success", "Visitor checked out successfully")
    clear_entries()

def view_current_visitors():
    current_visitors_text.delete(1.0, tk.END)
    c.execute("SELECT visitors.name, visits.check_in_time FROM visitors JOIN visits ON visitors.visitor_id = visits.visitor_id WHERE visits.check_out_time IS NULL")
    current_visitors = c.fetchall()
    for visitor in current_visitors:
        current_visitors_text.insert(tk.END, f"Name: {visitor[0]}, Check-In Time: {visitor[1]}\n")

def generate_report():
    report_text.delete(1.0, tk.END)
    c.execute("SELECT visitors.name, visits.check_in_time, visits.check_out_time FROM visitors JOIN visits ON visitors.visitor_id = visits.visitor_id")
    report_data = c.fetchall()
    for row in report_data:
        report_text.insert(tk.END, f"Name: {row[0]}, Check-In Time: {row[1]}, Check-Out Time: {row[2]}\n")

def clear_entries():
    visitor_name_entry.delete(0, tk.END)
    visitor_contact_entry.delete(0, tk.END)
    visitor_purpose_entry.delete(0, tk.END)
    check_in_visitor_id_entry.delete(0, tk.END)
    check_out_visit_id_entry.delete(0, tk.END)

# Frames
register_frame = ttk.LabelFrame(root, text="Register Visitor")
register_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

check_in_frame = ttk.LabelFrame(root, text="Check-In Visitor")
check_in_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

check_out_frame = ttk.LabelFrame(root, text="Check-Out Visitor")
check_out_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

current_visitors_frame = ttk.LabelFrame(root, text="Current Visitors")
current_visitors_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

report_frame = ttk.LabelFrame(root, text="Generate Report")
report_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

# Register Frame
ttk.Label(register_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
visitor_name_entry = ttk.Entry(register_frame)
visitor_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(register_frame, text="Contact").grid(row=1, column=0, padx=5, pady=5)
visitor_contact_entry = ttk.Entry(register_frame)
visitor_contact_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(register_frame, text="Purpose").grid(row=2, column=0, padx=5, pady=5)
visitor_purpose_entry = ttk.Entry(register_frame)
visitor_purpose_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(register_frame, text="Register Visitor", command=register_visitor).grid(row=3, column=0, columnspan=2, pady=5)

# Check-In Frame
ttk.Label(check_in_frame, text="Visitor ID").grid(row=0, column=0, padx=5, pady=5)
check_in_visitor_id_entry = ttk.Entry(check_in_frame)
check_in_visitor_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Button(check_in_frame, text="Check-In Visitor", command=check_in_visitor).grid(row=1, column=0, columnspan=2, pady=5)

# Check-Out Frame
ttk.Label(check_out_frame, text="Visit ID").grid(row=0, column=0, padx=5, pady=5)
check_out_visit_id_entry = ttk.Entry(check_out_frame)
check_out_visit_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Button(check_out_frame, text="Check-Out Visitor", command=check_out_visitor).grid(row=1, column=0, columnspan=2, pady=5)

# Current Visitors Frame
ttk.Button(current_visitors_frame, text="View Current Visitors", command=view_current_visitors).grid(row=0, column=0, pady=5)

current_visitors_text = tk.Text(current_visitors_frame, height=10, width=50)
current_visitors_text.grid(row=1, column=0, pady=5)

# Report Frame
ttk.Button(report_frame, text="Generate Report", command=generate_report).grid(row=0, column=0, pady=5)

report_text = tk.Text(report_frame, height=10, width=50)
report_text.grid(row=1, column=0, pady=5)

root.mainloop()

# Close the database connection
conn.close()
