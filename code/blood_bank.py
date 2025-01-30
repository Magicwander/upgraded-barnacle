import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('blood_bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donors
                 (id INTEGER PRIMARY KEY, name TEXT, blood_type TEXT, contact TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY, blood_type TEXT, quantity INTEGER, expiration_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS donations
                 (id INTEGER PRIMARY KEY, donor_id INTEGER, blood_type TEXT, quantity INTEGER, date TEXT,
                 FOREIGN KEY(donor_id) REFERENCES donors(id))''')
    conn.commit()
    conn.close()

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
