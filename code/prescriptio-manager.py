import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            specialization TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            medication TEXT,
            dosage TEXT,
            date TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
            FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a patient
def add_patient():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)', (name, age, gender))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Patient added successfully!")
    clear_entries()

# Function to update a patient
def update_patient():
    patient_id = update_patient_id_entry.get()
    name = update_name_entry.get()
    age = update_age_entry.get()
    gender = update_gender_entry.get()
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE patients SET name=?, age=?, gender=? WHERE patient_id=?', (name, age, gender, patient_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Patient updated successfully!")
    clear_entries()

# Function to add a doctor
def add_doctor():
    name = doctor_name_entry.get()
    specialization = doctor_specialization_entry.get()
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO doctors (name, specialization) VALUES (?, ?)', (name, specialization))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Doctor added successfully!")
    clear_entries()

# Function to add a prescription
def add_prescription():
    patient_id = patient_id_entry.get()
    doctor_id = doctor_id_entry.get()
    medication = medication_entry.get()
    dosage = dosage_entry.get()
    date = date_entry.get()
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO prescriptions (patient_id, doctor_id, medication, dosage, date) VALUES (?, ?, ?, ?, ?)',
                   (patient_id, doctor_id, medication, dosage, date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Prescription added successfully!")
    clear_entries()

# Function to update a prescription
def update_prescription():
    prescription_id = update_prescription_id_entry.get()
    medication = update_medication_entry.get()
    dosage = update_dosage_entry.get()
    date = update_date_entry.get()
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE prescriptions SET medication=?, dosage=?, date=? WHERE prescription_id=?',
                   (medication, dosage, date, prescription_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Prescription updated successfully!")
    clear_entries()

# Function to generate a report
def generate_report():
    patient_id = report_patient_id_entry.get()
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prescriptions WHERE patient_id = ?', (patient_id,))
    prescriptions = cursor.fetchall()
    conn.close()
    report = f"Prescription Report for Patient ID: {patient_id}\n"
    for prescription in prescriptions:
        report += f"Prescription ID: {prescription[0]}, Doctor ID: {prescription[2]}, Medication: {prescription[3]}, Dosage: {prescription[4]}, Date: {prescription[5]}\n"
    messagebox.showinfo("Report", report)
    clear_entries()

# Function to view all patients
def view_patients():
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    conn.close()
    patient_list = ""
    for patient in patients:
        patient_list += f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Gender: {patient[3]}\n"
    messagebox.showinfo("Patients", patient_list)

# Function to view all doctors
def view_doctors():
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM doctors')
    doctors = cursor.fetchall()
    conn.close()
    doctor_list = ""
    for doctor in doctors:
        doctor_list += f"ID: {doctor[0]}, Name: {doctor[1]}, Specialization: {doctor[2]}\n"
    messagebox.showinfo("Doctors", doctor_list)

# Function to view all prescriptions
def view_prescriptions():
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prescriptions')
    prescriptions = cursor.fetchall()
    conn.close()
    prescription_list = ""
    for prescription in prescriptions:
        prescription_list += f"ID: {prescription[0]}, Patient ID: {prescription[1]}, Doctor ID: {prescription[2]}, Medication: {prescription[3]}, Dosage: {prescription[4]}, Date: {prescription[5]}\n"
    messagebox.showinfo("Prescriptions", prescription_list)

# Function to search patients by name
def search_patient():
    name = search_name_entry.get()
    conn = sqlite3.connect('prescription_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE name LIKE ?', ('%' + name + '%',))
    patients = cursor.fetchall()
    conn.close()
    patient_list = ""
    for patient in patients:
        patient_list += f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Gender: {patient[3]}\n"
    messagebox.showinfo("Search Results", patient_list)
    clear_entries()

# Function to clear entries
def clear_entries():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    doctor_name_entry.delete(0, tk.END)
    doctor_specialization_entry.delete(0, tk.END)
    patient_id_entry.delete(0, tk.END)
    doctor_id_entry.delete(0, tk.END)
    medication_entry.delete(0, tk.END)
    dosage_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    report_patient_id_entry.delete(0, tk.END)
    update_patient_id_entry.delete(0, tk.END)
    update_name_entry.delete(0, tk.END)
    update_age_entry.delete(0, tk.END)
    update_gender_entry.delete(0, tk.END)
    update_prescription_id_entry.delete(0, tk.END)
    update_medication_entry.delete(0, tk.END)
    update_dosage_entry.delete(0, tk.END)
    update_date_entry.delete(0, tk.END)
    search_name_entry.delete(0, tk.END)

# Initialize the database
init_db()

# Create the main window
root = tk.Tk()
root.title("Prescription Management System")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create frames for each tab
patient_frame = ttk.Frame(notebook)
doctor_frame = ttk.Frame(notebook)
prescription_frame = ttk.Frame(notebook)
report_frame = ttk.Frame(notebook)
update_frame = ttk.Frame(notebook)
view_frame = ttk.Frame(notebook)
search_frame = ttk.Frame(notebook)

notebook.add(patient_frame, text='Add Patient')
notebook.add(doctor_frame, text='Add Doctor')
notebook.add(prescription_frame, text='Add Prescription')
notebook.add(report_frame, text='Generate Report')
notebook.add(update_frame, text='Update Information')
notebook.add(view_frame, text='View Information')
notebook.add(search_frame, text='Search Patient')

# Patient Frame
tk.Label(patient_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(patient_frame)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(patient_frame, text="Age:").grid(row=1, column=0, padx=10, pady=10)
age_entry = tk.Entry(patient_frame)
age_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(patient_frame, text="Gender:").grid(row=2, column=0, padx=10, pady=10)
gender_entry = tk.Entry(patient_frame)
gender_entry.grid(row=2, column=1, padx=10, pady=10)

add_patient_button = tk.Button(patient_frame, text="Add Patient", command=add_patient)
add_patient_button.grid(row=3, column=0, columnspan=2, pady=10)

# Doctor Frame
tk.Label(doctor_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
doctor_name_entry = tk.Entry(doctor_frame)
doctor_name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(doctor_frame, text="Specialization:").grid(row=1, column=0, padx=10, pady=10)
doctor_specialization_entry = tk.Entry(doctor_frame)
doctor_specialization_entry.grid(row=1, column=1, padx=10, pady=10)

add_doctor_button = tk.Button(doctor_frame, text="Add Doctor", command=add_doctor)
add_doctor_button.grid(row=2, column=0, columnspan=2, pady=10)

# Prescription Frame
tk.Label(prescription_frame, text="Patient ID:").grid(row=0, column=0, padx=10, pady=10)
patient_id_entry = tk.Entry(prescription_frame)
patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(prescription_frame, text="Doctor ID:").grid(row=1, column=0, padx=10, pady=10)
doctor_id_entry = tk.Entry(prescription_frame)
doctor_id_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(prescription_frame, text="Medication:").grid(row=2, column=0, padx=10, pady=10)
medication_entry = tk.Entry(prescription_frame)
medication_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(prescription_frame, text="Dosage:").grid(row=3, column=0, padx=10, pady=10)
dosage_entry = tk.Entry(prescription_frame)
dosage_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(prescription_frame, text="Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=10)
date_entry = tk.Entry(prescription_frame)
date_entry.grid(row=4, column=1, padx=10, pady=10)

add_prescription_button = tk.Button(prescription_frame, text="Add Prescription", command=add_prescription)
add_prescription_button.grid(row=5, column=0, columnspan=2, pady=10)

# Report Frame
tk.Label(report_frame, text="Patient ID:").grid(row=0, column=0, padx=10, pady=10)
report_patient_id_entry = tk.Entry(report_frame)
report_patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

generate_report_button = tk.Button(report_frame, text="Generate Report", command=generate_report)
generate_report_button.grid(row=1, column=0, columnspan=2, pady=10)

# Update Frame
tk.Label(update_frame, text="Update Patient").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(update_frame, text="Patient ID:").grid(row=1, column=0, padx=10, pady=10)
update_patient_id_entry = tk.Entry(update_frame)
update_patient_id_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(update_frame, text="Name:").grid(row=2, column=0, padx=10, pady=10)
update_name_entry = tk.Entry(update_frame)
update_name_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(update_frame, text="Age:").grid(row=3, column=0, padx=10, pady=10)
update_age_entry = tk.Entry(update_frame)
update_age_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(update_frame, text="Gender:").grid(row=4, column=0, padx=10, pady=10)
update_gender_entry = tk.Entry(update_frame)
update_gender_entry.grid(row=4, column=1, padx=10, pady=10)

update_patient_button = tk.Button(update_frame, text="Update Patient", command=update_patient)
update_patient_button.grid(row=5, column=0, columnspan=2, pady=10)

tk.Label(update_frame, text="Update Prescription").grid(row=6, column=0, columnspan=2, pady=10)

tk.Label(update_frame, text="Prescription ID:").grid(row=7, column=0, padx=10, pady=10)
update_prescription_id_entry = tk.Entry(update_frame)
update_prescription_id_entry.grid(row=7, column=1, padx=10, pady=10)

tk.Label(update_frame, text="Medication:").grid(row=8, column=0, padx=10, pady=10)
update_medication_entry = tk.Entry(update_frame)
update_medication_entry.grid(row=8, column=1, padx=10, pady=10)

tk.Label(update_frame, text="Dosage:").grid(row=9, column=0, padx=10, pady=10)
update_dosage_entry = tk.Entry(update_frame)
update_dosage_entry.grid(row=9, column=1, padx=10, pady=10)

tk.Label(update_frame, text="Date (YYYY-MM-DD):").grid(row=10, column=0, padx=10, pady=10)
update_date_entry = tk.Entry(update_frame)
update_date_entry.grid(row=10, column=1, padx=10, pady=10)

update_prescription_button = tk.Button(update_frame, text="Update Prescription", command=update_prescription)
update_prescription_button.grid(row=11, column=0, columnspan=2, pady=10)

# View Frame
view_patients_button = tk.Button(view_frame, text="View All Patients", command=view_patients)
view_patients_button.grid(row=0, column=0, columnspan=2, pady=10)

view_doctors_button = tk.Button(view_frame, text="View All Doctors", command=view_doctors)
view_doctors_button.grid(row=1, column=0, columnspan=2, pady=10)

view_prescriptions_button = tk.Button(view_frame, text="View All Prescriptions", command=view_prescriptions)
view_prescriptions_button.grid(row=2, column=0, columnspan=2, pady=10)

# Search Frame
tk.Label(search_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
search_name_entry = tk.Entry(search_frame)
search_name_entry.grid(row=0, column=1, padx=10, pady=10)

search_patient_button = tk.Button(search_frame, text="Search Patient", command=search_patient)
search_patient_button.grid(row=1, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
