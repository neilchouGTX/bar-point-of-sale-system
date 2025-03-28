from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os, sys
from styles.style_config import *
import os

from Controller_translations import languages

class CartView(Frame):
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
        #self.controller.clear_cart()
        self.create_submenu()
        self.create_main_area()
        self.load_drinks()
        # self.create_ui()
        
        #初始化語言 /initialize language
        self.languages = languages
        self.current_language = self.controller.current_language


    def create_submenu(self):
        self.submenu_frame = tk.Frame(self, bg="#291802")
        self.submenu_frame.grid(row=0, column=0, sticky="news")

        # Configuring grid for RWD
        self.submenu_frame.grid_columnconfigure(0, weight=1)
        self.submenu_frame.grid_columnconfigure(1, weight=1)
        self.submenu_frame.grid_columnconfigure(2, weight=1)
        self.submenu_frame.grid_columnconfigure(3, weight=1)
        self.submenu_frame.grid_columnconfigure(4, weight=1)

        # for category in ["Vitt vin", "Okryddad sprit"]:
        self.VittVin_btn = tk.Button(
            self.submenu_frame, 
            text="Back",
            **self.button_style,
            command=lambda: self.controller.view.show_frame("OrderViewNew") 
        )
        self.VittVin_btn.grid(row=0, column=0, sticky="news", padx=10, pady=10)

        self.price_reveal_label = tk.Label(
            self.submenu_frame,
            text="0 kr",
            fg="white",
            bg="#291802",
            font=self.custom_font
        )
        self.price_reveal_label.grid(row=0, column=4, sticky="e", padx=10, pady=10)

        self.total_price_label = tk.Label(
            self.submenu_frame,
            text="Total:",
            fg="white",
            bg="#291802",
            font=self.custom_font
        )
        self.total_price_label.grid(row=0, column=3, sticky="e", padx=10, pady=10)

        self.shopping_cart_btn = tk.Button(
            self.submenu_frame,
            text="Checkout",
            **self.button_style,
            command=lambda: (self.controller.view.show_frame("SendOrderView"), self.controller.refreshSendOrderView())
        )
        self.shopping_cart_btn.grid(row=0, column=5, sticky="ew", padx=10, pady=10)

        self.undo_btn = tk.Button(
            self.submenu_frame,
            text="undo",
            **self.button_style,
            command = self.undo
        )
        self.undo_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.redo_btn = tk.Button(
            self.submenu_frame,
            text="redo",
            **self.button_style,
            command=self.redo
        )
        self.redo_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        
    def undo(self):
        self.controller.cart_undo()
        self.refresh()
    def redo(self):
        self.controller.cart_redo()
        self.refresh()
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
        if self.controller.view.get_current_frame() == self:  # 確保當前 Frame 是顯示的
                if self.canvas.winfo_exists():
                    if self.winfo_toplevel().tk.call("tk", "windowingsystem") == "aqua":  # macOS
                        self.canvas.yview_scroll(int(-1 * (event.delta / 3)), "units")
                    else:  # Windows/Linux
                        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_drinks(self):
        """ loading drinks data into inner_frame """
        # Clear existing cards
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Get drinks data from controller
        drinks_data = self.controller.get_cart_data()

        row = 0
        items_count = 0
        for drink in drinks_data:
            card = DrinkCard(self.inner_frame, drink, self.controller)
            card.grid(row = row, column =  0, padx = 10, pady = 10)
            row += 1
            items_count += 1
            if items_count > 100:
                break
    def update_all_total_price(self):
        total_price = sum(float(drink.prisinklmoms) * self.controller.get_cart_quantity(drink) for drink in self.controller.get_cart_data())
        self.price_reveal_label.config(text=f"{total_price:.2f} kr")

    def refresh(self):
        self.load_drinks()
        self.update_all_total_price()
    
    def update_language(self, lang_code):
        """
        更新 CartView 的語言，僅更新標題和按鈕文字。
        Update the language of the CartView, focusing only on the title and buttons.
        """
        # 取得當前語言的字典 / Get the current language dictionary
        ldict = self.controller.languages[lang_code]

        # 更新標題文字 / Update the title label
        self.total_price_label.config(text=f"{ldict['total']}")

        # 更新按鈕文字 / Update button texts
        self.VittVin_btn.config(text=ldict['back'])
        self.shopping_cart_btn.config(text=ldict['checkout'])
        self.undo_btn.config(text=ldict['undo'])
        self.redo_btn.config(text=ldict['redo'])


class DrinkCard(tk.Frame):
    def __init__(self, parent, drink_data, controller):
        super().__init__(parent, bg="#B3E5FC", bd=2, relief="solid")
        self.controller = controller
        self.drink_data = drink_data
        self.quantity = self.controller.get_cart_quantity(self.drink_data)

        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        # Use default image if image not found
        img_path_jpg = "images/" + drink_data.namn + ".jpg"
        img_path_png = "images/" + drink_data.namn + ".png"
        if os.path.exists(img_path_jpg):
            img_path = img_path_jpg
        elif os.path.exists(img_path_png):
            img_path = img_path_png
        else:
            img_path = "images/no-preview.jpg"
        if os.path.exists(img_path):  
            img = Image.open(img_path)
            display_size = (120, 120)
            background = Image.new("RGBA", display_size, (255, 255, 255, 0))  # 白色背景，也可以改成透明(255,255,255,0)
            img.thumbnail(display_size, Image.Resampling.LANCZOS)
            img_x = (display_size[0] - img.size[0]) // 2
            img_y = (display_size[1] - img.size[1]) // 2
            background.paste(img, (img_x, img_y), mask=img if img.mode == "RGBA" else None)
            self.image = ImageTk.PhotoImage(background)
        else:
            self.image = None 

        # Main layout frame
        self.main_frame = tk.Frame(self, bg="#B3E5FC")
        self.main_frame.pack(fill="x", padx=10, pady=5)

        # Image Label (Left side)
        self.image_label = tk.Label(self.main_frame, image=self.image, bg="#B3E5FC")
        self.image_label.pack(side="left", padx=10)

        # Info Frame (Middle section)
        self.info_frame = tk.Frame(self.main_frame, bg="#B3E5FC")
        self.info_frame.pack(side="left", padx=10, expand=True)
        
        self.info_label = tk.Label(
            self.info_frame,
            text=f"Name: {drink_data.namn}\n"
                 f"Price: {drink_data.prisinklmoms} kr",
            justify="left",
            bg="#B3E5FC"
        )
        self.info_label.pack(anchor="w")



        # Quantity adjustment area (Far right)
        self.quantity_frame = tk.Frame(self.main_frame, bg="#B3E5FC")
        self.quantity_frame.pack(side="left", padx=10)

        self.minus_btn = tk.Button(self.quantity_frame, text="-", **self.button_style, command=self.decrease_quantity, width=3)
        self.minus_btn.grid(row=0, column=0, padx=5)

        self.quantity_label = tk.Label(self.quantity_frame, text=str(self.quantity), width=3, bg="white")
        self.quantity_label.grid(row=0, column=1)

        self.plus_btn = tk.Button(self.quantity_frame, text="+", **self.button_style, command=self.increase_quantity, width=3)
        self.plus_btn.grid(row=0, column=2, padx=5)

        # Quantity and total price frame (Right side)
        self.total_frame = tk.Frame(self.main_frame, bg="#B3E5FC")
        self.total_frame.pack(side="left", padx=10)

        self.total_price_label = tk.Label(
            self.total_frame,
            text=f"Total: {float(drink_data.prisinklmoms) * self.quantity:.2f} kr",
            bg="#B3E5FC"
        )
        self.total_price_label.pack()

    def increase_quantity(self):
        self.quantity += 1
        self.quantity_label.config(text=str(self.quantity))
        self.controller.add_drink_to_cart(self.drink_data)
        self.update_total_price()
        self.controller.cart_update_all_total_price()

    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.quantity_label.config(text=str(self.quantity))
            self.controller.remove_drink_to_cart(self.drink_data)
            self.update_total_price()
            self.controller.cart_update_all_total_price()
        if self.quantity == 0:
            self.controller.remove_drink_to_cart(self.drink_data)
            self.destroy()

    def update_total_price(self):
        total_price = float(self.drink_data.prisinklmoms) * self.quantity
        self.total_price_label.config(text=f"Total: {total_price:.2f} kr")
    