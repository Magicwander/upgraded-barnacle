import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime

# Initialize the database
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    roll_number TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    student_id INTEGER,
                    date TEXT,
                    status TEXT,
                    FOREIGN KEY(student_id) REFERENCES students(id))''')
    conn.commit()
    conn.close()

# Add a student
def add_student(name, roll_number):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, roll_number) VALUES (?, ?)", (name, roll_number))
    conn.commit()
    conn.close()

# Mark attendance
def mark_attendance(student_id, date, status):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
    conn.commit()
    conn.close()

# Get all students
def get_all_students():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT id, name, roll_number FROM students")
    students = c.fetchall()
    conn.close()
    return students

# Get attendance records
def get_attendance_records():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT attendance.id, students.name, attendance.date, attendance.status FROM attendance JOIN students ON attendance.student_id = students.id")
    records = c.fetchall()
    conn.close()
    return records

# Tkinter GUI
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance System")

        self.student_name = tk.StringVar()
        self.roll_number = tk.StringVar()
        self.student_id = tk.IntVar()
        self.date = tk.StringVar()
        self.status = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill="both")

        # Add Student Tab
        add_student_tab = ttk.Frame(notebook)
        notebook.add(add_student_tab, text='Add Student')

        tk.Label(add_student_tab, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(add_student_tab, textvariable=self.student_name).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(add_student_tab, text="Roll Number:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(add_student_tab, textvariable=self.roll_number).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(add_student_tab, text="Add Student", command=self.add_student).grid(row=2, column=1, padx=10, pady=10)

        # Mark Attendance Tab
        mark_attendance_tab = ttk.Frame(notebook)
        notebook.add(mark_attendance_tab, text='Mark Attendance')

        tk.Label(mark_attendance_tab, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(mark_attendance_tab, textvariable=self.student_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(mark_attendance_tab, text="Date:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(mark_attendance_tab, textvariable=self.date).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(mark_attendance_tab, text="Status:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(mark_attendance_tab, textvariable=self.status).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(mark_attendance_tab, text="Mark Attendance", command=self.mark_attendance).grid(row=3, column=1, padx=10, pady=10)

        # View All Students Tab
        view_students_tab = ttk.Frame(notebook)
        notebook.add(view_students_tab, text='View All Students')

        self.students_list = tk.Listbox(view_students_tab, width=100)
        self.students_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_students_tab, text="Refresh", command=self.refresh_students).grid(row=1, column=0, padx=10, pady=10)

        # View Attendance Records Tab
        view_attendance_tab = ttk.Frame(notebook)
        notebook.add(view_attendance_tab, text='View Attendance Records')

        self.attendance_list = tk.Listbox(view_attendance_tab, width=100)
        self.attendance_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_attendance_tab, text="Refresh", command=self.refresh_attendance).grid(row=1, column=0, padx=10, pady=10)

        self.refresh_students()
        self.refresh_attendance()

    def add_student(self):
        name = self.student_name.get()
        roll_number = self.roll_number.get()
        if name and roll_number:
            add_student(name, roll_number)
            messagebox.showinfo("Success", "Student added successfully.")
            self.refresh_students()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def mark_attendance(self):
        student_id = self.student_id.get()
        date = self.date.get()
        status = self.status.get()
        if student_id and date and status:
            mark_attendance(student_id, date, status)
            messagebox.showinfo("Success", "Attendance marked successfully.")
            self.refresh_attendance()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def refresh_students(self):
        self.students_list.delete(0, tk.END)
        students = get_all_students()
        for student in students:
            self.students_list.insert(tk.END, f"ID: {student[0]}, Name: {student[1]}, Roll Number: {student[2]}")

    def refresh_attendance(self):
        self.attendance_list.delete(0, tk.END)
        records = get_attendance_records()
        for record in records:
            self.attendance_list.insert(tk.END, f"ID: {record[0]}, Student: {record[1]}, Date: {record[2]}, Status: {record[3]}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
