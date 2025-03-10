import tkinter as tk
from tkinter import Frame
from PIL import Image, ImageTk
import random
from styles.style_config import *
from Controller_translations import languages

class HomeVIPView(Frame):
    """
    這個視圖負責在 VIP 登入後顯示用戶資訊與功能按鈕
    This view displays user info and function buttons after VIP login
    """
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        
        # 設定背景與字體 / Configure background and fonts
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        
        # 初始化語言相關屬性 / Initialize language attributes
        self.languages = languages
        self.current_language = self.controller.current_language
        
        # 產生用戶介面 / Build the user interface
        self._create_ui()
        
        # 根據當前語言更新文字 / Update texts according to current language
        self.update_language(self.current_language)

    def _create_ui(self):
        """
        建立主介面：左側資訊欄 + 右側功能按鈕欄
        Create the main UI: left info panel + right function button panel
        """
        # 全域配置 Grid
        # Global grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # 左側資訊欄 / left info panel
        self.grid_columnconfigure(1, weight=1)  # 右側功能欄 / right function panel

        # 左側資訊欄 (Info Panel)
        self.info_frame = tk.Frame(self, bg="#A7C7E7")
        self.info_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        # 使用者圖像 (User icon)
        self.user_icon_image = Image.open("images/user_icon.png").resize((150, 150))
        self.user_icon_photo = ImageTk.PhotoImage(self.user_icon_image)
        self.user_icon_label = tk.Label(self.info_frame, image=self.user_icon_photo, bg="#A7C7E7")
        self.user_icon_label.pack(pady=10)

        # 歡迎訊息 (Welcome message)
        self.label_welcome = tk.Label(self.info_frame, bg="#A7C7E7", font=("Arial", 18, "bold"))
        self.label_welcome.pack(pady=5)

        # 電話號碼 (Phone number)
        self.label_phone = tk.Label(self.info_frame, bg="#A7C7E7", font=("Arial", 14))
        self.label_phone.pack(pady=5)

        # 餘額 (Balance)
        self.label_balance = tk.Label(self.info_frame, bg="#A7C7E7", font=("Arial", 14))
        self.label_balance.pack(pady=5)

        # 右側功能欄 (Function Panel)
        self.func_frame = tk.Frame(self, bg="#A7C7E7")
        self.func_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # VIP Order Now!!! 按鈕
        self.btn_order_now = tk.Button(
            self.func_frame,
            text="VIP Order Now!!!",
            **self.button_style,
            command=self._go_to_vip_order
        )
        self.btn_order_now.pack(pady=10)

        # Self-service Drinks 按鈕
        self.btn_self_service = tk.Button(
            self.func_frame,
            text="Self-service Drinks",
            **self.button_style,
            command=self._show_self_service_code
        )
        self.btn_self_service.pack(pady=10)

        # Logout 按鈕 (標紅 / red text)
        self.btn_logout = tk.Button(
            self.func_frame,
            text="Logout",
            # **self.button_style,
            bg=self.button_style.get("bg", "#F0F0F0"),  # 手动设置背景色
            font=self.button_style.get("font", ("Arial", 12)),
            fg="red",  # 紅字 / red text
            command=self._logout
        )
        self.btn_logout.pack(pady=10)
        
        # 用於顯示 Self-service Drinks 提示的標籤
        # Label for showing the self-service drinks code message
        self.self_service_label = tk.Label(self, bg="#A7C7E7", font=("Arial", 16, "bold"), fg="red")
        self.self_service_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def _go_to_vip_order(self):
        """
        切換至 VIP 點單頁面
        Switch to the VIP Order page
        """
        self.controller.show_frame("OrderViewVIP")

    def _show_self_service_code(self):
        """
        顯示隨機 4 位數字的密碼及提示訊息
        Display a random 4-digit code and the instruction message
        """
        random_code = random.randint(1000, 9999)
        # 自助取飲料提示 / Self-service drinks prompt
        # 文字中包含 {code}，需根據多語系更新
        lang_dict = self.languages[self.current_language]
        self.self_service_label.config(
            text=lang_dict['vip_home_self_service_msg'].format(code=random_code),
            font=("Arial", 16, "bold"),  # 放大加粗 / enlarged & bold
            fg="red"
        )

    def _logout(self):
        """
        處理登出邏輯：登出後切回 HomeView
        Handle logout logic: log out and go back to HomeView
        """
        self.controller.userModel.logout()
        self.controller.vipModel.logout()
        self.controller.view.show_frame("HomeView")

    def update_language(self, lang_code):
        """
        根據指定語言更新介面文字
        Update the UI texts based on the specified language
        """
        self.current_language = lang_code
        lang_dict = self.languages[lang_code]

        # “歡迎！{username}” / “Welcome! {username}”
        # 這裡從 vipModel 取用戶資訊來獲得 username、phone、balance
        vip_info = None
        if self.controller.vipModel.is_logged_in:
            vip_info = self.controller.vipModel.get_user_info_by_phone(
                self.controller.vipModel.identifier
            )

        username = vip_info["username"] if vip_info else ""
        phone = vip_info["phone"] if vip_info else ""
        balance = vip_info["balance"] if vip_info else 0

        self.label_welcome.config(
            text=f"{lang_dict['vip_home_welcome']} {username}",
            fg="black"  # 設置標題為黑色
        )

        self.label_phone.config(
            text=f"{lang_dict['vip_home_phone']} {phone}",
            fg="blue"  # 正確使用 fg 設置文本顏色為藍色
        )

        self.label_balance.config(
            text=f"{lang_dict['vip_home_balance']} {balance} kr",
            fg="blue"
        )

        self.btn_order_now.config(text=lang_dict['vip_home_button_order'])
        self.btn_self_service.config(text=lang_dict['vip_home_button_self_service'])
        self.btn_logout.config(text=lang_dict['vip_home_button_logout'])
        
        # 如已顯示過自助取飲料提示，也應更新語言
        if self.self_service_label.cget("text"):
            random_code = random.randint(1000, 9999)
            self.self_service_label.config(
                text=lang_dict['vip_home_self_service_msg'].format(code=random_code)
            )
