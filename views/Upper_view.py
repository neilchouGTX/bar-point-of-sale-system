from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from styles.style_config import *
from PIL import Image, ImageTk
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

        # Configuring grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.display()
        self.language_select()

    def display(self):
        # Title and image frame
        self.top_frame = Frame(self)
        self.top_frame.configure(bg="#A7C7E7")
        self.top_frame.grid(row=0, column=0, sticky="ew")

        # Configuring frame to center title + image
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=0)
        self.top_frame.grid_columnconfigure(2, weight=0)
        self.top_frame.grid_columnconfigure(3, weight=1)

        # Flying Dutchman Image
        self.ship_image = Image.open("images/TheFlyingDutchman.png")
        self.ship_image = self.ship_image.resize((100, 75))
        self.ship_image = ImageTk.PhotoImage(self.ship_image)
        ship_image_label = Label(self.top_frame, image=self.ship_image, bg="#A7C7E7")
        ship_image_label.grid(row=0, column=1, padx=(0,10), pady=10)

        # Flying Dutchman Title
        self.title_label = Label(self.top_frame, text="The Flying Dutchman", font=("Georgia", 48, "bold"),
                            bg="#A7C7E7", fg="#000435")
        self.title_label.grid(row=0, column=2, sticky="w", padx=10, pady=10)

        # Resizing title based on window size
        self.bind("<Configure>", self.adjust_title)

        # Buttons frame
        self.upper_btns = Frame(self)
        self.upper_btns.configure(bg="#A7C7E7")
        self.upper_btns.grid(row=1, column=0, sticky="news")
        self.upper_btns.grid_columnconfigure(0, weight=1)
        self.upper_btns.grid_columnconfigure(1, weight=1)
        self.upper_btns.grid_columnconfigure(2, weight=1)
        self.upper_btns.grid_columnconfigure(3, weight=1)
        self.upper_btns.grid_columnconfigure(4, weight=1)

        self.upper_home_btn = tk.Button(self.upper_btns, text="Home", **self.button_style, command=lambda: self.changePage("HomeView"))
        self.upper_home_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.upper_my_orders_btn = tk.Button(self.upper_btns, text="Orders", **self.button_style, command=lambda: (self.changePage("OrderViewVIP"), self.controller.refreshOrderView(None)))
        self.upper_my_orders_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        # --TO DO--
        # Only allow access to "Staff" view if logged in as staff; otherwise, greyed out.

        self.upper_staff_view_btn = tk.Button(self.upper_btns, text="Staff", **self.button_style, command=lambda: self.changePage("StaffView"))
        self.upper_staff_view_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        # self.selected_var = tk.StringVar(value="English")
        # self.combo = ttk.Combobox(self, textvariable=self.selected_var, values=["English", "Svenska", "中文"])
        # self.combo.grid(row=0, column=4, sticky="news", padx=10, pady=10)
        # self.combo.current(0)
        
        self.upper_login_top_btn = tk.Button(self.upper_btns, text="Login", **self.button_style, command=lambda: self.changePage("LoginView"))
        self.upper_login_top_btn.grid(row=0, column=3, sticky="ew", padx=10, pady=10)

    def language_select(self):
        self.selected_var = tk.StringVar(value=self.current_language)
        self.combo = ttk.Combobox(self.upper_btns, textvariable=self.selected_var,
                                  values=list(self.languages.keys()), state="readonly")
        self.combo.grid(row=0, column=4, sticky="ew", padx=10, pady=10)
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

    def adjust_title(self, event):
        window_width = event.width

        if window_width < 500:
            font_size = 24
        elif 500 <= window_width < 800:
            font_size = 32
        else:
            font_size = 48

        self.title_label.config(font=("Georgia", font_size, "bold"))
