import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database setup
def init_db():
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY,
                    make TEXT,
                    model TEXT,
                    year INTEGER,
                    license_plate TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS drivers (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    license_number TEXT,
                    contact TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS maintenance (
                    id INTEGER PRIMARY KEY,
                    vehicle_id INTEGER,
                    date TEXT,
                    description TEXT,
                    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id))''')
    conn.commit()
    conn.close()

# CRUD operations
def add_vehicle(make, model, year, license_plate):
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("INSERT INTO vehicles (make, model, year, license_plate) VALUES (?, ?, ?, ?)", (make, model, year, license_plate))
    conn.commit()
    conn.close()

def add_driver(name, license_number, contact):
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("INSERT INTO drivers (name, license_number, contact) VALUES (?, ?, ?)", (name, license_number, contact))
    conn.commit()
    conn.close()

def add_maintenance(vehicle_id, date, description):
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("INSERT INTO maintenance (vehicle_id, date, description) VALUES (?, ?, ?)", (vehicle_id, date, description))
    conn.commit()
    conn.close()

def get_vehicles():
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles")
    vehicles = c.fetchall()
    conn.close()
    return vehicles

def get_drivers():
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("SELECT * FROM drivers")
    drivers = c.fetchall()
    conn.close()
    return drivers

def get_maintenance():
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("SELECT * FROM maintenance")
    maintenance = c.fetchall()
    conn.close()
    return maintenance

def delete_vehicle(vehicle_id):
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("DELETE FROM vehicles WHERE id=?", (vehicle_id,))
    conn.commit()
    conn.close()

def delete_driver(driver_id):
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("DELETE FROM drivers WHERE id=?", (driver_id,))
    conn.commit()
    conn.close()

def delete_maintenance(maintenance_id):
    conn = sqlite3.connect('fleet_management.db')
    c = conn.cursor()
    c.execute("DELETE FROM maintenance WHERE id=?", (maintenance_id,))
    conn.commit()
    conn.close()

# GUI setup
class FleetManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Fleet Management System")

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.vehicle_tab = ttk.Frame(self.tab_control)
        self.driver_tab = ttk.Frame(self.tab_control)
        self.maintenance_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.vehicle_tab, text='Vehicles')
        self.tab_control.add(self.driver_tab, text='Drivers')
        self.tab_control.add(self.maintenance_tab, text='Maintenance')

        self.tab_control.pack(expand=1, fill='both')

        self.create_vehicle_tab()
        self.create_driver_tab()
        self.create_maintenance_tab()

    def create_vehicle_tab(self):
        tk.Label(self.vehicle_tab, text="Make").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.vehicle_tab, text="Model").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.vehicle_tab, text="Year").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.vehicle_tab, text="License Plate").grid(row=3, column=0, padx=10, pady=5)

        self.vehicle_make = tk.Entry(self.vehicle_tab)
        self.vehicle_model = tk.Entry(self.vehicle_tab)
        self.vehicle_year = tk.Entry(self.vehicle_tab)
        self.vehicle_license_plate = tk.Entry(self.vehicle_tab)

        self.vehicle_make.grid(row=0, column=1, padx=10, pady=5)
        self.vehicle_model.grid(row=1, column=1, padx=10, pady=5)
        self.vehicle_year.grid(row=2, column=1, padx=10, pady=5)
        self.vehicle_license_plate.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.vehicle_tab, text='Add Vehicle', command=self.add_vehicle).grid(row=4, column=0, columnspan=2, pady=10)

        self.vehicle_list = tk.Listbox(self.vehicle_tab, width=50)
        self.vehicle_list.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.vehicle_tab, text='Delete Vehicle', command=self.delete_vehicle).grid(row=6, column=0, columnspan=2, pady=10)

        self.load_vehicles()

    def create_driver_tab(self):
        tk.Label(self.driver_tab, text="Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.driver_tab, text="License Number").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.driver_tab, text="Contact").grid(row=2, column=0, padx=10, pady=5)

        self.driver_name = tk.Entry(self.driver_tab)
        self.driver_license_number = tk.Entry(self.driver_tab)
        self.driver_contact = tk.Entry(self.driver_tab)

        self.driver_name.grid(row=0, column=1, padx=10, pady=5)
        self.driver_license_number.grid(row=1, column=1, padx=10, pady=5)
        self.driver_contact.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.driver_tab, text='Add Driver', command=self.add_driver).grid(row=3, column=0, columnspan=2, pady=10)

        self.driver_list = tk.Listbox(self.driver_tab, width=50)
        self.driver_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.driver_tab, text='Delete Driver', command=self.delete_driver).grid(row=5, column=0, columnspan=2, pady=10)

        self.load_drivers()

    def create_maintenance_tab(self):
        tk.Label(self.maintenance_tab, text="Vehicle ID").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.maintenance_tab, text="Date").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.maintenance_tab, text="Description").grid(row=2, column=0, padx=10, pady=5)

        self.maintenance_vehicle_id = tk.Entry(self.maintenance_tab)
        self.maintenance_date = tk.Entry(self.maintenance_tab)
        self.maintenance_description = tk.Entry(self.maintenance_tab)

        self.maintenance_vehicle_id.grid(row=0, column=1, padx=10, pady=5)
        self.maintenance_date.grid(row=1, column=1, padx=10, pady=5)
        self.maintenance_description.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.maintenance_tab, text='Add Maintenance', command=self.add_maintenance).grid(row=3, column=0, columnspan=2, pady=10)

        self.maintenance_list = tk.Listbox(self.maintenance_tab, width=50)
        self.maintenance_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.maintenance_tab, text='Delete Maintenance', command=self.delete_maintenance).grid(row=5, column=0, columnspan=2, pady=10)

        self.load_maintenance()

    def add_vehicle(self):
        make = self.vehicle_make.get()
        model = self.vehicle_model.get()
        year = self.vehicle_year.get()
        license_plate = self.vehicle_license_plate.get()
        if make and model and year and license_plate:
            add_vehicle(make, model, year, license_plate)
            self.load_vehicles()
            messagebox.showinfo("Success", "Vehicle added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide all vehicle details")

    def add_driver(self):
        name = self.driver_name.get()
        license_number = self.driver_license_number.get()
        contact = self.driver_contact.get()
        if name and license_number and contact:
            add_driver(name, license_number, contact)
            self.load_drivers()
            messagebox.showinfo("Success", "Driver added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide all driver details")

    def add_maintenance(self):
        vehicle_id = self.maintenance_vehicle_id.get()
        date = self.maintenance_date.get()
        description = self.maintenance_description.get()
        if vehicle_id and date and description:
            add_maintenance(vehicle_id, date, description)
            self.load_maintenance()
            messagebox.showinfo("Success", "Maintenance record added successfully!")
        else:
            messagebox.showwarning("Input error", "Please provide all maintenance details")

    def load_vehicles(self):
        self.vehicle_list.delete(0, tk.END)
        vehicles = get_vehicles()
        for vehicle in vehicles:
            self.vehicle_list.insert(tk.END, f"{vehicle[0]}: {vehicle[1]} {vehicle[2]} ({vehicle[3]}) - {vehicle[4]}")

    def load_drivers(self):
        self.driver_list.delete(0, tk.END)
        drivers = get_drivers()
        for driver in drivers:
            self.driver_list.insert(tk.END, f"{driver[0]}: {driver[1]} - {driver[2]} - {driver[3]}")

    def load_maintenance(self):
        self.maintenance_list.delete(0, tk.END)
        maintenance = get_maintenance()
        for record in maintenance:
            self.maintenance_list.insert(tk.END, f"{record[0]}: Vehicle ID: {record[1]}, Date: {record[2]}, Description: {record[3]}")

    def delete_vehicle(self):
        selected_index = self.vehicle_list.curselection()
        if selected_index:
            vehicle_id = self.vehicle_list.get(selected_index).split(':')[0]
            delete_vehicle(vehicle_id)
            self.load_vehicles()
            messagebox.showinfo("Success", "Vehicle deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a vehicle to delete")

    def delete_driver(self):
        selected_index = self.driver_list.curselection()
        if selected_index:
            driver_id = self.driver_list.get(selected_index).split(':')[0]
            delete_driver(driver_id)
            self.load_drivers()
            messagebox.showinfo("Success", "Driver deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a driver to delete")

    def delete_maintenance(self):
        selected_index = self.maintenance_list.curselection()
        if selected_index:
            maintenance_id = self.maintenance_list.get(selected_index).split(':')[0]
            delete_maintenance(maintenance_id)
            self.load_maintenance()
            messagebox.showinfo("Success", "Maintenance record deleted successfully!")
        else:
            messagebox.showwarning("Selection error", "Please select a maintenance record to delete")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = FleetManagementApp(root)
    root.mainloop()
