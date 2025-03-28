from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from styles.style_config import *
import os
from Controller_translations import languages

class OrderViewVIP(Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="white")
        
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1)
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        self.price = 0
        self.category = None  
        self.canvas = None
        self.scroll_y = None
        self.frame = None
        self.create_submenu()
        self.create_main_area()
        self.load_drinks()
        # self.create_ui()
        
        #初始化語言 /initialize language
        self.languages = languages
        self.current_language = self.controller.current_language

    def create_submenu(self):
        self.submenu_frame = tk.Frame(self, bg="#291802")
        self.submenu_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.submenu_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # for category in ["Vitt vin", "Okryddad sprit"]:
        All_btn = tk.Button(
            self.submenu_frame, 
            text="All",
            **self.button_style,
            command=lambda: self.refresh(0, "all")
        )
        All_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        under_300_btn = tk.Button(
            self.submenu_frame, 
            text="Under 300kr", 
            **self.button_style,
            command=lambda: self.refresh(300, "alc")
        )
        under_300_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        between_300_1000_btn = tk.Button(
            self.submenu_frame, 
            text="300-1000",
            **self.button_style,
            command=lambda: self.refresh(1000, "alc")
        )
        between_300_1000_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        greater_1000_btn = tk.Button(
            self.submenu_frame, 
            text="1000kr Up",
            **self.button_style,
            command=lambda: self.refresh(1001, "alc")
        )
        greater_1000_btn.grid(row=0, column=3, sticky="ew", padx=10, pady=10)

        food_btn = tk.Button(
            self.submenu_frame, 
            text="Food",
            **self.button_style,
            command=lambda: self.refresh(0, "food")
        )
        food_btn.grid(row=0, column=4, sticky="ew", padx=10, pady=10)

        VIP_btn = tk.Button(
            self.submenu_frame, 
            text="VIP",
            **self.button_style,
            command=lambda: self.refresh(0, "VIP")
        )
        VIP_btn.grid(row=0, column=5, sticky="ew", padx=10, pady=10)

        self.shopping_cart_btn = tk.Button(
            self.submenu_frame,
            text="Shopping Cart",
            **self.button_style,
            command=lambda: (self.controller.view.show_frame("CartView"), self.controller.cart_refresh())
        )
        self.shopping_cart_btn.grid(row=0, column=7, sticky="ew", padx=10, pady=10)

        self.remove_item_btn = tk.Button(
            self.submenu_frame,
            text="Remove Item",
            padx=15,
            pady=7,
            bd=0,
            fg="red",
            bg="white",
            activebackground="white",
            activeforeground="gray",
            font=font.Font(root=self, family="Georgia", size=8, weight="bold"),
            relief="flat"
        )
        self.remove_item_btn.grid(row=0, column=6, sticky="ew", padx=10, pady=5)

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

    def createDrinkCard(self, drink):
        card = DrinkCard(self.inner_frame, drink, self.controller)
        card.grid(row=self.row, column=self.col, padx=10, pady=10)
        self.bind("<Configure>", self.change_card_layout)
        self.col += 1
        if self.col > 4:  # Maximum 5 cards in a row
            self.col = 0
            self.row += 1
        self.items_count += 1
    
    def load_drinks(self):
        """ loading drinks data into inner_frame """
        # Clear existing cards
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Get drinks data from controller
        drinks_data = self.controller.getBeerDataFromMenu()
        self.row, self.col = 0, 0
        self.items_count = 0
        for drink in drinks_data:
            if self.items_count > 50:
                break
            if self.category == "food" and drink.varugrupp == "Food":
                self.createDrinkCard(drink)
                continue
            elif self.price == 300 and float(drink.prisinklmoms) < 300:
                self.createDrinkCard(drink)
                continue
            elif self.price == 1000 and 300 <= float(drink.prisinklmoms) < 1000:
                self.createDrinkCard(drink)
                continue
            elif self.price == 1001 and float(drink.prisinklmoms) >= 1000:
                self.createDrinkCard(drink)
                continue
            elif self.category == "all":
                self.createDrinkCard(drink)
                continue
            else:
                continue
        drinks_data_VIP = self.controller.getBeerDataFromVIPMenu()
        for drink in drinks_data_VIP:
            if self.items_count > 50:
                break
            if self.category == "VIP":
                self.createDrinkCard(drink)
                continue
            elif self.category == "food" and drink.varugrupp == "Food":
                self.createDrinkCard(drink)
                continue
            elif self.price == 300 and float(drink.prisinklmoms) < 300 and drink.varugrupp != "Food":
                self.createDrinkCard(drink)
                continue
            elif self.price == 1000 and 300 <= float(drink.prisinklmoms) < 1000 and drink.varugrupp != "Food":
                self.createDrinkCard(drink)
                continue
            elif self.price == 1001 and float(drink.prisinklmoms) >= 1000 and drink.varugrupp != "Food":
                self.createDrinkCard(drink)
                continue
            elif self.category == "all":
                self.createDrinkCard(drink)
                continue
            else:
                continue

    def refresh(self, price, new_category=None):
        """ Switch category and reload data """
        self.price = price
        self.category = new_category
        self.load_drinks()

    def change_card_layout(self, event):
        window_width = event.width

        if window_width < 750:
            card_per_row = 2
        elif 750 <= window_width < 1000:
            card_per_row = 3
        elif 1000 <= window_width < 1250:
            card_per_row = 4
        else:
            card_per_row = 5

        widgets = self.inner_frame.winfo_children()
        for index, widget in enumerate(widgets):
            row = index // card_per_row
            col = index % card_per_row
            widget.grid(row=row, column=col, sticky="ew", padx=10, pady=10)

    #更新點單视图的语言 / Update the language of the order view
    def update_language(self, lang_code):
        self.current_language = lang_code
        self.submenu_frame.winfo_children()[0].config(text=self.languages[lang_code]['all'])
        self.submenu_frame.winfo_children()[1].config(text=self.languages[lang_code]['under300'])
        self.submenu_frame.winfo_children()[2].config(text=self.languages[lang_code]['price300to1000'])
        self.submenu_frame.winfo_children()[3].config(text=self.languages[lang_code]['above1000'])
        self.submenu_frame.winfo_children()[4].config(text=self.languages[lang_code]['food'])
        self.submenu_frame.winfo_children()[5].config(text=self.languages[lang_code]['VIP'])
        self.submenu_frame.winfo_children()[6].config(text=self.languages[lang_code]['shopping_cart'])
        self.submenu_frame.winfo_children()[7].config(text=self.languages[lang_code]['remove_item'])
        # self.shopping_cart_btn.config(text=self.languages[lang_code]['shopping_cart'])
        
        for widget in self.inner_frame.winfo_children():
        # 判斷是否是 DrinkCard 類型
            if isinstance(widget, DrinkCard):
                widget.update_language(lang_code, widget.drink_data.varugrupp == "Food")




class DrinkCard(tk.Frame):
    MAX_LENGTH = 15

    def __init__(self, parent, drink_data, controller):
        super().__init__(parent, bg="#B3E5FC", bd=2, relief="solid")
        self.controller = controller
        self.drink_data = drink_data
        self.quantity = self.controller.get_cart_quantity(self.drink_data)  # number of drinks in cart

        self.languages = languages
        self.current_language = self.controller.current_language

        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

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
            display_size = (180, 180)
            background = Image.new("RGBA", display_size, (255, 255, 255, 0))  # 白色背景，也可以改成透明(255,255,255,0)
            img.thumbnail(display_size, Image.Resampling.LANCZOS)
            img_x = (display_size[0] - img.size[0]) // 2
            img_y = (display_size[1] - img.size[1]) // 2
            background.paste(img, (img_x, img_y), mask=img if img.mode == "RGBA" else None)
            self.image = ImageTk.PhotoImage(background)
        else:
            self.image = None 

        # image Label
        self.image_label = tk.Label(self, image=self.image, bg="#B3E5FC")
        self.image_label.pack(pady=5)
        
        # alcohol name Label
        if (drink_data.varugrupp == "Food"):
            self.info_label = tk.Label(
            self,
            text=f"Name: {drink_data.namn[0:self.MAX_LENGTH]}\n"
                 f"Country: {drink_data.ursprunglandnamn[0:self.MAX_LENGTH]}\n"
                 f"Price: {drink_data.prisinklmoms[:self.MAX_LENGTH]} kr",
            justify="left",
            bg="#B3E5FC"
            )
            language_for_food = True
        else:
            self.info_label = tk.Label(
                self,
                text=f"Name: {drink_data.namn[0:self.MAX_LENGTH]}\n"
                    f"Producer: {drink_data.producent[0:self.MAX_LENGTH]}\n"
                    f"Country: {drink_data.ursprunglandnamn[0:self.MAX_LENGTH]}\n"
                    f"Type: {drink_data.varugrupp[0:self.MAX_LENGTH]}\n"
                    f"Alc.: {drink_data.alkoholhalt[0:self.MAX_LENGTH]}\n"
                    f"Packaging: {drink_data.forpackning[:self.MAX_LENGTH]}\n"
                    f"Price: {drink_data.prisinklmoms[:self.MAX_LENGTH]} kr",
                justify="left",
                bg="#B3E5FC"
            )
            language_for_food = False
        self.info_label.pack(pady=5)

        self.update_language(self.current_language, language_for_food)

        # Quantity adjustment area
        self.quantity_frame = tk.Frame(self, bg="#B3E5FC")
        self.quantity_frame.pack(pady=5)

        self.minus_btn = tk.Button(self.quantity_frame, text="-", **self.button_style, command=self.decrease_quantity, width=3)
        self.minus_btn.grid(row=0, column=0, padx=5)

        self.quantity_label = tk.Label(self.quantity_frame, text=str(self.quantity), width=3, bg="white")
        self.quantity_label.grid(row=0, column=1)

        self.plus_btn = tk.Button(self.quantity_frame, text="+", **self.button_style, command=self.increase_quantity, width=3)
        self.plus_btn.grid(row=0, column=2, padx=5)

        self.bind("<ButtonPress-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        # drag and drop for child widgets
        for child in self.winfo_children():
            child.bind("<ButtonPress-1>", self.on_start_drag)
            child.bind("<B1-Motion>", self.on_drag)
            child.bind("<ButtonRelease-1>", self.on_drop)

        self._drag_data = {"x": 0, "y": 0}

    def on_start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_window = tk.Toplevel(self)
        self._drag_window.overrideredirect(True)  # 無邊框
        self._drag_window.attributes("-alpha", 0.5)  # 設定半透明 (50%透明)
        preview_label = tk.Label(self._drag_window, image=self.image, bg="white")
        preview_label.pack()
        self._drag_window.geometry(f"+{event.x_root}+{event.y_root}")

    def on_drag(self, event):
        if self._drag_window:
            new_x = event.x_root - self._drag_data["x"]
            new_y = event.y_root - self._drag_data["y"]
            self._drag_window.geometry(f"+{new_x}+{new_y}")

    def on_drop(self, event):
        if self._drag_window:
            self._drag_window.destroy()
            self._drag_window = None
        x, y = event.x_root, event.y_root
        print("on_drop", x, y)
        order_view = self.controller.view.frames["OrderViewNew"]
        if not order_view:
            print("OrderViewNew not found")
            return
        dropped_on_cart = False
        if hasattr(order_view, "shopping_cart_btn"):
            cart_btn = order_view.shopping_cart_btn
            btn_x = cart_btn.winfo_rootx()
            btn_y = cart_btn.winfo_rooty()
            btn_width = cart_btn.winfo_width()
            btn_height = cart_btn.winfo_height()
            if btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height:
                self.increase_quantity()
                self.controller.cart_refresh()
                dropped_on_cart = True
        if hasattr(order_view, "remove_item_btn"):
            remove_btn = order_view.remove_item_btn
            btn_x = remove_btn.winfo_rootx()
            btn_y = remove_btn.winfo_rooty()
            btn_width = remove_btn.winfo_width()
            btn_height = remove_btn.winfo_height()
            if btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height:
                self.decrease_quantity()
                self.controller.cart_refresh()
                dropped_on_cart = True
        if not dropped_on_cart:
            print("Dropped outside valid buttons")

    def increase_quantity(self):
        self.quantity = self.controller.get_cart_quantity(self.drink_data)
        self.quantity += 1
        self.quantity_label.config(text=str(self.quantity))
        self.controller.add_drink_to_cart(self.drink_data)

    def decrease_quantity(self):
        self.quantity = self.controller.get_cart_quantity(self.drink_data)
        if self.quantity > 0:
            self.quantity -= 1
            self.quantity_label.config(text=str(self.quantity))
            self.controller.remove_drink_to_cart(self.drink_data)

    def update_language(self, lang_code, language_for_food):
        self.current_language = lang_code
        if language_for_food:
            self.info_label.config(
                                    justify="left",
                                    text=f"{self.languages[lang_code]['name']:<12}{self.drink_data.namn[:self.MAX_LENGTH]:>20}\n"
                                        f"\n"
                                        f"\n"
                                        f"{self.languages[lang_code]['country']:<9}{self.drink_data.ursprunglandnamn[:self.MAX_LENGTH]:>20}\n"
                                        f"\n"
                                        f"\n"
                                        f"{self.languages[lang_code]['price']:<11}{self.drink_data.prisinklmoms[:self.MAX_LENGTH]:>20} kr")
        else:
            self.info_label.config(
                                    justify="left",
                                    text=f"{self.languages[lang_code]['name']:<12}{self.drink_data.namn[:self.MAX_LENGTH]:>20}\n"
                                    f"{self.languages[lang_code]['producer']:<8}{self.drink_data.producent[:self.MAX_LENGTH]:>20}\n"
                                    f"{self.languages[lang_code]['country']:<9}{self.drink_data.ursprunglandnamn[:self.MAX_LENGTH]:>20}\n"
                                    f"{self.languages[lang_code]['type']:<12}{self.drink_data.varugrupp[:self.MAX_LENGTH]:>20}\n"
                                    f"{self.languages[lang_code]['alc']:<13}{self.drink_data.alkoholhalt[:self.MAX_LENGTH]:>20}\n"
                                    f"{self.languages[lang_code]['packaging']:<7}{self.drink_data.forpackning[:self.MAX_LENGTH]:>20}\n"
                                    f"{self.languages[lang_code]['price']:<11}{self.drink_data.prisinklmoms[:self.MAX_LENGTH]:>20} kr")
        self.info_label.update()

    
   