import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime, timedelta

# Initialize the database
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY,
                    book_id INTEGER,
                    member_id INTEGER,
                    loan_date TEXT,
                    due_date TEXT,
                    return_date TEXT,
                    FOREIGN KEY(book_id) REFERENCES books(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS fines (
                    id INTEGER PRIMARY KEY,
                    loan_id INTEGER,
                    amount REAL,
                    paid BOOLEAN,
                    FOREIGN KEY(loan_id) REFERENCES loans(id))''')
    conn.commit()
    conn.close()

# Add a book
def add_book(title, author):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

# Add a member
def add_member(name):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO members (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# Loan a book
def loan_book(book_id, member_id, loan_date, due_date):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("INSERT INTO loans (book_id, member_id, loan_date, due_date) VALUES (?, ?, ?, ?)",
              (book_id, member_id, loan_date, due_date))
    conn.commit()
    conn.close()

# Return a book
def return_book(loan_id, return_date):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("UPDATE loans SET return_date = ? WHERE id = ?", (return_date, loan_id))
    conn.commit()
    conn.close()

# Calculate fine
def calculate_fine(loan_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT due_date, return_date FROM loans WHERE id = ?", (loan_id,))
    loan = c.fetchone()
    due_date = datetime.strptime(loan[0], '%Y-%m-%d')
    return_date = datetime.strptime(loan[1], '%Y-%m-%d') if loan[1] else datetime.now()
    if return_date > due_date:
        days_overdue = (return_date - due_date).days
        fine_amount = days_overdue * 0.5  # Assume fine is $0.50 per day
        c.execute("INSERT INTO fines (loan_id, amount, paid) VALUES (?, ?, ?)", (loan_id, fine_amount, False))
        conn.commit()
    conn.close()

# Pay fine
def pay_fine(fine_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("UPDATE fines SET paid = ? WHERE id = ?", (True, fine_id))
    conn.commit()
    conn.close()

# Get all books
def get_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT id, title, author FROM books")
    books = c.fetchall()
    conn.close()
    return books

# Get all members
def get_all_members():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM members")
    members = c.fetchall()
    conn.close()
    return members

# Get all loans
def get_all_loans():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT loans.id, books.title, members.name, loans.loan_date, loans.due_date, loans.return_date FROM loans JOIN books ON loans.book_id = books.id JOIN members ON loans.member_id = members.id")
    loans = c.fetchall()
    conn.close()
    return loans

# Get all fines
def get_all_fines():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT fines.id, loans.id, members.name, fines.amount, fines.paid FROM fines JOIN loans ON fines.loan_id = loans.id JOIN members ON loans.member_id = members.id")
    fines = c.fetchall()
    conn.close()
    return fines

# Tkinter GUI
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Fine Management System")

        self.book_title = tk.StringVar()
        self.book_author = tk.StringVar()
        self.member_name = tk.StringVar()
        self.book_id = tk.IntVar()
        self.member_id = tk.IntVar()
        self.loan_date = tk.StringVar()
        self.due_date = tk.StringVar()
        self.return_date = tk.StringVar()
        self.loan_id = tk.IntVar()
        self.fine_id = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill="both")

        # Add Book Tab
        add_book_tab = ttk.Frame(notebook)
        notebook.add(add_book_tab, text='Add Book')

        tk.Label(add_book_tab, text="Title:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(add_book_tab, textvariable=self.book_title).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(add_book_tab, text="Author:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(add_book_tab, textvariable=self.book_author).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(add_book_tab, text="Add Book", command=self.add_book).grid(row=2, column=1, padx=10, pady=10)

        # Add Member Tab
        add_member_tab = ttk.Frame(notebook)
        notebook.add(add_member_tab, text='Add Member')

        tk.Label(add_member_tab, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(add_member_tab, textvariable=self.member_name).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(add_member_tab, text="Add Member", command=self.add_member).grid(row=1, column=1, padx=10, pady=10)

        # Loan Book Tab
        loan_book_tab = ttk.Frame(notebook)
        notebook.add(loan_book_tab, text='Loan Book')

        tk.Label(loan_book_tab, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(loan_book_tab, textvariable=self.book_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(loan_book_tab, text="Member ID:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(loan_book_tab, textvariable=self.member_id).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(loan_book_tab, text="Loan Date:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(loan_book_tab, textvariable=self.loan_date).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(loan_book_tab, text="Due Date:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(loan_book_tab, textvariable=self.due_date).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(loan_book_tab, text="Loan Book", command=self.loan_book).grid(row=4, column=1, padx=10, pady=10)

        # Return Book Tab
        return_book_tab = ttk.Frame(notebook)
        notebook.add(return_book_tab, text='Return Book')

        tk.Label(return_book_tab, text="Loan ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(return_book_tab, textvariable=self.loan_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(return_book_tab, text="Return Date:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(return_book_tab, textvariable=self.return_date).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(return_book_tab, text="Return Book", command=self.return_book).grid(row=2, column=1, padx=10, pady=10)

        # Calculate Fine Tab
        calculate_fine_tab = ttk.Frame(notebook)
        notebook.add(calculate_fine_tab, text='Calculate Fine')

        tk.Label(calculate_fine_tab, text="Loan ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(calculate_fine_tab, textvariable=self.loan_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(calculate_fine_tab, text="Calculate Fine", command=self.calculate_fine).grid(row=1, column=1, padx=10, pady=10)

        # Pay Fine Tab
        pay_fine_tab = ttk.Frame(notebook)
        notebook.add(pay_fine_tab, text='Pay Fine')

        tk.Label(pay_fine_tab, text="Fine ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(pay_fine_tab, textvariable=self.fine_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(pay_fine_tab, text="Pay Fine", command=self.pay_fine).grid(row=1, column=1, padx=10, pady=10)

        # View All Books Tab
        view_books_tab = ttk.Frame(notebook)
        notebook.add(view_books_tab, text='View All Books')

        self.books_list = tk.Listbox(view_books_tab, width=100)
        self.books_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_books_tab, text="Refresh", command=self.refresh_books).grid(row=1, column=0, padx=10, pady=10)

        # View All Members Tab
        view_members_tab = ttk.Frame(notebook)
        notebook.add(view_members_tab, text='View All Members')

        self.members_list = tk.Listbox(view_members_tab, width=100)
        self.members_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_members_tab, text="Refresh", command=self.refresh_members).grid(row=1, column=0, padx=10, pady=10)

        # View All Loans Tab
        view_loans_tab = ttk.Frame(notebook)
        notebook.add(view_loans_tab, text='View All Loans')

        self.loans_list = tk.Listbox(view_loans_tab, width=100)
        self.loans_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_loans_tab, text="Refresh", command=self.refresh_loans).grid(row=1, column=0, padx=10, pady=10)

        # View All Fines Tab
        view_fines_tab = ttk.Frame(notebook)
        notebook.add(view_fines_tab, text='View All Fines')

        self.fines_list = tk.Listbox(view_fines_tab, width=100)
        self.fines_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_fines_tab, text="Refresh", command=self.refresh_fines).grid(row=1, column=0, padx=10, pady=10)

        self.refresh_books()
        self.refresh_members()
        self.refresh_loans()
        self.refresh_fines()

    def add_book(self):
        title = self.book_title.get()
        author = self.book_author.get()
        if title and author:
            add_book(title, author)
            messagebox.showinfo("Success", "Book added successfully.")
            self.refresh_books()
        else:
            messagebox.showwarning("Input error", "Please enter title and author.")

    def add_member(self):
        name = self.member_name.get()
        if name:
            add_member(name)
            messagebox.showinfo("Success", "Member added successfully.")
            self.refresh_members()
        else:
            messagebox.showwarning("Input error", "Please enter a name.")

    def loan_book(self):
        book_id = self.book_id.get()
        member_id = self.member_id.get()
        loan_date = self.loan_date.get()
        due_date = self.due_date.get()
        if book_id and member_id and loan_date and due_date:
            loan_book(book_id, member_id, loan_date, due_date)
            messagebox.showinfo("Success", "Book loaned successfully.")
            self.refresh_loans()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def return_book(self):
        loan_id = self.loan_id.get()
        return_date = self.return_date.get()
        if loan_id and return_date:
            return_book(loan_id, return_date)
            messagebox.showinfo("Success", "Book returned successfully.")
            self.refresh_loans()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def calculate_fine(self):
        loan_id = self.loan_id.get()
        if loan_id:
            calculate_fine(loan_id)
            messagebox.showinfo("Success", "Fine calculated successfully.")
            self.refresh_fines()
        else:
            messagebox.showwarning("Input error", "Please enter a loan ID.")

    def pay_fine(self):
        fine_id = self.fine_id.get()
        if fine_id:
            pay_fine(fine_id)
            messagebox.showinfo("Success", "Fine paid successfully.")
            self.refresh_fines()
        else:
            messagebox.showwarning("Input error", "Please enter a fine ID.")

    def refresh_books(self):
        self.books_list.delete(0, tk.END)
        books = get_all_books()
        for book in books:
            self.books_list.insert(tk.END, f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}")

    def refresh_members(self):
        self.members_list.delete(0, tk.END)
        members = get_all_members()
        for member in members:
            self.members_list.insert(tk.END, f"ID: {member[0]}, Name: {member[1]}")

    def refresh_loans(self):
        self.loans_list.delete(0, tk.END)
        loans = get_all_loans()
        for loan in loans:
            self.loans_list.insert(tk.END, f"ID: {loan[0]}, Book: {loan[1]}, Member: {loan[2]}, Loan Date: {loan[3]}, Due Date: {loan[4]}, Return Date: {loan[5]}")

    def refresh_fines(self):
        self.fines_list.delete(0, tk.END)
        fines = get_all_fines()
        for fine in fines:
            self.fines_list.insert(tk.END, f"ID: {fine[0]}, Loan ID: {fine[1]}, Member: {fine[2]}, Amount: {fine[3]}, Paid: {fine[4]}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
