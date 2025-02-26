from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from styles.style_config import *

class StaffView(Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        self.display()

    def display(self):
        title = tk.Label(self, text="Staff Page", font=self.custom_font, bg="#e0e0e0")
        title.pack(pady=20)

        # Section for checking orders
        check_order_frame = tk.Frame(self, bg="#e0e0e0")
        check_order_frame.pack(pady=10)
        check_order_lbl = tk.Label(check_order_frame, text="Check Orders", font=self.custom_font, bg="#e0e0e0")
        check_order_lbl.pack(side="left", padx=10)
        check_order_btn = tk.Button(check_order_frame, text="View Orders", **self.button_style, command=self.controller.checkOrders)
        check_order_btn.pack(side="left", padx=10)

        # Section for modifying menu
        modify_menu_frame = tk.Frame(self, bg="#e0e0e0")
        modify_menu_frame.pack(pady=10)
        modify_menu_lbl = tk.Label(modify_menu_frame, text="Modify Menu", font=self.custom_font, bg="#e0e0e0")
        modify_menu_lbl.pack(side="left", padx=10)
        add_item_btn = tk.Button(modify_menu_frame, text="Add Beverage", **self.button_style, command=self.controller.addBeverage)
        add_item_btn.pack(side="left", padx=10)
        remove_item_btn = tk.Button(modify_menu_frame, text="Remove Beverage", **self.button_style, command=self.controller.removeBeverage)
        remove_item_btn.pack(side="left", padx=10)

        # Section for updating stock data
        update_stock_frame = tk.Frame(self, bg="#e0e0e0")
        update_stock_frame.pack(pady=10)
        beverage_id_lbl = tk.Label(update_stock_frame, text="Beverage ID:", font=self.custom_font, bg="#e0e0e0")
        beverage_id_lbl.grid(row=0, column=0, padx=5, pady=5)
        self.beverage_id_entry = tk.Entry(update_stock_frame)
        self.beverage_id_entry.grid(row=0, column=1, padx=5, pady=5)
        stock_amount_lbl = tk.Label(update_stock_frame, text="New Stock Amount:", font=self.custom_font, bg="#e0e0e0")
        stock_amount_lbl.grid(row=1, column=0, padx=5, pady=5)
        self.stock_amount_entry = tk.Entry(update_stock_frame)
        self.stock_amount_entry.grid(row=1, column=1, padx=5, pady=5)
        update_stock_btn = tk.Button(update_stock_frame, text="Update Stock", **self.button_style, command=self.update_stock)
        update_stock_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Section for viewing total stock
        view_stock_frame = tk.Frame(self, bg="#e0e0e0")
        view_stock_frame.pack(pady=10)
        view_stock_btn = tk.Button(view_stock_frame, text="View Total Stock", **self.button_style, command=self.controller.viewTotalStock)
        view_stock_btn.pack(side="left", padx=10)

        # Back button
        back_btn = tk.Button(self, text="Back", **self.button_style, command=lambda: self.controller.view.show_frame("HomeView"))
        back_btn.pack(pady=20)

    def update_stock(self):
        beverage_id = self.beverage_id_entry.get()
        try:
            amount = int(self.stock_amount_entry.get())
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("Input Error", "Please enter a valid number for stock amount.")
            return
        self.controller.updateStockData(beverage_id, amount)
