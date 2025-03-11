from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os
from styles.style_config import *
from Controller_translations import languages

class MyOrderView(Frame):
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
        self.table_number = self.controller.get_table_number()
        
        self.create_submenu()
        self.create_main_area()
        self.load_drinks()
        self.refresh()

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
            command=lambda: self.controller.view.show_frame("HomeView") 
        )
        self.back_btn.pack(side="left", padx=10, pady=5)

        self.payment_btn = tk.Button(
            self.submenu_frame, 
            text="Pay Now",
            **self.button_style,
            command=lambda: (self.controller.view.show_frame("PaymentView"), self.controller.refreshpaymentView())
        )
        self.payment_btn.pack(side="left", padx=10, pady=5)

        self.YourOrders_label = tk.Label(
            self.submenu_frame,
            text="Your Orders",
            fg="white",
            bg="#291802"
        )
        self.YourOrders_label.pack(side="left", pady=5)
        self.bind("<Configure>", self.adjust_font_size)

        self.Table_label = tk.Label(
            self.submenu_frame,
            text=f"Your table number is:",
            fg="white",
            bg="#291802"
        )
        self.Table_label.pack(side="left", pady=5)

        self.Table_number_label = tk.Label(
            self.submenu_frame,
            text=f"{self.table_number}",
            fg="white",
            bg="#291802"
        )
        self.Table_number_label.pack(side="left", pady=5)

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
        orders_data = self.controller.get_my_orders()
        row = 0
        for order in orders_data:
            print(f"Table {order.tableNumber}: Total Price: {order.totalPrice}")
            for item in order.orderItems:
                print(f"  Item ID: {item.id}, Amount: {item.amount}, Price: {item.price}")
        for drink in orders_data:
            if drink.tableNumber == self.table_number:
                for item in drink.orderItems:
                    card = DrinkCard(self.inner_frame, item, self.controller)
                    card.grid(row=row, column=0, padx=10, pady=10)
                    row += 1

    def refresh(self):
        self.table_number = self.controller.get_table_number()
        if self.table_number == -1:
            self.Table_number_label.config(text=f"Unknown, Please Order first.")
        else:
            self.Table_number_label.config(text=f"{self.table_number}")
        self.load_drinks()
        # self.update_all_total_price()

    def update_language(self, lang_code):
        """
        更新 SendOrderView 的語言，僅更新標題和按鈕文字。
        Update the language of the SendOrderView, focusing only on the title and buttons.
        """
        # 取得當前語言的字典 / Get the current language dictionary
        ldict = self.controller.languages[lang_code]

        # 更新標題文字 / Update the title label
        self.YourOrders_label.config(text=ldict['Your_Orders'])
        self.Table_label.config(text=ldict['Your_table_number_is'])
        if self.table_number == -1:
            self.Table_number_label.config(text=ldict['Unknown, Please Order first.'])

        # 更新按鈕文字 / Update button texts
        self.back_btn.config(text=ldict['back'])
        self.payment_btn.config(text=ldict['payment'])

    def adjust_font_size(self, event):
        window_width = event.width

        if window_width < 550:
            font_size = 14
        elif 500<= window_width < 800:
            font_size = 18
        else:
            font_size = 25

        self.YourOrders_label.config(font=("Arial", font_size, "bold"))
        self.Table_label.config(font=("Arial", font_size, "bold"))
        self.Table_number_label.config(font=("Arial", font_size, "bold"))


class DrinkCard(tk.Frame):
    def __init__(self, parent, drink_data, controller):
        super().__init__(parent, bg="#B3E5FC", bd=2, relief="solid")
        self.controller = controller
        self.drink_data = drink_data
        self.quantity = self.drink_data.amount
        self.price = self.drink_data.price
        self.menuData = self.controller.getBeerDataFromMenu()
        for menu in self.menuData:
            if int(menu.nr) == int(drink_data.id):
                self.drink_name = menu.namn
                break
        self.VIPmenuData = self.controller.getBeerDataFromVIPMenu()
        for menu in self.VIPmenuData:
            if int(menu.nr) == int(drink_data.id):
                self.drink_name = menu.namn
                break

        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        # Use default image if image not found
        img_path_jpg = "images/" + self.drink_name + ".jpg"
        img_path_png = "images/" + self.drink_name + ".png"
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
            text=f"Name: {self.drink_name}\n",
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