import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime

# Initialize the database
def init_db():
    conn = sqlite3.connect('timeoff.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY,
                    employee_id INTEGER,
                    type TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    status TEXT,
                    FOREIGN KEY(employee_id) REFERENCES employees(id))''')
    conn.commit()
    conn.close()

# Add an employee
def add_employee(name):
    conn = sqlite3.connect('timeoff.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# Add a time-off request
def add_request(employee_id, request_type, start_date, end_date):
    conn = sqlite3.connect('timeoff.db')
    c = conn.cursor()
    c.execute("INSERT INTO requests (employee_id, type, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
              (employee_id, request_type, start_date, end_date, 'Pending'))
    conn.commit()
    conn.close()

# Approve or reject a request
def update_request(request_id, status):
    conn = sqlite3.connect('timeoff.db')
    c = conn.cursor()
    c.execute("UPDATE requests SET status = ? WHERE id = ?", (status, request_id))
    conn.commit()
    conn.close()

# Generate a report
def generate_report():
    conn = sqlite3.connect('timeoff.db')
    c = conn.cursor()
    c.execute("SELECT employees.name, requests.type, requests.start_date, requests.end_date, requests.status FROM requests JOIN employees ON requests.employee_id = employees.id")
    report = c.fetchall()
    conn.close()
    return report

# Get pending requests
def get_pending_requests():
    conn = sqlite3.connect('timeoff.db')
    c = conn.cursor()
    c.execute("SELECT requests.id, employees.name, requests.type, requests.start_date, requests.end_date FROM requests JOIN employees ON requests.employee_id = employees.id WHERE requests.status = 'Pending'")
    pending_requests = c.fetchall()
    conn.close()
    return pending_requests

# Get all employees
def get_all_employees():
    conn = sqlite3.connect('timeoff.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM employees")
    employees = c.fetchall()
    conn.close()
    return employees

# Get all requests
def get_all_requests():
    conn = sqlite3.connect('timeoff.db')
    c = conn.cursor()
    c.execute("SELECT requests.id, employees.name, requests.type, requests.start_date, requests.end_date, requests.status FROM requests JOIN employees ON requests.employee_id = employees.id")
    requests = c.fetchall()
    conn.close()
    return requests

# Tkinter GUI
class TimeOffApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time-off Request Management System")

        self.employee_name = tk.StringVar()
        self.request_type = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()
        self.employee_id = tk.IntVar()
        self.request_id = tk.IntVar()
        self.status = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill="both")

        # Add Employee Tab
        add_employee_tab = ttk.Frame(notebook)
        notebook.add(add_employee_tab, text='Add Employee')

        tk.Label(add_employee_tab, text="Employee Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(add_employee_tab, textvariable=self.employee_name).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(add_employee_tab, text="Add Employee", command=self.add_employee).grid(row=0, column=2, padx=10, pady=10)

        # Add Request Tab
        add_request_tab = ttk.Frame(notebook)
        notebook.add(add_request_tab, text='Add Request')

        tk.Label(add_request_tab, text="Employee ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(add_request_tab, textvariable=self.employee_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(add_request_tab, text="Request Type:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(add_request_tab, textvariable=self.request_type).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(add_request_tab, text="Start Date:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(add_request_tab, textvariable=self.start_date).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(add_request_tab, text="End Date:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(add_request_tab, textvariable=self.end_date).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(add_request_tab, text="Add Request", command=self.add_request).grid(row=4, column=1, padx=10, pady=10)

        # Update Request Tab
        update_request_tab = ttk.Frame(notebook)
        notebook.add(update_request_tab, text='Update Request')

        tk.Label(update_request_tab, text="Request ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(update_request_tab, textvariable=self.request_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(update_request_tab, text="Status:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(update_request_tab, textvariable=self.status).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(update_request_tab, text="Update Request", command=self.update_request).grid(row=2, column=1, padx=10, pady=10)

        # Generate Report Tab
        generate_report_tab = ttk.Frame(notebook)
        notebook.add(generate_report_tab, text='Generate Report')

        tk.Button(generate_report_tab, text="Generate Report", command=self.generate_report).grid(row=0, column=0, padx=10, pady=10)

        # Pending Requests Tab
        pending_requests_tab = ttk.Frame(notebook)
        notebook.add(pending_requests_tab, text='Pending Requests')

        self.pending_requests_list = tk.Listbox(pending_requests_tab, width=100)
        self.pending_requests_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(pending_requests_tab, text="Refresh", command=self.refresh_pending_requests).grid(row=1, column=0, padx=10, pady=10)

        # View All Employees Tab
        view_employees_tab = ttk.Frame(notebook)
        notebook.add(view_employees_tab, text='View All Employees')

        self.employees_list = tk.Listbox(view_employees_tab, width=100)
        self.employees_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_employees_tab, text="Refresh", command=self.refresh_employees).grid(row=1, column=0, padx=10, pady=10)

        # View All Requests Tab
        view_requests_tab = ttk.Frame(notebook)
        notebook.add(view_requests_tab, text='View All Requests')

        self.requests_list = tk.Listbox(view_requests_tab, width=100)
        self.requests_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_requests_tab, text="Refresh", command=self.refresh_requests).grid(row=1, column=0, padx=10, pady=10)

        self.refresh_pending_requests()
        self.refresh_employees()
        self.refresh_requests()

    def add_employee(self):
        name = self.employee_name.get()
        if name:
            add_employee(name)
            messagebox.showinfo("Success", "Employee added successfully.")
            self.refresh_employees()
        else:
            messagebox.showwarning("Input error", "Please enter a name.")

    def add_request(self):
        employee_id = self.employee_id.get()
        request_type = self.request_type.get()
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        if employee_id and request_type and start_date and end_date:
            add_request(employee_id, request_type, start_date, end_date)
            messagebox.showinfo("Success", "Request added successfully.")
            self.refresh_pending_requests()
            self.refresh_requests()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def update_request(self):
        request_id = self.request_id.get()
        status = self.status.get()
        if request_id and status:
            update_request(request_id, status)
            messagebox.showinfo("Success", "Request updated successfully.")
            self.refresh_pending_requests()
            self.refresh_requests()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def generate_report(self):
        report = generate_report()
        report_window = tk.Toplevel(self.root)
        report_window.title("Leave Report")
        text = tk.Text(report_window)
        text.pack()
        for row in report:
            text.insert(tk.END, f"{row}\n")

    def refresh_pending_requests(self):
        self.pending_requests_list.delete(0, tk.END)
        pending_requests = get_pending_requests()
        for request in pending_requests:
            self.pending_requests_list.insert(tk.END, f"ID: {request[0]}, Employee: {request[1]}, Type: {request[2]}, Start Date: {request[3]}, End Date: {request[4]}")

    def refresh_employees(self):
        self.employees_list.delete(0, tk.END)
        employees = get_all_employees()
        for employee in employees:
            self.employees_list.insert(tk.END, f"ID: {employee[0]}, Name: {employee[1]}")

    def refresh_requests(self):
        self.requests_list.delete(0, tk.END)
        requests = get_all_requests()
        for request in requests:
            self.requests_list.insert(tk.END, f"ID: {request[0]}, Employee: {request[1]}, Type: {request[2]}, Start Date: {request[3]}, End Date: {request[4]}, Status: {request[5]}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = TimeOffApp(root)
    root.mainloop()
