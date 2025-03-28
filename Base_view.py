import json
import tkinter as tk
from tkinter import font
from views.Order_view import *
from views.Login_view import *
from views.Upper_view import *
from views.Home_view import *
from views.Order_viewNew import *
from views.Order_view_VIP import *
from views.My_orders_view import *
from views.Staff_view import *
from views.Cart_view import *
from views.SendOrder_view import *
from views.Reservation_view import *
from views.Home_VIP_view import *
from views.Payment_view import *

class BaseView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.frames = {}
        self.title("Ordering System")
        self.configure(bg="#211402")
        self.geometry("1366x768")
        self.current_frame = None

        self.grid_rowconfigure(0, weight=1, minsize=30)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize Frame pages
        for F in (HomeView, UpperView, OrderView, LoginView, OrderViewNew, OrderViewVIP, MyOrderView,StaffView, CartView, ReservationView, SendOrderView, HomeVIPView, PaymentView):

            page_name = F.__name__
            frame = F(root=self, controller=self.controller)
            self.frames[page_name] = frame
            if page_name == "UpperView":
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame.grid(row=1, column=0, sticky="nsew")
    
        # 設置初始語言 / Set the initial language
        self.update_all_languages(self.controller.current_language)
  
        self.show_frame("HomeView")

    def show_frame(self, page_name):
        if page_name == "LoginView":
            # 檢查當前是否已登入 / Check if login
            if self.controller.userModel.is_logged_in or self.controller.vipModel.is_logged_in:
                self.controller.login_view.show_logout_view( ... )  # 視情況而定
            else:
                self.controller.login_view.show_login_view()
        frame = self.frames[page_name]
        self.current_frame = frame
        frame.tkraise()
        
        for f in self.frames.values():
            if hasattr(f, "canvas"):
                f.canvas.unbind("<MouseWheel>")

        # 只對當前顯示的 Frame 綁定滾輪事件
        if hasattr(frame, "canvas"):
            frame.canvas.bind("<MouseWheel>", frame._on_mousewheel)
    
           # 确保新显示的页面也同步语言 / Ensure new page also updates language
        if hasattr(frame, "update_language"):
            frame.update_language(self.controller.current_language)
    
    def set_current_frame(self, frame):
        self.current_frame = frame

    def get_current_frame(self):
        return self.current_frame
    
    def update_all_languages(self, lang_code):
        """
        讓所有視圖的語言與當前語言設置同步
        Synchronize the language of all views with the current language setting
        """
        for frame in self.frames.values():
            if hasattr(frame, "update_language"):
                frame.update_language(lang_code)
