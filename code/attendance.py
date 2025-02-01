import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import gettext
import logging
import unittest
import csv

# Initialize the database
def init_db():
    """
    Initialize the database by creating the necessary tables if they do not exist.
    """
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
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

# Add a student
def add_student(name, roll_number):
    """
    Add a new student to the database.

    Parameters:
    name (str): The name of the student.
    roll_number (str): The roll number of the student.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, roll_number) VALUES (?, ?)", (name, roll_number))
    conn.commit()
    conn.close()
    logging.info(f"Student added: {name}, {roll_number}")

# Mark attendance
def mark_attendance(student_id, date, status):
    """
    Mark the attendance of a student.

    Parameters:
    student_id (int): The ID of the student.
    date (str): The date of the attendance.
    status (str): The status of the attendance (e.g., Present, Absent).
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
    conn.commit()
    conn.close()
    logging.info(f"Attendance marked: Student ID: {student_id}, Date: {date}, Status: {status}")

# Get all students
def get_all_students():
    """
    Retrieve all students from the database.

    Returns:
    list: A list of tuples containing student information.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT id, name, roll_number FROM students")
    students = c.fetchall()
    conn.close()
    return students

# Get attendance records
def get_attendance_records():
    """
    Retrieve all attendance records from the database.

    Returns:
    list: A list of tuples containing attendance information.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT attendance.id, students.name, attendance.date, attendance.status FROM attendance JOIN students ON attendance.student_id = students.id")
    records = c.fetchall()
    conn.close()
    return records

# Get attendance records for a specific student
def get_student_attendance(student_id):
    """
    Retrieve attendance records for a specific student.

    Parameters:
    student_id (int): The ID of the student.

    Returns:
    list: A list of tuples containing attendance information for the specified student.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT date, status FROM attendance WHERE student_id = ?", (student_id,))
    records = c.fetchall()
    conn.close()
    return records

# Update student information
def update_student(student_id, name, roll_number):
    """
    Update the information of an existing student.

    Parameters:
    student_id (int): The ID of the student.
    name (str): The new name of the student.
    roll_number (str): The new roll number of the student.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("UPDATE students SET name = ?, roll_number = ? WHERE id = ?", (name, roll_number, student_id))
    conn.commit()
    conn.close()
    logging.info(f"Student updated: ID: {student_id}, Name: {name}, Roll Number: {roll_number}")

# Delete a student
def delete_student(student_id):
    """
    Delete a student from the database.

    Parameters:
    student_id (int): The ID of the student to be deleted.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    logging.info(f"Student deleted: ID: {student_id}")

# Delete an attendance record
def delete_attendance(attendance_id):
    """
    Delete an attendance record from the database.

    Parameters:
    attendance_id (int): The ID of the attendance record to be deleted.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
    conn.commit()
    conn.close()
    logging.info(f"Attendance record deleted: ID: {attendance_id}")

# Search for a student by name or roll number
def search_student(query):
    """
    Search for a student by name or roll number.

    Parameters:
    query (str): The search query (name or roll number).

    Returns:
    list: A list of tuples containing student information that matches the query.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT id, name, roll_number FROM students WHERE name LIKE ? OR roll_number LIKE ?", ('%' + query + '%', '%' + query + '%'))
    students = c.fetchall()
    conn.close()
    return students

# Generate attendance report for a specific date range
def generate_attendance_report(start_date, end_date):
    """
    Generate an attendance report for a specific date range.

    Parameters:
    start_date (str): The start date of the report.
    end_date (str): The end date of the report.

    Returns:
    list: A list of tuples containing attendance information within the specified date range.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT students.name, attendance.date, attendance.status FROM attendance JOIN students ON attendance.student_id = students.id WHERE attendance.date BETWEEN ? AND ?", (start_date, end_date))
    records = c.fetchall()
    conn.close()
    return records

# Get student by ID
def get_student_by_id(student_id):
    """
    Retrieve a student by their ID.

    Parameters:
    student_id (int): The ID of the student.

    Returns:
    tuple: A tuple containing the student information.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT id, name, roll_number FROM students WHERE id = ?", (student_id,))
    student = c.fetchone()
    conn.close()
    return student

# Get attendance record by ID
def get_attendance_by_id(attendance_id):
    """
    Retrieve an attendance record by its ID.

    Parameters:
    attendance_id (int): The ID of the attendance record.

    Returns:
    tuple: A tuple containing the attendance information.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT id, student_id, date, status FROM attendance WHERE id = ?", (attendance_id,))
    record = c.fetchone()
    conn.close()
    return record

# Update attendance record
def update_attendance(attendance_id, student_id, date, status):
    """
    Update an existing attendance record.

    Parameters:
    attendance_id (int): The ID of the attendance record.
    student_id (int): The new student ID.
    date (str): The new date.
    status (str): The new status.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("UPDATE attendance SET student_id = ?, date = ?, status = ? WHERE id = ?", (student_id, date, status, attendance_id))
    conn.commit()
    conn.close()
    logging.info(f"Attendance record updated: ID: {attendance_id}, Student ID: {student_id}, Date: {date}, Status: {status}")

# Validate date format
def validate_date(date_text):
    """
    Validate the date format.

    Parameters:
    date_text (str): The date string to validate.

    Returns:
    bool: True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Export attendance report to CSV
def export_attendance_report_to_csv(start_date, end_date, file_path):
    """
    Export an attendance report for a specific date range to a CSV file.

    Parameters:
    start_date (str): The start date of the report.
    end_date (str): The end date of the report.
    file_path (str): The file path where the CSV will be saved.
    """
    records = generate_attendance_report(start_date, end_date)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Student Name", "Date", "Status"])
        writer.writerows(records)
    logging.info(f"Attendance report exported to {file_path}")

# Import students from CSV
def import_students_from_csv(file_path):
    """
    Import students from a CSV file.

    Parameters:
    file_path (str): The file path of the CSV file.
    """
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            name, roll_number = row
            add_student(name, roll_number)
    logging.info(f"Students imported from {file_path}")

# Import attendance from CSV
def import_attendance_from_csv(file_path):
    """
    Import attendance records from a CSV file.

    Parameters:
    file_path (str): The file path of the CSV file.
    """
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            student_id, date, status = row
            mark_attendance(int(student_id), date, status)
    logging.info(f"Attendance records imported from {file_path}")

# User authentication functions
def hash_password(password):
    """
    Hash a password using SHA-256.

    Parameters:
    password (str): The password to hash.

    Returns:
    str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role):
    """
    Register a new user.

    Parameters:
    username (str): The username of the user.
    password (str): The password of the user.
    role (str): The role of the user (admin, teacher, student).
    """
    hashed_password = hash_password(password)
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
    conn.commit()
    conn.close()
    logging.info(f"User registered: Username: {username}, Role: {role}")

def login_user(username, password):
    """
    Log in a user.

    Parameters:
    username (str): The username of the user.
    password (str): The password of the user.

    Returns:
    tuple: A tuple containing the user information if login is successful, None otherwise.
    """
    hashed_password = hash_password(password)
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

# Tkinter GUI for user authentication
class AuthApp:
    def __init__(self, root):
        """
        Initialize the AuthApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("User Authentication")

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.role = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.username).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.password, show='*').grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Role:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.role).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Register", command=self.register_user).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Login", command=self.login_user).grid(row=3, column=1, padx=10, pady=10)

    def register_user(self):
        """
        Register a new user.
        """
        username = self.username.get()
        password = self.password.get()
        role = self.role.get()
        if username and password and role:
            register_user(username, password, role)
            messagebox.showinfo("Success", "User registered successfully.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def login_user(self):
        """
        Log in a user.
        """
        username = self.username.get()
        password = self.password.get()
        if username and password:
            user = login_user(username, password)
            if user:
                messagebox.showinfo("Success", f"Welcome, {user[1]}!")
                # Proceed to the main application
                self.root.destroy()
                main_app = AttendanceApp(tk.Tk())
                main_app.root.mainloop()
            else:
                messagebox.showwarning("Login error", "Invalid username or password.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

# Generate attendance chart
def generate_attendance_chart(start_date, end_date):
    """
    Generate an attendance chart for a specific date range.

    Parameters:
    start_date (str): The start date of the report.
    end_date (str): The end date of the report.

    Returns:
    Figure: A Matplotlib figure containing the attendance chart.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT students.name, attendance.date, attendance.status FROM attendance JOIN students ON attendance.student_id = students.id WHERE attendance.date BETWEEN ? AND ?", (start_date, end_date))
    records = c.fetchall()
    conn.close()

    attendance_data = {}
    for record in records:
        student_name = record[0]
        status = record[2]
        if student_name not in attendance_data:
            attendance_data[student_name] = {"Present": 0, "Absent": 0}
        attendance_data[student_name][status] += 1

    fig, ax = plt.subplots()
    for student, data in attendance_data.items():
        ax.bar(student, data["Present"], label='Present', color='g')
        ax.bar(student, data["Absent"], bottom=data["Present"], label='Absent', color='r')

    ax.set_ylabel('Number of Days')
    ax.set_title('Attendance Report')
    ax.legend()

    return fig

class ReportApp:
    def __init__(self, root):
        """
        Initialize the ReportApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Attendance Report")

        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text="Start Date:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.start_date).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.root, text="End Date:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.end_date).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Generate Chart", command=self.generate_chart).grid(row=2, column=1, padx=10, pady=10)

        self.canvas = tk.Canvas(self.root, width=800, height=400)
        self.canvas.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def generate_chart(self):
        """
        Generate and display the attendance chart.
        """
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        if start_date and end_date:
            if validate_date(start_date) and validate_date(end_date):
                fig = generate_attendance_chart(start_date, end_date)
                canvas = FigureCanvasTkAgg(fig, master=self.canvas)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            else:
                messagebox.showwarning("Input error", "Please enter valid dates in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please enter both start and end dates.")

# Send email notifications
def send_email_notification(to_email, subject, body):
    """
    Send an email notification.

    Parameters:
    to_email (str): The recipient's email address.
    subject (str): The subject of the email.
    body (str): The body of the email.
    """
    from_email = "your_email@example.com"
    from_password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()
    logging.info(f"Email sent to {to_email}")

def send_attendance_reminder(student_email, student_name, date):
    """
    Send an attendance reminder to a student.

    Parameters:
    student_email (str): The student's email address.
    student_name (str): The student's name.
    date (str): The date of the attendance.
    """
    subject = "Attendance Reminder"
    body = f"Dear {student_name},\n\nThis is a reminder that your attendance for {date} has not been marked. Please contact your teacher for more information.\n\nBest regards,\nAttendance System"
    send_email_notification(student_email, subject, body)
    logging.info(f"Attendance reminder sent to {student_email}")

def send_attendance_update(student_email, student_name, date, status):
    """
    Send an attendance update to a student.

    Parameters:
    student_email (str): The student's email address.
    student_name (str): The student's name.
    date (str): The date of the attendance.
    status (str): The status of the attendance.
    """
    subject = "Attendance Update"
    body = f"Dear {student_name},\n\nYour attendance for {date} has been marked as {status}.\n\nBest regards,\nAttendance System"
    send_email_notification(student_email, subject, body)
    logging.info(f"Attendance update sent to {student_email}")

class NotificationApp:
    def __init__(self, root):
        """
        Initialize the NotificationApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Notification System")

        self.student_email = tk.StringVar()
        self.student_name = tk.StringVar()
        self.date = tk.StringVar()
        self.status = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text="Student Email:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.student_email).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Student Name:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.student_name).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Date:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.date).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Status:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.status).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Send Reminder", command=self.send_reminder).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Send Update", command=self.send_update).grid(row=4, column=1, padx=10, pady=10)

    def send_reminder(self):
        """
        Send an attendance reminder.
        """
        student_email = self.student_email.get()
        student_name = self.student_name.get()
        date = self.date.get()
        if student_email and student_name and date:
            if validate_date(date):
                send_attendance_reminder(student_email, student_name, date)
                messagebox.showinfo("Success", "Reminder sent successfully.")
            else:
                messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def send_update(self):
        """
        Send an attendance update.
        """
        student_email = self.student_email.get()
        student_name = self.student_name.get()
        date = self.date.get()
        status = self.status.get()
        if student_email and student_name and date and status:
            if validate_date(date):
                send_attendance_update(student_email, student_name, date, status)
                messagebox.showinfo("Success", "Update sent successfully.")
            else:
                messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

# Advanced search for students
def advanced_search_students(name=None, roll_number=None, attendance_status=None, start_date=None, end_date=None):
    """
    Perform an advanced search for students based on various criteria.

    Parameters:
    name (str): The name of the student.
    roll_number (str): The roll number of the student.
    attendance_status (str): The attendance status of the student.
    start_date (str): The start date of the attendance.
    end_date (str): The end date of the attendance.

    Returns:
    list: A list of tuples containing student information that matches the criteria.
    """
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    query = "SELECT DISTINCT students.id, students.name, students.roll_number FROM students"
    conditions = []
    params = []

    if name:
        conditions.append("students.name LIKE ?")
        params.append('%' + name + '%')
    if roll_number:
        conditions.append("students.roll_number LIKE ?")
        params.append('%' + roll_number + '%')
    if attendance_status:
        conditions.append("attendance.status = ?")
        params.append(attendance_status)
    if start_date and end_date:
        conditions.append("attendance.date BETWEEN ? AND ?")
        params.append(start_date)
        params.append(end_date)

    if conditions:
        query += " JOIN attendance ON students.id = attendance.student_id WHERE " + " AND ".join(conditions)

    c.execute(query, params)
    students = c.fetchall()
    conn.close()
    return students

class AdvancedSearchApp:
    def __init__(self, root):
        """
        Initialize the AdvancedSearchApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Advanced Search")

        self.name = tk.StringVar()
        self.roll_number = tk.StringVar()
        self.attendance_status = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.name).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Roll Number:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.roll_number).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Attendance Status:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.attendance_status).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Start Date:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.start_date).grid(row=3, column=1, padx=10, pady=10)
        tk.Label(self.root, text="End Date:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.end_date).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Search", command=self.search_students).grid(row=5, column=1, padx=10, pady=10)

        self.search_results_list = tk.Listbox(self.root, width=100)
        self.search_results_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def search_students(self):
        """
        Perform an advanced search for students.
        """
        name = self.name.get()
        roll_number = self.roll_number.get()
        attendance_status = self.attendance_status.get()
        start_date = self.start_date.get()
        end_date = self.end_date.get()

        if start_date and end_date:
            if not (validate_date(start_date) and validate_date(end_date)):
                messagebox.showwarning("Input error", "Please enter valid dates in YYYY-MM-DD format.")
                return

        students = advanced_search_students(name, roll_number, attendance_status, start_date, end_date)
        self.search_results_list.delete(0, tk.END)
        for student in students:
            self.search_results_list.insert(tk.END, f"ID: {student[0]}, Name: {student[1]}, Roll Number: {student[2]}")

# Data validation functions
def validate_name(name):
    """
    Validate the name.

    Parameters:
    name (str): The name to validate.

    Returns:
    bool: True if the name is valid, False otherwise.
    """
    return bool(name.strip())

def validate_roll_number(roll_number):
    """
    Validate the roll number.

    Parameters:
    roll_number (str): The roll number to validate.

    Returns:
    bool: True if the roll number is valid, False otherwise.
    """
    return bool(roll_number.strip())

def validate_status(status):
    """
    Validate the attendance status.

    Parameters:
    status (str): The attendance status to validate.

    Returns:
    bool: True if the status is valid, False otherwise.
    """
    return status in ["Present", "Absent"]

def validate_email(email):
    """
    Validate the email address.

    Parameters:
    email (str): The email address to validate.

    Returns:
    bool: True if the email is valid, False otherwise.
    """
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

class ValidationApp:
    def __init__(self, root):
        """
        Initialize the ValidationApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Data Validation")

        self.name = tk.StringVar()
        self.roll_number = tk.StringVar()
        self.status = tk.StringVar()
        self.date = tk.StringVar()
        self.email = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.name).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Roll Number:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.roll_number).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Status:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.status).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Date:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.date).grid(row=3, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Email:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.email).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Validate", command=self.validate_data).grid(row=5, column=1, padx=10, pady=10)

    def validate_data(self):
        """
        Validate the input data.
        """
        name = self.name.get()
        roll_number = self.roll_number.get()
        status = self.status.get()
        date = self.date.get()
        email = self.email.get()

        if not validate_name(name):
            messagebox.showwarning("Input error", "Please enter a valid name.")
        elif not validate_roll_number(roll_number):
            messagebox.showwarning("Input error", "Please enter a valid roll number.")
        elif not validate_status(status):
            messagebox.showwarning("Input error", "Please enter a valid status (Present or Absent).")
        elif not validate_date(date):
            messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        elif not validate_email(email):
            messagebox.showwarning("Input error", "Please enter a valid email address.")
        else:
            messagebox.showinfo("Success", "All inputs are valid.")

# Unit tests
class TestAttendanceSystem(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE students (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            roll_number TEXT NOT NULL)''')
        self.c.execute('''CREATE TABLE attendance (
                            id INTEGER PRIMARY KEY,
                            student_id INTEGER,
                            date TEXT,
                            status TEXT,
                            FOREIGN KEY(student_id) REFERENCES students(id))''')
        self.c.execute('''CREATE TABLE users (
                            id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            role TEXT NOT NULL)''')
        self.conn.commit()

    def tearDown(self):
        """
        Tear down the test environment.
        """
        self.conn.close()

    def test_add_student(self):
        """
        Test adding a student.
        """
        add_student("John Doe", "12345")
        self.c.execute("SELECT * FROM students WHERE name = ? AND roll_number = ?", ("John Doe", "12345"))
        student = self.c.fetchone()
        self.assertIsNotNone(student)

    def test_mark_attendance(self):
        """
        Test marking attendance.
        """
        add_student("Jane Smith", "67890")
        self.c.execute("SELECT id FROM students WHERE name = ? AND roll_number = ?", ("Jane Smith", "67890"))
        student_id = self.c.fetchone()[0]
        mark_attendance(student_id, "2023-10-01", "Present")
        self.c.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ? AND status = ?", (student_id, "2023-10-01", "Present"))
        attendance = self.c.fetchone()
        self.assertIsNotNone(attendance)

    def test_validate_date(self):
        """
        Test date validation.
        """
        self.assertTrue(validate_date("2023-10-01"))
        self.assertFalse(validate_date("01-10-2023"))

    def test_register_user(self):
        """
        Test registering a user.
        """
        register_user("admin", "password123", "admin")
        self.c.execute("SELECT * FROM users WHERE username = ? AND role = ?", ("admin", "admin"))
        user = self.c.fetchone()
        self.assertIsNotNone(user)

    def test_login_user(self):
        """
        Test logging in a user.
        """
        register_user("teacher", "password123", "teacher")
        user = login_user("teacher", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user[2], "teacher")

    def test_validate_email(self):
        """
        Test email validation.
        """
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid-email"))

if __name__ == '__main__':
    unittest.main()

# Internationalization
localedir = 'locales'
lang = gettext.translation('attendance', localedir, languages=['en'])
lang.install()

def _(text):
    """
    Translate text using gettext.

    Parameters:
    text (str): The text to translate.

    Returns:
    str: The translated text.
    """
    return lang.gettext(text)

class InternationalizationApp:
    def __init__(self, root):
        """
        Initialize the InternationalizationApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title(_("Internationalization"))

        self.language = tk.StringVar(value="en")

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text=_("Select Language:")).grid(row=0, column=0, padx=10, pady=10)
        tk.OptionMenu(self.root, self.language, "en", "fr", "es").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text=_("Change Language"), command=self.change_language).grid(row=1, column=1, padx=10, pady=10)

    def change_language(self):
        """
        Change the language of the application.
        """
        selected_language = self.language.get()
        lang.install()
        lang = gettext.translation('attendance', localedir, languages=[selected_language])
        lang.install()
        self.root.title(_("Internationalization"))
        self.create_widgets()

# Accessibility
class AccessibilityApp:
    def __init__(self, root):
        """
        Initialize the AccessibilityApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Accessibility")

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text="Accessibility Features", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Increase Font Size", command=self.increase_font_size).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Decrease Font Size", command=self.decrease_font_size).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.root, text="High Contrast Mode", command=self.toggle_high_contrast).grid(row=3, column=0, padx=10, pady=10)

    def increase_font_size(self):
        """
        Increase the font size of the application.
        """
        current_font = self.root.cget("font")
        font_size = int(current_font.split()[-1]) + 2
        new_font = (current_font.split()[0], font_size)
        self.root.config(font=new_font)

    def decrease_font_size(self):
        """
        Decrease the font size of the application.
        """
        current_font = self.root.cget("font")
        font_size = int(current_font.split()[-1]) - 2
        new_font = (current_font.split()[0], font_size)
        self.root.config(font=new_font)

    def toggle_high_contrast(self):
        """
        Toggle high contrast mode.
        """
        current_bg = self.root.cget("bg")
        if current_bg == "SystemButtonFace":
            self.root.config(bg="black", fg="white")
        else:
            self.root.config(bg="SystemButtonFace", fg="black")

# Main application
class AttendanceApp:
    def __init__(self, root):
        """
        Initialize the AttendanceApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Student Attendance System")

        self.student_name = tk.StringVar()
        self.roll_number = tk.StringVar()
        self.student_id = tk.IntVar()
        self.date = tk.StringVar()
        self.status = tk.StringVar()
        self.search_query = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()
        self.attendance_id = tk.IntVar()
        self.csv_file_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
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

        # Update Student Tab
        update_student_tab = ttk.Frame(notebook)
        notebook.add(update_student_tab, text='Update Student')

        tk.Label(update_student_tab, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(update_student_tab, textvariable=self.student_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(update_student_tab, text="Name:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(update_student_tab, textvariable=self.student_name).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(update_student_tab, text="Roll Number:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(update_student_tab, textvariable=self.roll_number).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(update_student_tab, text="Update Student", command=self.update_student).grid(row=3, column=1, padx=10, pady=10)

        # Delete Student Tab
        delete_student_tab = ttk.Frame(notebook)
        notebook.add(delete_student_tab, text='Delete Student')

        tk.Label(delete_student_tab, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(delete_student_tab, textvariable=self.student_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(delete_student_tab, text="Delete Student", command=self.delete_student).grid(row=1, column=1, padx=10, pady=10)

        # Delete Attendance Record Tab
        delete_attendance_tab = ttk.Frame(notebook)
        notebook.add(delete_attendance_tab, text='Delete Attendance Record')

        tk.Label(delete_attendance_tab, text="Attendance ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(delete_attendance_tab, textvariable=self.attendance_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(delete_attendance_tab, text="Delete Attendance Record", command=self.delete_attendance).grid(row=1, column=1, padx=10, pady=10)

        # Search Student Tab
        search_student_tab = ttk.Frame(notebook)
        notebook.add(search_student_tab, text='Search Student')

        tk.Label(search_student_tab, text="Search Query:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(search_student_tab, textvariable=self.search_query).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(search_student_tab, text="Search", command=self.search_student).grid(row=1, column=1, padx=10, pady=10)
        self.search_results_list = tk.Listbox(search_student_tab, width=100)
        self.search_results_list.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Generate Attendance Report Tab
        generate_report_tab = ttk.Frame(notebook)
        notebook.add(generate_report_tab, text='Generate Attendance Report')

        tk.Label(generate_report_tab, text="Start Date:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(generate_report_tab, textvariable=self.start_date).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(generate_report_tab, text="End Date:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(generate_report_tab, textvariable=self.end_date).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(generate_report_tab, text="Generate Report", command=self.generate_attendance_report).grid(row=2, column=1, padx=10, pady=10)
        self.report_list = tk.Listbox(generate_report_tab, width=100)
        self.report_list.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Update Attendance Record Tab
        update_attendance_tab = ttk.Frame(notebook)
        notebook.add(update_attendance_tab, text='Update Attendance Record')

        tk.Label(update_attendance_tab, text="Attendance ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(update_attendance_tab, textvariable=self.attendance_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(update_attendance_tab, text="Student ID:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(update_attendance_tab, textvariable=self.student_id).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(update_attendance_tab, text="Date:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(update_attendance_tab, textvariable=self.date).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(update_attendance_tab, text="Status:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(update_attendance_tab, textvariable=self.status).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(update_attendance_tab, text="Update Attendance Record", command=self.update_attendance_record).grid(row=4, column=1, padx=10, pady=10)

        # Export Attendance Report Tab
        export_report_tab = ttk.Frame(notebook)
        notebook.add(export_report_tab, text='Export Attendance Report')

        tk.Label(export_report_tab, text="Start Date:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(export_report_tab, textvariable=self.start_date).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(export_report_tab, text="End Date:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(export_report_tab, textvariable=self.end_date).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(export_report_tab, text="File Path:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(export_report_tab, textvariable=self.csv_file_path).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(export_report_tab, text="Export Report", command=self.export_attendance_report).grid(row=3, column=1, padx=10, pady=10)

        # Import Students Tab
        import_students_tab = ttk.Frame(notebook)
        notebook.add(import_students_tab, text='Import Students')

        tk.Label(import_students_tab, text="File Path:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(import_students_tab, textvariable=self.csv_file_path).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(import_students_tab, text="Import Students", command=self.import_students).grid(row=1, column=1, padx=10, pady=10)

        # Import Attendance Tab
        import_attendance_tab = ttk.Frame(notebook)
        notebook.add(import_attendance_tab, text='Import Attendance')

        tk.Label(import_attendance_tab, text="File Path:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(import_attendance_tab, textvariable=self.csv_file_path).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(import_attendance_tab, text="Import Attendance", command=self.import_attendance).grid(row=1, column=1, padx=10, pady=10)

        self.refresh_students()
        self.refresh_attendance()

    def add_student(self):
        """
        Add a new student to the database.
        """
        name = self.student_name.get()
        roll_number = self.roll_number.get()
        if name and roll_number:
            add_student(name, roll_number)
            messagebox.showinfo("Success", "Student added successfully.")
            self.refresh_students()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def mark_attendance(self):
        """
        Mark the attendance of a student.
        """
        student_id = self.student_id.get()
        date = self.date.get()
        status = self.status.get()
        if student_id and date and status:
            if validate_date(date):
                mark_attendance(student_id, date, status)
                messagebox.showinfo("Success", "Attendance marked successfully.")
                self.refresh_attendance()
            else:
                messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def refresh_students(self):
        """
        Refresh the list of students.
        """
        self.students_list.delete(0, tk.END)
        students = get_all_students()
        for student in students:
            self.students_list.insert(tk.END, f"ID: {student[0]}, Name: {student[1]}, Roll Number: {student[2]}")

    def refresh_attendance(self):
        """
        Refresh the list of attendance records.
        """
        self.attendance_list.delete(0, tk.END)
        records = get_attendance_records()
        for record in records:
            self.attendance_list.insert(tk.END, f"ID: {record[0]}, Student: {record[1]}, Date: {record[2]}, Status: {record[3]}")

    def update_student(self):
        """
        Update the information of an existing student.
        """
        student_id = self.student_id.get()
        name = self.student_name.get()
        roll_number = self.roll_number.get()
        if student_id and name and roll_number:
            update_student(student_id, name, roll_number)
            messagebox.showinfo("Success", "Student information updated successfully.")
            self.refresh_students()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def delete_student(self):
        """
        Delete a student from the database.
        """
        student_id = self.student_id.get()
        if student_id:
            delete_student(student_id)
            messagebox.showinfo("Success", "Student deleted successfully.")
            self.refresh_students()
        else:
            messagebox.showwarning("Input error", "Please enter a valid Student ID.")

    def delete_attendance(self):
        """
        Delete an attendance record from the database.
        """
        attendance_id = self.attendance_id.get()
        if attendance_id:
            delete_attendance(attendance_id)
            messagebox.showinfo("Success", "Attendance record deleted successfully.")
            self.refresh_attendance()
        else:
            messagebox.showwarning("Input error", "Please enter a valid Attendance ID.")

    def search_student(self):
        """
        Search for a student by name or roll number.
        """
        query = self.search_query.get()
        if query:
            students = search_student(query)
            self.search_results_list.delete(0, tk.END)
            for student in students:
                self.search_results_list.insert(tk.END, f"ID: {student[0]}, Name: {student[1]}, Roll Number: {student[2]}")
        else:
            messagebox.showwarning("Input error", "Please enter a search query.")

    def generate_attendance_report(self):
        """
        Generate an attendance report for a specific date range.
        """
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        if start_date and end_date:
            if validate_date(start_date) and validate_date(end_date):
                records = generate_attendance_report(start_date, end_date)
                self.report_list.delete(0, tk.END)
                for record in records:
                    self.report_list.insert(tk.END, f"Student: {record[0]}, Date: {record[1]}, Status: {record[2]}")
            else:
                messagebox.showwarning("Input error", "Please enter valid dates in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please enter both start and end dates.")

    def update_attendance_record(self):
        """
        Update an existing attendance record.
        """
        attendance_id = self.attendance_id.get()
        student_id = self.student_id.get()
        date = self.date.get()
        status = self.status.get()
        if attendance_id and student_id and date and status:
            if validate_date(date):
                update_attendance(attendance_id, student_id, date, status)
                messagebox.showinfo("Success", "Attendance record updated successfully.")
                self.refresh_attendance()
            else:
                messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def export_attendance_report(self):
        """
        Export an attendance report for a specific date range to a CSV file.
        """
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        file_path = self.csv_file_path.get()
        if start_date and end_date and file_path:
            if validate_date(start_date) and validate_date(end_date):
                export_attendance_report_to_csv(start_date, end_date, file_path)
                messagebox.showinfo("Success", "Attendance report exported successfully.")
            else:
                messagebox.showwarning("Input error", "Please enter valid dates in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please enter both start and end dates and a valid file path.")

    def import_students(self):
        """
        Import students from a CSV file.
        """
        file_path = self.csv_file_path.get()
        if file_path:
            import_students_from_csv(file_path)
            messagebox.showinfo("Success", "Students imported successfully.")
            self.refresh_students()
        else:
            messagebox.showwarning("Input error", "Please enter a valid file path.")

    def import_attendance(self):
        """
        Import attendance records from a CSV file.
        """
        file_path = self.csv_file_path.get()
        if file_path:
            import_attendance_from_csv(file_path)
            messagebox.showinfo("Success", "Attendance records imported successfully.")
            self.refresh_attendance()
        else:
            messagebox.showwarning("Input error", "Please enter a valid file path.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
