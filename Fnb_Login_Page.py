import tkinter as tk
import HomePage
from tkinter import *
import pymysql
from tkinter import messagebox
from tkinter.ttk import *
from Guarantor_Details import *
from PIL import Image, ImageTk

global mainwindow,title
mypass = "mysql"
con = pymysql.connect(host="localhost", user="root", password=mypass, database="fnb")
cur = con.cursor()

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

Login_Page()
# Run the Tkinter event loop
mainwindow.mainloop()

