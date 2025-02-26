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
        self.main_frame = tk.Frame(self, bg="#A7C7E7", width=1250, height=650)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Flying Dutchman Image
        self.ship_image = Image.open("images/TheFlyingDutchman.png")
        self.ship_image = self.ship_image.resize((400,300))
        self.ship_image = ImageTk.PhotoImage(self.ship_image)
        ship_image_label = Label(self, image=self.ship_image, bg="#A7C7E7")
        ship_image_label.pack(pady=20)

        # Placing buttons below image
        login_btns = Frame(self, bg="#A7C7E7")
        login_btns.pack(side="top", padx=10, pady=10, fill="x")

        # In the main screen, the Order Now and VIP blocks
        self.order_btn = tk.Button(login_btns, text="Order Now", **self.button_style, width=10, command=lambda: self.changePage("OrderView"))
        self.order_btn.pack(side="top", padx=10, pady=10)

        self.order_btn = tk.Button(login_btns, text="Order Now NEW!!!", **self.button_style, width=10, command=lambda: self.changePage("OrderViewNew"))
        self.order_btn.pack(side="top", padx=10, pady=10)
        
        self.login_btn = tk.Button(login_btns, text="Staff Login", **self.button_style, width=10, command=lambda: self.changePage("LoginView"))
        self.login_btn.pack(side="top", padx=10, pady=10)

        self.login_btn = tk.Button(login_btns, text="Customer Login", **self.button_style,
                                   width=10, command=lambda: self.changePage("LoginView"))
        self.login_btn.pack(side="top", padx=10, pady=10)


    def changePage(self, page_name):
        self.controller.view.show_frame(page_name)
