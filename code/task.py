import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime

# Initialize the database
def init_db():
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

# Add a task
def add_task(title, description, due_date):
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)", (title, description, due_date))
    conn.commit()
    conn.close()

# Update a task
def update_task(task_id, title, description, due_date, status):
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET title = ?, description = ?, due_date = ?, status = ? WHERE id = ?",
              (title, description, due_date, status, task_id))
    conn.commit()
    conn.close()

# Delete a task
def delete_task(task_id):
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Mark a task as complete
def mark_task_complete(task_id):
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Get all tasks
def get_all_tasks():
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    c.execute("SELECT id, title, description, due_date, status FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

# Tkinter GUI
class TaskManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")

        self.task_id = tk.IntVar()
        self.task_title = tk.StringVar()
        self.task_description = tk.StringVar()
        self.task_due_date = tk.StringVar()
        self.task_status = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill="both")

        # Add Task Tab
        add_task_tab = ttk.Frame(notebook)
        notebook.add(add_task_tab, text='Add Task')

        tk.Label(add_task_tab, text="Title:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(add_task_tab, textvariable=self.task_title).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(add_task_tab, text="Description:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(add_task_tab, textvariable=self.task_description).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(add_task_tab, text="Due Date:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(add_task_tab, textvariable=self.task_due_date).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(add_task_tab, text="Add Task", command=self.add_task).grid(row=3, column=1, padx=10, pady=10)

        # Update Task Tab
        update_task_tab = ttk.Frame(notebook)
        notebook.add(update_task_tab, text='Update Task')

        tk.Label(update_task_tab, text="Task ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(update_task_tab, textvariable=self.task_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(update_task_tab, text="Title:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(update_task_tab, textvariable=self.task_title).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(update_task_tab, text="Description:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(update_task_tab, textvariable=self.task_description).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(update_task_tab, text="Due Date:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(update_task_tab, textvariable=self.task_due_date).grid(row=3, column=1, padx=10, pady=10)
        tk.Label(update_task_tab, text="Status:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(update_task_tab, textvariable=self.task_status).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(update_task_tab, text="Update Task", command=self.update_task).grid(row=5, column=1, padx=10, pady=10)

        # Delete Task Tab
        delete_task_tab = ttk.Frame(notebook)
        notebook.add(delete_task_tab, text='Delete Task')

        tk.Label(delete_task_tab, text="Task ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(delete_task_tab, textvariable=self.task_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(delete_task_tab, text="Delete Task", command=self.delete_task).grid(row=1, column=1, padx=10, pady=10)

        # Mark Task as Complete Tab
        mark_complete_tab = ttk.Frame(notebook)
        notebook.add(mark_complete_tab, text='Mark Task as Complete')

        tk.Label(mark_complete_tab, text="Task ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(mark_complete_tab, textvariable=self.task_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(mark_complete_tab, text="Mark as Complete", command=self.mark_task_complete).grid(row=1, column=1, padx=10, pady=10)

        # View All Tasks Tab
        view_tasks_tab = ttk.Frame(notebook)
        notebook.add(view_tasks_tab, text='View All Tasks')

        self.tasks_list = tk.Listbox(view_tasks_tab, width=100)
        self.tasks_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_tasks_tab, text="Refresh", command=self.refresh_tasks).grid(row=1, column=0, padx=10, pady=10)

        self.refresh_tasks()

    def add_task(self):
        title = self.task_title.get()
        description = self.task_description.get()
        due_date = self.task_due_date.get()
        if title and description and due_date:
            add_task(title, description, due_date)
            messagebox.showinfo("Success", "Task added successfully.")
            self.refresh_tasks()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def update_task(self):
        task_id = self.task_id.get()
        title = self.task_title.get()
        description = self.task_description.get()
        due_date = self.task_due_date.get()
        status = self.task_status.get()
        if task_id and title and description and due_date and status:
            update_task(task_id, title, description, due_date, status)
            messagebox.showinfo("Success", "Task updated successfully.")
            self.refresh_tasks()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def delete_task(self):
        task_id = self.task_id.get()
        if task_id:
            delete_task(task_id)
            messagebox.showinfo("Success", "Task deleted successfully.")
            self.refresh_tasks()
        else:
            messagebox.showwarning("Input error", "Please enter a task ID.")

    def mark_task_complete(self):
        task_id = self.task_id.get()
        if task_id:
            mark_task_complete(task_id)
            messagebox.showinfo("Success", "Task marked as complete successfully.")
            self.refresh_tasks()
        else:
            messagebox.showwarning("Input error", "Please enter a task ID.")

    def refresh_tasks(self):
        self.tasks_list.delete(0, tk.END)
        tasks = get_all_tasks()
        for task in tasks:
            self.tasks_list.insert(tk.END, f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Due Date: {task[3]}, Status: {task[4]}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = TaskManagementApp(root)
    root.mainloop()
