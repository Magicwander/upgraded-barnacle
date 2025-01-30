import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, name TEXT, room_number INTEGER, payment REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS rooms
                 (room_number INTEGER PRIMARY KEY, capacity INTEGER, available INTEGER)''')
    conn.commit()
    conn.close()

# Add a new student
def add_student():
    name = entry_name.get()
    room_number = entry_room_number.get()
    payment = entry_payment.get()
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, room_number, payment) VALUES (?, ?, ?)",
              (name, room_number, payment))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student added successfully!")
    clear_entries()
    view_students()

# Update student information
def update_student():
    name = entry_name.get()
    room_number = entry_room_number.get()
    payment = entry_payment.get()
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("UPDATE students SET room_number = ?, payment = ? WHERE name = ?", (room_number, payment, name))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student information updated successfully!")
    clear_entries()
    view_students()

# Delete a student
def delete_student():
    name = entry_name.get()
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully!")
    clear_entries()
    view_students()

# Search for a student by name
def search_student():
    name = entry_name.get()
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE name = ?", (name,))
    rows = c.fetchall()
    conn.close()
    if rows:
        messagebox.showinfo("Student Found", f"Name: {rows[0][1]}, Room Number: {rows[0][2]}, Payment: {rows[0][3]}")
    else:
        messagebox.showinfo("Student Not Found", "No student found with the given name.")

# Allocate a room to a student
def allocate_room():
    room_number = entry_room_number.get()
    capacity = entry_capacity.get()
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("INSERT INTO rooms (room_number, capacity, available) VALUES (?, ?, ?)",
              (room_number, capacity, capacity))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Room allocated successfully!")
    clear_entries()
    view_rooms()

# Update room availability
def update_room():
    room_number = entry_room_number.get()
    available = entry_available.get()
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("UPDATE rooms SET available = ? WHERE room_number = ?", (available, room_number))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Room availability updated successfully!")
    clear_entries()
    view_rooms()

# View students in a table
def view_students():
    for i in tree_students.get_children():
        tree_students.delete(i)
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_students.insert("", "end", values=row)

# View rooms in a table
def view_rooms():
    for i in tree_rooms.get_children():
        tree_rooms.delete(i)
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM rooms")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_rooms.insert("", "end", values=row)

# Clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_room_number.delete(0, tk.END)
    entry_payment.delete(0, tk.END)
    entry_capacity.delete(0, tk.END)
    entry_available.delete(0, tk.END)

# Create the main application window
root = tk.Tk()
root.title("Student Hostel Management System")

# Initialize the database
init_db()

# Create and place widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_name = ttk.Entry(frame)
entry_name.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Room Number:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_room_number = ttk.Entry(frame)
entry_room_number.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Payment:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_payment = ttk.Entry(frame)
entry_payment.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Capacity:").grid(row=3, column=0, sticky=tk.W, pady=5)
entry_capacity = ttk.Entry(frame)
entry_capacity.grid(row=3, column=1, pady=5)

ttk.Label(frame, text="Available:").grid(row=4, column=0, sticky=tk.W, pady=5)
entry_available = ttk.Entry(frame)
entry_available.grid(row=4, column=1, pady=5)

ttk.Button(frame, text="Add Student", command=add_student).grid(row=5, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Update Student", command=update_student).grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Delete Student", command=delete_student).grid(row=7, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Search Student", command=search_student).grid(row=8, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Allocate Room", command=allocate_room).grid(row=9, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Update Room", command=update_room).grid(row=10, column=0, columnspan=2, pady=5)

# Create treeviews for displaying tables
tree_students = ttk.Treeview(frame, columns=("ID", "Name", "Room Number", "Payment"), show='headings')
tree_students.heading("ID", text="ID")
tree_students.heading("Name", text="Name")
tree_students.heading("Room Number", text="Room Number")
tree_students.heading("Payment", text="Payment")
tree_students.grid(row=11, column=0, columnspan=2, pady=5)

tree_rooms = ttk.Treeview(frame, columns=("Room Number", "Capacity", "Available"), show='headings')
tree_rooms.heading("Room Number", text="Room Number")
tree_rooms.heading("Capacity", text="Capacity")
tree_rooms.heading("Available", text="Available")
tree_rooms.grid(row=12, column=0, columnspan=2, pady=5)

# View initial data
view_students()
view_rooms()

# Run the application
root.mainloop()
