# -*- coding: utf-8 -*-
"""
Upper_view.py
優化重點：
1. 語言切換後，根據當前的登入狀態（VIP、Staff、未登入）正確顯示「Login / Logout」。
2. 將按钮文字切換改為從多語言字典 (languages) 動態讀取。
3. 在 update_language() 內呼叫 update_header()，確保狀態與文字保持一致。

Using Python + Tkinter (MVC) Project
Written in Traditional Chinese & English bilingual comments
"""

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from styles.style_config import *
from PIL import Image, ImageTk
import json

from Controller_translations import languages

class UpperView(Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)

        # 多語系字典（預設英文）/ Multi-language dictionary (default English)
        self.languages = languages
        self.current_language = self.controller.current_language

        # Grid配置 / Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 顯示標題與按鈕 / Show title & buttons
        self.display()
        # 語言下拉選單 / Language selector
        self.language_select()
        # 根據登入狀態更新頂部選單 / Update top nav based on login status
        self.update_login_status()  

    def display(self):
        """
        建立標題區與按鈕區
        Create title area and button area
        """
        # Title & image frame
        self.top_frame = Frame(self, bg="#A7C7E7")
        self.top_frame.grid(row=0, column=0, sticky="ew")

        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=0)
        self.top_frame.grid_columnconfigure(2, weight=0)
        self.top_frame.grid_columnconfigure(3, weight=1)

        # Title image
        self.ship_image = Image.open("images/TheFlyingDutchman.png")
        self.ship_image = self.ship_image.resize((100, 75))
        self.ship_image = ImageTk.PhotoImage(self.ship_image)
        ship_image_label = Label(self.top_frame, image=self.ship_image, bg="#A7C7E7")
        ship_image_label.grid(row=0, column=1, padx=(0, 10), pady=10)

        # Title text
        self.title_label = Label(
            self.top_frame,
            text="The Flying Dutchman",
            font=("Georgia", 48, "bold"),
            bg="#A7C7E7",
            fg="#000435"
        )
        self.title_label.grid(row=0, column=2, sticky="w", padx=10, pady=10)

        # Window resize event to adjust title font size
        self.bind("<Configure>", self.adjust_title)

        # Buttons frame
        self.upper_btns = Frame(self, bg="#A7C7E7")
        self.upper_btns.grid(row=1, column=0, sticky="news")
        for col_idx in range(5):
            self.upper_btns.grid_columnconfigure(col_idx, weight=1)

        # Home button
        self.upper_home_btn = tk.Button(
            self.upper_btns,
            text="Home",
            **self.button_style,
            command=lambda: self.changePage("HomeView")
        )
        self.upper_home_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Orders button
        self.upper_my_orders_btn = tk.Button(
            self.upper_btns,
            text="Orders",
            **self.button_style,
            command=lambda: (self.changePage("MyOrderView"), self.controller.refreshMyOrder())
        )
        self.upper_my_orders_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        # Staff button (only staff can use, but default is shown)
        self.upper_staff_view_btn = tk.Button(
            self.upper_btns,
            text="Staff",
            **self.button_style,
            command=lambda: self.changePage("StaffView")
        )
        self.upper_staff_view_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        # Login/Logout button
        self.upper_login_top_btn = tk.Button(
            self.upper_btns,
            text="Login",
            **self.button_style,
            command=lambda: self.changePage("LoginView")
        )
        self.upper_login_top_btn.grid(row=0, column=3, sticky="ew", padx=10, pady=10)

    def language_select(self):
        """
        建立語言選擇下拉框 / Create a language dropdown selector
        """
        self.selected_var = tk.StringVar(value=self.current_language)
        self.combo = ttk.Combobox(
            self.upper_btns,
            textvariable=self.selected_var,
            values=list(self.languages.keys()),
            state="readonly"
        )
        self.combo.grid(row=0, column=4, sticky="ew", padx=10, pady=10)
        self.combo.current(0)

        # 綁定語言選擇事件 / Bind language selection event
        self.combo.bind("<<ComboboxSelected>>", self._on_language_change)

    def _on_language_change(self, event=None):
        """
        當使用者從下拉框切換語言時呼叫
        Called when user selects a different language in the combobox
        """
        selected_language = self.selected_var.get()
        self.controller.set_language(selected_language)
        # 在此同時，更新本視圖的語言設定
        # Also update this view's language setting
        self.update_language(selected_language)

    def update_language(self, lang_code):
        """
        根據新的語言代碼，更新當前語言，並刷新所有按鈕文字
        Update the current UI text based on the new language code
        """
        self.current_language = lang_code
        self.title_label.config(text=self.languages[lang_code].get('app_title', "The Flying Dutchman"))
        # 為了保持按鈕文字和登入狀態一致，我們在這裡呼叫 update_header()
        # To keep button text consistent with login status, call update_header() here
        self.update_header()

    def update_header(self):
        """
        根據登入狀態 + 所選語言，同步更新頂部按鈕文字
        Dynamically update the top navigation buttons based on login status + selected language
        """

        # 移除所有按鈕佈局 / Remove all button layouts first
        self.upper_home_btn.grid_forget()
        self.upper_my_orders_btn.grid_forget()
        self.upper_staff_view_btn.grid_forget()
        self.upper_login_top_btn.grid_forget()

        lang_dict = self.languages.get(self.current_language, {})

        # 檢查是否為 VIP 登入
        # Check if VIP is logged in
        if self.controller.vipModel.is_logged_in:
            # VIP Home
            self.upper_home_btn.config(
                text=lang_dict.get('vip_home_button', "VIP Home"),
                fg="black",
                command=self._go_vip_home
            )
            self.upper_home_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

            # Orders
            self.upper_my_orders_btn.config(
                text=lang_dict.get('order_button', "Orders"),
                fg="black",
                command=lambda: (self.changePage("MyOrderView"), self.controller.refreshMyOrder())
            )
            self.upper_my_orders_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

            # 隱藏 Staff 按鈕 / Hide Staff button
            self.upper_staff_view_btn.grid_remove()

            # Logout
            self.upper_login_top_btn.config(
                text=lang_dict.get('logout_button', "Logout"),
                fg="red",
                command=self._logout
            )
            self.upper_login_top_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        # 若 Staff 登入
        # If Staff is logged in
        elif self.controller.userModel.is_logged_in and self.controller.userModel.user_type == "Staff":
            # Home
            self.upper_home_btn.config(
                text=lang_dict.get('home_button', lang_dict.get('app_title', "Home")),
                fg="black",
                command=lambda: self.changePage("HomeView")
            )
            self.upper_home_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

            # Orders
            self.upper_my_orders_btn.config(
                text=lang_dict.get('order_button', "Orders"),
                fg="black",
                command=lambda: (self.changePage("MyOrderView"), self.controller.refreshMyOrder())
            )
            self.upper_my_orders_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

            # Staff
            self.upper_staff_view_btn.config(
                text=lang_dict.get('staff_button', "Staff"),
                fg="black",
                command=lambda: self.changePage("StaffView")
            )
            self.upper_staff_view_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

            # Logout
            self.upper_login_top_btn.config(
                text=lang_dict.get('logout_button', "Logout"),
                fg="red",
                command=lambda: self.controller.handle_logout()
            )
            self.upper_login_top_btn.grid(row=0, column=3, sticky="ew", padx=10, pady=10)

        else:
            # 未登入
            # Not logged in
            self.upper_home_btn.config(
                text=lang_dict.get('home_button', lang_dict.get('app_title', "Home")),
                fg="black",
                command=lambda: self.changePage("HomeView")
            )
            self.upper_home_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

            self.upper_my_orders_btn.config(
                text=lang_dict.get('order_button', "Orders"),
                fg="black",
                command=lambda: (self.changePage("MyOrderView"), self.controller.refreshMyOrder())
            )
            self.upper_my_orders_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

            self.upper_staff_view_btn.config(
                text=lang_dict.get('staff_button', "Staff"),
                fg="black",
                command=lambda: self.changePage("StaffView")
            )
            self.upper_staff_view_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

            self.upper_login_top_btn.config(
                text=lang_dict.get('login_button', "Login"),
                fg="black",
                command=lambda: self.changePage("LoginView")
            )
            self.upper_login_top_btn.grid(row=0, column=3, sticky="ew", padx=10, pady=10)

    def update_login_status(self):
        """
        根據當前登入資訊來刷新導航列
        Refresh nav bar based on current login status
        """
        self.update_header()

    def _logout(self):
        """
        處理 VIP 用戶登出邏輯：登出後切回 HomeView
        Handle logout logic for VIP user: logout and go back to HomeView
        """
        self.controller.userModel.logout()
        self.controller.vipModel.logout()
        self.controller.view.show_frame("HomeView")
        self.update_header()

    def _go_vip_home(self):
        """
        切換至 HomeVIPView，若當前已經是 HomeVIPView 則無動作
        Switch to HomeVIPView; if already on HomeVIPView, do nothing
        """
        current_frame_name = type(self.controller.view.get_current_frame()).__name__
        if current_frame_name != "HomeVIPView":
            self.controller.show_frame("HomeVIPView")
        # 如果已在 HomeVIPView，則不做任何事

    def changePage(self, page_name):
        """
        切換頁面 / Change the page
        """
        if page_name == "LoginView":
            self.controller.login_view.show_login_view()
        self.controller.show_frame(page_name)

    def adjust_title(self, event):
        """
        根據視窗寬度動態調整標題大小
        Dynamically adjust the title font size based on window width
        """
        window_width = event.width
        if window_width < 500:
            font_size = 24
        elif 500 <= window_width < 800:
            font_size = 32
        else:
            font_size = 48

        self.title_label.config(font=("Georgia", font_size, "bold"))

