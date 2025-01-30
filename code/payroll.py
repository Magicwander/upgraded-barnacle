import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY, name TEXT, position TEXT, salary REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY, employee_id INTEGER, date TEXT, status TEXT,
                 FOREIGN KEY(employee_id) REFERENCES employees(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS salaries
                 (id INTEGER PRIMARY KEY, employee_id INTEGER, month TEXT, amount REAL,
                 FOREIGN KEY(employee_id) REFERENCES employees(id))''')
    conn.commit()
    conn.close()

# Add a new employee
def add_employee():
    name = entry_name.get()
    position = entry_position.get()
    salary = entry_salary.get()
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)",
              (name, position, salary))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Employee added successfully!")
    clear_entries()
    view_employees()

# Update employee information
def update_employee():
    name = entry_name.get()
    position = entry_position.get()
    salary = entry_salary.get()
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("UPDATE employees SET position = ?, salary = ? WHERE name = ?", (position, salary, name))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Employee information updated successfully!")
    clear_entries()
    view_employees()

# Delete an employee
def delete_employee():
    name = entry_name.get()
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Employee deleted successfully!")
    clear_entries()
    view_employees()

# Search for an employee by name
def search_employee():
    name = entry_name.get()
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE name = ?", (name,))
    rows = c.fetchall()
    conn.close()
    if rows:
        messagebox.showinfo("Employee Found", f"Name: {rows[0][1]}, Position: {rows[0][2]}, Salary: {rows[0][3]}")
    else:
        messagebox.showinfo("Employee Not Found", "No employee found with the given name.")

# Record employee attendance
def record_attendance():
    name = entry_name.get()
    date = entry_date.get()
    status = entry_status.get()
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("SELECT id FROM employees WHERE name = ?", (name,))
    employee_id = c.fetchone()[0]
    c.execute("INSERT INTO attendance (employee_id, date, status) VALUES (?, ?, ?)",
              (employee_id, date, status))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Attendance recorded successfully!")
    clear_entries()
    view_attendance()

# Calculate and record employee salary
def calculate_salary():
    name = entry_name.get()
    month = entry_month.get()
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("SELECT id, salary FROM employees WHERE name = ?", (name,))
    employee_data = c.fetchone()
    employee_id, base_salary = employee_data[0], employee_data[1]

    c.execute("SELECT COUNT(*) FROM attendance WHERE employee_id = ? AND status = 'Present' AND strftime('%Y-%m', date) = ?",
              (employee_id, month))
    present_days = c.fetchone()[0]

    amount = base_salary * (present_days / 30)  # Simplified salary calculation
    c.execute("INSERT INTO salaries (employee_id, month, amount) VALUES (?, ?, ?)",
              (employee_id, month, amount))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Salary calculated and recorded successfully!")
    clear_entries()
    view_salaries()

# View employees in a table
def view_employees():
    for i in tree_employees.get_children():
        tree_employees.delete(i)
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_employees.insert("", "end", values=row)

# View attendance in a table
def view_attendance():
    for i in tree_attendance.get_children():
        tree_attendance.delete(i)
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_attendance.insert("", "end", values=row)

# View salaries in a table
def view_salaries():
    for i in tree_salaries.get_children():
        tree_salaries.delete(i)
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("SELECT * FROM salaries")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_salaries.insert("", "end", values=row)

# Clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_salary.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_status.delete(0, tk.END)
    entry_month.delete(0, tk.END)

# Create the main application window
root = tk.Tk()
root.title("Payroll Management System")

# Initialize the database
init_db()

# Create and place widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_name = ttk.Entry(frame)
entry_name.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Position:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_position = ttk.Entry(frame)
entry_position.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Salary:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_salary = ttk.Entry(frame)
entry_salary.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=5)
entry_date = ttk.Entry(frame)
entry_date.grid(row=3, column=1, pady=5)

ttk.Label(frame, text="Status:").grid(row=4, column=0, sticky=tk.W, pady=5)
entry_status = ttk.Entry(frame)
entry_status.grid(row=4, column=1, pady=5)

ttk.Label(frame, text="Month (YYYY-MM):").grid(row=5, column=0, sticky=tk.W, pady=5)
entry_month = ttk.Entry(frame)
entry_month.grid(row=5, column=1, pady=5)

ttk.Button(frame, text="Add Employee", command=add_employee).grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Update Employee", command=update_employee).grid(row=7, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Delete Employee", command=delete_employee).grid(row=8, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Search Employee", command=search_employee).grid(row=9, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Record Attendance", command=record_attendance).grid(row=10, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Calculate Salary", command=calculate_salary).grid(row=11, column=0, columnspan=2, pady=5)

# Create treeviews for displaying tables
tree_employees = ttk.Treeview(frame, columns=("ID", "Name", "Position", "Salary"), show='headings')
tree_employees.heading("ID", text="ID")
tree_employees.heading("Name", text="Name")
tree_employees.heading("Position", text="Position")
tree_employees.heading("Salary", text="Salary")
tree_employees.grid(row=12, column=0, columnspan=2, pady=5)

tree_attendance = ttk.Treeview(frame, columns=("ID", "Employee ID", "Date", "Status"), show='headings')
tree_attendance.heading("ID", text="ID")
tree_attendance.heading("Employee ID", text="Employee ID")
tree_attendance.heading("Date", text="Date")
tree_attendance.heading("Status", text="Status")
tree_attendance.grid(row=13, column=0, columnspan=2, pady=5)

tree_salaries = ttk.Treeview(frame, columns=("ID", "Employee ID", "Month", "Amount"), show='headings')
tree_salaries.heading("ID", text="ID")
tree_salaries.heading("Employee ID", text="Employee ID")
tree_salaries.heading("Month", text="Month")
tree_salaries.heading("Amount", text="Amount")
tree_salaries.grid(row=14, column=0, columnspan=2, pady=5)

# View initial data
view_employees()
view_attendance()
view_salaries()

# Run the application
root.mainloop()
