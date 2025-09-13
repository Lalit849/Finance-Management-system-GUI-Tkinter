import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class fin():
    def __init__(self,root):
        self.root = root
        self.root.title("Finance Management")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Finance Management System", bd=4, relief="groove", font=("Arial",50,"bold"), bg="light green")
        title.pack(side="top", fill="x")

        # add frame

        addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(200,210,180))
        addFrame.place(width=self.width/3, height=self.height-180, x=70, y=100)

        amountLbl = tk.Label(addFrame, text="Amount:", bg=self.clr(200,210,180), font=("Arial",15,"bold"))
        amountLbl.grid(row=0, column=0, padx=20, pady=30)
        self.amount = tk.Entry(addFrame, bd=2, width=20, font=("arial", 15))
        self.amount.grid(row=0, column=1, padx=10, pady=30)

        typeLbl = tk.Label(addFrame, text="Type:", bg=self.clr(200,210,180), font=("Arial",15,"bold"))
        typeLbl.grid(row=1, column=0, padx=20,pady=30)
        self.type = tk.Entry(addFrame, bd=2, width=20, font=("arial", 15))
        self.type.grid(row=1, column=1, padx=10, pady=30)

        incBtn = tk.Button(addFrame,command=self.incomeFun, bd=2, relief="raised", width=20, font=("arial", 20,"bold"), text="Income")
        incBtn.grid(row=2, column=0, padx=30, pady=30, columnspan=2)

        expBtn = tk.Button(addFrame,command=self.expFun, bd=2, relief="raised", width=20, font=("arial", 20,"bold"), text="Expence")
        expBtn.grid(row=3, column=0, padx=30, pady=30, columnspan=2)

        audBtn = tk.Button(addFrame,command=self.auditFun, bd=2, relief="raised", width=20, font=("arial", 20,"bold"), text="Audit")
        audBtn.grid(row=4, column=0, padx=30, pady=30, columnspan=2)

        # detail frame

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(210,180,200))
        self.detFrame.place(width=self.width/2, height=self.height-180, x=self.width/3+140, y=100)

        lbl = tk.Label(self.detFrame, text="Audit Details", bd=3, relief="groove", bg=self.clr(110,150,200), font=("Arial", 30, "bold"))
        lbl.pack(side="top", fill="x")

        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=5, relief="ridge", bg="cyan")
        tabFrame.place(width=self.width/2-40, height=self.height-270, x=17, y=70)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("comp","inc", "exp", "aud"))
        
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("comp", text="Company")
        self.table.heading("inc", text="Income")
        self.table.heading("exp", text="Expence")
        self.table.heading("aud", text="Balance")
        self.table["show"]="headings"
        

        self.table.pack(fill="both", expand=1)


    def incomeFun(self):
        amount = self.amount.get()
        tp = self.type.get()

        if amount and tp:
            amount_int = int(amount)
            try:
                self.dbFun()
                self.cur.execute("select income from finance where company='ABC'")
                row = self.cur.fetchone()
                upd = row[0]+amount_int
                self.cur.execute("update finance set income=%s where company='ABC'",upd)
                self.con.commit()
                tk.messagebox.showinfo("Success",f"{amount_int} amount of {tp} is added as Income")

                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from finance where company='ABC'")
                data = self.cur.fetchone()
                self.table.insert('',tk.END,values=data)
                self.con.close()


            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")

        else:
            tk.messagebox.showerror("Error", "Fill All Input Fields")


    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()

    def expFun(self):
        amount = self.amount.get()
        tp = self.type.get()

        if amount and tp:
            amount_int = int(amount)
            try:
                self.dbFun()
                self.cur.execute("select expence from finance where company='ABC'")
                row = self.cur.fetchone()
                upd = row[0]+amount_int
                self.cur.execute("update finance set expence=%s where company='ABC'",upd)
                self.con.commit()
                tk.messagebox.showinfo("Success",f"{amount_int} amount of {tp} is added as Expence")
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from finance where company='ABC'")
                data = self.cur.fetchone()
                self.table.insert('',tk.END,values=data)
                self.con.close()

            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")
        else:
            tk.messagebox.showerror("Error", "Fill All Input Fields")


    def auditFun(self):
        try:
            self.dbFun()
            self.cur.execute("select income, expence from finance where company='ABC'")
            data = self.cur.fetchone()
            inc = data[0]
            exp = data[1]
            audit = inc - exp
            self.cur.execute("update finance set balance=%s where company='ABC'",audit)
            self.con.commit()

            if audit >0:
                tk.messagebox.showinfo("Information","Company is in Profit")
            elif audit <0:
                tk.messagebox.showinfo("Information","Company is in Loss")

            self.tabFun()
            self.table.delete(*self.table.get_children())
            self.cur.execute("select * from finance where company='ABC'")
            info = self.cur.fetchone()
            self.table.insert('',tk.END,values=info)

        
        except Exception as e:
            tk.messagebox.showerror("Error",f"Error: {e}")


root = tk.Tk()
obj = fin(root)
root.mainloop()
