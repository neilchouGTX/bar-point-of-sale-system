import tkinter as tk
#from Login_Controller import *
from tkinter import ttk
class LoginView(tk.Frame):
    def __init__(self,root,controller):
        super().__init__(root)
        self.controller=controller
        self.username_var=tk.StringVar()
        self.password_var=tk.StringVar()

        self.display()
    def display(self):

        # username & password
        self.username_lbl=ttk.Label(self, text="Account:")
        self.username_lbl.grid(row=0, column=0)
        self.username_ent=ttk.Entry(self,textvariable=self.username_var)
        self.username_ent.grid(row=0,column=1)

        self.password_lbl=ttk.Label(self, text="password:")
        self.password_lbl.grid(row=1,column=0)
        self.password_ent=ttk.Entry(self,textvariable=self.password_var)
        self.password_ent.grid(row=1,column=1)

        #checkBox
        self.vip_cbtn=ttk.Checkbutton(self,text="VIP")
        self.vip_cbtn.grid(row=2, column=0)

        self.staff_cbtn=ttk.Checkbutton(self,text="Staff")
        self.staff_cbtn.grid(row=2, column=1)

        #LoginButton
        log_btn=ttk.Button(self, text="Login",command=self.login)
        log_btn.grid(row=2,column=2)

        guestLog_btn=ttk.Button(self,text="GuestLogin",command=self.guestLogin)
        guestLog_btn.grid(row=3,column=1)

        

    def login(self):
        theUsername=self.username_var.get()
        thePassword=self.password_var.get()
        self.controller.Login(theUsername,thePassword)
    
    def guestLogin(self):
        self.controller.view.show_frame("OrderView")
        



