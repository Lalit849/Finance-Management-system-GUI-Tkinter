import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import hashlib
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------- Helpers -----------------
def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def safe_int(x, default=0):
    try:
        return int(x)
    except:
        return default
    


# ----------------- Main App -----------------
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finance Management System")
        
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Set window size to full screen
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.minsize(screen_width, screen_height)
        self.configure(bg="#f3f6fb")
        
        self.init_db()

        # In-memory storage
        self.users = {}
        self.data = {}

        # background images per frame
        self.backgrounds = {}

        # Container
        self.container = tk.Frame(self, bg="#f3f6fb")
        self.container.place(relwidth=1, relheight=1)

        # Create frames
        self.frames = {}
        for F in (LoginFrame, SignupFrame, DashboardFrame, AnalyticsFrame):
            frame = F(self.container, self)
            frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
            self.frames[F] = frame

        self.show_frame(LoginFrame)

    
    def init_db(self):
        self.conn = sqlite3.connect("finance.db")
        self.cur = self.conn.cursor()

        # Users table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)

        # Companies table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                name TEXT,
                income INTEGER,
                expense INTEGER,
                balance INTEGER,
                FOREIGN KEY(username) REFERENCES users(username)
            )
        """)
        self.conn.commit()

    def show_frame(self, cls):
        frame = self.frames[cls]
        frame.tkraise()

    def get_user_companies(self, username):
        if username not in self.data:
            self.data[username] = []
        return self.data[username]

# ----------------- Login Frame -----------------
# ----------------- Login Frame -----------------
class LoginFrame(tk.Frame):
    def __init__(self, parent, app: MainApp):
        super().__init__(parent, bg="#94e7bf")
        self.app = app

        box = tk.Frame(self, bg="skyblue", bd=6, relief="ridge")
        box.place(relx=0.465, rely=0.511, anchor="center", width=470, height=352)

        title = tk.Label(box, text="Finance Management — Login", font=("Segoe UI", 22, "bold"), bg="skyblue", fg="#003a6b")
        title.pack(pady=(10,8))

        tk.Label(box, text="Username", font=("Segoe UI", 12), bg="skyblue").pack(pady=(8,2))
        self.username = tk.Entry(box, font=("Segoe UI", 14), width=28)
        self.username.pack()

        tk.Label(box, text="Password", font=("Segoe UI", 12), bg="skyblue").pack(pady=(10,2))
        self.password = tk.Entry(box, font=("Segoe UI", 14), show="*", width=28)
        self.password.pack()

        btn_frame = tk.Frame(box, bg="skyblue")
        btn_frame.pack(pady=18, fill="x", padx=20)

        login_btn = tk.Button(btn_frame, text="Login", font=("Segoe UI", 13, "bold"), bg="#28a745", fg="white",
                              command=self.login)
        login_btn.pack(side="left", expand=True, fill="x", padx=(0,10))

        signup_btn = tk.Button(btn_frame, text="Signup", font=("Segoe UI", 13, "bold"), bg="#007bff", fg="white",
                               command=lambda: app.show_frame(SignupFrame))
        signup_btn.pack(side="right", expand=True, fill="x", padx=(10,0))

        forgot_btn = tk.Button(box, text="Forgot Password?", font=("Segoe UI", 10, "underline"),
                       fg="blue", bg="skyblue", bd=0, cursor="hand2",
                       command=self.forgot_password)
        forgot_btn.pack(pady=(4,0))

    def login(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Input Error", "Both username and password required.")
            return

        self.app.cur.execute("SELECT password FROM users WHERE username=?", (user,))
        row = self.app.cur.fetchone()
        if row and row[0] == hash_password(pwd):
            self.app.current_user = user
            self.app.frames[DashboardFrame].refresh_table()
            self.app.show_frame(DashboardFrame)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")
            
    # Inside LoginFrame __init__, after signup_btn

    def forgot_password(self):
        win = tk.Toplevel(self)
        win.title("Reset Password")
        win.geometry("420x300")  # Make it slightly bigger
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Enter your username:", font=("Segoe UI", 12)).pack(pady=(20,6))
        username_e = tk.Entry(win, font=("Segoe UI", 12), width=30)
        username_e.pack()

        tk.Label(win, text="New Password:", font=("Segoe UI", 12)).pack(pady=(12,6))
        new_pw = tk.Entry(win, font=("Segoe UI", 12), show="*", width=30)
        new_pw.pack()

        tk.Label(win, text="Confirm Password:", font=("Segoe UI", 12)).pack(pady=(12,6))
        confirm_pw = tk.Entry(win, font=("Segoe UI", 12), show="*", width=30)
        confirm_pw.pack()

        def reset():
            user = username_e.get().strip()
            p1 = new_pw.get().strip()
            p2 = confirm_pw.get().strip()

            if not user or not p1 or not p2:
                messagebox.showwarning("Input Error", "All fields are required.")
                return
            if p1 != p2:
                messagebox.showwarning("Input Error", "Passwords do not match.")
                return

            self.app.cur.execute("SELECT username FROM users WHERE username=?", (user,))
            if not self.app.cur.fetchone():
                messagebox.showerror("Error", "Username does not exist.")
                return

            hashed = hash_password(p1)
            self.app.cur.execute("UPDATE users SET password=? WHERE username=?", (hashed, user))
            self.app.conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            win.destroy()

        tk.Button(win, text="Save / Reset Password", font=("Segoe UI", 12, "bold"),
              bg="#ff6f00", fg="white", command=reset).pack(pady=(20,10))



# ----------------- Signup Frame -----------------
class SignupFrame(tk.Frame):
    def __init__(self, parent, app: MainApp):
        super().__init__(parent, bg="#fff6ea")
        self.app = app

        box = tk.Frame(self, bg="white", bd=6, relief="ridge")
        box.place(relx=0.5, rely=0.5, anchor="center", width=520, height=440)

        title = tk.Label(box, text="Create Account — Signup", font=("Segoe UI", 22, "bold"), bg="white", fg="#7a2b2b")
        title.pack(pady=(8,8))

        tk.Label(box, text="Choose Username", font=("Segoe UI", 12), bg="white").pack(pady=(6,2))
        self.username = tk.Entry(box, font=("Segoe UI", 14), width=28)
        self.username.pack()

        tk.Label(box, text="Choose Password", font=("Segoe UI", 12), bg="white").pack(pady=(10,2))
        self.password = tk.Entry(box, font=("Segoe UI", 14), show="*", width=28)
        self.password.pack()

        tk.Label(box, text="Confirm Password", font=("Segoe UI", 12), bg="white").pack(pady=(10,2))
        self.password2 = tk.Entry(box, font=("Segoe UI", 14), show="*", width=28)
        self.password2.pack()

        btn_frame = tk.Frame(box, bg="white")
        btn_frame.pack(pady=18, fill="x", padx=20)

        reg_btn = tk.Button(btn_frame, text="Register", font=("Segoe UI", 13, "bold"), bg="#ff6f00", fg="white",
                            command=self.register)
        reg_btn.pack(side="left", expand=True, fill="x", padx=(0,10))

        back_btn = tk.Button(btn_frame, text="Back to Login", font=("Segoe UI", 13, "bold"), bg="#6c757d", fg="white",
                             command=lambda: app.show_frame(LoginFrame))
        back_btn.pack(side="right", expand=True, fill="x", padx=(10,0))

    def register(self):
        user = self.username.get().strip()
        p1 = self.password.get().strip()
        p2 = self.password2.get().strip()

        if not user or not p1 or not p2:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        if p1 != p2:
            messagebox.showwarning("Input Error", "Passwords do not match.")
            return

        hashed_pw = hash_password(p1)

        try:
            self.app.cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (user, hashed_pw))
            self.app.conn.commit()
            messagebox.showinfo("Registered", "Account created successfully! Please login.")
            self.app.show_frame(LoginFrame)
        except sqlite3.IntegrityError:
            messagebox.showerror("Register Error", "Username already exists.")


# ----------------- Dashboard Frame -----------------
class DashboardFrame(tk.Frame):
    def __init__(self, parent, app: MainApp):
        super().__init__(parent, bg="#f9fff4")
        self.app = app

        # background
        self.bg_label = tk.Label(self, bg="#f9fff4")
        self.bg_label.place(relwidth=0.8, relheight=1)

        # Header
        header = tk.Frame(self, bg="#0b3d91")
        header.place(relx=0, rely=0, relwidth=1, height=80)
        self.title_lbl = tk.Label(header, text="Company Finance Management System", font=("Segoe UI", 20, "bold"),
                                  fg="white", bg="#0b3d91")
        self.title_lbl.pack(side="left", padx=18)
        # username display + logout
        self.user_lbl = tk.Label(header, text="", font=("Segoe UI", 12), fg="white", bg="#0b3d91")
        self.user_lbl.pack(side="right", padx=18)
        logout_btn = tk.Button(header, text="Logout", bg="#ff5c5c", fg="white", font=("Segoe UI", 10, "bold"),
                               command=self.logout)
        logout_btn.pack(side="right", padx=12)

        # Action frame (Add Income/Expense / Audit / Analytics)
        action = tk.Frame(self, bg="#f9fff4")
        action.place(relx=0.02, rely=0.12, relwidth=0.96, height=110)

        # Company combobox
        tk.Label(action, text="Company:", font=("Segoe UI", 12), bg="#f9fff4").place(relx=0.01, rely=0.12)
        self.company_cb = ttk.Combobox(action, values=[], font=("Segoe UI", 12), width=26, state="readonly")
        self.company_cb.place(relx=0.12, rely=0.12)

        # Amount
        tk.Label(action, text="Amount (₹):", font=("Segoe UI", 12), bg="#f9fff4").place(relx=0.01, rely=0.6)
        self.amount_entry = tk.Entry(action, font=("Segoe UI", 12), width=18)
        self.amount_entry.place(relx=0.12, rely=0.6)

        # Type combobox
        tk.Label(action, text="Type:", font=("Segoe UI", 12), bg="#f9fff4").place(relx=0.42, rely=0.12)
        self.type_cb = ttk.Combobox(action, values=["Income", "Expense"], font=("Segoe UI", 12), width=14, state="readonly")
        self.type_cb.place(relx=0.48, rely=0.12)
        self.type_cb.set("Income")

        # Add button
        add_btn = tk.Button(action, text="Add Transaction", font=("Segoe UI", 12, "bold"), bg="#198754", fg="white",
                            command=self.add_transaction)
        add_btn.place(relx=0.48, rely=0.55, width=170, height=34)

        # Audit button
        audit_btn = tk.Button(action, text="Audit (Recompute Balances)", font=("Segoe UI", 12, "bold"), bg="#0d6efd", fg="white",
                              command=self.audit_all)
        audit_btn.place(relx=0.7, rely=0.12, width=280, height=34)

        # Analytics button and Set Background
        analytics_btn = tk.Button(action, text="Show Analytics (Charts)", font=("Segoe UI", 12, "bold"), bg="#6f42c1", fg="white",
                                  command=lambda: self.app.show_frame(AnalyticsFrame))
        analytics_btn.place(relx=0.7, rely=0.55, width=200, height=34)

        # Table area
        table_frame = tk.Frame(self, bg="white", bd=1, relief="sunken")
        table_frame.place(relx=0.02, rely=0.32, relwidth=0.96, relheight=0.56)

        cols = ("Company", "Income", "Expense", "Balance")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Bottom full-width buttons (Add Company / Delete Company)
        bottom = tk.Frame(self, bg="#f9fff4")
        bottom.place(relx=0, rely=0.92, relwidth=1, relheight=0.08)

        add_company_btn = tk.Button(bottom, text="➕ Add Company Data", font=("Segoe UI", 14, "bold"),
                                    bg="#20c997", fg="white", command=self.add_company_popup)
        add_company_btn.pack(side="left", expand=True, fill="x", padx=8, pady=6)

        del_company_btn = tk.Button(bottom, text="🗑️ Delete Company Data (Select Row)", font=("Segoe UI", 14, "bold"),
                                    bg="#dc3545", fg="white", command=self.delete_company)
        del_company_btn.pack(side="left", expand=True, fill="x", padx=8, pady=6)
        
        export_btn = tk.Button(bottom, text="📂 Export CSV Report", font=("Segoe UI", 14, "bold"),
                       bg="#0dcaf0", fg="white", command=self.export_csv)
        export_btn.pack(side="left", expand=True, fill="x", padx=8, pady=6)


    def refresh_company_combobox(self):
        self.app.cur.execute("SELECT name FROM companies WHERE username=?", (self.app.current_user,))
        comps = [r[0] for r in self.app.cur.fetchall()]
        self.company_cb['values'] = comps
        if comps:
            self.company_cb.set(comps[0])
        else:
            self.company_cb.set("")

    def refresh_table(self):
        self.user_lbl.configure(text=f"User: {self.app.current_user}")
        for r in self.tree.get_children():
            self.tree.delete(r)

        self.app.cur.execute("SELECT name,income,expense,balance FROM companies WHERE username=?",
                            (self.app.current_user,))
        rows = self.app.cur.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

        self.refresh_company_combobox()


    def add_company_popup(self):
        win = tk.Toplevel(self)
        win.title("Add Company")
        win.geometry("420x300")
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Company Name:", font=("Segoe UI", 12)).pack(pady=(18,6))
        name_e = tk.Entry(win, font=("Segoe UI", 12), width=36)
        name_e.pack()

        tk.Label(win, text="Initial Income (₹):", font=("Segoe UI", 12)).pack(pady=(12,6))
        income_e = tk.Entry(win, font=("Segoe UI", 12), width=36)
        income_e.pack()

        tk.Label(win, text="Initial Expense (₹):", font=("Segoe UI", 12)).pack(pady=(12,6))
        expense_e = tk.Entry(win, font=("Segoe UI", 12), width=36)
        expense_e.pack()

        def save():
            name = name_e.get().strip()
            if not name:
                messagebox.showwarning("Input Error", "Company name required.")
                return
            income = safe_int(income_e.get(), 0)
            expense = safe_int(expense_e.get(), 0)
            balance = income - expense

            # Check duplicate
            self.app.cur.execute("SELECT 1 FROM companies WHERE username=? AND LOWER(name)=?",
                                (self.app.current_user, name.lower()))
            if self.app.cur.fetchone():
                messagebox.showerror("Duplicate", "Company already exists.")
                return

            self.app.cur.execute("INSERT INTO companies (username,name,income,expense,balance) VALUES (?,?,?,?,?)",
                                (self.app.current_user, name, income, expense, balance))
            self.app.conn.commit()
            self.refresh_table()
            win.destroy()


        tk.Button(win, text="Save Company", font=("Segoe UI", 12, "bold"), bg="#0d6efd", fg="white", command=save).pack(pady=18)

    def delete_company(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Row", "Please select a company row to delete.")
            return
        item = self.tree.item(sel[0])
        name = item['values'][0]
        comps = self.app.get_user_companies(self.app.current_user)
        newlist = [c for c in comps if c['name'] != name]
        self.app.data[self.app.current_user] = newlist
        self.refresh_table()

    def add_transaction(self):
        company = self.company_cb.get()
        amount = safe_int(self.amount_entry.get(), 0)
        ttype = self.type_cb.get()

        if not company or amount <= 0:
            messagebox.showwarning("Input Error", "Select company and valid amount.")
            return

        if ttype == "Income":
            self.app.cur.execute("""
                UPDATE companies 
                SET income = income + ?, balance = balance + ? 
                WHERE username=? AND name=?""",
                (amount, amount, self.app.current_user, company))
        else:  # Expense
            self.app.cur.execute("""
                UPDATE companies 
                SET expense = expense + ?, balance = balance - ? 
                WHERE username=? AND name=?""",
                (amount, amount, self.app.current_user, company))

        self.app.conn.commit()
        self.refresh_table()
        messagebox.showinfo("Success", f"{ttype} of ₹{amount} added to {company}.")


    def audit_all(self):
        self.app.cur.execute("SELECT name, income, expense FROM companies WHERE username=?",
                            (self.app.current_user,))
        rows = self.app.cur.fetchall()

        if not rows:
            messagebox.showinfo("Audit", "No company data available.")
            return

        messages = []
        for name, income, expense in rows:
            balance = (income or 0) - (expense or 0)
            status = "Profit" if balance >= 0 else "Loss"
            messages.append(f"{name}: {status} (Balance ₹{balance})")

        # popup me show karna
        result = "\n".join(messages)
        messagebox.showinfo("Audit Result", result)

        # table refresh bhi kare
        self.refresh_table()

    
    def export_csv(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file:
            return

        # --- Fetch latest data from DB ---
        self.app.cur.execute(
            "SELECT name,income,expense,balance FROM companies WHERE username=?",
            (self.app.current_user,)
        )
        rows = self.app.cur.fetchall()

        if not rows:
            messagebox.showinfo("No Data", "No company data to export.")
            return

        # --- Write CSV ---
        import csv
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Company", "Income", "Expense", "Balance"])
            writer.writerows(rows)

        messagebox.showinfo("Exported", f"Data exported to {file}")


    def logout(self):
        self.app.current_user = None
        self.app.show_frame(LoginFrame)

# ----------------- Analytics Frame -----------------
class AnalyticsFrame(tk.Frame):
    def __init__(self, parent, app: MainApp):
        super().__init__(parent, bg="#fffaf0")
        self.app = app

        self.bg_label = tk.Label(self, bg="#fffaf0")
        self.bg_label.place(relwidth=1, relheight=1)

        header = tk.Frame(self, bg="#343a40")
        header.place(relx=0, rely=0, relwidth=1, height=70)
        tk.Label(header, text="Analytics — Charts", font=("Segoe UI", 18, "bold"), fg="white", bg="#343a40").pack(side="left", padx=16)
        tk.Button(header, text="Back", bg="#fd7e14", fg="white", font=("Segoe UI", 11, "bold"),
                  command=self.go_back).pack(side="right", padx=12)

        # Chart area
        self.canvas_frame = tk.Frame(self, bg="white", bd=1, relief="sunken")
        self.canvas_frame.place(relx=0.02, rely=0.12, relwidth=0.96, relheight=0.76)

        # Buttons for chart type and set bg
        controls = tk.Frame(self, bg="#fffaf0")
        controls.place(relx=0.02, rely=0.9, relwidth=0.96, relheight=0.08)
        bar_btn = tk.Button(controls, text="Bar Chart (Income vs Expense)", font=("Segoe UI", 12, "bold"),
                            bg="#0dcaf0", fg="white", command=self.plot_bar)
        bar_btn.pack(side="left", expand=True, fill="x", padx=8, pady=8)
        pie_btn = tk.Button(controls, text="Pie Chart (Expense Distribution)", font=("Segoe UI", 12, "bold"),
                            bg="#6610f2", fg="white", command=self.plot_pie)
        pie_btn.pack(side="left", expand=True, fill="x", padx=8, pady=8)
        
    def go_back(self):
        # before going back refresh dashboard
        self.app.frames[DashboardFrame].refresh_table()
        self.app.show_frame(DashboardFrame)

    def clear_canvas(self):
        for w in self.canvas_frame.winfo_children():
            w.destroy()


    def plot_bar(self):
        self.clear_canvas()
        self.app.cur.execute("SELECT name,income,expense FROM companies WHERE username=?",
                            (self.app.current_user,))
        rows = self.app.cur.fetchall()
        if not rows:
            messagebox.showinfo("No Data", "No company data available to plot.")
            return

        names = [r[0] for r in rows]
        incomes = [r[1] or 0 for r in rows]
        expenses = [r[2] or 0 for r in rows]

        fig, ax = plt.subplots(figsize=(8,4.5))
        x = range(len(names))
        ax.bar([i-0.2 for i in x], incomes, width=0.4, label='Income')
        ax.bar([i+0.2 for i in x], expenses, width=0.4, label='Expense')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=30, ha="right")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Income vs Expense per Company")
        ax.legend()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def plot_pie(self):
        self.clear_canvas()
        self.app.cur.execute("SELECT name,expense FROM companies WHERE username=?",
                            (self.app.current_user,))
        rows = self.app.cur.fetchall()
        pairs = [(r[0], r[1]) for r in rows if (r[1] or 0) > 0]
        if not pairs:
            messagebox.showinfo("No Expense Data", "All companies have zero expenses.")
            return

        names, expenses = zip(*pairs)
        fig, ax = plt.subplots(figsize=(6,6))
        ax.pie(expenses, labels=names, autopct='%1.1f%%', startangle=140)
        ax.set_title("Expense Distribution (by Company)")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# ----------------- Run -----------------
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
