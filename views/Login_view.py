import tkinter as tk
from tkinter import ttk

class LoginView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="#A7C7E7")
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.staff_var = tk.IntVar()  # Variable for staff checkbox
        self.login_type = tk.StringVar(value="Customer")
        self.display()

    def display(self):
        # Login Title
        self.title = ttk.Label(self, text=f"{self.login_type.get()} Login", font=("Georgia", 24, "bold"))

        # username & password
        self.username_lbl = ttk.Label(self, text="Account:")
        self.username_lbl.grid(row=0, column=0)
        self.username_ent = ttk.Entry(self, textvariable=self.username_var)
        self.username_ent.grid(row=0, column=1)

        self.password_lbl = ttk.Label(self, text="Password:")
        self.password_lbl.grid(row=1, column=0)
        self.password_ent = ttk.Entry(self, textvariable=self.password_var, show="*")
        self.password_ent.grid(row=1, column=1)

        # Checkboxes
        self.vip_cbtn = ttk.Checkbutton(self, text="VIP")
        self.vip_cbtn.grid(row=2, column=0)

        self.staff_cbtn = ttk.Checkbutton(self, text="Staff", variable=self.staff_var)
        self.staff_cbtn.grid(row=2, column=1)

        # Buttons
        log_btn = ttk.Button(self, text="Login", command=self.login)
        log_btn.grid(row=2, column=2)

        #guestLog_btn = ttk.Button(self, text="GuestLogin", command=self.guestLogin)
        #guestLog_btn.grid(row=3, column=1)

    def login(self):
        theUsername = self.username_var.get()
        thePassword = self.password_var.get()
        if self.staff_var.get() == 1:
            self.controller.Login(theUsername, thePassword, is_staff=True)
        else:
            self.controller.Login(theUsername, thePassword)
    
    def guestLogin(self):
        self.controller.view.show_frame("OrderView")
