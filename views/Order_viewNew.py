from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from styles.style_config import *
import os

class OrderViewNew(Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="white")
        

        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1)
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        self.category = "Cognac"  
        self.canvas = None
        self.scroll_y = None
        self.frame = None
        self.create_submenu()
        self.create_main_area()
        self.load_drinks()
        # self.create_ui()

    def create_submenu(self):
        self.submenu_frame = tk.Frame(self, bg="#291802")
        self.submenu_frame.grid(row=0, column=0, sticky="ew")

        # for category in ["Vitt vin", "Okryddad sprit"]:
        VittVin_btn = tk.Button(
            self.submenu_frame, 
            text="Vitt vin",
            **self.button_style,
            command=lambda: self.refresh("Vitt vin")
        )
        VittVin_btn.pack(side="left", padx=10, pady=5)

        OkryddadSprit_btn = tk.Button(
            self.submenu_frame, 
            text="Okryddad sprit", 
            **self.button_style,
            command=lambda: self.refresh("Okryddad sprit")
        )
        OkryddadSprit_btn.pack(side="left", padx=10, pady=5)

        Cognac_btn = tk.Button(
            self.submenu_frame, 
            text="Cognac",
            **self.button_style,
            command=lambda: self.refresh("Cognac")
        )
        Cognac_btn.pack(side="left", padx=10, pady=5)

        shopping_cart_btn = tk.Button(
            self.submenu_frame,
            text="Shopping Cart",
            **self.button_style,
            command=lambda: self.controller.show_frame("OrderView")
        )
        shopping_cart_btn.pack(side="right", padx=10, pady=5)

    def create_main_area(self):
        # main scrollable area
        self.canvas = tk.Canvas(self, bg="white")
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # This frame will be placed in the canvas to display drink cards
        self.inner_frame = tk.Frame(self.canvas, bg="white")

        # Setting Canvas
        self.inner_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Use grid to place canvas and scrollbar
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scroll_y.grid(row=1, column=1, sticky="ns")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
    # windows scroll event (event.delta is a multiple of 120)
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def load_drinks(self):
        """ loading drinks data into inner_frame """
        # Clear existing cards
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Get drinks data from controller
        drinks_data = self.controller.getMenuData(self.category)

        row, col = 0, 0
        items_count = 0
        for drink in drinks_data:
            card = DrinkCard(self.inner_frame, drink)
            card.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 4:  # Maximum 5 cards in a row
                col = 0
                row += 1
            items_count += 1
            if items_count > 20:
                break


    def refresh(self, new_category):
        """ Switch category and reload data """
        self.category = new_category
        self.load_drinks()


class DrinkCard(tk.Frame):
    def __init__(self, parent, drink_data):
        super().__init__(parent, bg="#B3E5FC", bd=2, relief="solid")

        self.drink_data = drink_data
        self.quantity = 0  # number of drinks in cart

        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        # Use default image if image not found
        img_path = "images/hei.jpg"  
        if os.path.exists(img_path):  
            img = Image.open(img_path)
            img = img.resize((180, 180), Image.Resampling.LANCZOS)  # change size to fit card
            self.image = ImageTk.PhotoImage(img)
        else:
            self.image = None 

        # image Label
        self.image_label = tk.Label(self, image=self.image, bg="#B3E5FC")
        self.image_label.pack(pady=5)

        # alcohol name Label
        self.info_label = tk.Label(
            self,
            text=f"Name: {drink_data.namn}\n"
                 f"Producer: {drink_data.producent}\n"
                 f"Country: {drink_data.ursprunglandnamn}\n"
                 f"Type: {drink_data.varugrupp}\n"
                 f"Alc.: {drink_data.alkoholhalt}\n"
                 f"Packaging: {drink_data.forpackning}\n"
                 f"Price: {drink_data.prisinklmoms} kr",
            justify="left",
            bg="#B3E5FC"
        )
        self.info_label.pack(pady=5)

        # Quantity adjustment area
        self.quantity_frame = tk.Frame(self, bg="#B3E5FC")
        self.quantity_frame.pack(pady=5)

        self.minus_btn = tk.Button(self.quantity_frame, text="-", **self.button_style, command=self.decrease_quantity, width=3)
        self.minus_btn.grid(row=0, column=0, padx=5)

        self.quantity_label = tk.Label(self.quantity_frame, text="0", width=3, bg="white")
        self.quantity_label.grid(row=0, column=1)

        self.plus_btn = tk.Button(self.quantity_frame, text="+", **self.button_style, command=self.increase_quantity, width=3)
        self.plus_btn.grid(row=0, column=2, padx=5)

    def increase_quantity(self):
        self.quantity += 1
        self.quantity_label.config(text=str(self.quantity))

    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.quantity_label.config(text=str(self.quantity))