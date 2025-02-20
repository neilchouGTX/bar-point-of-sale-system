from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from styles.style_config import *
import json

class UpperView(Frame):
    def __init__(self,root,controller):
        super().__init__(root)
        self.controller=controller
        self.configure(bg="#140c01")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        self.display()

    def display(self):
        self.upper_home_btn = tk.Button(self, text="Home", **self.button_style, command=lambda: self.changePage("HomeView"))
        self.upper_home_btn.place(x=10, y=8)

        self.upper_my_orders_btn = tk.Button(self, text="My orders", **self.button_style, command=lambda: self.changePage("OrderViewNew"))
        self.upper_my_orders_btn.place(x=100, y=8)
        
        self.upper_login_top_btn = tk.Button(self, text="Login", **self.button_style, command=lambda: self.changePage("LoginView"))
        self.upper_login_top_btn.place(x=1100, y=8)
        
        self.selected_var = tk.StringVar(value = "English")
        self.combo = ttk.Combobox(self, textvariable=self.selected_var, values=["English", "Svenska", "中文"])
        self.combo.place(x = 1200, y = 8)
        self.combo.current(0)

    def changePage(self, page_name):
        self.controller.view.show_frame(page_name)
