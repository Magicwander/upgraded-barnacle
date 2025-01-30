import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('voting_system.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS voters (
                voter_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                has_voted INTEGER DEFAULT 0)''')

c.execute('''CREATE TABLE IF NOT EXISTS candidates (
                candidate_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                vote_count INTEGER DEFAULT 0)''')

c.execute('''CREATE TABLE IF NOT EXISTS votes (
                vote_id INTEGER PRIMARY KEY,
                voter_id INTEGER,
                candidate_id INTEGER,
                vote_time TEXT,
                FOREIGN KEY(voter_id) REFERENCES voters(voter_id),
                FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id))''')

conn.commit()

# GUI setup
root = tk.Tk()
root.title("Online Voting System")
root.geometry("800x600")

# Styles
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", foreground="#000")
style.configure("TLabel", padding=6, background="#fff", foreground="#000")
style.configure("TFrame", padding=6, background="#fff")

# Functions
def register_voter():
    name = voter_name_entry.get()
    c.execute("INSERT INTO voters (name) VALUES (?)", (name,))
    conn.commit()
    messagebox.showinfo("Success", "Voter registered successfully")
    clear_entries()

def register_candidate():
    name = candidate_name_entry.get()
    c.execute("INSERT INTO candidates (name) VALUES (?)", (name,))
    conn.commit()
    messagebox.showinfo("Success", "Candidate registered successfully")
    clear_entries()

def cast_vote():
    voter_id = int(vote_voter_id_entry.get())
    candidate_id = int(vote_candidate_id_entry.get())
    vote_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the voter has already voted
    c.execute("SELECT has_voted FROM voters WHERE voter_id = ?", (voter_id,))
    has_voted = c.fetchone()[0]
    if has_voted:
        messagebox.showerror("Error", "Voter has already voted")
    else:
        c.execute("INSERT INTO votes (voter_id, candidate_id, vote_time) VALUES (?, ?, ?)", (voter_id, candidate_id, vote_time))
        c.execute("UPDATE voters SET has_voted = 1 WHERE voter_id = ?", (voter_id,))
        c.execute("UPDATE candidates SET vote_count = vote_count + 1 WHERE candidate_id = ?", (candidate_id,))
        conn.commit()
        messagebox.showinfo("Success", "Vote cast successfully")
    clear_entries()

def show_results():
    results_text.delete(1.0, tk.END)
    c.execute("SELECT name, vote_count FROM candidates")
    results = c.fetchall()
    for candidate in results:
        results_text.insert(tk.END, f"Candidate: {candidate[0]}, Votes: {candidate[1]}\n")

def clear_entries():
    voter_name_entry.delete(0, tk.END)
    candidate_name_entry.delete(0, tk.END)
    vote_voter_id_entry.delete(0, tk.END)
    vote_candidate_id_entry.delete(0, tk.END)

# Frames
register_voter_frame = ttk.LabelFrame(root, text="Register Voter")
register_voter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

register_candidate_frame = ttk.LabelFrame(root, text="Register Candidate")
register_candidate_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

vote_frame = ttk.LabelFrame(root, text="Cast Vote")
vote_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

results_frame = ttk.LabelFrame(root, text="Results")
results_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

# Register Voter Frame
ttk.Label(register_voter_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
voter_name_entry = ttk.Entry(register_voter_frame)
voter_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Button(register_voter_frame, text="Register Voter", command=register_voter).grid(row=1, column=0, columnspan=2, pady=5)

# Register Candidate Frame
ttk.Label(register_candidate_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
candidate_name_entry = ttk.Entry(register_candidate_frame)
candidate_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Button(register_candidate_frame, text="Register Candidate", command=register_candidate).grid(row=1, column=0, columnspan=2, pady=5)

# Vote Frame
ttk.Label(vote_frame, text="Voter ID").grid(row=0, column=0, padx=5, pady=5)
vote_voter_id_entry = ttk.Entry(vote_frame)
vote_voter_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(vote_frame, text="Candidate ID").grid(row=1, column=0, padx=5, pady=5)
vote_candidate_id_entry = ttk.Entry(vote_frame)
vote_candidate_id_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(vote_frame, text="Cast Vote", command=cast_vote).grid(row=2, column=0, columnspan=2, pady=5)

# Results Frame
ttk.Button(results_frame, text="Show Results", command=show_results).grid(row=0, column=0, pady=5)

results_text = tk.Text(results_frame, height=10, width=50)
results_text.grid(row=1, column=0, pady=5)

root.mainloop()

# Close the database connection
conn.close()
