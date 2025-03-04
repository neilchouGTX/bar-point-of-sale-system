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

        self.shopping_cart_btn = tk.Button(
            self.submenu_frame,
            text="Shopping Cart",
            **self.button_style,
            command=lambda: (self.controller.view.show_frame("CartView"), self.controller.cart_refresh())
        )
        self.shopping_cart_btn.pack(side="right", padx=10, pady=5)

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
        drinks_data = self.controller.getBeerDataFromMenu()
        row, col = 0, 0
        items_count = 0
        for drink in drinks_data:
            card = DrinkCard(self.inner_frame, drink, self.controller)
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
        if(new_category != None):
            self.category = new_category
        self.load_drinks()


class DrinkCard(tk.Frame):
    def __init__(self, parent, drink_data, controller):
        super().__init__(parent, bg="#B3E5FC", bd=2, relief="solid")
        self.controller = controller
        self.drink_data = drink_data
        self.quantity = self.controller.get_cart_quantity(self.drink_data)  # number of drinks in cart

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

        self.quantity_label = tk.Label(self.quantity_frame, text=str(self.quantity), width=3, bg="white")
        self.quantity_label.grid(row=0, column=1)

        self.plus_btn = tk.Button(self.quantity_frame, text="+", **self.button_style, command=self.increase_quantity, width=3)
        self.plus_btn.grid(row=0, column=2, padx=5)

        self.bind("<ButtonPress-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        # 如果内部的子控件（如标签、按钮）也需要触发拖拽，可以为它们绑定同样的事件
        for child in self.winfo_children():
            child.bind("<ButtonPress-1>", self.on_start_drag)
            child.bind("<B1-Motion>", self.on_drag)
            child.bind("<ButtonRelease-1>", self.on_drop)

        self._drag_data = {"x": 0, "y": 0}

    def on_start_drag(self, event):
        # 记录初始点击的位置（相对于当前控件）
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        # 建立預覽視窗
        self._drag_window = tk.Toplevel(self)
        self._drag_window.overrideredirect(True)  # 無邊框
        self._drag_window.attributes("-alpha", 0.5)  # 設定半透明 (50%透明)
        # 放入圖片（假設 self.image 為已建立的 ImageTk.PhotoImage）
        preview_label = tk.Label(self._drag_window, image=self.image, bg="white")
        preview_label.pack()
        # 初始定位到鼠標所在位置
        self._drag_window.geometry(f"+{event.x_root}+{event.y_root}")

    def on_drag(self, event):
        if self._drag_window:
            # 更新預覽視窗的位置
            new_x = event.x_root - self._drag_data["x"]
            new_y = event.y_root - self._drag_data["y"]
            self._drag_window.geometry(f"+{new_x}+{new_y}")

    def on_drop(self, event):
        if self._drag_window:
            self._drag_window.destroy()
            self._drag_window = None
        # 获取当前鼠标在屏幕中的坐标
        x, y = event.x_root, event.y_root
        print("on_drop", x, y)
        # 取得 OrderViewNew 中购物车按钮的引用（请确保在 OrderViewNew 中保存了该按钮，例如 self.shopping_cart_btn）
        order_view = self.controller.view.frames["OrderViewNew"]
        print(type(order_view))
        if order_view and hasattr(order_view, "shopping_cart_btn"):
            cart_btn = order_view.shopping_cart_btn
            btn_x = cart_btn.winfo_rootx()
            btn_y = cart_btn.winfo_rooty()
            btn_width = cart_btn.winfo_width()
            btn_height = cart_btn.winfo_height()
            # 判断是否释放在购物车按钮范围内
            if btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height:
                # 放下时增加数量：这里调用 increase_quantity 即可
                self.increase_quantity()
                # 同时，可以触发控制器刷新购物车视图，例如：
                self.controller.cart_refresh()
        else:
            print("No shopping cart button found in OrderViewNew")

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