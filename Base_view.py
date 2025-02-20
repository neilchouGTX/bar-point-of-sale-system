import json
import tkinter as tk
from tkinter import font
from views.Order_view import *
from views.Login_view import *
from views.Upper_view import *
from views.Home_view import *
from views.Order_viewNew import *
from views.Staff_view import *

class BaseView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.frames = {}
        self.title("Ordering System")
        self.configure(bg="#211402")
        self.geometry("1366x768")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize Frame pages
        for F in (HomeView, UpperView, OrderView, LoginView, OrderViewNew, StaffView):
            page_name = F.__name__
            frame = F(root=self, controller=self.controller)
            self.frames[page_name] = frame
            if page_name == "UpperView":
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame.grid(row=1, column=0, sticky="nsew")
    
        self.show_frame("HomeView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
