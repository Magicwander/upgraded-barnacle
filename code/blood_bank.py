import tkinter as tk
from tkinter import messagebox, ttk
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
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donors (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    blood_type TEXT NOT NULL,
                    contact TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    blood_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    expiration_date TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS donations (
                    id INTEGER PRIMARY KEY,
                    donor_id INTEGER,
                    blood_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY(donor_id) REFERENCES donors(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

# Add a new donor
def add_donor():
    name = entry_name.get()
    blood_type = entry_blood_type.get()
    contact = entry_contact.get()
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("INSERT INTO donors (name, blood_type, contact) VALUES (?, ?, ?)",
              (name, blood_type, contact))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Donor added successfully!")
    clear_entries()
    view_donors()

# Update donor information
def update_donor():
    name = entry_name.get()
    blood_type = entry_blood_type.get()
    contact = entry_contact.get()
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("UPDATE donors SET blood_type = ?, contact = ? WHERE name = ?", (blood_type, contact, name))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Donor information updated successfully!")
    clear_entries()
    view_donors()

# Delete a donor
def delete_donor():
    name = entry_name.get()
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("DELETE FROM donors WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Donor deleted successfully!")
    clear_entries()
    view_donors()

# Search for a donor by name
def search_donor():
    name = entry_name.get()
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donors WHERE name = ?", (name,))
    rows = c.fetchall()
    conn.close()
    if rows:
        messagebox.showinfo("Donor Found", f"Name: {rows[0][1]}, Blood Type: {rows[0][2]}, Contact: {rows[0][3]}")
    else:
        messagebox.showinfo("Donor Not Found", "No donor found with the given name.")

# Add blood to inventory
def add_blood():
    blood_type = entry_blood_type.get()
    quantity = entry_quantity.get()
    expiration_date = entry_expiration_date.get()
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (blood_type, quantity, expiration_date) VALUES (?, ?, ?)",
              (blood_type, quantity, expiration_date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Blood added to inventory successfully!")
    clear_entries()
    view_inventory()

# Update blood inventory
def update_inventory():
    blood_type = entry_blood_type.get()
    quantity = entry_quantity.get()
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("UPDATE inventory SET quantity = ? WHERE blood_type = ?", (quantity, blood_type))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Blood inventory updated successfully!")
    clear_entries()
    view_inventory()

# Record a donation
def record_donation():
    donor_name = entry_name.get()
    blood_type = entry_blood_type.get()
    quantity = entry_quantity.get()
    date = entry_date.get()
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("SELECT id FROM donors WHERE name = ?", (donor_name,))
    donor_id = c.fetchone()[0]
    c.execute("INSERT INTO donations (donor_id, blood_type, quantity, date) VALUES (?, ?, ?, ?)",
              (donor_id, blood_type, quantity, date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Donation recorded successfully!")
    clear_entries()
    view_donations()

# View donors in a table
def view_donors():
    for i in tree_donors.get_children():
        tree_donors.delete(i)
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donors")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_donors.insert("", "end", values=row)

# View inventory in a table
def view_inventory():
    for i in tree_inventory.get_children():
        tree_inventory.delete(i)
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_inventory.insert("", "end", values=row)

# View donations in a table
def view_donations():
    for i in tree_donations.get_children():
        tree_donations.delete(i)
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donations")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree_donations.insert("", "end", values=row)

# Clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_blood_type.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_expiration_date.delete(0, tk.END)
    entry_date.delete(0, tk.END)

# Create the main application window
root = tk.Tk()
root.title("Blood Bank Management System")

# Initialize the database
init_db()

# Create and place widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_name = ttk.Entry(frame)
entry_name.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Blood Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_blood_type = ttk.Entry(frame)
entry_blood_type.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Contact:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_contact = ttk.Entry(frame)
entry_contact.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W, pady=5)
entry_quantity = ttk.Entry(frame)
entry_quantity.grid(row=3, column=1, pady=5)

ttk.Label(frame, text="Expiration Date (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W, pady=5)
entry_expiration_date = ttk.Entry(frame)
entry_expiration_date.grid(row=4, column=1, pady=5)

ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=5, column=0, sticky=tk.W, pady=5)
entry_date = ttk.Entry(frame)
entry_date.grid(row=5, column=1, pady=5)

ttk.Button(frame, text="Add Donor", command=add_donor).grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Update Donor", command=update_donor).grid(row=7, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Delete Donor", command=delete_donor).grid(row=8, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Search Donor", command=search_donor).grid(row=9, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Add Blood", command=add_blood).grid(row=10, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Update Inventory", command=update_inventory).grid(row=11, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Record Donation", command=record_donation).grid(row=12, column=0, columnspan=2, pady=5)

# Create treeviews for displaying tables
tree_donors = ttk.Treeview(frame, columns=("ID", "Name", "Blood Type", "Contact"), show='headings')
tree_donors.heading("ID", text="ID")
tree_donors.heading("Name", text="Name")
tree_donors.heading("Blood Type", text="Blood Type")
tree_donors.heading("Contact", text="Contact")
tree_donors.grid(row=13, column=0, columnspan=2, pady=5)

tree_inventory = ttk.Treeview(frame, columns=("ID", "Blood Type", "Quantity", "Expiration Date"), show='headings')
tree_inventory.heading("ID", text="ID")
tree_inventory.heading("Blood Type", text="Blood Type")
tree_inventory.heading("Quantity", text="Quantity")
tree_inventory.heading("Expiration Date", text="Expiration Date")
tree_inventory.grid(row=14, column=0, columnspan=2, pady=5)

tree_donations = ttk.Treeview(frame, columns=("ID", "Donor ID", "Blood Type", "Quantity", "Date"), show='headings')
tree_donations.heading("ID", text="ID")
tree_donations.heading("Donor ID", text="Donor ID")
tree_donations.heading("Blood Type", text="Blood Type")
tree_donations.heading("Quantity", text="Quantity")
tree_donations.heading("Date", text="Date")
tree_donations.grid(row=15, column=0, columnspan=2, pady=5)

# View initial data
view_donors()
view_inventory()
view_donations()

# Run the application
root.mainloop()

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
    role (str): The role of the user (admin, staff, donor).
    """
    hashed_password = hash_password(password)
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
    conn.commit()
    conn.close()

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
    conn = sqlite3.connect('blood_bank.db')
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
                main_app = BloodBankApp(tk.Tk())
                main_app.root.mainloop()
            else:
                messagebox.showwarning("Login error", "Invalid username or password.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    auth_app = AuthApp(root)
    root.mainloop()

# Generate donation chart
def generate_donation_chart(start_date, end_date):
    """
    Generate a donation chart for a specific date range.

    Parameters:
    start_date (str): The start date of the report.
    end_date (str): The end date of the report.

    Returns:
    Figure: A Matplotlib figure containing the donation chart.
    """
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute("SELECT donors.name, donations.date, donations.quantity FROM donations JOIN donors ON donations.donor_id = donors.id WHERE donations.date BETWEEN ? AND ?", (start_date, end_date))
    records = c.fetchall()
    conn.close()

    donation_data = {}
    for record in records:
        donor_name = record[0]
        quantity = record[2]
        if donor_name not in donation_data:
            donation_data[donor_name] = 0
        donation_data[donor_name] += quantity

    fig, ax = plt.subplots()
    for donor, data in donation_data.items():
        ax.bar(donor, data, color='b')

    ax.set_ylabel('Quantity of Blood Donated')
    ax.set_title('Donation Report')
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
        self.root.title("Donation Report")

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
        Generate and display the donation chart.
        """
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        if start_date and end_date:
            if validate_date(start_date) and validate_date(end_date):
                fig = generate_donation_chart(start_date, end_date)
                canvas = FigureCanvasTkAgg(fig, master=self.canvas)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            else:
                messagebox.showwarning("Input error", "Please enter valid dates in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please enter both start and end dates.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    report_app = ReportApp(root)
    root.mainloop()

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

def send_donation_reminder(donor_email, donor_name, date):
    """
    Send a donation reminder to a donor.

    Parameters:
    donor_email (str): The donor's email address.
    donor_name (str): The donor's name.
    date (str): The date of the donation.
    """
    subject = "Donation Reminder"
    body = f"Dear {donor_name},\n\nThis is a reminder that your donation for {date} has not been marked. Please contact the blood bank for more information.\n\nBest regards,\nBlood Bank System"
    send_email_notification(donor_email, subject, body)

def send_donation_update(donor_email, donor_name, date, quantity):
    """
    Send a donation update to a donor.

    Parameters:
    donor_email (str): The donor's email address.
    donor_name (str): The donor's name.
    date (str): The date of the donation.
    quantity (int): The quantity of blood donated.
    """
    subject = "Donation Update"
    body = f"Dear {donor_name},\n\nYour donation for {date} has been marked as {quantity} units of blood.\n\nBest regards,\nBlood Bank System"
    send_email_notification(donor_email, subject, body)

class NotificationApp:
    def __init__(self, root):
        """
        Initialize the NotificationApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Notification System")

        self.donor_email = tk.StringVar()
        self.donor_name = tk.StringVar()
        self.date = tk.StringVar()
        self.quantity = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text="Donor Email:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.donor_email).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Donor Name:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.donor_name).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Date:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.date).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Quantity:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.quantity).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Send Reminder", command=self.send_reminder).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Send Update", command=self.send_update).grid(row=4, column=1, padx=10, pady=10)

    def send_reminder(self):
        """
        Send a donation reminder.
        """
        donor_email = self.donor_email.get()
        donor_name = self.donor_name.get()
        date = self.date.get()
        if donor_email and donor_name and date:
            if validate_date(date):
                send_donation_reminder(donor_email, donor_name, date)
                messagebox.showinfo("Success", "Reminder sent successfully.")
            else:
                messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def send_update(self):
        """
        Send a donation update.
        """
        donor_email = self.donor_email.get()
        donor_name = self.donor_name.get()
        date = self.date.get()
        quantity = self.quantity.get()
        if donor_email and donor_name and date and quantity:
            if validate_date(date):
                send_donation_update(donor_email, donor_name, date, quantity)
                messagebox.showinfo("Success", "Update sent successfully.")
            else:
                messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    notification_app = NotificationApp(root)
    root.mainloop()

# Advanced search for donors
def advanced_search_donors(name=None, blood_type=None, donation_status=None, start_date=None, end_date=None):
    """
    Perform an advanced search for donors based on various criteria.

    Parameters:
    name (str): The name of the donor.
    blood_type (str): The blood type of the donor.
    donation_status (str): The donation status of the donor.
    start_date (str): The start date of the donation.
    end_date (str): The end date of the donation.

    Returns:
    list: A list of tuples containing donor information that matches the criteria.
    """
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()

    query = "SELECT DISTINCT donors.id, donors.name, donors.blood_type FROM donors"
    conditions = []
    params = []

    if name:
        conditions.append("donors.name LIKE ?")
        params.append('%' + name + '%')
    if blood_type:
        conditions.append("donors.blood_type = ?")
        params.append(blood_type)
    if donation_status:
        conditions.append("donations.quantity > 0")
    if start_date and end_date:
        conditions.append("donations.date BETWEEN ? AND ?")
        params.append(start_date)
        params.append(end_date)

    if conditions:
        query += " JOIN donations ON donors.id = donations.donor_id WHERE " + " AND ".join(conditions)

    c.execute(query, params)
    donors = c.fetchall()
    conn.close()
    return donors

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
        self.blood_type = tk.StringVar()
        self.donation_status = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.name).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Blood Type:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.blood_type).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Donation Status:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.donation_status).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Start Date:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.start_date).grid(row=3, column=1, padx=10, pady=10)
        tk.Label(self.root, text="End Date:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.end_date).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Search", command=self.search_donors).grid(row=5, column=1, padx=10, pady=10)

        self.search_results_list = tk.Listbox(self.root, width=100)
        self.search_results_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def search_donors(self):
        """
        Perform an advanced search for donors.
        """
        name = self.name.get()
        blood_type = self.blood_type.get()
        donation_status = self.donation_status.get()
        start_date = self.start_date.get()
        end_date = self.end_date.get()

        if start_date and end_date:
            if not (validate_date(start_date) and validate_date(end_date)):
                messagebox.showwarning("Input error", "Please enter valid dates in YYYY-MM-DD format.")
                return

        donors = advanced_search_donors(name, blood_type, donation_status, start_date, end_date)
        self.search_results_list.delete(0, tk.END)
        for donor in donors:
            self.search_results_list.insert(tk.END, f"ID: {donor[0]}, Name: {donor[1]}, Blood Type: {donor[2]}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    advanced_search_app = AdvancedSearchApp(root)
    root.mainloop()

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

def validate_blood_type(blood_type):
    """
    Validate the blood type.

    Parameters:
    blood_type (str): The blood type to validate.

    Returns:
    bool: True if the blood type is valid, False otherwise.
    """
    valid_blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    return blood_type in valid_blood_types

def validate_status(status):
    """
    Validate the donation status.

    Parameters:
    status (str): The donation status to validate.

    Returns:
    bool: True if the status is valid, False otherwise.
    """
    return status in ["Donated", "Not Donated"]

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
        self.blood_type = tk.StringVar()
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
        tk.Label(self.root, text="Blood Type:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.blood_type).grid(row=1, column=1, padx=10, pady=10)
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
        blood_type = self.blood_type.get()
        status = self.status.get()
        date = self.date.get()
        email = self.email.get()

        if not validate_name(name):
            messagebox.showwarning("Input error", "Please enter a valid name.")
        elif not validate_blood_type(blood_type):
            messagebox.showwarning("Input error", "Please enter a valid blood type.")
        elif not validate_status(status):
            messagebox.showwarning("Input error", "Please enter a valid status (Donated or Not Donated).")
        elif not validate_date(date):
            messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        elif not validate_email(email):
            messagebox.showwarning("Input error", "Please enter a valid email address.")
        else:
            messagebox.showinfo("Success", "All inputs are valid.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    validation_app = ValidationApp(root)
    root.mainloop()

# Unit tests
class TestBloodBankSystem(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE donors (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            blood_type TEXT NOT NULL,
                            contact TEXT NOT NULL)''')
        self.c.execute('''CREATE TABLE inventory (
                            id INTEGER PRIMARY KEY,
                            blood_type TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            expiration_date TEXT NOT NULL)''')
        self.c.execute('''CREATE TABLE donations (
                            id INTEGER PRIMARY KEY,
                            donor_id INTEGER,
                            blood_type TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            FOREIGN KEY(donor_id) REFERENCES donors(id))''')
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

    def test_add_donor(self):
        """
        Test adding a donor.
        """
        add_donor("John Doe", "A+", "john.doe@example.com")
        self.c.execute("SELECT * FROM donors WHERE name = ? AND blood_type = ? AND contact = ?", ("John Doe", "A+", "john.doe@example.com"))
        donor = self.c.fetchone()
        self.assertIsNotNone(donor)

    def test_mark_donation(self):
        """
        Test marking a donation.
        """
        add_donor("Jane Smith", "B+", "jane.smith@example.com")
        self.c.execute("SELECT id FROM donors WHERE name = ? AND blood_type = ? AND contact = ?", ("Jane Smith", "B+", "jane.smith@example.com"))
        donor_id = self.c.fetchone()[0]
        mark_donation(donor_id, "2023-10-01", "A+", 1)
        self.c.execute("SELECT * FROM donations WHERE donor_id = ? AND date = ? AND blood_type = ? AND quantity = ?", (donor_id, "2023-10-01", "A+", 1))
        donation = self.c.fetchone()
        self.assertIsNotNone(donation)

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
        register_user("staff", "password123", "staff")
        user = login_user("staff", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user[2], "staff")

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
lang = gettext.translation('blood_bank', localedir, languages=['en'])
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
        lang = gettext.translation('blood_bank', localedir, languages=[selected_language])
        lang.install()
        self.root.title(_("Internationalization"))
        self.create_widgets()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    i18n_app = InternationalizationApp(root)
    root.mainloop()

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

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    accessibility_app = AccessibilityApp(root)
    root.mainloop()

# Main Application
class BloodBankApp:
    def __init__(self, root):
        """
        Initialize the BloodBankApp class.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Blood Bank Management System")

        self.donor_name = tk.StringVar()
        self.blood_type = tk.StringVar()
        self.contact = tk.StringVar()
        self.donor_id = tk.IntVar()
        self.date = tk.StringVar()
        self.quantity = tk.IntVar()
        self.search_query = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()
        self.donation_id = tk.IntVar()
        self.csv_file_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the Tkinter GUI.
        """
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill="both")

        # Add Donor Tab
        add_donor_tab = ttk.Frame(notebook)
        notebook.add(add_donor_tab, text='Add Donor')

        tk.Label(add_donor_tab, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(add_donor_tab, textvariable=self.donor_name).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(add_donor_tab, text="Blood Type:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(add_donor_tab, textvariable=self.blood_type).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(add_donor_tab, text="Contact:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(add_donor_tab, textvariable=self.contact).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(add_donor_tab, text="Add Donor", command=self.add_donor).grid(row=3, column=0, columnspan=2, pady=10)

        # Mark Donation Tab
        mark_donation_tab = ttk.Frame(notebook)
        notebook.add(mark_donation_tab, text='Mark Donation')

        tk.Label(mark_donation_tab, text="Donor ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(mark_donation_tab, textvariable=self.donor_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(mark_donation_tab, text="Date:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(mark_donation_tab, textvariable=self.date).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(mark_donation_tab, text="Blood Type:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(mark_donation_tab, textvariable=self.blood_type).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(mark_donation_tab, text="Quantity:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(mark_donation_tab, textvariable=self.quantity).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(mark_donation_tab, text="Mark Donation", command=self.mark_donation).grid(row=4, column=0, columnspan=2, pady=10)

        # View All Donors Tab
        view_donors_tab = ttk.Frame(notebook)
        notebook.add(view_donors_tab, text='View All Donors')

        self.donors_list = tk.Listbox(view_donors_tab, width=100)
        self.donors_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_donors_tab, text="Refresh", command=self.refresh_donors).grid(row=1, column=0, padx=10, pady=10)

        # View Donations Tab
        view_donations_tab = ttk.Frame(notebook)
        notebook.add(view_donations_tab, text='View Donations')

        self.donations_list = tk.Listbox(view_donations_tab, width=100)
        self.donations_list.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(view_donations_tab, text="Refresh", command=self.refresh_donations).grid(row=1, column=0, padx=10, pady=10)

        # Update Donor Tab
        update_donor_tab = ttk.Frame(notebook)
        notebook.add(update_donor_tab, text='Update Donor')

        tk.Label(update_donor_tab, text="Donor ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(update_donor_tab, textvariable=self.donor_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(update_donor_tab, text="Name:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(update_donor_tab, textvariable=self.donor_name).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(update_donor_tab, text="Blood Type:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(update_donor_tab, textvariable=self.blood_type).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(update_donor_tab, text="Contact:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(update_donor_tab, textvariable=self.contact).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(update_donor_tab, text="Update Donor", command=self.update_donor).grid(row=4, column=0, columnspan=2, pady=10)

        # Delete Donor Tab
        delete_donor_tab = ttk.Frame(notebook)
        notebook.add(delete_donor_tab, text='Delete Donor')

        tk.Label(delete_donor_tab, text="Donor ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(delete_donor_tab, textvariable=self.donor_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(delete_donor_tab, text="Delete Donor", command=self.delete_donor).grid(row=1, column=0, columnspan=2, pady=10)

        # Delete Donation Tab
        delete_donation_tab = ttk.Frame(notebook)
        notebook.add(delete_donation_tab, text='Delete Donation')

        tk.Label(delete_donation_tab, text="Donation ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(delete_donation_tab, textvariable=self.donation_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(delete_donation_tab, text="Delete Donation", command=self.delete_donation).grid(row=1, column=0, columnspan=2, pady=10)

        # Search Donor Tab
        search_donor_tab = ttk.Frame(notebook)
        notebook.add(search_donor_tab, text='Search Donor')

        tk.Label(search_donor_tab, text="Search Query:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(search_donor_tab, textvariable=self.search_query).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(search_donor_tab, text="Search", command=self.search_donor).grid(row=1, column=0, columnspan=2, pady=10)
        self.search_results_list = tk.Listbox(search_donor_tab, width=100)
        self.search_results_list.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Generate Donation Report Tab
        generate_report_tab = ttk.Frame(notebook)
        notebook.add(generate_report_tab, text='Generate Donation Report')

        tk.Label(generate_report_tab, text="Start Date:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(generate_report_tab, textvariable=self.start_date).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(generate_report_tab, text="End Date:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(generate_report_tab, textvariable=self.end_date).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(generate_report_tab, text="Generate Report", command=self.generate_donation_report).grid(row=2, column=0, columnspan=2, pady=10)
        self.report_list = tk.Listbox(generate_report_tab, width=100)
        self.report_list.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Update Donation Tab
        update_donation_tab = ttk.Frame(notebook)
        notebook.add(update_donation_tab, text='Update Donation')

        tk.Label(update_donation_tab, text="Donation ID:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(update_donation_tab, textvariable=self.donation_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(update_donation_tab, text="Donor ID:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(update_donation_tab, textvariable=self.donor_id).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(update_donation_tab, text="Date:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(update_donation_tab, textvariable=self.date).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(update_donation_tab, text="Blood Type:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(update_donation_tab, textvariable=self.blood_type).grid(row=3, column=1, padx=10, pady=10)
        tk.Label(update_donation_tab, text="Quantity:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(update_donation_tab, textvariable=self.quantity).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(update_donation_tab, text="Update Donation", command=self.update_donation).grid(row=5, column=0, columnspan=2, pady=10)

        # Export Donation Report Tab
        export_report_tab = ttk.Frame(notebook)
        notebook.add(export_report_tab, text='Export Donation Report')

        tk.Label(export_report_tab, text="Start Date:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(export_report_tab, textvariable=self.start_date).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(export_report_tab, text="End Date:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(export_report_tab, textvariable=self.end_date).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(export_report_tab, text="File Path:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(export_report_tab, textvariable=self.csv_file_path).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(export_report_tab, text="Export Report", command=self.export_donation_report).grid(row=3, column=0, columnspan=2, pady=10)

        # Import Donors Tab
        import_donors_tab = ttk.Frame(notebook)
        notebook.add(import_donors_tab, text='Import Donors')

        tk.Label(import_donors_tab, text="File Path:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(import_donors_tab, textvariable=self.csv_file_path).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(import_donors_tab, text="Import Donors", command=self.import_donors).grid(row=1, column=0, columnspan=2, pady=10)

        # Import Donations Tab
        import_donations_tab = ttk.Frame(notebook)
        notebook.add(import_donations_tab, text='Import Donations')

        tk.Label(import_donations_tab, text="File Path:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(import_donations_tab, textvariable=self.csv_file_path).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(import_donations_tab, text="Import Donations", command=self.import_donations).grid(row=1, column=0, columnspan=2, pady=10)

        self.refresh_donors()
        self.refresh_donations()

    def add_donor(self):
        """
        Add a new donor to the database.
        """
        name = self.donor_name.get()
        blood_type = self.blood_type.get()
        contact = self.contact.get()
        if name and blood_type and contact:
            add_donor(name, blood_type, contact)
            messagebox.showinfo("Success", "Donor added successfully!")
            self.refresh_donors()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def mark_donation(self):
        """
        Mark a donation.
        """
        donor_id = self.donor_id.get()
        date = self.date.get()
        blood_type = self.blood_type.get()
        quantity = self.quantity.get()
        if donor_id and date and blood_type and quantity:
            if validate_date(date):
                mark_donation(donor_id, date, blood_type, quantity)
                messagebox.showinfo("Success", "Donation marked successfully!")
                self.refresh_donations()
            else:
                messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def refresh_donors(self):
        """
        Refresh the list of donors.
        """
        self.donors_list.delete(0, tk.END)
        donors = get_all_donors()
        for donor in donors:
            self.donors_list.insert(tk.END, f"ID: {donor[0]}, Name: {donor[1]}, Blood Type: {donor[2]}, Contact: {donor[3]}")

    def refresh_donations(self):
        """
        Refresh the list of donations.
        """
        self.donations_list.delete(0, tk.END)
        donations = get_all_donations()
        for donation in donations:
            self.donations_list.insert(tk.END, f"ID: {donation[0]}, Donor ID: {donation[1]}, Date: {donation[2]}, Blood Type: {donation[3]}, Quantity: {donation[4]}")

    def update_donor(self):
        """
        Update the information of an existing donor.
        """
        donor_id = self.donor_id.get()
        name = self.donor_name.get()
        blood_type = self.blood_type.get()
        contact = self.contact.get()
        if donor_id and name and blood_type and contact:
            update_donor(donor_id, name, blood_type, contact)
            messagebox.showinfo("Success", "Donor information updated successfully!")
            self.refresh_donors()
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def delete_donor(self):
        """
        Delete a donor from the database.
        """
        donor_id = self.donor_id.get()
        if donor_id:
            delete_donor(donor_id)
            messagebox.showinfo("Success", "Donor deleted successfully!")
            self.refresh_donors()
        else:
            messagebox.showwarning("Input error", "Please enter a valid Donor ID.")

    def delete_donation(self):
        """
        Delete a donation from the database.
        """
        donation_id = self.donation_id.get()
        if donation_id:
            delete_donation(donation_id)
            messagebox.showinfo("Success", "Donation deleted successfully!")
            self.refresh_donations()
        else:
            messagebox.showwarning("Input error", "Please enter a valid Donation ID.")

    def search_donor(self):
        """
        Search for a donor by name or contact.
        """
        query = self.search_query.get()
        if query:
            donors = search_donor(query)
            self.search_results_list.delete(0, tk.END)
            for donor in donors:
                self.search_results_list.insert(tk.END, f"ID: {donor[0]}, Name: {donor[1]}, Blood Type: {donor[2]}, Contact: {donor[3]}")
        else:
            messagebox.showwarning("Input error", "Please enter a search query.")

    def generate_donation_report(self):
        """
        Generate a donation report for a specific date range.
        """
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        if start_date and end_date:
            if validate_date(start_date) and validate_date(end_date):
                donations = generate_donation_report(start_date, end_date)
                self.report_list.delete(0, tk.END)
                for donation in donations:
                    self.report_list.insert(tk.END, f"Donation ID: {donation[0]}, Donor ID: {donation[1]}, Date: {donation[2]}, Blood Type: {donation[3]}, Quantity: {donation[4]}")
            else:
                messagebox.showwarning("Input error", "Please enter valid dates in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please enter both start and end dates.")

    def update_donation(self):
        """
        Update an existing donation.
        """
        donation_id = self.donation_id.get()
        donor_id = self.donor_id.get()
        date = self.date.get()
        blood_type = self.blood_type.get()
        quantity = self.quantity.get()
        if donation_id and donor_id and date and blood_type and quantity:
            if validate_date(date):
                update_donation(donation_id, donor_id, date, blood_type, quantity)
                messagebox.showinfo("Success", "Donation updated successfully!")
                self.refresh_donations()
            else:
                messagebox.showwarning("Input error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please fill in all fields.")

    def export_donation_report(self):
        """
        Export a donation report for a specific date range to a CSV file.
        """
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        file_path = self.csv_file_path.get()
        if start_date and end_date and file_path:
            if validate_date(start_date) and validate_date(end_date):
                export_donation_report_to_csv(start_date, end_date, file_path)
                messagebox.showinfo("Success", "Donation report exported successfully!")
            else:
                messagebox.showwarning("Input error", "Please enter valid dates in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input error", "Please enter both start and end dates and a valid file path.")

    def import_donors(self):
        """
        Import donors from a CSV file.
        """
        file_path = self.csv_file_path.get()
        if file_path:
            import_donors_from_csv(file_path)
            messagebox.showinfo("Success", "Donors imported successfully!")
            self.refresh_donors()
        else:
            messagebox.showwarning("Input error", "Please enter a valid file path.")

    def import_donations(self):
        """
        Import donations from a CSV file.
        """
        file_path = self.csv_file_path.get()
        if file_path:
            import_donations_from_csv(file_path)
            messagebox.showinfo("Success", "Donations imported successfully!")
            self.refresh_donations()
        else:
            messagebox.showwarning("Input error", "Please enter a valid file path.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BloodBankApp(root)
    root.mainloop()
