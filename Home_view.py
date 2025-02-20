from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from styles.style_config import *
import json

class HomeView(Frame):
    def __init__(self,root,controller):
        super().__init__(root)
        self.controller=controller
        self.configure(bg="#211402")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        self.display()

    def display(self):
        # self.main_frame = tk.Frame(self, bg="#10081a", width=1250, height=650)
        # self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 在主畫面中的 Order Now 與 VIP 區塊
        self.order_btn = tk.Button(self, text="Order Now", **self.button_style, command=lambda: self.changePage("OrderView"))
        self.order_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.order_btn = tk.Button(self, text="Order Now NEW!!!", **self.button_style, command=lambda: self.changePage("OrderViewNew"))
        self.order_btn.place(relx=0.7, rely=0.4, anchor=tk.CENTER)
        
        self.vip_label = tk.Label(self, text="VIP?", font=self.custom_font)
        self.vip_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        
        self.login_btn = tk.Button(self, text="Login", **self.button_style, command=lambda: self.changePage("LoginView"))
        self.login_btn.place(relx=0.5, rely=0.65, anchor=tk.CENTER) 


    def changePage(self, page_name):
        self.controller.view.show_frame(page_name)
