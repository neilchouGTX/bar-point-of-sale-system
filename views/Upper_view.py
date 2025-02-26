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
        self.upper_home_btn.grid(row=0, column=0, padx=10, pady=10)

        self.upper_my_orders_btn = tk.Button(self, text="Orders", **self.button_style, command=lambda: self.changePage("OrderViewNew"))
        self.upper_my_orders_btn.grid(row=0, column=1, padx=10, pady=10)

        self.upper_staff_view_btn = tk.Button(self, text="Reservations", **self.button_style, command=lambda: self.changePage("ReservationView"))
        self.upper_staff_view_btn.grid(row=0, column=2, padx=10, pady=10)
        # Title
        title_label = Label(self, text="The Flying Dutchman", font=("Georgia", 30, "bold"),
                            bg="#A7C7E7", fg="#000435")
        title_label.grid(row=0, column=3, sticky="news", padx=10, pady=10)

        # Adjusting grid to center title
        self.columnconfigure(3, weight=1)

        self.selected_var = tk.StringVar(value="English")
        self.combo = ttk.Combobox(self, textvariable=self.selected_var, values=["English", "Svenska", "中文"])
        self.combo.grid(row=0, column=4, sticky="news", padx=10, pady=10)
        self.combo.current(0)
        
        self.upper_login_top_btn = tk.Button(self, text="Login", **self.button_style, command=lambda: self.changePage("LoginView"))
        self.upper_login_top_btn.grid(row=0, column=5, padx=10, pady=10)

    def changePage(self, page_name):
        self.controller.view.show_frame(page_name)
