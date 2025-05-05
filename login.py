import tkinter as tk
from tkinter import messagebox
import pandas as pd
import subprocess
import sys
import os

USERS_FILE = "users.csv"

# Load user-role mapping
try:
    users_df = pd.read_csv(USERS_FILE)
except FileNotFoundError:
    messagebox.showerror("Missing File", f"{USERS_FILE} not found.")
    sys.exit()


def login():
    username = username_entry.get().strip().lower()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    match = users_df[users_df["Username"].str.lower() == username]
    if match.empty:
        messagebox.showerror("Login Failed", "Username not found.")
        return

    stored_password = match.iloc[0]["Password"]
    if stored_password != password:
        messagebox.showerror("Login Failed", "Incorrect password.")
        return

    role = match.iloc[0]["Role"].lower()
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if role == "admin":
        admin_path = os.path.join(current_dir, "librarian_panel.py")
        subprocess.Popen([sys.executable, admin_path])
    else:
        user_portal_path = os.path.join(current_dir, "user_portal.py")
        subprocess.Popen([sys.executable, user_portal_path, username])

    root.destroy()


# GUI Setup
root = tk.Tk()
root.title("Library System Login")
root.geometry("300x220")
root.configure(bg="#ecf0f1")

tk.Label(root, text="Enter Username", font=("Segoe UI", 12), bg="#ecf0f1").pack(pady=8)
username_entry = tk.Entry(root, font=("Segoe UI", 11), width=25)
username_entry.pack()

tk.Label(root, text="Enter Password", font=("Segoe UI", 12), bg="#ecf0f1").pack(pady=8)
password_entry = tk.Entry(root, font=("Segoe UI", 11), width=25, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login, bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"), width=20).pack(pady=20)

root.mainloop()
