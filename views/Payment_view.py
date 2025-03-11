import tkinter as tk
from tkinter import Frame, Canvas, Scrollbar, Button, Label, Toplevel
from PIL import Image, ImageTk
import os
from styles.style_config import get_custom_font, get_button_style2
from Controller_translations import languages

class PaymentView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="white")
        # pending_items: 存放待付款的數量，key 為品項 id
        self.pending_items = {}

        # 使用 grid 設定 3 行：row 0 = submenu, row 1 = 三欄主區域, row 2 = 底部 Pay 按鈕區域
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)
        self.table_number = self.controller.get_table_number()

        self.create_submenu()
        self.create_main_area()
        self.load_payment_items()
        self.refresh()

        # 初始化語言設定
        self.languages = languages
        self.current_language = self.controller.current_language

    def create_submenu(self):
        self.submenu_frame = tk.Frame(self, bg="#291802")
        self.submenu_frame.grid(row=0, column=0, sticky="ew")
        self.back_btn = Button(
            self.submenu_frame,
            text="Back",
            **self.button_style,
            command=lambda: self.controller.view.show_frame("MyOrderView")
        )
        self.back_btn.pack(side="left", padx=10, pady=5)
        self.pay_all_btn = Button(
            self.submenu_frame,
            text="Pay All",
            **self.button_style,
            command=self.pay_all
        )
        self.pay_all_btn.pack(side="right", padx=10, pady=5)
        self.Table_label = Label(
            self.submenu_frame,
            text=f"Table: {self.table_number}",
            fg="white",
            bg="#291802"
        )
        self.Table_label.pack(side="left", padx=10, pady=5)

    def create_scrollable_frame(self, parent, bg_color):
        canvas = Canvas(parent, bg=bg_color, highlightthickness=0)
        scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=bg_color)
        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        return frame

    def create_main_area(self):
        # 主區域（row=1）：建立一個包含三欄的容器，背景使用淺灰色
        self.main_area = tk.Frame(self, bg="#f0f0f0")
        self.main_area.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(2, weight=1)

        # 左側欄：未付款
        self.left_container = tk.Frame(self.main_area, bg="#f0f0f0")
        self.left_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.unpaid_label = Label(self.left_container, text="Unpaid Items", bg="#f0f0f0", font=self.custom_font)
        self.unpaid_label.pack(anchor="n", pady=5)
        self.left_frame = self.create_scrollable_frame(self.left_container, "#f0f0f0")

        # 中間欄：待付款
        self.middle_container = tk.Frame(self.main_area, bg="#f0f0f0")
        self.middle_container.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.pending_label = Label(self.middle_container, text="Pending Items", bg="#f0f0f0", font=self.custom_font)
        self.pending_label.pack(anchor="n", pady=5)
        self.middle_frame = self.create_scrollable_frame(self.middle_container, "#f0f0f0")
        # 儲存中間欄容器作為拖放判斷區域
        self.pending_area = self.middle_container

        # 右側欄：已付款
        self.right_container = tk.Frame(self.main_area, bg="#f0f0f0")
        self.right_container.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.paid_label = Label(self.right_container, text="Paid Items", bg="#f0f0f0", font=self.custom_font)
        self.paid_label.pack(anchor="n", pady=5)
        self.right_frame = self.create_scrollable_frame(self.right_container, "#f0f0f0")

        # 下方：Pay 按鈕放在三欄下方正中（row=2）
        self.bottom_frame = tk.Frame(self, bg="white")
        self.bottom_frame.grid(row=2, column=0, pady=10)
        self.pay_btn = Button(
            self.bottom_frame,
            text="Pay",
            **self.button_style,
            command=self.pay_pending
        )
        self.pay_btn.pack(pady=5)

    def load_payment_items(self):
        # 清空所有欄位
        for frame in (self.left_frame, self.middle_frame, self.right_frame):
            for widget in frame.winfo_children():
                widget.destroy()
        orders = self.controller.get_my_orders()
        for order in orders:
            if order.tableNumber == self.table_number:
                for item in order.orderItems:
                    if item.paid >= item.amount:
                        # 完全付款品項放右欄
                        card = PaymentItemCard(self.right_frame, item, self.controller,
                                               state="paid", display_qty=item.amount)
                        card.pack(fill="x", padx=5, pady=5)
                    else:
                        pending = self.pending_items.get(item.id, 0)
                        unpaid_remaining = item.amount - item.paid - pending
                        if unpaid_remaining > 0:
                            # 未付款部分放左欄，且不顯示 paid 標籤，加入「單件」與「全部」按鈕，並啟用拖曳
                            card = PaymentItemCard(self.left_frame, item, self.controller,
                                                   state="unpaid", display_qty=unpaid_remaining,
                                                   on_single=self.move_single, on_all=self.move_all,
                                                   drag_callback=self.drag_move_all, pending_area=self.pending_area)
                            card.pack(fill="x", padx=5, pady=5)
                        if pending > 0:
                            # 待付款部分放中間欄，點擊可還原回左欄
                            card = PaymentItemCard(self.middle_frame, item, self.controller,
                                                   state="pending", display_qty=pending,
                                                   on_pending_click=self.remove_pending)
                            card.pack(fill="x", padx=5, pady=5)

    def move_single(self, item):
        pending = self.pending_items.get(item.id, 0)
        if item.amount - item.paid - pending >= 1:
            self.pending_items[item.id] = pending + 1
            self.load_payment_items()

    def move_all(self, item):
        pending = self.pending_items.get(item.id, 0)
        remaining = item.amount - item.paid - pending
        if remaining > 0:
            self.pending_items[item.id] = pending + remaining
            self.load_payment_items()

    def remove_pending(self, item):
        self.pending_items[item.id] = 0
        self.load_payment_items()

    def drag_move_all(self, item):
        # 拖放成功且放在中間欄內則視同 move_all
        self.move_all(item)

    def pay_pending(self):
        orders = self.controller.get_my_orders()
        for order in orders:
            if order.tableNumber == self.table_number:
                for item in order.orderItems:
                    pending = self.pending_items.get(item.id, 0)
                    if pending > 0:
                        item.paid += pending
        self.pending_items.clear()
        self.controller.order_model.saveData()
        self.load_payment_items()
        self.refresh()

    def pay_all(self):
        orders = self.controller.get_my_orders()
        for order in orders:
            if order.tableNumber == self.table_number:
                for item in order.orderItems:
                    if item.paid < item.amount:
                        remaining = item.amount - item.paid - self.pending_items.get(item.id, 0)
                        if remaining > 0:
                            self.pending_items[item.id] = self.pending_items.get(item.id, 0) + remaining
        self.pay_pending()

    def refresh(self):
        self.table_number = self.controller.get_table_number()
        self.Table_label.config(text=f"Table: {self.table_number}")
        self.load_payment_items()

    def update_language(self, lang_code):
        ldict = self.controller.languages[lang_code]
        self.back_btn.config(text=ldict.get('back', 'Back'))
        self.pay_all_btn.config(text=ldict.get('pay_all', 'Pay All'))
        self.unpaid_label.config(text=ldict.get('unpaid_items', 'Unpaid Items'))
        self.pending_label.config(text=ldict.get('pending_items', 'Pending Items'))
        self.paid_label.config(text=ldict.get('paid_items', 'Paid Items'))
        self.pay_btn.config(text=ldict.get('pay', 'Pay'))
        self.Table_label.config(text=f"Table: {self.table_number}")

class PaymentItemCard(tk.Frame):
    def __init__(self, parent, item_data, controller, state, display_qty,
                 on_single=None, on_all=None, on_pending_click=None,
                 drag_callback=None, pending_area=None):
        """
        state: "unpaid", "pending", "paid"
        display_qty: 要顯示的數量（未付款時顯示剩餘數，待付款時顯示 pending 數，已付款時顯示付款數）
        on_single: unpaid 狀態下「單件」按鈕的 callback
        on_all: unpaid 狀態下「全部」按鈕的 callback
        on_pending_click: pending 狀態下點擊品項的 callback（還原回未付款）
        drag_callback: unpaid 狀態下拖移完成時的 callback
        pending_area: 用來判斷拖移是否落在中間欄的 widget
        """
        super().__init__(parent, bg="#B3E5FC", bd=2, relief="solid")
        self.controller = controller
        self.item_data = item_data
        self.state = state
        self.display_qty = display_qty
        self.on_single = on_single
        self.on_all = on_all
        self.on_pending_click = on_pending_click
        self.drag_callback = drag_callback
        self.pending_area = pending_area

        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style2(self)

        # 從菜單資料中取得品項名稱
        self.drink_name = None
        self.menuData = self.controller.getBeerDataFromMenu()
        for menu in self.menuData:
            if int(menu.nr) == int(item_data.id):
                self.drink_name = menu.namn
                break
        if self.drink_name is None:
            self.VIPmenuData = self.controller.getBeerDataFromVIPMenu()
            for menu in self.VIPmenuData:
                if int(menu.nr) == int(item_data.id):
                    self.drink_name = menu.namn
                    break
        if self.drink_name is None:
            self.drink_name = "Unknown"

        # 載入圖片
        img_path_jpg = "images/" + self.drink_name + ".jpg"
        img_path_png = "images/" + self.drink_name + ".png"
        if os.path.exists(img_path_jpg):
            img_path = img_path_jpg
        elif os.path.exists(img_path_png):
            img_path = img_path_png
        else:
            img_path = "images/no-preview.jpg"
        if os.path.exists(img_path):
            from PIL import Image
            img = Image.open(img_path)
            display_size = (80, 80)
            background = Image.new("RGBA", display_size, (255, 255, 255, 0))
            img.thumbnail(display_size, Image.Resampling.LANCZOS)
            img_x = (display_size[0] - img.size[0]) // 2
            img_y = (display_size[1] - img.size[1]) // 2
            background.paste(img, (img_x, img_y), mask=img if img.mode=="RGBA" else None)
            self.image = ImageTk.PhotoImage(background)
        else:
            self.image = None

        # 主區塊
        self.main_frame = tk.Frame(self, bg="#B3E5FC")
        self.main_frame.pack(fill="x", padx=5, pady=5)
        if self.image:
            self.image_label = Label(self.main_frame, image=self.image, bg="#B3E5FC")
            self.image_label.pack(side="left", padx=5)
        # 資訊顯示：未付款時不顯示已付款數值
        if self.state == "unpaid":
            info_text = f"Name: {self.drink_name}\nQty: {self.display_qty}"
        elif self.state == "pending":
            info_text = f"Name: {self.drink_name}\nPending: {self.display_qty}"
        else:
            info_text = f"Name: {self.drink_name}\nPaid: {self.item_data.paid}"
        self.info_label = Label(self.main_frame, text=info_text, bg="#B3E5FC", font=self.custom_font, justify="left")
        self.info_label.pack(side="left", padx=5)

        # unpaid 狀態下加入「單件」與「全部」按鈕
        if self.state == "unpaid":
            self.btn_frame = tk.Frame(self, bg="#B3E5FC")
            self.btn_frame.pack(fill="x", padx=5, pady=5)
            self.single_btn = Button(self.btn_frame, text="單件", **self.button_style,
                                       command=lambda: self.on_single(self.item_data) if self.on_single else None)
            self.single_btn.pack(side="left", padx=2)
            self.all_btn = Button(self.btn_frame, text="全部", **self.button_style,
                                  command=lambda: self.on_all(self.item_data) if self.on_all else None)
            self.all_btn.pack(side="left", padx=2)
        # pending 狀態下，點擊品項可還原回未付款
        if self.state == "pending" and self.on_pending_click:
            self.bind("<Button-1>", lambda event: self.on_pending_click(self.item_data))
            self.main_frame.bind("<Button-1>", lambda event: self.on_pending_click(self.item_data))
            self.info_label.bind("<Button-1>", lambda event: self.on_pending_click(self.item_data))
            if hasattr(self, "btn_frame"):
                self.btn_frame.bind("<Button-1>", lambda event: self.on_pending_click(self.item_data))
        # 若 unpaid 狀態啟用拖移：將所有子物件均綁定拖曳事件
        if self.state == "unpaid":
            self.bind_drag_events()

    def bind_drag_events(self):
        for widget in self.winfo_children():
            widget.bind("<ButtonPress-1>", self.on_start_drag)
            widget.bind("<B1-Motion>", self.on_drag)
            widget.bind("<ButtonRelease-1>", self.on_drop)
        self.bind("<ButtonPress-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        self._drag_data = {"x": 0, "y": 0}

    def on_start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_window = Toplevel(self)
        self._drag_window.overrideredirect(True)
        self._drag_window.attributes("-alpha", 0.5)
        # 使用目前物件的 snapshot (此處簡化處理，實際可用 PIL 截圖)
        w = self.winfo_width()
        h = self.winfo_height()
        self._drag_window.geometry(f"{w}x{h}+{event.x_root}+{event.y_root}")
        # 以當前 info_label 的文字作為預覽（你也可以用更完整的方式）
        preview = Label(self._drag_window, text=self.info_label.cget("text"), bg="white", font=self.custom_font)
        preview.pack()

    def on_drag(self, event):
        if self._drag_window:
            new_x = event.x_root - self._drag_data["x"]
            new_y = event.y_root - self._drag_data["y"]
            self._drag_window.geometry(f"+{new_x}+{new_y}")

    def on_drop(self, event):
        if self._drag_window:
            self._drag_window.destroy()
            self._drag_window = None
        # 檢查是否放在 pending_area 範圍內
        if self.pending_area:
            area_x = self.pending_area.winfo_rootx()
            area_y = self.pending_area.winfo_rooty()
            area_width = self.pending_area.winfo_width()
            area_height = self.pending_area.winfo_height()
            if (area_x <= event.x_root <= area_x + area_width) and (area_y <= event.y_root <= area_y + area_height):
                if self.drag_callback:
                    self.drag_callback(self.item_data)
