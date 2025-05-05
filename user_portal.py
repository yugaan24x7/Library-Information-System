import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import sys
from datetime import datetime, timedelta

STUDENTS_FILE = "studentlist.csv"
BOOKS_FILE = "booklist.csv"

if len(sys.argv) < 2:
    messagebox.showerror("Error", "Username not provided")
    sys.exit()

username = sys.argv[1].lower()

# Load student record
try:
    students_df = pd.read_csv(STUDENTS_FILE)
    books_df = pd.read_csv(BOOKS_FILE)
except FileNotFoundError as e:
    messagebox.showerror("File Error", f"Required file not found: {str(e)}")
    sys.exit()

print("DEBUG: Available usernames =", students_df["Username"].str.lower().tolist())
print("DEBUG: Username provided =", username)
match = students_df[students_df["Username"].str.lower() == username]
if match.empty:
    messagebox.showerror("Error", "Student record not found.")
    sys.exit()

student = match.iloc[0]
student_id = student["Student ID"]
student_name = student["Student Name"]
books_issued = student["Books Issued"] if pd.notna(student["Books Issued"]) else ""
due_dates = student["Due Dates"] if pd.notna(student["Due Dates"]) else ""
fines_due = student["Fines Due"]
membership_expiry = student["Membership Expiry"]
reservations = student["Reservations"] if pd.notna(student["Reservations"]) else ""


def show_dashboard():
    msg = f"""📘 Dashboard for {student_name} (ID: {student_id})

📚 Books Issued:
{books_issued if books_issued else 'None'}

📅 Due Dates:
{due_dates if due_dates else 'N/A'}

💰 Fines Due:
₹{fines_due}

🪪 Membership Expiry:
{membership_expiry}

📌 Reservations:
{reservations if reservations else 'None'}
"""
    messagebox.showinfo("User Dashboard", msg)


def search_books():
    global books_df

    search_window = tk.Toplevel(root)
    search_window.title("Search Books")
    search_window.geometry("600x400")

    tk.Label(search_window, text="Search Books", font=("Segoe UI", 14, "bold")).pack(pady=10)

    search_frame = tk.Frame(search_window)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=1, padx=5)

    results_listbox = tk.Listbox(search_window, width=70, height=15)
    results_listbox.pack(pady=10, padx=20)

    # Display all books initially
    for _, row in books_df.iterrows():
        results_listbox.insert(tk.END,
                               f"{row['Book ID']} | {row['Book Name']} | {row['Author']} | Available: {row['Availability']}")

    def perform_search():
        results_listbox.delete(0, tk.END)
        query = search_entry.get().lower()

        for _, row in books_df.iterrows():
            if (query in str(row['Book ID']).lower() or
                    query in str(row['Book Name']).lower() or
                    query in str(row['Author']).lower()):
                results_listbox.insert(tk.END,
                                       f"{row['Book ID']} | {row['Book Name']} | {row['Author']} | Available: {row['Availability']}")

    tk.Button(search_frame, text="Search", command=perform_search).grid(row=0, column=2, padx=5)
    tk.Button(search_window, text="Close", command=search_window.destroy).pack(pady=10)


def issue_book():
    global books_issued, due_dates, books_df

    book_id = simpledialog.askstring("Issue Book", "Enter Book ID to issue:")
    if not book_id:
        return

    # Check if book exists and is available
    book_match = books_df[books_df["Book ID"] == book_id]
    if book_match.empty:
        messagebox.showerror("Error", f"Book ID {book_id} not found.")
        return

    if book_match.iloc[0]["Availability"] <= 0:
        messagebox.showerror("Error", f"Book {book_id} is not available.")
        return

    # Load fresh data
    df = pd.read_csv(STUDENTS_FILE)
    student_row = df[df["Username"].str.lower() == username]

    if student_row.empty:
        messagebox.showerror("Error", "Student record not found.")
        return

    student = student_row.iloc[0]

    # Overdue check
    due_str = student["Due Dates"]
    if pd.notna(due_str) and due_str.strip() != "":
        due_date_list = [d.strip() for d in due_str.split(",")]
        for date in due_date_list:
            try:
                if pd.to_datetime(date).date() < datetime.today().date():
                    messagebox.showerror("Blocked", "You have overdue books. Return them first.")
                    return
            except:
                continue

    # Update student record
    books = student["Books Issued"]
    dues = student["Due Dates"]
    new_due = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")

    updated_books = f"{books},{book_id}" if pd.notna(books) and books != "" else book_id
    updated_dues = f"{dues},{new_due}" if pd.notna(dues) and dues != "" else new_due

    # Save student changes
    df.loc[df["Username"].str.lower() == username, "Books Issued"] = updated_books
    df.loc[df["Username"].str.lower() == username, "Due Dates"] = updated_dues
    df.to_csv(STUDENTS_FILE, index=False)

    # Update book availability
    books_df = pd.read_csv(BOOKS_FILE)
    books_df.loc[books_df["Book ID"] == book_id, "Availability"] -= 1
    books_df.to_csv(BOOKS_FILE, index=False)

    messagebox.showinfo("Success", f"Book {book_id} issued! Due on {new_due}.")

    # Update local variables for dashboard
    books_issued = updated_books
    due_dates = updated_dues


def return_book():
    global books_issued, due_dates, books_df

    if not books_issued:
        messagebox.showinfo("Info", "You don't have any books to return.")
        return

    issued_books = books_issued.split(",") if books_issued else []
    if not issued_books:
        messagebox.showinfo("Info", "You don't have any books to return.")
        return

    window = tk.Toplevel(root)
    window.title("Return Book")
    window.geometry("400x300")

    tk.Label(window, text="Select Book to Return:", font=("Segoe UI", 12)).pack(pady=10)

    listbox = tk.Listbox(window, width=50, height=10)
    listbox.pack(pady=5, padx=20)

    for book_id in issued_books:
        book_info = books_df[books_df["Book ID"] == book_id.strip()]
        if not book_info.empty:
            book_name = book_info.iloc[0]["Book Name"]
            listbox.insert(tk.END, f"{book_id.strip()} - {book_name}")

    def process_return():
        nonlocal issued_books
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to return.")
            return

        book_id = issued_books[selected[0]].strip()

        # Update files
        students_df = pd.read_csv(STUDENTS_FILE)
        books_df_local = pd.read_csv(BOOKS_FILE)

        # Update student's records
        student_row = students_df[students_df["Username"].str.lower() == username]
        if student_row.empty:
            messagebox.showerror("Error", "Student record not found.")
            return

        # Get current books and due dates
        current_books = student_row.iloc[0]["Books Issued"].split(",") if pd.notna(
            student_row.iloc[0]["Books Issued"]) else []
        current_due_dates = student_row.iloc[0]["Due Dates"].split(",") if pd.notna(
            student_row.iloc[0]["Due Dates"]) else []

        # Find index of book to remove
        book_index = -1
        for i, b in enumerate(current_books):
            if b.strip() == book_id:
                book_index = i
                break

        if book_index >= 0:
            current_books.pop(book_index)
            if book_index < len(current_due_dates):
                current_due_dates.pop(book_index)

            # Update student record
            new_books = ",".join(current_books) if current_books else ""
            new_due_dates = ",".join(current_due_dates) if current_due_dates else ""

            students_df.loc[students_df["Username"].str.lower() == username, "Books Issued"] = new_books
            students_df.loc[students_df["Username"].str.lower() == username, "Due Dates"] = new_due_dates
            students_df.to_csv(STUDENTS_FILE, index=False)

            # Update book availability
            books_df_local.loc[books_df_local["Book ID"] == book_id, "Availability"] += 1
            books_df_local.to_csv(BOOKS_FILE, index=False)

            # Update global state with local changes
            global books_df
            books_df = books_df_local

            # Update local variables
            global books_issued, due_dates
            books_issued = new_books
            due_dates = new_due_dates

            messagebox.showinfo("Success", f"Book {book_id} returned successfully!")
            window.destroy()
        else:
            messagebox.showerror("Error", "Book not found in your records.")

    tk.Button(window, text="Return Selected Book", command=process_return, bg="#e67e22", fg="white").pack(pady=10)
    tk.Button(window, text="Cancel", command=window.destroy).pack()


def renew_membership():
    global membership_expiry

    current_expiry = datetime.strptime(membership_expiry, "%Y-%m-%d")
    new_expiry = current_expiry + timedelta(days=365)

    result = messagebox.askyesno("Renew Membership",
                                 f"Your current membership expires on {membership_expiry}.\n\n"
                                 f"Do you want to renew for one more year until {new_expiry.strftime('%Y-%m-%d')}?")

    if result:
        students_df = pd.read_csv(STUDENTS_FILE)
        students_df.loc[students_df["Username"].str.lower() == username, "Membership Expiry"] = new_expiry.strftime(
            "%Y-%m-%d")
        students_df.to_csv(STUDENTS_FILE, index=False)

        membership_expiry = new_expiry.strftime("%Y-%m-%d")

        messagebox.showinfo("Success", f"Membership renewed successfully until {new_expiry.strftime('%Y-%m-%d')}!")


# GUI
root = tk.Tk()
root.title(f"Library User Portal - {student_name}")
root.geometry("400x500")
root.configure(bg="#f5f6fa")

tk.Label(root, text=f"📘 Welcome {student_name}", font=("Segoe UI", 13, "bold"), bg="#f5f6fa").pack(pady=10)

tk.Button(root, text="📊 Dashboard", command=show_dashboard, bg="#1abc9c", fg="white", width=30).pack(pady=6)
tk.Button(root, text="🔍 Search Books", command=search_books, bg="#2980b9", fg="white", width=30).pack(pady=6)
tk.Button(root, text="📚 Issue Book", command=issue_book, bg="#27ae60", fg="white", width=30).pack(pady=6)
tk.Button(root, text="↩️ Return Book", command=return_book, bg="#e67e22", fg="white", width=30).pack(pady=6)
tk.Button(root, text="🔄 Renew Membership", command=renew_membership, bg="#9b59b6", fg="white", width=30).pack(pady=6)
tk.Button(root, text="Exit", command=root.quit, bg="gray", fg="white", width=30).pack(pady=20)

root.mainloop()