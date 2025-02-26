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
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        self.display()

    def display(self):

        self.upper_home_btn = tk.Button(self, text="Home", **self.button_style, command=lambda: self.changePage("HomeView"))
        self.upper_home_btn.pack(side="left", padx=15, pady=10)

        self.upper_my_orders_btn = tk.Button(self, text="Orders", **self.button_style, command=lambda: self.changePage("OrderViewNew"))
        self.upper_my_orders_btn.pack(side="left", padx=15, pady=10)

        self.upper_staff_view_btn = tk.Button(self, text="Staff", **self.button_style, command=lambda: self.changePage("StaffView"))
        self.upper_staff_view_btn.pack(side="left", padx=15, pady=10)

        # Title
        title_label = Label(self, text="The Flying Dutchman", font=("Georgia", 24, "bold"),
                            bg="#A7C7E7", fg="#000435")
        title_label.pack(side="left", expand=True, padx=100, pady=10)

        self.selected_var = tk.StringVar(value="English")
        self.combo = ttk.Combobox(self, textvariable=self.selected_var, values=["English", "Svenska", "中文"])
        self.combo.pack(side="right", padx=15, pady=10)
        self.combo.current(0)
        
        self.upper_login_top_btn = tk.Button(self, text="Login", **self.button_style, command=lambda: self.changePage("LoginView"))
        self.upper_login_top_btn.pack(side="right", padx=15, pady=10)

    def changePage(self, page_name):
        self.controller.view.show_frame(page_name)
