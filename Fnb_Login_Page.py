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

def login_check():
    username = usernameField.get()
    password = passwordField.get()
    if username == "" or password == "":
        messagebox.showinfo("Error", "All fields are required")
    else:
        try:
            cur.execute("select * from login where user_name='%s'" % (username))
            op = cur.fetchone()
            uname = op[1]
            passw = op[2]
            if uname == username and passw == password:
                try:
                    login_frame.destroy()
                    HomePage.Home(mainwindow)
                except:
                    pass
        except:
            messagebox.showerror("Error Due to: ", "enter correct details")
mainwindow = Tk()
mainwindow.geometry("800x600")
mainwindow.config(bg="#E3F0F1")
img = PhotoImage(file="sevarity.png")
mainwindow.iconphoto(False, img)
mainwindow.title("Login Page")
def Login_Page():
    global login_frame,usernameField,passwordField
    login_frame = Frame(mainwindow, width=400, height=300, highlightbackground='black', highlightthicknes=2)
    login_frame.pack(expand=True)
    login_frame.config(bg="#E3F0F1")
    username_label = Label(login_frame, text="Enter Username:", font=("arial", 12))
    username_label.place(x=80, y=50)
    usernameField = Entry(login_frame, width=20, font=("bold", 14))
    usernameField.place(x=80, y=70)

    password_label = Label(login_frame, text="Enter Password:", font=("arial", 12))
    password_label.place(x=80, y=100)
    passwordField = Entry(login_frame, show="*", width=20, font=("bold", 14))
    passwordField.place(x=80, y=125)

    # Create a button to print the details
    print_button = tk.Button(login_frame, text="Login", command=login_check)
    print_button.place(x=260, y=170)
Login_Page()
# Run the Tkinter event loop
mainwindow.mainloop()
