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
        

        self.grid_rowconfigure(0, weight=0)  # 不隨視窗放大
        self.grid_rowconfigure(1, weight=1)  # 可隨視窗放大
        self.grid_columnconfigure(0, weight=1)
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        self.category = "Cognac"  # 預設分類
        self.canvas = None
        self.scroll_y = None
        self.frame = None
        self.create_submenu()
        self.create_main_area()
        self.load_drinks()
        # self.create_ui()

    # def create_ui(self):
    #     """創建可滾動的界面"""
    #     self.canvas = tk.Canvas(self, bg="white")
    #     self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
    #     self.frame = tk.Frame(self.canvas, bg="white")

    #     # 設定滾動
    #     self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    #     self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
    #     self.canvas.configure(yscrollcommand=self.scroll_y.set)

    #     # 佈局滾動視窗
    #     self.canvas.pack(side="left", fill="both", expand=True)
    #     self.scroll_y.pack(side="right", fill="y")
    #     self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    #     self.load_drinks()
    def create_submenu(self):
        self.submenu_frame = tk.Frame(self, bg="#291802")
        self.submenu_frame.grid(row=0, column=0, sticky="ew")

        # 例如放 Drinks、Food 兩個按鈕
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

    def create_main_area(self):
        """主要的滾動區域"""
        self.canvas = tk.Canvas(self, bg="white")
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # 這個 Frame 會被放在 Canvas 裡，用來顯示 drink cards
        self.inner_frame = tk.Frame(self.canvas, bg="white")

        # 設定 Canvas
        self.inner_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # 用 grid 來放置 canvas 與 scrollbar
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scroll_y.grid(row=1, column=1, sticky="ns")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
    # Windows 滾輪事件 (event.delta 為 120 的倍數)
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def load_drinks(self):
        """載入 drinks 資料並顯示在 inner_frame 裡"""
        # 先清空原有卡片
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # 從 controller 取得資料
        drinks_data = self.controller.getMenuData(self.category)

        row, col = 0, 0
        items_count = 0
        for drink in drinks_data:
            card = DrinkCard(self.inner_frame, drink)
            card.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 4:  # 每行最多放 5 張卡片
                col = 0
                row += 1
            items_count += 1
            if items_count > 50:
                break


    def refresh(self, new_category):
        """切換分類並重新加載資料"""
        self.category = new_category
        self.load_drinks()


class DrinkCard(tk.Frame):
    def __init__(self, parent, drink_data):
        super().__init__(parent, bg="#B3E5FC", bd=2, relief="solid")

        self.drink_data = drink_data
        self.quantity = 0  # 數量變數

        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        # 使用 JPG 預設圖片
        img_path = "images/hei.jpg"  # 統一使用 JPG
        if os.path.exists(img_path):  
            img = Image.open(img_path)
            img = img.resize((180, 180), Image.Resampling.LANCZOS)  # 調整大小
            self.image = ImageTk.PhotoImage(img)
        else:
            self.image = None  # 如果圖片不存在，避免錯誤

        # 圖片 Label
        self.image_label = tk.Label(self, image=self.image, bg="#B3E5FC")
        self.image_label.pack(pady=5)

        # 酒品資訊 Label
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

        # 數量調整區域
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