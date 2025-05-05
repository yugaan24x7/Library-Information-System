# 📚 Library Information System

A clean and user-friendly desktop application for managing library operations using Python and Tkinter. This system distinguishes between **Admins** (librarians) and **Users** (students/faculty), and maintains all data using simple CSV files.

---

## 🔧 Features

### ✅ Login System
- Password-protected login for both admins and users.
- Credentials stored securely in `users.csv`.

### 🧑‍💼 Admin Panel (Librarian)
- Add, edit, or delete book records.
- Add, update, or delete student accounts.
- View issued books per student.

### 👩‍🎓 User Portal (Students/Faculty)
- View dashboard with:
  - Books issued
  - Due dates
  - Fines
  - Membership expiry
- Search and browse books.
- Issue or return books (if no overdue).
- Renew library membership.

---

## 📁 Project Structure

```
library-info-system/
├── booklist.csv           # Book catalog and availability
├── studentlist.csv        # Students and their book records
├── users.csv              # Login credentials (Username, Role, Password)
├── login.py               # Login interface (entry point)
├── user_portal.py         # GUI for students/faculty
├── librarian_panel.py     # Admin interface for librarians
├── README.md              # Project documentation
```

---

## 🚀 Getting Started

### Step 1: Clone or Download
```bash
git clone https://github.com/your-username/library-info-system.git
cd library-info-system
```

### Step 2: Run the System
No external packages needed. Only built-in modules like `tkinter`, `pandas`, and `datetime` are used.

Ensure Python 3.8+ is installed.

```bash
python login.py
```

> ⚠️ **Note**: Sometimes the app doesn't launch properly if you run it using a text editor's "Run" button.  
> In that case, run it via command line using the command above.

---

## 🧪 Sample Users

| Username | Role   | Password  |
|----------|--------|-----------|
| admin1   | admin  | admin123  |
| admin2   | admin  | admin234  |
| bob      | user   | bobpass   |
| alice    | user   | alicepass |

More users are listed in `users.csv`.

---

## 📝 License
Free to use and modify. No license restrictions.
