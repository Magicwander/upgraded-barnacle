import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database setup
def init_db():
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY,
                    make TEXT,
                    model TEXT,
                    year INTEGER,
                    available INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    contact TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS rentals (
                    id INTEGER PRIMARY KEY,
                    car_id INTEGER,
                    customer_id INTEGER,
                    rental_date TEXT,
                    return_date TEXT,
                    FOREIGN KEY(car_id) REFERENCES cars(id),
                    FOREIGN KEY(customer_id) REFERENCES customers(id))''')
    conn.commit()
    conn.close()

# CRUD operations
def add_car(make, model, year, available):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("INSERT INTO cars (make, model, year, available) VALUES (?, ?, ?, ?)", (make, model, year, available))
    conn.commit()
    conn.close()

def add_customer(name, contact):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (name, contact))
    conn.commit()
    conn.close()

def add_rental(car_id, customer_id, rental_date, return_date):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("INSERT INTO rentals (car_id, customer_id, rental_date, return_date) VALUES (?, ?, ?, ?)", (car_id, customer_id, rental_date, return_date))
    conn.commit()
    conn.close()

def get_cars():
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cars")
    cars = c.fetchall()
    conn.close()
    return cars

def get_customers():
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    customers = c.fetchall()
    conn.close()
    return customers

def get_rentals():
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("SELECT * FROM rentals")
    rentals = c.fetchall()
    conn.close()
    return rentals

def delete_car(car_id):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("DELETE FROM cars WHERE id=?", (car_id,))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()
    conn.close()

def delete_rental(rental_id):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("DELETE FROM rentals WHERE id=?", (rental_id,))
    conn.commit()
    conn.close()

# GUI setup
class CarRentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental Management System")

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.car_tab = ttk.Frame(self.tab_control)
        self.customer_tab = ttk.Frame(self.tab_control)
        self.rental_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.car_tab, text='Cars')
        self.tab_control.add(self.customer_tab, text='Customers')
        self.tab_control.add(self.rental_tab, text='Rentals')

        self.tab_control.pack(expand=1, fill='both')

        self.create_car_tab()
        self.create_customer_tab()
        self.create_rental_tab()

    def create_car_tab(self):
        tk.Label(self.car_tab, text="Make").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.car_tab, text="Model").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.car_tab, text="Year").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.car_tab, text="Available").grid(row=3, column=0, padx=10, pady=5)

        self.car_make = tk.Entry(self.car_tab)
        self.car_model = tk.Entry(self.car_tab)
        self.car_year = tk.Entry(self.car_tab)
        self.car_available = tk.Entry(self.car_tab)

        self.car_make.grid(row=0, column=1, padx=10, pady=5)
        self.car_model.grid(row=1, column=1, padx=10, pady=5)
        self.car_year.grid(row=2, column=1, padx=10, pady=5)
        self.car_available.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.car_tab, text='Add Car', command=self.add_car).grid(row=4, column=0, columnspan=2, pady=10)

        self.car_list = tk.Listbox(self.car_tab, width=50)
        self.car_list.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.car_tab, text='Delete Car', command=self.delete_car).grid(row=6, column=0, columnspan=2, pady=10)

        self.load_cars()

    def create_customer_tab(self):
        tk.Label(self.customer_tab, text="Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.customer_tab, text="Contact").grid(row=1, column=0, padx=10, pady=5)

        self.customer_name = tk.Entry(self.customer_tab)
        self.customer_contact = tk.Entry(self.customer_tab)

        self.customer_name.grid(row=0, column=1, padx=10, pady=5)
        self.customer_contact.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.customer_tab, text='Add Customer', command=self.add_customer).grid(row=2, column=0, columnspan=2, pady=10)

        self.customer_list = tk.Listbox(self.customer_tab, width=50)
        self.customer_list.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.customer_tab, text='Delete Customer', command=self.delete_customer).grid(row=4, column=0, columnspan=2, pady=10)

        self.load_customers()

    def create_rental_tab(self):
        tk.Label(self.rental_tab, text="Car ID").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.rental_tab, text="Customer ID").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.rental_tab, text="Rental Date").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.rental_tab, text="Return Date").grid(row=3, column=0, padx=10, pady=5)

        self.rental_car_id = tk.Entry(self.rental_tab)
        self.rental_customer_id = tk.Entry(self.rental_tab)
        self.rental_date = tk.Entry(self.rental_tab)
        self.return_date = tk.Entry(self.rental_tab)

        self.rental_car_id.grid(row=0, column=1, padx=10, pady=5)
        self.rental_customer_id.grid(row=1, column=1, padx=10, pady=5)
        self.rental_date.grid(row=2, column=1, padx=10, pady=5)
        self.return_date.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.rental_tab, text='Add Rental', command=self.add_rental).grid(row=4, column=0, columnspan=2, pady=10)

        self.rental_list = tk.Listbox(self.rental_tab, width=50)
        self.rental_list.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.rental_tab, text='Delete Rental', command=self.delete_rental).grid(row=6, column=0, columnspan=2, pady=10)

        self.load_rentals()

    def add_car(self):
        make = self.car_make.get()
        model = self.car_model.get()
        year = self.car_year.get()
        available = self.car_available.get()
        if make and model and year and available:
            add_car(make, model, year, available)
            self.load_cars()
            messagebox.showinfo("Success", "Car added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide all car details")

    def add_customer(self):
        name = self.customer_name.get()
        contact = self.customer_contact.get()
        if name and contact:
            add_customer(name, contact)
            self.load_customers()
            messagebox.showinfo("Success", "Customer added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide both name and contact")

    def add_rental(self):
        car_id = self.rental_car_id.get()
        customer_id = self.rental_customer_id.get()
        rental_date = self.rental_date.get()
        return_date = self.return_date.get()
        if car_id and customer_id and rental_date and return_date:
            add_rental(car_id, customer_id, rental_date, return_date)
            self.load_rentals()
            messagebox.showinfo("Success", "Rental added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide all rental details")

    def load_cars(self):
        self.car_list.delete(0, tk.END)
        cars = get_cars()
        for car in cars:
            self.car_list.insert(tk.END, f"{car[0]}: {car[1]} {car[2]} ({car[3]}) - Available: {car[4]}")

    def load_customers(self):
        self.customer_list.delete(0, tk.END)
        customers = get_customers()
        for customer in customers:
            self.customer_list.insert(tk.END, f"{customer[0]}: {customer[1]} - {customer[2]}")

    def load_rentals(self):
        self.rental_list.delete(0, tk.END)
        rentals = get_rentals()
        for rental in rentals:
            self.rental_list.insert(tk.END, f"{rental[0]}: Car ID: {rental[1]}, Customer ID: {rental[2]}, Rental Date: {rental[3]}, Return Date: {rental[4]}")

    def delete_car(self):
        selected_index = self.car_list.curselection()
        if selected_index:
            car_id = self.car_list.get(selected_index).split(':')[0]
            delete_car(car_id)
            self.load_cars()
            messagebox.showinfo("Success", "Car deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a car to delete")

    def delete_customer(self):
        selected_index = self.customer_list.curselection()
        if selected_index:
            customer_id = self.customer_list.get(selected_index).split(':')[0]
            delete_customer(customer_id)
            self.load_customers()
            messagebox.showinfo("Success", "Customer deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a customer to delete")

    def delete_rental(self):
        selected_index = self.rental_list.curselection()
        if selected_index:
            rental_id = self.rental_list.get(selected_index).split(':')[0]
            delete_rental(rental_id)
            self.load_rentals()
            messagebox.showinfo("Success", "Rental deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a rental to delete")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = CarRentalApp(root)
    root.mainloop()
