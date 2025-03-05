"""
LoginView.py

視圖 (View) - 負責使用者介面 (Tkinter)
修改後的 LoginView，作為 Frame 嵌入其他視窗中使用
"""

import tkinter as tk
from tkinter import ttk
# 從 model 引入多語系字典 (languages)
from Controller_translations import languages

class LoginView(tk.Frame):
    """
    登錄視圖 (Frame)
    此版本用作其他視窗中的一個 Frame，而非獨立窗口
    """
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        
        # 取得多語系字典
        self.languages = languages  
        
        self.current_language = self.controller.current_language  
        # 初始化UI
        self._init_ui()
        self.update_language(self.current_language)  # 初始化时更新语言
        
    def _init_ui(self):
        """
        介面初始化 / Initialize the user interface
        """
        # 建立一個主框架，用於包含其他元件
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        # self._create_language_selector()
        self._create_user_type_selector()
        self._create_identifier_input()
        self._create_buttons()
        self._create_error_label()
        
    # def _create_language_selector(self):
    #     """
    #     建立語言切換組件 / Create language selection components
    #     """
    #     lang_text = self.languages[self.current_language]['language_label']
    #     self.lang_label = ttk.Label(self.main_frame, text=lang_text)
    #     self.lang_label.pack(pady=5)

    #     self.language_var = tk.StringVar(value=self.current_language)
    #     self.language_combobox = ttk.Combobox(
    #         self.main_frame,
    #         textvariable=self.language_var,
    #         values=list(self.languages.keys()),
    #         state="readonly"
    #     )
    #     self.language_combobox.pack(pady=5)
        
    def _create_user_type_selector(self):
        """
        建立使用者類型選擇組件 (VIP或Staff) / Create user type selection (VIP or Staff)
        """
        self.user_type_var = tk.StringVar(value='VIP')
        vip_text = self.languages[self.current_language]['radio_vip']
        staff_text = self.languages[self.current_language]['radio_staff']
        
        self.vip_radio = ttk.Radiobutton(
            self.main_frame,
            text=vip_text,
            variable=self.user_type_var,
            value='VIP'
        )
        self.staff_radio = ttk.Radiobutton(
            self.main_frame,
            text=staff_text,
            variable=self.user_type_var,
            value='Staff'
        )
        self.vip_radio.pack(pady=5)
        self.staff_radio.pack(pady=5)
        
    def _create_identifier_input(self):
        """
        建立識別資訊輸入欄位 / Create identifier input field
        """
        self.identifier_var = tk.StringVar()
        identifier_label_text = self.languages[self.current_language]['identifier_label']
        self.identifier_label = ttk.Label(self.main_frame, text=identifier_label_text)
        self.identifier_label.pack(pady=(10, 0))
        
        self.identifier_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.identifier_var,
            width=30
        )
        self.identifier_entry.pack(pady=5)
        
    def _create_buttons(self):
        """
        建立按鈕組件（登入、登出、非會員） / Create button components (login, logout, non-member)
        """
        self.login_button_text = tk.StringVar(
            value=self.languages[self.current_language]['login_button']
        )
        self.login_button = ttk.Button(
            self.main_frame,
            textvariable=self.login_button_text
        )
        self.login_button.pack(pady=5)
        
        self.logout_button_text = tk.StringVar(
            value=self.languages[self.current_language]['logout_button']
        )
        self.logout_button = ttk.Button(
            self.main_frame,
            textvariable=self.logout_button_text
        )
        self.logout_button.pack_forget()
        
        self.nonmember_button_text = tk.StringVar(
            value=self.languages[self.current_language].get('nonmember_button', "Non-member")
        )
        self.nonmember_button = ttk.Button(
            self.main_frame,
            textvariable=self.nonmember_button_text
        )
        self.nonmember_button.pack(pady=5)
        
    def _create_error_label(self):
        """
        建立錯誤訊息標籤 / Create error message label for user hints
        """
        self.error_label = ttk.Label(self.main_frame, foreground="red")
        self.error_label.pack(pady=5)
        
    # 綁定控制器函式 / Binding controller functions
    def bind_login(self, callback):
        self.login_button.config(command=callback)
        
    def bind_logout(self, callback):
        self.logout_button.config(command=callback)
        
    def bind_language_change(self, callback):
        self.language_combobox.bind("<<ComboboxSelected>>", lambda e: callback())
        
    def get_selected_language(self):
        return self.language_var.get()
    
    def get_selected_user_type(self):
        return self.user_type_var.get()
    
    def get_identifier_input(self):
        return self.identifier_var.get()
    
    def show_error_message(self, message):
        self.error_label.config(text=message)
        
    def update_language(self, lang_code):
        """
        更新登录视图的语言 / Update the language of the login view
        """
        self.current_language = lang_code
        # 更新視窗標題，由於此為 Frame，故更新其父容器的標題
        # if self.master is not None:
        #     self.master.title(self.languages[self.current_language]['app_title'])
        # 更新各個文字標籤
        
        self.vip_radio.config(text=self.languages[self.current_language]['radio_vip'])
        self.staff_radio.config(text=self.languages[self.current_language]['radio_staff'])
        self.identifier_label.config(text=self.languages[self.current_language]['identifier_label'])
        self.login_button_text.set(self.languages[self.current_language]['login_button'])
        self.logout_button_text.set(self.languages[self.current_language]['logout_button'])
        self.nonmember_button_text.set(self.languages[self.current_language]['nonmember_button'])
        
    def show_login_view(self):
        """
        顯示登入畫面：清除輸入並顯示登入按鈕
        """
        self.identifier_var.set("")
        self.error_label.config(text="")
        self.login_button.pack(pady=5)
        self.logout_button.pack_forget()
        self.update()
        
    def show_logout_view(self, user_type, identifier):
        """
        顯示登出畫面：隱藏登入按鈕並顯示登出按鈕與用戶資訊
        """
        self.login_button.pack_forget()
        self.logout_button.pack(pady=5)
        msg = f"{self.languages[self.current_language]['welcome_message']} {user_type}: {identifier}"
        self.error_label.config(text=msg)
        self.update()
        