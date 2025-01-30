import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime
import hashlib

# Database setup
conn = sqlite3.connect('project_management.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT,
                role TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id))''')
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                name TEXT,
                description TEXT,
                status TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(project_id))''')
c.execute('''CREATE TABLE IF NOT EXISTS team_members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY(project_id) REFERENCES projects(project_id),
                FOREIGN KEY(user_id) REFERENCES users(user_id))''')
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

def create_project(user_id):
    name = project_name_entry.get()
    description = project_description_entry.get()
    start_date = project_start_date_entry.get()
    end_date = project_end_date_entry.get()
    status = "Not Started"
    c.execute("INSERT INTO projects (name, description, start_date, end_date, status, user_id) VALUES (?, ?, ?, ?, ?, ?)",
              (name, description, start_date, end_date, status, user_id))
    conn.commit()
    messagebox.showinfo("Success", "Project created successfully!")

def view_projects(user_id):
    c.execute("SELECT project_id, name, description, start_date, end_date, status FROM projects WHERE user_id = ?", (user_id,))
    projects = c.fetchall()
    project_info = "Your Projects:\n"
    for project in projects:
        project_info += f"Project ID: {project[0]}, Name: {project[1]}, Description: {project[2]}, Start Date: {project[3]}, End Date: {project[4]}, Status: {project[5]}\n"
    messagebox.showinfo("Projects", project_info)

def delete_project(user_id):
    project_id = int(project_id_entry.get())
    c.execute("DELETE FROM projects WHERE project_id = ? AND user_id = ?", (project_id, user_id))
    conn.commit()
    messagebox.showinfo("Success", "Project deleted successfully!")

def add_task(project_id):
    name = task_name_entry.get()
    description = task_description_entry.get()
    status = "Not Started"
    c.execute("INSERT INTO tasks (project_id, name, description, status) VALUES (?, ?, ?, ?)", (project_id, name, description, status))
    conn.commit()
    messagebox.showinfo("Success", "Task added successfully!")

def view_tasks(project_id):
    c.execute("SELECT task_id, name, description, status FROM tasks WHERE project_id = ?", (project_id,))
    tasks = c.fetchall()
    task_info = "Tasks:\n"
    for task in tasks:
        task_info += f"Task ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Status: {task[3]}\n"
    messagebox.showinfo("Tasks", task_info)

def update_task(task_id):
    status = task_status_entry.get()
    c.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (status, task_id))
    conn.commit()
    messagebox.showinfo("Success", "Task updated successfully!")

def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    conn.commit()
    messagebox.showinfo("Success", "Task deleted successfully!")

def add_team_member(project_id, user_id):
    member_username = member_username_entry.get()
    c.execute("SELECT user_id FROM users WHERE username = ?", (member_username,))
    member = c.fetchone()
    if member:
        member_id = member[0]
        c.execute("INSERT INTO team_members (project_id, user_id) VALUES (?, ?)", (project_id, member_id))
        conn.commit()
        messagebox.showinfo("Success", "Team member added successfully!")
    else:
        messagebox.showerror("Error", "User not found!")

def view_team_members(project_id):
    c.execute("SELECT u.username, u.email, u.role FROM team_members tm JOIN users u ON tm.user_id = u.user_id WHERE tm.project_id = ?", (project_id,))
    members = c.fetchall()
    member_info = "Team Members:\n"
    for member in members:
        member_info += f"Username: {member[0]}, Email: {member[1]}, Role: {member[2]}\n"
    messagebox.showinfo("Team Members", member_info)

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
            c.execute("SELECT p.project_id, p.name, COUNT(t.task_id) FROM projects p LEFT JOIN tasks t ON p.project_id = t.project_id GROUP BY p.project_id")
            report = c.fetchall()
            report_info = "Project Report:\n"
            for row in report:
                report_info += f"Project ID: {row[0]}, Project Name: {row[1]}, Number of Tasks: {row[2]}\n"
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
root.title("Project Management System")

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

        project_tab = ttk.Frame(notebook)
        task_tab = ttk.Frame(notebook)
        team_tab = ttk.Frame(notebook)
        admin_tab = ttk.Frame(notebook)

        notebook.add(project_tab, text="Project Management")
        notebook.add(task_tab, text="Task Management")
        notebook.add(team_tab, text="Team Management")
        if role == "admin":
            notebook.add(admin_tab, text="Admin Panel")

        # Project Management Tab
        tk.Label(project_tab, text="Create Project", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(project_tab, text="Project Name").pack()
        global project_name_entry
        project_name_entry = tk.Entry(project_tab)
        project_name_entry.pack()
        tk.Label(project_tab, text="Description").pack()
        global project_description_entry
        project_description_entry = tk.Entry(project_tab)
        project_description_entry.pack()
        tk.Label(project_tab, text="Start Date (YYYY-MM-DD)").pack()
        global project_start_date_entry
        project_start_date_entry = tk.Entry(project_tab)
        project_start_date_entry.pack()
        tk.Label(project_tab, text="End Date (YYYY-MM-DD)").pack()
        global project_end_date_entry
        project_end_date_entry = tk.Entry(project_tab)
        project_end_date_entry.pack()
        create_project_button = tk.Button(project_tab, text="Create Project", command=lambda: create_project(user_id))
        create_project_button.pack(pady=10)

        view_projects_button = tk.Button(project_tab, text="View Projects", command=lambda: view_projects(user_id))
        view_projects_button.pack(pady=10)

        tk.Label(project_tab, text="Delete Project", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(project_tab, text="Project ID").pack()
        global project_id_entry
        project_id_entry = tk.Entry(project_tab)
        project_id_entry.pack()
        delete_project_button = tk.Button(project_tab, text="Delete Project", command=lambda: delete_project(user_id))
        delete_project_button.pack(pady=10)

        # Task Management Tab
        tk.Label(task_tab, text="Add Task", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(task_tab, text="Project ID").pack()
        global task_project_id_entry
        task_project_id_entry = tk.Entry(task_tab)
        task_project_id_entry.pack()
        tk.Label(task_tab, text="Task Name").pack()
        global task_name_entry
        task_name_entry = tk.Entry(task_tab)
        task_name_entry.pack()
        tk.Label(task_tab, text="Description").pack()
        global task_description_entry
        task_description_entry = tk.Entry(task_tab)
        task_description_entry.pack()
        add_task_button = tk.Button(task_tab, text="Add Task", command=lambda: add_task(int(task_project_id_entry.get())))
        add_task_button.pack(pady=10)

        tk.Label(task_tab, text="View Tasks", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(task_tab, text="Project ID").pack()
        global view_tasks_project_id_entry
        view_tasks_project_id_entry = tk.Entry(task_tab)
        view_tasks_project_id_entry.pack()
        view_tasks_button = tk.Button(task_tab, text="View Tasks", command=lambda: view_tasks(int(view_tasks_project_id_entry.get())))
        view_tasks_button.pack(pady=10)

        tk.Label(task_tab, text="Update Task", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(task_tab, text="Task ID").pack()
        global task_id_entry
        task_id_entry = tk.Entry(task_tab)
        task_id_entry.pack()
        tk.Label(task_tab, text="Status").pack()
        global task_status_entry
        task_status_entry = tk.Entry(task_tab)
        task_status_entry.pack()
        update_task_button = tk.Button(task_tab, text="Update Task", command=lambda: update_task(int(task_id_entry.get())))
        update_task_button.pack(pady=10)

        tk.Label(task_tab, text="Delete Task", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(task_tab, text="Task ID").pack()
        global delete_task_id_entry
        delete_task_id_entry = tk.Entry(task_tab)
        delete_task_id_entry.pack()
        delete_task_button = tk.Button(task_tab, text="Delete Task", command=lambda: delete_task(int(delete_task_id_entry.get())))
        delete_task_button.pack(pady=10)

        # Team Management Tab
        tk.Label(team_tab, text="Add Team Member", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(team_tab, text="Project ID").pack()
        global team_project_id_entry
        team_project_id_entry = tk.Entry(team_tab)
        team_project_id_entry.pack()
        tk.Label(team_tab, text="Member Username").pack()
        global member_username_entry
        member_username_entry = tk.Entry(team_tab)
        member_username_entry.pack()
        add_team_member_button = tk.Button(team_tab, text="Add Team Member", command=lambda: add_team_member(int(team_project_id_entry.get()), user_id))
        add_team_member_button.pack(pady=10)

        tk.Label(team_tab, text="View Team Members", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(team_tab, text="Project ID").pack()
        global view_team_project_id_entry
        view_team_project_id_entry = tk.Entry(team_tab)
        view_team_project_id_entry.pack()
        view_team_members_button = tk.Button(team_tab, text="View Team Members", command=lambda: view_team_members(int(view_team_project_id_entry.get())))
        view_team_members_button.pack(pady=10)

        # Admin Panel Tab
        if role == "admin":
            admin_button = tk.Button(admin_tab, text="Admin Panel", command=admin_panel)
            admin_button.pack(pady=10)

        logout_button = tk.Button(root, text="Logout", command=main_menu)
        logout_button.pack(pady=10)
    else:
        tk.Label(root, text="Project Management System", font=("Helvetica", 16)).pack(pady=10)

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
