from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from styles.style_config import *
import json

from Controller_translations import languages

class UpperView(Frame):
    def __init__(self,root,controller):
        super().__init__(root)
        self.controller=controller
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)

        # 获取多语言字典，默认使用英语 / Load multi-language dictionary, default to English
        self.languages = languages
        self.current_language = "English"

        self.display()
        self.language_select()

    def display(self):

        self.upper_home_btn = tk.Button(self, text="Home", **self.button_style, command=lambda: self.changePage("HomeView"))
        self.upper_home_btn.grid(row=0, column=0, padx=10, pady=10)

        self.upper_my_orders_btn = tk.Button(self, text="Orders", **self.button_style, command=lambda: (self.changePage("OrderViewNew"), self.controller.refreshOrderView(None)))
        self.upper_my_orders_btn.grid(row=0, column=1, padx=10, pady=10)

        # --TO DO--
        # Only allow access to "Staff" view if logged in as staff; otherwise, greyed out.

        self.upper_staff_view_btn = tk.Button(self, text="Staff", **self.button_style, command=lambda: self.changePage("StaffView"))
        self.upper_staff_view_btn.grid(row=0, column=2, padx=10, pady=10)

        # Title
        title_label = Label(self, text="The Flying Dutchman", font=("Georgia", 30, "bold"),
                            bg="#A7C7E7", fg="#000435")
        title_label.grid(row=0, column=3, sticky="news", padx=10, pady=10)

        # Adjusting grid to center title
        self.columnconfigure(3, weight=1)

        # self.selected_var = tk.StringVar(value="English")
        # self.combo = ttk.Combobox(self, textvariable=self.selected_var, values=["English", "Svenska", "中文"])
        # self.combo.grid(row=0, column=4, sticky="news", padx=10, pady=10)
        # self.combo.current(0)
        
        self.upper_login_top_btn = tk.Button(self, text="Login", **self.button_style, command=lambda: self.changePage("LoginView"))
        self.upper_login_top_btn.grid(row=0, column=5, padx=10, pady=10)

    def language_select(self):
        self.selected_var = tk.StringVar(value=self.current_language)
        self.combo = ttk.Combobox(self, textvariable=self.selected_var, 
                                  values=list(self.languages.keys()), state="readonly")
        self.combo.grid(row=0, column=4, sticky="news", padx=10, pady=10)
        self.combo.current(0)
        
        # 绑定语言选择事件 / Bind language selection event
        #self.combo.bind("<<ComboboxSelected>>", self.handle_language_change)

    # def handle_language_change(self, event=None):
    #     """
    #     处理语言切换逻辑 / Handle language switching logic
    #     """
    #     selected_language = self.selected_var.get()
    #     self.controller.set_language(selected_language)  # 让 Controller 处理语言更新

    def update_language(self, lang_code):
        """
        更新 UI 组件的文本 / Update text for UI components
        """
        self.current_language = lang_code
        self.upper_home_btn.config(text=self.languages[lang_code]['app_title'])
        self.upper_my_orders_btn.config(text=self.languages[lang_code].get('order_button', "Orders"))
        self.upper_staff_view_btn.config(text=self.languages[lang_code].get('staff_button', "Staff"))
        self.upper_login_top_btn.config(text=self.languages[lang_code]['login_button'])
        #self.title_label.config(text=self.languages[lang_code]['app_title'])

    def changePage(self, page_name):
        """
        切换页面 / Change page
        """
        self.controller.show_frame(page_name)
