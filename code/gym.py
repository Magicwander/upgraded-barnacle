import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            membership_status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            date TEXT,
            FOREIGN KEY (member_id) REFERENCES members (member_id)
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a member
def add_member():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    membership_status = "Active"
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO members (name, age, gender, membership_status) VALUES (?, ?, ?, ?)',
                   (name, age, gender, membership_status))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Member added successfully!")
    clear_entries()

# Function to update a member
def update_member():
    member_id = update_member_id_entry.get()
    name = update_name_entry.get()
    age = update_age_entry.get()
    gender = update_gender_entry.get()
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET name=?, age=?, gender=? WHERE member_id=?', (name, age, gender, member_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Member updated successfully!")
    clear_entries()

# Function to view all members
def view_members():
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()
    conn.close()
    member_list = ""
    for member in members:
        member_list += f"ID: {member[0]}, Name: {member[1]}, Age: {member[2]}, Gender: {member[3]}, Status: {member[4]}\n"
    messagebox.showinfo("Members", member_list)

# Function to track attendance
def track_attendance():
    member_id = attendance_member_id_entry.get()
    date = attendance_date_entry.get()
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO attendance (member_id, date) VALUES (?, ?)', (member_id, date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Attendance tracked successfully!")
    clear_entries()

# Function to update membership status
def update_membership_status():
    member_id = status_member_id_entry.get()
    status = status_entry.get()
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET membership_status=? WHERE member_id=?', (status, member_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Membership status updated successfully!")
    clear_entries()

# Function to clear entries
def clear_entries():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    update_member_id_entry.delete(0, tk.END)
    update_name_entry.delete(0, tk.END)
    update_age_entry.delete(0, tk.END)
    update_gender_entry.delete(0, tk.END)
    attendance_member_id_entry.delete(0, tk.END)
    attendance_date_entry.delete(0, tk.END)
    status_member_id_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)

# Initialize the database
init_db()

# Create the main window
root = tk.Tk()
root.title("Gym Membership Management System")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create frames for each tab
add_member_frame = ttk.Frame(notebook)
update_member_frame = ttk.Frame(notebook)
view_members_frame = ttk.Frame(notebook)
track_attendance_frame = ttk.Frame(notebook)
update_status_frame = ttk.Frame(notebook)

notebook.add(add_member_frame, text='Add Member')
notebook.add(update_member_frame, text='Update Member')
notebook.add(view_members_frame, text='View Members')
notebook.add(track_attendance_frame, text='Track Attendance')
notebook.add(update_status_frame, text='Update Status')

# Add Member Frame
tk.Label(add_member_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(add_member_frame)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(add_member_frame, text="Age:").grid(row=1, column=0, padx=10, pady=10)
age_entry = tk.Entry(add_member_frame)
age_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(add_member_frame, text="Gender:").grid(row=2, column=0, padx=10, pady=10)
gender_entry = tk.Entry(add_member_frame)
gender_entry.grid(row=2, column=1, padx=10, pady=10)

add_member_button = tk.Button(add_member_frame, text="Add Member", command=add_member)
add_member_button.grid(row=3, column=0, columnspan=2, pady=10)

# Update Member Frame
tk.Label(update_member_frame, text="Member ID:").grid(row=0, column=0, padx=10, pady=10)
update_member_id_entry = tk.Entry(update_member_frame)
update_member_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(update_member_frame, text="Name:").grid(row=1, column=0, padx=10, pady=10)
update_name_entry = tk.Entry(update_member_frame)
update_name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(update_member_frame, text="Age:").grid(row=2, column=0, padx=10, pady=10)
update_age_entry = tk.Entry(update_member_frame)
update_age_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(update_member_frame, text="Gender:").grid(row=3, column=0, padx=10, pady=10)
update_gender_entry = tk.Entry(update_member_frame)
update_gender_entry.grid(row=3, column=1, padx=10, pady=10)

update_member_button = tk.Button(update_member_frame, text="Update Member", command=update_member)
update_member_button.grid(row=4, column=0, columnspan=2, pady=10)

# View Members Frame
view_members_button = tk.Button(view_members_frame, text="View Members", command=view_members)
view_members_button.grid(row=0, column=0, columnspan=2, pady=10)

# Track Attendance Frame
tk.Label(track_attendance_frame, text="Member ID:").grid(row=0, column=0, padx=10, pady=10)
attendance_member_id_entry = tk.Entry(track_attendance_frame)
attendance_member_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(track_attendance_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
attendance_date_entry = tk.Entry(track_attendance_frame)
attendance_date_entry.grid(row=1, column=1, padx=10, pady=10)

track_attendance_button = tk.Button(track_attendance_frame, text="Track Attendance", command=track_attendance)
track_attendance_button.grid(row=2, column=0, columnspan=2, pady=10)

# Update Status Frame
tk.Label(update_status_frame, text="Member ID:").grid(row=0, column=0, padx=10, pady=10)
status_member_id_entry = tk.Entry(update_status_frame)
status_member_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(update_status_frame, text="Status:").grid(row=1, column=0, padx=10, pady=10)
status_entry = tk.Entry(update_status_frame)
status_entry.grid(row=1, column=1, padx=10, pady=10)

update_status_button = tk.Button(update_status_frame, text="Update Status", command=update_membership_status)
update_status_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
