from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os
from styles.style_config import *
from Controller_translations import languages

class SendOrderView(Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="white")

        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1)
        self.custom_font = get_custom_font(self)
        self.custom_send_order_button_style = get_send_order_button_style(self)
        self.button_style = get_button_style2(self)

        self.category = "Cognac"  
        self.canvas = None
        self.scroll_y = None
        self.frame = None
        
        self.create_submenu()
        self.create_main_area()
        self.create_table_selector()
        self.create_submit_button()
        self.load_drinks()

        #初始化語言 /initialize language
        self.languages = languages
        self.current_language = self.controller.current_language

        


    def create_submenu(self):
        self.submenu_frame = tk.Frame(self, bg="#291802")
        self.submenu_frame.grid(row=0, column=0, sticky="ew")

        self.back_btn = tk.Button(
            self.submenu_frame, 
            text="Back",
            **self.button_style,
            command=lambda: self.controller.view.show_frame("CartView") 
        )
        self.back_btn.pack(side="left", padx=10, pady=5)

        self.confirmed_label = tk.Label(
            self.submenu_frame,
            text="Confirmed Order",
            fg="white",
            bg="#291802",
            font=("Arial", 25, "bold")
        )
        self.confirmed_label.pack(side="top", pady=5)

        self.total_price_label = tk.Label(
            self.submenu_frame,
            text="Total: 0 kr",
            fg="white",
            bg="#291802",
            font=self.custom_font
        )
        self.total_price_label.pack(side="right", padx=10, pady=5)

        # checkout_btn = tk.Button(
        #     self.submenu_frame,
        #     text="Checkout",
        #     **self.button_style,
        #     command=lambda: self.controller.view.show_frame("SendOrderView")
        # )
        # checkout_btn.pack(side="right", padx=10, pady=5)

    def create_main_area(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner_frame = tk.Frame(self.canvas, bg="white")

        self.inner_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scroll_y.grid(row=1, column=1, sticky="ns")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def create_table_selector(self):
        self.table_selector_frame = tk.Frame(self, bg="white")
        self.table_selector_frame.grid(row=2, column=0, pady=10)
        
        tk.Label(self.table_selector_frame, text="Select Table:", font=self.custom_font, bg="white").pack(side="left", padx=5)
        
        self.table_var = tk.StringVar(value="Table 1")
        self.table_dropdown = tk.OptionMenu(self.table_selector_frame, self.table_var, *[f"Table {i}" for i in range(1, 11)])
        self.table_dropdown.config(font=("Arial", 14), width=10)  # Increased size
        self.table_dropdown.pack(side="left", padx=5)

    def create_submit_button(self):
        self.submit_btn = tk.Button(
            self,
            text="Send Order",
            **self.custom_send_order_button_style,
            command=self.submit_order
        )
        self.submit_btn.grid(row=3, column=0, pady=10)

    def submit_order(self):
        selected_table = self.table_var.get()
        table_number = int(selected_table.split(" ")[1])  # 取得數字部分
        self.controller.send_order(table_number)
        print(f"Order submitted for {selected_table}")  # Replace with actual order handling logic

    def _on_mousewheel(self, event):
        if self.controller.view.get_current_frame() == self:
            if self.canvas.winfo_exists():
                if self.winfo_toplevel().tk.call("tk", "windowingsystem") == "aqua":  # macOS
                    self.canvas.yview_scroll(int(-1 * (event.delta / 3)), "units")
                else:  # Windows/Linux
                    self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_drinks(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        drinks_data = self.controller.get_cart_data()
        row = 0
        for drink in drinks_data:
            card = DrinkCard(self.inner_frame, drink, self.controller)
            card.grid(row=row, column=0, padx=10, pady=10)
            row += 1

    def update_all_total_price(self):
        total_price = sum(float(drink.prisinklmoms) * self.controller.get_cart_quantity(drink) for drink in self.controller.get_cart_data())
        self.total_price_label.config(text=f"Total: {total_price:.2f} kr")

    def refresh(self):
        self.load_drinks()
        self.update_all_total_price()

    def update_language(self, lang_code):
        """
        更新 SendOrderView 的語言，僅更新標題和按鈕文字。
        Update the language of the SendOrderView, focusing only on the title and buttons.
        """
        # 取得當前語言的字典 / Get the current language dictionary
        ldict = self.controller.languages[lang_code]

        # 更新標題文字 / Update the title label
        self.confirmed_label.config(text=ldict['confirmed_order'])
        self.total_price_label.config(text=f"{ldict['total']}: 0 kr")

        # 更新按鈕文字 / Update button texts
        self.submit_btn.config(text=ldict['send_order'])
        self.back_btn.config(text=ldict['back'])


class DrinkCard(tk.Frame):
    def __init__(self, parent, drink_data, controller):
        super().__init__(parent, bg="#B3E5FC", bd=2, relief="solid")
        self.controller = controller
        self.drink_data = drink_data
        self.quantity = self.controller.get_cart_quantity(self.drink_data)

        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        # Use default image if image not found
        img_path = "images/hei.jpg"  
        if os.path.exists(img_path):  
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(img)
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

        self.quantity_label = tk.Label(self.quantity_frame, text=str(self.quantity), width=3, bg="white")
        self.quantity_label.grid(row=0, column=1)

        # Quantity and total price frame (Right side)
        self.total_frame = tk.Frame(self.main_frame, bg="#B3E5FC")
        self.total_frame.pack(side="left", padx=10)

        self.total_price_label = tk.Label(
            self.total_frame,
            text=f"Total: {float(drink_data.prisinklmoms) * self.quantity:.2f} kr",
            bg="#B3E5FC"
        )
        self.total_price_label.pack()

    def update_total_price(self):
        total_price = float(self.drink_data.prisinklmoms) * self.quantity
        self.total_price_label.config(text=f"Total: {total_price:.2f} kr")

