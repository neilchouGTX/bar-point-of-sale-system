from views.Login_view import *
from Model import *
from views.Order_view import *
from Base_view import *

class Controller():
    def __init__(self):
        ## Model
        self.userModel = UsersModel()
        self.beerModel = BeerModel()
        self.cartModel = CartModel()
        self.stockModel = stockModel  # Now using the JSON-backed stock model
        self.menuModel = MenuModel()
        # For demonstration, initialize a dummy orders list
        self.orders = ["Order1: 2 x Beverage A", "Order2: 1 x Beverage B"]

        ## View
        self.view = BaseView(self)

    def toggle_language_menu(self):
        if self.view.UpperViewlanguage_frame.winfo_ismapped():
            self.view.language_frame.place_forget()
        else:
            self.view.language_frame.place(x=1200, y=50)
            self.view.language_frame.lift()

    def toggle_drinks_menu(self):
        if self.view.drinks_menu_frame.winfo_ismapped():
            self.view.drinks_menu_frame.place_forget()
        else:
            self.view.drinks_menu_frame.place(x=100, y=90)
            self.view.drinks_menu_frame.lift()
            self.model.get_drinks_list()

    def displayView(self):
        self.view.display()
    
    def Login(self, username, password, is_staff=False):
        userData = self.userModel.checkLogin(username, password)
        if userData is not None:
            print("Login success")
            if is_staff:
                self.show_staff_page()
            else:
                self.view.show_frame("OrderView")
        else:
            print("Login fail")
    
    def getMenuData(self, varugrupp):
        theData = self.beerModel.getDataByCategory(varugrupp)
        return theData
    
    def refreshOrderView(self, category):
        """讓 OrderViewNew 重新加載新分類的數據"""
        order_view = self.view.frames.get("OrderViewNew")
        if order_view:
            order_view.refresh(category)
    
    def updateStockData(self, beverage_id, amount):
        """Update stock data for a given beverage in the JSON file"""
        self.stockModel.update_stock(beverage_id, amount)
        import tkinter.messagebox as mbox
        mbox.showinfo("Stock Update", f"Updated stock for beverage {beverage_id} to {amount}")

    def checkOrders(self):
        """Display current orders to staff"""
        import tkinter.messagebox as mbox
        order_text = "\n".join(self.orders)
        mbox.showinfo("Current Orders", order_text)
    
    def viewTotalStock(self):
        """Display current total stock from the stock model"""
        total = 0
        details = ""
        for bev, amount in self.stockModel.stock.items():
            total += amount
            details += f"Beverage {bev}: {amount}\n"
        if not details:
            details = "No stock available."
        from tkinter import messagebox
        messagebox.showinfo("Total Stock", f"Total stock: {total}\n\nDetails:\n{details}")


    def addBeverage(self):
        import tkinter.simpledialog as sd
        import tkinter.messagebox as mbox
        nr = sd.askstring("Add Beverage", "Enter beverage nr:")
        artikelid = sd.askstring("Add Beverage", "Enter artikelid:")
        varnummer = sd.askstring("Add Beverage", "Enter varnummer:")
        namn = sd.askstring("Add Beverage", "Enter beverage name:")
        pris = sd.askstring("Add Beverage", "Enter price (prisinklmoms):")
        total_stock = sd.askinteger("Add Beverage", "Enter initial stock:")
        if nr and namn:
             new_beverage = {
                  "nr": nr,
                  "artikelid": artikelid if artikelid else "",
                  "varnummer": varnummer if varnummer else "",
                  "namn": namn,
                  "namn2": "",
                  "prisinklmoms": pris if pris else "0",
                  "volymiml": None,
                  "total_stock": total_stock if total_stock is not None else 0
             }
             self.stockModel.add_beverage(new_beverage)
             mbox.showinfo("Add Beverage", f"Beverage '{namn}' added.")
        else:
             mbox.showerror("Add Beverage", "Beverage nr and name are required.")

    def removeBeverage(self):
        import tkinter.simpledialog as sd
        import tkinter.messagebox as mbox
        namn = sd.askstring("Remove Beverage", "Enter beverage name to remove:")
        if namn:
             removed = self.stockModel.remove_beverage(namn)
             if removed:
                 mbox.showinfo("Remove Beverage", f"Beverage '{namn}' removed.")
             else:
                 mbox.showinfo("Remove Beverage", f"Beverage '{namn}' not found.")
        else:
             mbox.showerror("Remove Beverage", "Beverage name is required.")

    def viewTotalStock(self, page=1, page_size=20):
        """Display current total stock from the JSON file in a paginated window"""
        total, details, current_page, total_pages = self.stockModel.view_total_stock_page(page, page_size)
        import tkinter as tk

        win = tk.Toplevel()
        win.title(f"Total Stock - Page {current_page} of {total_pages}")

        text = tk.Text(win, width=80, height=20)
        text.insert(tk.END, f"Total stock: {total}\n\n{details}")
        text.config(state=tk.DISABLED)
        text.pack(padx=10, pady=10)

        button_frame = tk.Frame(win)
        button_frame.pack(pady=5)

        def go_previous():
            if current_page > 1:
                win.destroy()
                self.viewTotalStock(page=current_page-1, page_size=page_size)

        def go_next():
            if current_page < total_pages:
                win.destroy()
                self.viewTotalStock(page=current_page+1, page_size=page_size)

        prev_btn = tk.Button(button_frame, text="Previous", command=go_previous)
        prev_btn.pack(side=tk.LEFT, padx=5)

        next_btn = tk.Button(button_frame, text="Next", command=go_next)
        next_btn.pack(side=tk.LEFT, padx=5)

        close_btn = tk.Button(button_frame, text="Close", command=win.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)

    def show_staff_page(self):
        self.view.show_frame("StaffView")

    def get_cart_quantity(self, drink_data):
        return self.cartModel.get_quantity(drink_data)
    def add_drink_to_cart(self, drink_data):
        self.cartModel.add_to_cart(drink_data)
    def remove_drink_to_cart(self, drink_data):
        self.cartModel.remove_from_cart(drink_data)

    def get_cart_data(self):
        return self.cartModel.get_cart_data()
    def cart_refresh(self):
        cart_view = self.view.frames.get("CartView")
        if cart_view:
            cart_view.refresh()
    def cart_update_all_total_price(self):
        cart_view = self.view.frames.get("CartView")
        if cart_view:
            cart_view.update_all_total_price()


    def addItemToMenu(self,menuItem):
        theItem=menuItem
        self.menuModel.addItem(theItem)
    
    def removeItemFromMenu(self,index):
        self.menuModel.removeItem(index)
