import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import pandas as pd
from datetime import datetime

BOOKS_FILE = "booklist.csv"
STUDENTS_FILE = "studentlist.csv"

books_df = pd.read_csv(BOOKS_FILE)
students_df = pd.read_csv(STUDENTS_FILE)

def refresh_book_listbox(listbox, query=""):
    listbox.delete(0, tk.END)
    for _, row in books_df.iterrows():
        if query.lower() in row["Book Name"].lower() or query.lower() in row["Author"].lower():
            listbox.insert(tk.END, f"{row['Book ID']} | {row['Book Name']} | {row['Author']} | Available: {row['Availability']}")

def refresh_student_listbox(listbox, query=""):
    listbox.delete(0, tk.END)
    for _, row in students_df.iterrows():
        name = row["Student Name"]
        issued = row.get("Books Issued", "")
        expiry = row.get("Membership Expiry", "")
        fine = row.get("Fines Due", 0)

        flags = []
        if fine > 0:
            flags.append("FINE")
        try:
            if datetime.strptime(str(expiry), "%Y-%m-%d").date() < datetime.today().date():
                flags.append("EXPIRED")
        except:
            pass

        flag_str = " ⚠️ " + ", ".join(flags) if flags else ""
        if query.lower() in name.lower():
            listbox.insert(tk.END, f"{row['Student ID']} | {name} | Issued: {issued}{flag_str}")

def export_books():
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if path:
        books_df.to_csv(path, index=False)
        messagebox.showinfo("Exported", f"Books exported to {path}")

def export_students():
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if path:
        students_df.to_csv(path, index=False)
        messagebox.showinfo("Exported", f"Student data exported to {path}")

def add_book():
    global books_df
    book_id = simpledialog.askstring("Book ID", "Enter Book ID:")
    name = simpledialog.askstring("Book Name", "Enter Book Name:")
    author = simpledialog.askstring("Author", "Enter Author:")
    copies = simpledialog.askinteger("Copies", "Enter Number of Copies:")

    if book_id and name and author and copies is not None:
        books_df = pd.concat([books_df, pd.DataFrame([{
            'Book ID': book_id, 'Book Name': name, 'Author': author, 'Availability': copies
        }])], ignore_index=True)
        books_df.to_csv(BOOKS_FILE, index=False)
        refresh_book_listbox(book_listbox)

def delete_book():
    global books_df
    selected = book_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    book_id = books_df.iloc[index]['Book ID']
    books_df = books_df[books_df['Book ID'] != book_id]
    books_df.to_csv(BOOKS_FILE, index=False)
    refresh_book_listbox(book_listbox)

def add_student():
    global students_df
    sid = simpledialog.askinteger("Student ID", "Enter Student ID:")
    name = simpledialog.askstring("Student Name", "Enter Student Name:")
    if sid and name:
        students_df = pd.concat([students_df, pd.DataFrame([{
            'Student ID': sid,
            'Student Name': name,
            'Username': name.lower(),
            'Books Issued': '',
            'Due Dates': '',
            'Fines Due': 0,
            'Membership Expiry': datetime.today().date().strftime("%Y-%m-%d"),
            'Reservations': ''
        }])], ignore_index=True)
        students_df.to_csv(STUDENTS_FILE, index=False)
        refresh_student_listbox(student_listbox)

def delete_student():
    global students_df
    selected = student_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    sid = students_df.iloc[index]['Student ID']
    students_df = students_df[students_df['Student ID'] != sid]
    students_df.to_csv(STUDENTS_FILE, index=False)
    refresh_student_listbox(student_listbox)

# GUI
root = tk.Tk()
root.title("📚 Librarian Panel")
root.geometry("900x650")
root.configure(bg="#f5f6fa")

# --- Book Section ---
tk.Label(root, text="📘 Book Management", font=("Segoe UI", 14, "bold"), bg="#f5f6fa").pack(pady=5)
book_search = tk.Entry(root, width=40)
book_search.pack()
tk.Button(root, text="Search Books", command=lambda: refresh_book_listbox(book_listbox, book_search.get())).pack(pady=3)

book_listbox = tk.Listbox(root, width=100, height=8, font=("Courier", 10))
book_listbox.pack(pady=5)

tk.Button(root, text="Add Book", command=add_book, bg="#3498db", fg="white").pack(pady=2)
tk.Button(root, text="Delete Book", command=delete_book, bg="#e74c3c", fg="white").pack(pady=2)
tk.Button(root, text="Export Book CSV", command=export_books, bg="#2ecc71", fg="white").pack(pady=5)

# --- Student Section ---
tk.Label(root, text="👥 Student Records", font=("Segoe UI", 14, "bold"), bg="#f5f6fa").pack(pady=10)
student_search = tk.Entry(root, width=40)
student_search.pack()
tk.Button(root, text="Search Students", command=lambda: refresh_student_listbox(student_listbox, student_search.get())).pack(pady=3)

student_listbox = tk.Listbox(root, width=100, height=8, font=("Courier", 10))
student_listbox.pack(pady=5)

tk.Button(root, text="Add Student", command=add_student, bg="#27ae60", fg="white").pack(pady=2)
tk.Button(root, text="Delete Student", command=delete_student, bg="#c0392b", fg="white").pack(pady=2)
tk.Button(root, text="Export Student CSV", command=export_students, bg="#f1c40f", fg="black").pack(pady=5)

tk.Button(root, text="Exit", command=root.quit, bg="gray", fg="white", width=20).pack(pady=20)

refresh_book_listbox(book_listbox)
refresh_student_listbox(student_listbox)

root.mainloop()
