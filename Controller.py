from views.Login_view import *
from Model import *
from views.Order_view import *
from Base_view import *
from Controller_translations import languages
class Controller():
    def __init__(self):
        self.languages = languages
        ## Model
        self.userModel = UserModel()
        self.vipModel = VIPModel()
        self.beerModel = BeerModel()
        self.cartModel = CartModel()
        self.orderModel = OrderModel()
        self.stockModel = StockModel()  
        self.menuModel = MenuModel()
        self.reservationModel = ReservationModelAndData()
        # For demonstration, initialize a dummy orders list
        self.orders = ["Order1: 2 x Beverage A", "Order2: 1 x Beverage B"]
        self.table_number = -1

        ## Global language setting
        self.current_language = "English"

        ## View # Must initialize self.view at first
        self.view = BaseView(self)

        # Initialize all views    
        self.view.update_all_languages(self.current_language)


        # create the login view
        if 'LoginView' in self.view.frames:
            self.login_view = self.view.frames['LoginView']
        else:
            self.login_view = LoginView(self.view, self)
            self.view.frames['LoginView'] = self.login_view
        
        # Bind login and logout events
        self.login_view.bind_login(self.handle_login)
        self.login_view.bind_logout(self.handle_logout)

        # Bind Language change in Upperview.py
        self.upper_view = self.view.frames.get("UpperView")

        if self.upper_view and hasattr(self.upper_view, "combo"):
            print("Combo box found, binding event...")
            self.upper_view.combo.bind("<<ComboboxSelected>>", self.handle_language_change)
        else:
            print("Combo box not found!")

    def handle_login(self):
        """
        Handle login logic:
        - If user_type is VIP, verify phone number. If successful, go to VIPView.
        - If user_type is Staff, proceed to StaffView (for now).
        - If identifier is invalid or verification fails, show error.
        """
        user_type = self.login_view.get_selected_user_type()
        identifier = self.login_view.get_identifier_input().strip()

        # Check if identifier is not empty
        if not identifier:
            self.login_view.show_error_message("請輸入有效資訊 / Please enter valid information.")
            return
        
        if user_type == "VIP":
            # Verify phone number via vipModel
            success = self.vipModel.verify_login_by_phone(identifier)
            if success:
                # Record VIP login info and go to VIPView
                self.login_view.show_logout_view("VIP", identifier)
                #self.show_VIP_page()
                self.show_frame("HomeVIPView")
                self.view.frames["UpperView"].update_header()
            else:
                # Show error message if phone number is invalid
                self.login_view.show_error_message("電話號碼錯誤 / Incorrect phone number.")
        else:
            # Staff: Currently login directly and enter StaffView. Can add staff ID verification as needed
            self.userModel.login("Staff", identifier)
            self.login_view.show_logout_view("Staff", identifier)
            self.show_staff_page()
            self.view.frames["UpperView"].update_header()

    def handle_logout(self):
        """
        Handle logout logic: call model.logout and update the view to show login page
        """
        self.userModel.logout()    # or self.vipModel.logout() if you like to unify
        self.vipModel.logout()
        self.login_view.show_login_view()
        self.view.frames["UpperView"].update_header()
        self.view.show_frame("HomeView")
    
    def handle_non_member(self):
        """
        Handle non-member action and navigate to HomeView
        """
        self.view.show_frame("HomeView")
        
    def handle_language_change(self, event=None):
        """
        Handle the language change event, update the global language, and notify views to refresh
        """
        selected_lang = self.upper_view.selected_var.get()
        self.set_language(selected_lang)
    
    def set_language(self, lang_code):
        """
        Set the global language and notify Base_view to update all view languages
        """
        self.current_language = lang_code
        self.view.update_all_languages(lang_code)

    def show_frame(self, page_name):
        # Show the specified page and ensure the language is synchronized
        self.view.show_frame(page_name)
        frame = self.view.frames.get(page_name)
        if frame and hasattr(frame, "update_language"):
            frame.update_language(self.current_language)

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
    
    # def Login(self, username, password, is_staff=False):
    #     userData = self.userModel.checkLogin(username, password)
    #     if userData is not None:
    #         print("Login success")
    #         if is_staff:
    #             self.show_staff_page()
    #         else:
    #             self.view.show_frame("OrderView")
    #     else:
    #         print("Login fail")
    
    def getMenuData(self, varugrupp):
        theData = self.beerModel.getDataByCategory(varugrupp)
        return theData
    
    def refreshOrderView(self, category):
        # Refresh the OrderView with the given category
        order_view = self.view.frames.get("OrderViewNew")
        order_view_VIP = self.view.frames.get("OrderViewVIP")
        if order_view:
            order_view.refresh(0, "all")
        if order_view_VIP:
            order_view_VIP.refresh(0, "all")

    def refreshSendOrderView(self):
        send_order_view = self.view.frames.get("SendOrderView")
        if send_order_view:
            send_order_view.refresh()
    
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
    
    def show_VIP_page(self):
        self.view.show_frame("OrderViewVIP")

    def get_cart_quantity(self, drink_data):
        return self.cartModel.get_quantity(drink_data)
    def add_drink_to_cart(self, drink_data):
        self.cartModel.add_to_cart(drink_data)
    def remove_drink_to_cart(self, drink_data):
        self.cartModel.remove_from_cart(drink_data)
    def cart_undo(self):
        self.cartModel.cart_undo()
    def cart_redo(self):
        self.cartModel.cart_redo()
    def clear_cart(self):
        self.cartModel.clear_cart()
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

    def send_order(self, table_number):
        # 取得購物車資料
        cart_data = self.cartModel.get_cart_data()
        if not cart_data:
            print("Cart is empty!")
            return
        self.table_number = table_number
        self.orderModel.add_order(table_number, cart_data)
        self.cartModel.clear_cart()
        self.cart_refresh()
        self.refreshSendOrderView()
    def payment_saveData(self, orders):
        self.orderModel.orders_object_to_json(orders)
    def archive_full_paid_order(self, table_number):
        self.orderModel.archive_full_paid_order(table_number)
    
    def refreshMyOrder(self):
        myOrderView = self.view.frames.get("MyOrderView")
        if myOrderView:
            myOrderView.refresh()
    def refreshpaymentView(self):
        paymentView = self.view.frames.get("PaymentView")
        if paymentView:
            paymentView.refresh()
    def get_table_number(self):
        return self.table_number
    def get_my_orders(self):
        return self.orderModel.merge_orders_to_objects()


    def addItemToMenu(self, menuItem):
        self.menuModel.addItem(menuItem)
        if menuItem.id not in self.stockModel.stock:
            beer_data = self.beerModel.getDataById(menuItem.id)
            if beer_data:
                new_beverage = {
                    "nr": beer_data.nr,
                    "artikelid": beer_data.artikelid,
                    "varnummer": getattr(beer_data, 'varnummer', ''),  # Default to empty string if missing
                    "namn": beer_data.namn,
                    "namn2": getattr(beer_data, 'namn2', ''),  # Default for optional field
                    "prisinklmoms": beer_data.prisinklmoms,
                    "volymiml": getattr(beer_data, 'volymiml', None),  # Default for optional field
                    "total_stock": 10
                }
                self.stockModel.add_beverage(new_beverage)
            else:
                print(f"Beer with id {menuItem.id} not found in beerModel.")
    
    def removeItemFromMenu(self,index):
        self.menuModel.removeItem(index)
    
    def getBeerDataFromMenu(self,):
        menuData=self.menuModel.getData()
        ids=[]
        for theData in menuData:
            ids.append(theData.id.strip())
        
        print(ids)
        
        theBeerStaticData=self.beerModel.getDataByIds(ids)
        #print(theBeerStaticData)
        return theBeerStaticData
    
    def getBeerDataFromVIPMenu(self,):
        menuData=self.menuModel.getVIPData()
        ids=[]
        for theData in menuData:
            ids.append(theData.id.strip())
        
        print(ids)
        
        theBeerStaticData=self.beerModel.getDataByIds(ids)
        #print(theBeerStaticData)
        return theBeerStaticData
    
    def addItemToVIPMenu(self, menuItem):
        self.menuModel.addVIPItem(menuItem)
        if menuItem.id not in self.stockModel.stock:
            beer_data = self.beerModel.getDataById(menuItem.id)
            if beer_data:
                new_beverage = {
                    "nr": beer_data.nr,
                    "artikelid": beer_data.artikelid,
                    "varnummer": getattr(beer_data, 'varnummer', ''),  # Default to empty string if missing
                    "namn": beer_data.namn,
                    "namn2": getattr(beer_data, 'namn2', ''),  # Default for optional field
                    "prisinklmoms": beer_data.prisinklmoms,
                    "volymiml": getattr(beer_data, 'volymiml', None),  # Default for optional field
                    "total_stock": 10
                }
                self.stockModel.add_beverage(new_beverage)
            else:
                print(f"Beer with id {menuItem.id} not found in beerModel.")
    
    def removeItemFromVIPMenu(self,index):
        self.menuModel.removeVIPItem(index)

    def get_menu_and_vip_menu_ids(self):
        menu_items = self.menuModel.getData()
        vip_menu_items = self.menuModel.getVIPData()
        all_ids = set(item.id for item in menu_items).union(set(item.id for item in vip_menu_items))
        return all_ids

    def get_reservations(self):
        #Retrieve all reservations from the model.
        return self.reservationModel.get_reservations()

    def add_reservation(self, table_number, people, time):
        #Add a new reservation with validation.
        try:
            table_number = int(table_number)
        except ValueError:
            raise ValueError("Table number must be an integer.")
        self.reservationModel.add_reservation(table_number, time, people)

    def complete_reservation(self, index):
        #Mark a reservation as completed.
        self.reservationModel.remove_reservation(index)

    def cancel_reservation(self, index):
        #Mark a reservation as canceled.
        self.reservationModel.remove_reservation(index)