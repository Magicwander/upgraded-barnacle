import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('library_catalog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            available INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowings (
            borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            borrower_name TEXT,
            borrow_date TEXT,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books (book_id)
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a book
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()
    conn = sqlite3.connect('library_catalog.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, genre, available) VALUES (?, ?, ?, ?)', (title, author, genre, 1))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book added successfully!")
    clear_entries()

# Function to update a book
def update_book():
    book_id = update_book_id_entry.get()
    title = update_title_entry.get()
    author = update_author_entry.get()
    genre = update_genre_entry.get()
    conn = sqlite3.connect('library_catalog.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET title=?, author=?, genre=? WHERE book_id=?', (title, author, genre, book_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book updated successfully!")
    clear_entries()

# Function to view the catalog
def view_catalog():
    conn = sqlite3.connect('library_catalog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    catalog = ""
    for book in books:
        catalog += f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Available: {'Yes' if book[4] else 'No'}\n"
    messagebox.showinfo("Catalog", catalog)

# Function to search books
def search_books():
    keyword = search_entry.get()
    conn = sqlite3.connect('library_catalog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ?', ('%' + keyword + '%', '%' + keyword + '%'))
    books = cursor.fetchall()
    conn.close()
    results = ""
    for book in books:
        results += f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Available: {'Yes' if book[4] else 'No'}\n"
    messagebox.showinfo("Search Results", results)
    clear_entries()

# Function to borrow a book
def borrow_book():
    book_id = borrow_book_id_entry.get()
    borrower_name = borrower_name_entry.get()
    borrow_date = borrow_date_entry.get()
    conn = sqlite3.connect('library_catalog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT available FROM books WHERE book_id = ?', (book_id,))
    available = cursor.fetchone()[0]
    if available:
        cursor.execute('UPDATE books SET available=? WHERE book_id=?', (0, book_id))
        cursor.execute('INSERT INTO borrowings (book_id, borrower_name, borrow_date, return_date) VALUES (?, ?, ?, ?)',
                       (book_id, borrower_name, borrow_date, ''))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book borrowed successfully!")
    else:
        messagebox.showerror("Error", "Book is not available!")
    clear_entries()

# Function to return a book
def return_book():
    borrow_id = return_borrow_id_entry.get()
    return_date = return_date_entry.get()
    conn = sqlite3.connect('library_catalog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT book_id FROM borrowings WHERE borrow_id = ?', (borrow_id,))
    book_id = cursor.fetchone()[0]
    cursor.execute('UPDATE books SET available=? WHERE book_id=?', (1, book_id))
    cursor.execute('UPDATE borrowings SET return_date=? WHERE borrow_id=?', (return_date, borrow_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book returned successfully!")
    clear_entries()

# Function to clear entries
def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    update_book_id_entry.delete(0, tk.END)
    update_title_entry.delete(0, tk.END)
    update_author_entry.delete(0, tk.END)
    update_genre_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)
    borrow_book_id_entry.delete(0, tk.END)
    borrower_name_entry.delete(0, tk.END)
    borrow_date_entry.delete(0, tk.END)
    return_borrow_id_entry.delete(0, tk.END)
    return_date_entry.delete(0, tk.END)

# Initialize the database
init_db()

# Create the main window
root = tk.Tk()
root.title("Library Cataloging System")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create frames for each tab
add_book_frame = ttk.Frame(notebook)
update_book_frame = ttk.Frame(notebook)
view_catalog_frame = ttk.Frame(notebook)
search_frame = ttk.Frame(notebook)
borrow_frame = ttk.Frame(notebook)
return_frame = ttk.Frame(notebook)

notebook.add(add_book_frame, text='Add Book')
notebook.add(update_book_frame, text='Update Book')
notebook.add(view_catalog_frame, text='View Catalog')
notebook.add(search_frame, text='Search Books')
notebook.add(borrow_frame, text='Borrow Book')
notebook.add(return_frame, text='Return Book')

# Add Book Frame
tk.Label(add_book_frame, text="Title:").grid(row=0, column=0, padx=10, pady=10)
title_entry = tk.Entry(add_book_frame)
title_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(add_book_frame, text="Author:").grid(row=1, column=0, padx=10, pady=10)
author_entry = tk.Entry(add_book_frame)
author_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(add_book_frame, text="Genre:").grid(row=2, column=0, padx=10, pady=10)
genre_entry = tk.Entry(add_book_frame)
genre_entry.grid(row=2, column=1, padx=10, pady=10)

add_book_button = tk.Button(add_book_frame, text="Add Book", command=add_book)
add_book_button.grid(row=3, column=0, columnspan=2, pady=10)

# Update Book Frame
tk.Label(update_book_frame, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
update_book_id_entry = tk.Entry(update_book_frame)
update_book_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(update_book_frame, text="Title:").grid(row=1, column=0, padx=10, pady=10)
update_title_entry = tk.Entry(update_book_frame)
update_title_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(update_book_frame, text="Author:").grid(row=2, column=0, padx=10, pady=10)
update_author_entry = tk.Entry(update_book_frame)
update_author_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(update_book_frame, text="Genre:").grid(row=3, column=0, padx=10, pady=10)
update_genre_entry = tk.Entry(update_book_frame)
update_genre_entry.grid(row=3, column=1, padx=10, pady=10)

update_book_button = tk.Button(update_book_frame, text="Update Book", command=update_book)
update_book_button.grid(row=4, column=0, columnspan=2, pady=10)

# View Catalog Frame
view_catalog_button = tk.Button(view_catalog_frame, text="View Catalog", command=view_catalog)
view_catalog_button.grid(row=0, column=0, columnspan=2, pady=10)

# Search Frame
tk.Label(search_frame, text="Keyword:").grid(row=0, column=0, padx=10, pady=10)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=10, pady=10)

search_button = tk.Button(search_frame, text="Search Books", command=search_books)
search_button.grid(row=1, column=0, columnspan=2, pady=10)

# Borrow Frame
tk.Label(borrow_frame, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
borrow_book_id_entry = tk.Entry(borrow_frame)
borrow_book_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(borrow_frame, text="Borrower Name:").grid(row=1, column=0, padx=10, pady=10)
borrower_name_entry = tk.Entry(borrow_frame)
borrower_name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(borrow_frame, text="Borrow Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
borrow_date_entry = tk.Entry(borrow_frame)
borrow_date_entry.grid(row=2, column=1, padx=10, pady=10)

borrow_book_button = tk.Button(borrow_frame, text="Borrow Book", command=borrow_book)
borrow_book_button.grid(row=3, column=0, columnspan=2, pady=10)

# Return Frame
tk.Label(return_frame, text="Borrow ID:").grid(row=0, column=0, padx=10, pady=10)
return_borrow_id_entry = tk.Entry(return_frame)
return_borrow_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(return_frame, text="Return Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
return_date_entry = tk.Entry(return_frame)
return_date_entry.grid(row=1, column=1, padx=10, pady=10)

return_book_button = tk.Button(return_frame, text="Return Book", command=return_book)
return_book_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
