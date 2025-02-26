import json
import tkinter as tk
from tkinter import font
from views.Order_view import *
from views.Login_view import *
from views.Upper_view import *
from views.Home_view import *
from views.Order_viewNew import *
from views.Staff_view import *
from views.Cart_view import *
from views.Reservation_view import *

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
        for F in (HomeView, UpperView, OrderView, LoginView, OrderViewNew, StaffView, CartView, ReservationView):
            page_name = F.__name__
            frame = F(root=self, controller=self.controller)
            self.frames[page_name] = frame
            if page_name == "UpperView":
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame.grid(row=1, column=0, sticky="nsew")
    
        self.show_frame("HomeView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        self.current_frame = frame
        frame.tkraise()
        
        for f in self.frames.values():
            if hasattr(f, "canvas"):
                f.canvas.unbind("<MouseWheel>")

        # 只對當前顯示的 Frame 綁定滾輪事件
        if hasattr(frame, "canvas"):
            frame.canvas.bind("<MouseWheel>", frame._on_mousewheel)
    
    def set_current_frame(self, frame):
        self.current_frame = frame

    def get_current_frame(self):
        return self.current_frame
