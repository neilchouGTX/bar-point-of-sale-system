"""
LoginView.py

視圖 (View) - 負責使用者介面 (Tkinter)
修改後的 LoginView，作為 Frame 嵌入其他視窗中使用
"""
#         self.error_label.config(text=msg)
import tkinter as tk
from tkinter import ttk
from functools import partial
from Controller_translations import languages

class LoginView(tk.Frame):
    """
    登錄視圖 (Frame)
    使用 grid 方式排版與較大字體，並將使用者類型切換改為按鈕高亮
    Login view (Frame)
    Uses grid layout with larger fonts, and user type switching via highlighted buttons
    """
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        
        # 取得多語系字典 / Get multilingual dictionary
        self.languages = languages  
        
        # 記錄目前語言
        self.current_language = self.controller.current_language  
        
        # 使用者選擇 - 預設為 'VIP'
        # User selection - default to 'VIP'
        self.selected_user_type = 'VIP'
        
        # 初始化UI
        self._init_ui()
        
        # 根據當前語言更新文字 / Update text according to current language
        self.update_language(self.current_language)

    def _init_ui(self):
        """
        初始化所有 UI 結構；拆分成多個小方法，保持可讀性
        Initialize all UI components; split into multiple small methods for readability
        """
        self._setup_styles_and_layout()
        self._setup_title_label()
        self._setup_user_type_buttons()
        self._setup_identifier_input()
        self._setup_hint_label()        # 顯示測試提示文字（程序完成后刪除）
        self._setup_action_buttons()
        self._setup_error_label()


    def _setup_styles_and_layout(self):
        """
        設定整體外觀(背景、字體)與布局規則
        Set overall appearance (background, fonts) and layout rules
        """
        # 設定整體背景與字體
        self.config(bg="#F2F2F2")
        self.title_font = ("Arial", 22, "bold")
        self.label_font = ("Arial", 14, "bold")
        self.button_font = ("Arial", 12, "bold")

        # 主框架 / Main frame
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Row/Column 配置 / Configuration for resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def _setup_title_label(self):
        """
        設置標題 / Setup the title label
        """
        self.title_label = tk.Label(
            self.main_frame, 
            text="Login", 
            font=self.title_font, 
            bg="#F2F2F2"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    def _setup_user_type_buttons(self):
        """
        建立使用者類型按鈕 (VIP / Staff)，並以預設高亮 VIP
        Create user type buttons (VIP / Staff), highlight VIP by default
        """
        self.vip_button = tk.Button(
            self.main_frame, 
            text="VIP", 
            font=self.button_font,
            command=partial(self.handle_user_type_selection, 'VIP'),
            width=10
        )
        self.staff_button = tk.Button(
            self.main_frame, 
            text="Staff", 
            font=self.button_font,
            command=partial(self.handle_user_type_selection, 'Staff'),
            width=10
        )
        self.vip_button.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.staff_button.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        # 預設高亮 VIP
        self._highlight_selected_button('VIP')

    def _setup_identifier_input(self):
        """
        建立輸入欄位：電話 / 員工ID
        Create input field: phone / staff ID
        """
        self.identifier_label = ttk.Label(self.main_frame, font=self.label_font)
        self.identifier_label.grid(row=2, column=0, columnspan=2, pady=(20, 5))
        
        self.identifier_var = tk.StringVar()
        self.identifier_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.identifier_var,
            width=30,
        )
        self.identifier_entry.grid(row=3, column=0, columnspan=2, pady=5)

    def _setup_hint_label(self):
        """
        提示讯息（项目完成后可移除）
        """
        hint_label_cn = ttk.Label(
            self.main_frame, 
            text="測試階段，輸入 '123' 即可登入", 
            foreground="red"
        )
        hint_label_cn.grid(row=7, column=0, columnspan=2, pady=(10, 2), sticky="n")

        hint_label_en = ttk.Label(
            self.main_frame, 
            text="During the testing phase, enter '123' to log in", 
            foreground="red"
        )
        hint_label_en.grid(row=8, column=0, columnspan=2, pady=(2, 10), sticky="n")

    def _setup_action_buttons(self):
        """
        建立登入、登出、非會員按鈕
        Create login, logout, and non-member buttons
        """
        # 登入按鈕
        self.login_button_text = tk.StringVar()
        self.login_button = ttk.Button(
            self.main_frame,
            textvariable=self.login_button_text,
            command=None,  # 之後由控制器在外部綁定
            width=15
        )
        self.login_button.grid(row=4, column=0, columnspan=2, pady=(20, 5))

        # 登出按鈕（預設隱藏）
        self.logout_button_text = tk.StringVar()
        self.logout_button = ttk.Button(
            self.main_frame,
            textvariable=self.logout_button_text,
            command=None,  # 之後由控制器在外部綁定
            width=15
        )
        self.logout_button.grid_forget()

        # 非會員按鈕（跳轉首頁）
        self.nonmember_button_text = tk.StringVar()
        self.nonmember_button = ttk.Button(
            self.main_frame,
            textvariable=self.nonmember_button_text,
            command=lambda: self.controller.handle_non_member(),
            width=15
        )
        self.nonmember_button.grid(row=5, column=0, columnspan=2, pady=(5, 20))

    def _setup_error_label(self):
        """
        建立錯誤訊息標籤
        Create error message label
        """
        self.error_label = ttk.Label(self.main_frame, foreground="red", font=("Arial", 12))
        self.error_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))


    def handle_user_type_selection(self, user_type):
        """
        切換 VIP / Staff 後，更新高亮按鈕與目前選擇
        Switch between VIP / Staff, update the highlighted button and current selection
        """
        self.selected_user_type = user_type
        self._highlight_selected_button(user_type)

    def _highlight_selected_button(self, user_type):
        """
        高亮指定用戶類型按鈕，另一個恢復普通樣式
        Highlight the specified user type button, revert the other
        """
        if user_type == 'VIP':
            self.vip_button.config(bg="#FFD700", fg="black")   # VIP高亮
            self.staff_button.config(bg="#F0F0F0", fg="black") # Staff一般
        else:
            self.vip_button.config(bg="#F0F0F0", fg="black")
            self.staff_button.config(bg="#FFD700", fg="black")

    # 綁定控制器函式 / Binding controller functions
    def bind_login(self, callback):
        self.login_button.config(command=callback)
        
    def bind_logout(self, callback):
        self.logout_button.config(command=callback)

    def get_selected_user_type(self):
        """
        回傳使用者選擇 'VIP' 或 'Staff'
        Return the user type selection: 'VIP' or 'Staff'
        """
        return self.selected_user_type
    
    def get_identifier_input(self):
        """
        取得使用者輸入的識別資訊 (電話或員工ID)
        Get the user-entered identifier (phone or staff ID)
        """
        return self.identifier_var.get()
    
    def show_error_message(self, message):
        """
        在錯誤訊息標籤顯示文字
        Display given message on the error_label
        """
        self.error_label.config(text=message)
        
    def update_language(self, lang_code):
        """
        根據語言設定更新文字
        Update text based on the language setting
        """
        self.current_language = lang_code
        lang_dict = self.languages[lang_code]

        # 標題 & 各種文字 / Title & various texts
        self.title_label.config(text=lang_dict.get('app_title', "Login"))
        
        # 按鈕文字
        self.login_button_text.set(lang_dict['login_button'])
        self.logout_button_text.set(lang_dict['logout_button'])
        self.nonmember_button_text.set(lang_dict['nonmember_button'])
        
        # 識別欄位標籤
        self.identifier_label.config(text=lang_dict['identifier_label'])
        
        # 若已存在登入或錯誤訊息，需要及時清理或重設
        self.error_label.config(text="")

    def show_login_view(self):
        """
        顯示登入畫面：清除輸入並顯示登入按鈕
        Show the login view: clear input and show login button
        """
        # self.identifier_var.set("")
        # self.error_label.config(text="")
        # self.login_button.grid(row=4, column=0, columnspan=2, pady=(20, 5))
        # self.logout_button.grid_forget()
        # self._highlight_selected_button('VIP')  # 預設回到 VIP
        # self.selected_user_type = 'VIP'
        self.identifier_var.set("")  # 清空電話/帳號輸入
        self.error_label.config(text="")
        self.login_button.grid(row=4, column=0, columnspan=2, pady=(20, 5))
        self.logout_button.grid_forget()


    def show_logout_view(self, user_type, identifier):
        """
        顯示登出畫面：隱藏登入按鈕並顯示登出按鈕與用戶資訊
        Show the logout view: hide login button and display logout button + user info
        """
        self.login_button.grid_forget()
        self.logout_button.grid(row=4, column=0, columnspan=2, pady=(20, 5))
        msg = f"{self.languages[self.current_language]['welcome_message']} {user_type}: {identifier}"
        self.error_label.config(text=msg)
