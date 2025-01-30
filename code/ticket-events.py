import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('ticket_booking.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            venue TEXT,
            capacity INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            customer_name TEXT,
            num_tickets INTEGER,
            FOREIGN KEY (event_id) REFERENCES events (event_id)
        )
    ''')
    conn.commit()
    conn.close()

# Function to add an event
def add_event():
    name = event_name_entry.get()
    date = event_date_entry.get()
    venue = event_venue_entry.get()
    capacity = event_capacity_entry.get()
    conn = sqlite3.connect('ticket_booking.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO events (name, date, venue, capacity) VALUES (?, ?, ?, ?)', (name, date, venue, capacity))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Event added successfully!")
    clear_entries()

# Function to book a ticket
def book_ticket():
    event_id = booking_event_id_entry.get()
    customer_name = booking_customer_name_entry.get()
    num_tickets = booking_num_tickets_entry.get()
    conn = sqlite3.connect('ticket_booking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT capacity FROM events WHERE event_id = ?', (event_id,))
    capacity = cursor.fetchone()[0]
    cursor.execute('SELECT SUM(num_tickets) FROM bookings WHERE event_id = ?', (event_id,))
    booked_tickets = cursor.fetchone()[0] or 0
    if booked_tickets + int(num_tickets) <= capacity:
        cursor.execute('INSERT INTO bookings (event_id, customer_name, num_tickets) VALUES (?, ?, ?)',
                       (event_id, customer_name, num_tickets))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Ticket booked successfully!")
    else:
        messagebox.showerror("Error", "Not enough tickets available!")
    clear_entries()

# Function to view all bookings
def view_bookings():
    conn = sqlite3.connect('ticket_booking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    booking_list = ""
    for booking in bookings:
        booking_list += f"ID: {booking[0]}, Event ID: {booking[1]}, Customer: {booking[2]}, Tickets: {booking[3]}\n"
    messagebox.showinfo("Bookings", booking_list)

# Function to generate a report
def generate_report():
    event_id = report_event_id_entry.get()
    conn = sqlite3.connect('ticket_booking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE event_id = ?', (event_id,))
    bookings = cursor.fetchall()
    conn.close()
    report = f"Booking Report for Event ID: {event_id}\n"
    for booking in bookings:
        report += f"Booking ID: {booking[0]}, Customer: {booking[2]}, Tickets: {booking[3]}\n"
    messagebox.showinfo("Report", report)
    clear_entries()

# Function to clear entries
def clear_entries():
    event_name_entry.delete(0, tk.END)
    event_date_entry.delete(0, tk.END)
    event_venue_entry.delete(0, tk.END)
    event_capacity_entry.delete(0, tk.END)
    booking_event_id_entry.delete(0, tk.END)
    booking_customer_name_entry.delete(0, tk.END)
    booking_num_tickets_entry.delete(0, tk.END)
    report_event_id_entry.delete(0, tk.END)

# Initialize the database
init_db()

# Create the main window
root = tk.Tk()
root.title("Ticket Booking System")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create frames for each tab
event_frame = ttk.Frame(notebook)
booking_frame = ttk.Frame(notebook)
view_frame = ttk.Frame(notebook)
report_frame = ttk.Frame(notebook)

notebook.add(event_frame, text='Add Event')
notebook.add(booking_frame, text='Book Ticket')
notebook.add(view_frame, text='View Bookings')
notebook.add(report_frame, text='Generate Report')

# Event Frame
tk.Label(event_frame, text="Event Name:").grid(row=0, column=0, padx=10, pady=10)
event_name_entry = tk.Entry(event_frame)
event_name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(event_frame, text="Event Date:").grid(row=1, column=0, padx=10, pady=10)
event_date_entry = tk.Entry(event_frame)
event_date_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(event_frame, text="Venue:").grid(row=2, column=0, padx=10, pady=10)
event_venue_entry = tk.Entry(event_frame)
event_venue_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(event_frame, text="Capacity:").grid(row=3, column=0, padx=10, pady=10)
event_capacity_entry = tk.Entry(event_frame)
event_capacity_entry.grid(row=3, column=1, padx=10, pady=10)

add_event_button = tk.Button(event_frame, text="Add Event", command=add_event)
add_event_button.grid(row=4, column=0, columnspan=2, pady=10)

# Booking Frame
tk.Label(booking_frame, text="Event ID:").grid(row=0, column=0, padx=10, pady=10)
booking_event_id_entry = tk.Entry(booking_frame)
booking_event_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(booking_frame, text="Customer Name:").grid(row=1, column=0, padx=10, pady=10)
booking_customer_name_entry = tk.Entry(booking_frame)
booking_customer_name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(booking_frame, text="Number of Tickets:").grid(row=2, column=0, padx=10, pady=10)
booking_num_tickets_entry = tk.Entry(booking_frame)
booking_num_tickets_entry.grid(row=2, column=1, padx=10, pady=10)

book_ticket_button = tk.Button(booking_frame, text="Book Ticket", command=book_ticket)
book_ticket_button.grid(row=3, column=0, columnspan=2, pady=10)

# View Frame
view_bookings_button = tk.Button(view_frame, text="View All Bookings", command=view_bookings)
view_bookings_button.grid(row=0, column=0, columnspan=2, pady=10)

# Report Frame
tk.Label(report_frame, text="Event ID:").grid(row=0, column=0, padx=10, pady=10)
report_event_id_entry = tk.Entry(report_frame)
report_event_id_entry.grid(row=0, column=1, padx=10, pady=10)

generate_report_button = tk.Button(report_frame, text="Generate Report", command=generate_report)
generate_report_button.grid(row=1, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
