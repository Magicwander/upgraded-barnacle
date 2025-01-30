import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime, timedelta

# Database setup
conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS checkouts (
                checkout_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                book_id INTEGER,
                checkout_date TEXT,
                return_date TEXT,
                FOREIGN KEY(student_id) REFERENCES students(student_id),
                FOREIGN KEY(book_id) REFERENCES books(book_id))''')

conn.commit()

# GUI setup
root = tk.Tk()
root.title("Student Library Access System")
root.geometry("800x800")

# Styles
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", foreground="#000")
style.configure("TLabel", padding=6, background="#fff", foreground="#000")
style.configure("TFrame", padding=6, background="#fff")

# Functions
def add_student():
    student_id = int(student_id_entry.get())
    name = student_name_entry.get()
    c.execute("INSERT INTO students (student_id, name) VALUES (?, ?)", (student_id, name))
    conn.commit()
    messagebox.showinfo("Success", "Student added successfully")
    clear_entries()

def add_book():
    book_id = int(book_id_entry.get())
    title = book_title_entry.get()
    c.execute("INSERT INTO books (book_id, title) VALUES (?, ?)", (book_id, title))
    conn.commit()
    messagebox.showinfo("Success", "Book added successfully")
    clear_entries()

def checkout_book():
    student_id = int(checkout_student_id_entry.get())
    book_id = int(checkout_book_id_entry.get())
    checkout_date = datetime.now().strftime("%Y-%m-%d")
    return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    c.execute("INSERT INTO checkouts (student_id, book_id, checkout_date, return_date) VALUES (?, ?, ?, ?)",
              (student_id, book_id, checkout_date, return_date))
    conn.commit()
    messagebox.showinfo("Success", "Book checked out successfully")
    clear_entries()

def return_book():
    checkout_id = int(return_checkout_id_entry.get())
    c.execute("UPDATE checkouts SET return_date = ? WHERE checkout_id = ?",
              (datetime.now().strftime("%Y-%m-%d"), checkout_id))
    conn.commit()
    messagebox.showinfo("Success", "Book returned successfully")
    clear_entries()

def generate_report():
    report_type = report_type_var.get()
    report_text.delete(1.0, tk.END)
    if report_type == "Overdue":
        c.execute("SELECT students.name, books.title, checkouts.checkout_date, checkouts.return_date "
                  "FROM checkouts "
                  "JOIN students ON checkouts.student_id = students.student_id "
                  "JOIN books ON checkouts.book_id = books.book_id "
                  "WHERE checkouts.return_date < ? AND checkouts.return_date IS NOT NULL",
                  (datetime.now().strftime("%Y-%m-%d"),))
    elif report_type == "Access":
        c.execute("SELECT students.name, books.title, checkouts.checkout_date, checkouts.return_date "
                  "FROM checkouts "
                  "JOIN students ON checkouts.student_id = students.student_id "
                  "JOIN books ON checkouts.book_id = books.book_id")

    report_data = c.fetchall()
    for row in report_data:
        report_text.insert(tk.END, f"Student: {row[0]}, Book: {row[1]}, Checkout Date: {row[2]}, Return Date: {row[3]}\n")

def search_student():
    student_id = int(search_student_id_entry.get())
    c.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    student_data = c.fetchone()
    if student_data:
        messagebox.showinfo("Student Info", f"Student ID: {student_data[0]}, Name: {student_data[1]}")
    else:
        messagebox.showinfo("Student Info", "Student not found")
    clear_entries()

def search_book():
    book_id = int(search_book_id_entry.get())
    c.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    book_data = c.fetchone()
    if book_data:
        messagebox.showinfo("Book Info", f"Book ID: {book_data[0]}, Title: {book_data[1]}")
    else:
        messagebox.showinfo("Book Info", "Book not found")
    clear_entries()

def update_student():
    student_id = int(update_student_id_entry.get())
    name = update_student_name_entry.get()
    c.execute("UPDATE students SET name = ? WHERE student_id = ?", (name, student_id))
    conn.commit()
    messagebox.showinfo("Success", "Student updated successfully")
    clear_entries()

def update_book():
    book_id = int(update_book_id_entry.get())
    title = update_book_title_entry.get()
    c.execute("UPDATE books SET title = ? WHERE book_id = ?", (title, book_id))
    conn.commit()
    messagebox.showinfo("Success", "Book updated successfully")
    clear_entries()

def delete_student():
    student_id = int(delete_student_id_entry.get())
    c.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    messagebox.showinfo("Success", "Student deleted successfully")
    clear_entries()

def delete_book():
    book_id = int(delete_book_id_entry.get())
    c.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    conn.commit()
    messagebox.showinfo("Success", "Book deleted successfully")
    clear_entries()

def clear_entries():
    student_id_entry.delete(0, tk.END)
    student_name_entry.delete(0, tk.END)
    book_id_entry.delete(0, tk.END)
    book_title_entry.delete(0, tk.END)
    checkout_student_id_entry.delete(0, tk.END)
    checkout_book_id_entry.delete(0, tk.END)
    return_checkout_id_entry.delete(0, tk.END)
    search_student_id_entry.delete(0, tk.END)
    search_book_id_entry.delete(0, tk.END)
    update_student_id_entry.delete(0, tk.END)
    update_student_name_entry.delete(0, tk.END)
    update_book_id_entry.delete(0, tk.END)
    update_book_title_entry.delete(0, tk.END)
    delete_student_id_entry.delete(0, tk.END)
    delete_book_id_entry.delete(0, tk.END)

# Frames
student_frame = ttk.LabelFrame(root, text="Add Student")
student_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

book_frame = ttk.LabelFrame(root, text="Add Book")
book_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

checkout_frame = ttk.LabelFrame(root, text="Checkout Book")
checkout_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

return_frame = ttk.LabelFrame(root, text="Return Book")
return_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

search_frame = ttk.LabelFrame(root, text="Search")
search_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

update_frame = ttk.LabelFrame(root, text="Update")
update_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

delete_frame = ttk.LabelFrame(root, text="Delete")
delete_frame.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

report_frame = ttk.LabelFrame(root, text="Generate Report")
report_frame.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

# Student Frame
ttk.Label(student_frame, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
student_id_entry = ttk.Entry(student_frame)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(student_frame, text="Student Name").grid(row=1, column=0, padx=5, pady=5)
student_name_entry = ttk.Entry(student_frame)
student_name_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(student_frame, text="Add Student", command=add_student).grid(row=2, column=0, columnspan=2, pady=5)

# Book Frame
ttk.Label(book_frame, text="Book ID").grid(row=0, column=0, padx=5, pady=5)
book_id_entry = ttk.Entry(book_frame)
book_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(book_frame, text="Book Title").grid(row=1, column=0, padx=5, pady=5)
book_title_entry = ttk.Entry(book_frame)
book_title_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(book_frame, text="Add Book", command=add_book).grid(row=2, column=0, columnspan=2, pady=5)

# Checkout Frame
ttk.Label(checkout_frame, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
checkout_student_id_entry = ttk.Entry(checkout_frame)
checkout_student_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(checkout_frame, text="Book ID").grid(row=1, column=0, padx=5, pady=5)
checkout_book_id_entry = ttk.Entry(checkout_frame)
checkout_book_id_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(checkout_frame, text="Checkout Book", command=checkout_book).grid(row=2, column=0, columnspan=2, pady=5)

# Return Frame
ttk.Label(return_frame, text="Checkout ID").grid(row=0, column=0, padx=5, pady=5)
return_checkout_id_entry = ttk.Entry(return_frame)
return_checkout_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Button(return_frame, text="Return Book", command=return_book).grid(row=1, column=0, columnspan=2, pady=5)

# Search Frame
ttk.Label(search_frame, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
search_student_id_entry = ttk.Entry(search_frame)
search_student_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Button(search_frame, text="Search Student", command=search_student).grid(row=0, column=2, pady=5)

ttk.Label(search_frame, text="Book ID").grid(row=1, column=0, padx=5, pady=5)
search_book_id_entry = ttk.Entry(search_frame)
search_book_id_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(search_frame, text="Search Book", command=search_book).grid(row=1, column=2, pady=5)

# Update Frame
ttk.Label(update_frame, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
update_student_id_entry = ttk.Entry(update_frame)
update_student_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(update_frame, text="Student Name").grid(row=1, column=0, padx=5, pady=5)
update_student_name_entry = ttk.Entry(update_frame)
update_student_name_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(update_frame, text="Update Student", command=update_student).grid(row=2, column=0, columnspan=2, pady=5)

ttk.Label(update_frame, text="Book ID").grid(row=3, column=0, padx=5, pady=5)
update_book_id_entry = ttk.Entry(update_frame)
update_book_id_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(update_frame, text="Book Title").grid(row=4, column=0, padx=5, pady=5)
update_book_title_entry = ttk.Entry(update_frame)
update_book_title_entry.grid(row=4, column=1, padx=5, pady=5)

ttk.Button(update_frame, text="Update Book", command=update_book).grid(row=5, column=0, columnspan=2, pady=5)

# Delete Frame
ttk.Label(delete_frame, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
delete_student_id_entry = ttk.Entry(delete_frame)
delete_student_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Button(delete_frame, text="Delete Student", command=delete_student).grid(row=0, column=2, pady=5)

ttk.Label(delete_frame, text="Book ID").grid(row=1, column=0, padx=5, pady=5)
delete_book_id_entry = ttk.Entry(delete_frame)
delete_book_id_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(delete_frame, text="Delete Book", command=delete_book).grid(row=1, column=2, pady=5)

# Report Frame
ttk.Label(report_frame, text="Report Type").grid(row=0, column=0, padx=5, pady=5)
report_type_var = tk.StringVar(value="Overdue")
ttk.OptionMenu(report_frame, report_type_var, "Overdue", "Access").grid(row=0, column=1, padx=5, pady=5)

ttk.Button(report_frame, text="Generate Report", command=generate_report).grid(row=1, column=0, columnspan=2, pady=5)

report_text = tk.Text(report_frame, height=10, width=50)
report_text.grid(row=2, column=0, columnspan=2, pady=5)

root.mainloop()

# Close the database connection
conn.close()
