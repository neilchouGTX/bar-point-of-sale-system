from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from styles.style_config import *
from PIL import Image, ImageTk
import json

class HomeView(Frame):
    def __init__(self,root,controller):
        super().__init__(root)
        self.controller=controller
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        self.display()

    def display(self):
        # Background Image
        self.bg_image = Image.open("images/ocean_background.jpg").resize((1600, 784))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

        # User icon image
        user_icon = Image.open("images/user_icon.png").resize((150, 150))
        self.user_icon = ImageTk.PhotoImage(user_icon)
        user_label = tk.Label(self, image=self.user_icon, bg="#A7C7E7")
        user_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        # # In the main screen, the Order Now and VIP blocks
        # self.order_btn = tk.Button(login_btns, text="Order Now", **self.button_style, width=10, command=lambda: self.changePage("OrderView"))
        # self.order_btn.pack(side="top", padx=10, pady=10)

        self.order_btn = tk.Button(self, text="Order Now", **self.button_style, width=10, command=lambda: (self.changePage("OrderViewNew"), self.controller.refreshOrderView(None)))
        self.order_btn.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        
        self.staff_login_btn = tk.Button(self, text="Login", **self.button_style, width=10, command=lambda: self.changePage("LoginView"))
        self.staff_login_btn.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.customer_login_btn = tk.Button(self, text="VIP", **self.button_style,
                                   width=10, command=lambda:(self.changePage("OrderViewVIP"),self.controller.refreshOrderView(None)))
        self.customer_login_btn.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def changePage(self, page_name):
        self.controller.view.show_frame(page_name)