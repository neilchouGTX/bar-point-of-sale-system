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
        self.stockModel = StockModel()  # Now using the JSON-backed stock model
        self.menuModel = MenuModel()
        # For demonstration, initialize a dummy orders list
        self.orders = ["Order1: 2 x Beverage A", "Order2: 1 x Beverage B"]
        self.table_number = -1

        ## 全局语言设置 / Global language setting
        self.current_language = "English"

        ## View # Must initialize self.view at first
        self.view = BaseView(self)

        # 設置初始語言給所有視圖    
        self.view.update_all_languages(self.current_language)


        # 建立或取得登录视图，并绑定登录相关事件
        if 'LoginView' in self.view.frames:
            self.login_view = self.view.frames['LoginView']
        else:
            self.login_view = LoginView(self.view, self)
            self.view.frames['LoginView'] = self.login_view
        
        # 绑定登录、登出事件 / Bind login and logout events
        self.login_view.bind_login(self.handle_login)
        self.login_view.bind_logout(self.handle_logout)

        # 绑定 UpperView 里的语言切换控件/ Bind Language change in Upperview.py
        self.upper_view = self.view.frames.get("UpperView")

        if self.upper_view and hasattr(self.upper_view, "combo"):
            print("Combo box found, binding event...")
            self.upper_view.combo.bind("<<ComboboxSelected>>", self.handle_language_change)
        else:
            print("Combo box not found!")

    # def handle_login(self):
    #     """
    #     處理登入邏輯：取得使用者類型與識別資訊，
    #     若輸入有效，則透過 model 執行 login，並更新視圖以顯示登出狀態；
    #     否則顯示錯誤訊息。
    #     """
    #     user_type = self.login_view.get_selected_user_type()
    #     identifier = self.login_view.get_identifier_input()
    #     if identifier.strip():
    #         self.userModel.login(user_type, identifier)
    #         self.login_view.show_logout_view(user_type, identifier)
    #         if user_type == "Staff":
    #             self.show_staff_page()
    #         if user_type == "VIP":
    #             self.show_VIP_page()

    #     else:
    #         self.login_view.show_error_message("請輸入有效資訊 / Please enter valid information.")
    
    # def handle_logout(self):
    #     """
    #     處理登出邏輯：呼叫 model.logout 並更新視圖顯示登入畫面。
    #     """
    #     self.userModel.logout()
    #     self.login_view.show_login_view()
    def handle_login(self):
        """
        處理登入邏輯：
        如果是 VIP，檢查電話號碼是否有效；若成功則登入並進入 VIPView。
        如果是 Staff，暫時直接登入並進入 StaffView。
        如果識別資訊為空或驗證失敗，顯示錯誤訊息。
        Handle login logic:
        - If user_type is VIP, verify phone number. If successful, go to VIPView.
        - If user_type is Staff, proceed to StaffView (for now).
        - If identifier is invalid or verification fails, show error.
        """
        user_type = self.login_view.get_selected_user_type()
        identifier = self.login_view.get_identifier_input().strip()

        # 檢查是否有輸入識別資訊 / Check if identifier is not empty
        if not identifier:
            self.login_view.show_error_message("請輸入有效資訊 / Please enter valid information.")
            return
        
        if user_type == "VIP":
            # 透過 vipModel 驗證手機號碼
            # Verify phone number via vipModel
            success = self.vipModel.verify_login_by_phone(identifier)
            if success:
                # 成功後紀錄 VIP 登入資訊，並跳轉至 VIPView
                self.login_view.show_logout_view("VIP", identifier)
                #self.show_VIP_page()
                self.show_frame("HomeVIPView")
                self.view.frames["UpperView"].update_header()
            else:
                # 顯示錯誤提示
                self.login_view.show_error_message("電話號碼錯誤 / Incorrect phone number.")
        else:
            # Staff：目前直接登入並進入 StaffView。可依需求擴充檢驗員工ID
            self.userModel.login("Staff", identifier)
            self.login_view.show_logout_view("Staff", identifier)
            self.show_staff_page()
            self.view.frames["UpperView"].update_header()

    def handle_logout(self):
        """
        處理登出邏輯：呼叫 model.logout 並更新視圖顯示登入畫面
        Handle logout logic: call model.logout and update the view to show login page
        """
        self.userModel.logout()    # or self.vipModel.logout() if you like to unify
        self.vipModel.logout()
        self.login_view.show_login_view()
        self.view.frames["UpperView"].update_header()
        self.view.show_frame("HomeView")
    
    def handle_non_member(self):
        """
        處理非會員操作，跳轉到首頁
        Handle non-member action and navigate to HomeView
        """
        self.view.show_frame("HomeView")
        
    def handle_language_change(self, event=None):
        """
        處理語言切換事件，更新全局語言並通知視圖更新
        Handle the language change event, update the global language, and notify views to refresh
        """
        selected_lang = self.upper_view.selected_var.get()
        self.set_language(selected_lang)
    
    def set_language(self, lang_code):
        """
        設置全局語言並通知 Base_view 更新所有視圖語言
        Set the global language and notify Base_view to update all view languages
        """
        self.current_language = lang_code
        self.view.update_all_languages(lang_code)

    # def handle_language_change(self):
    #     """
    #     處理語言切換邏輯：取得使用者選擇的語言並更新視圖顯示。
    #     """
    #     selected_lang = self.login_view.get_selected_language()
    #     self.login_view.update_language(selected_lang)

    def show_frame(self, page_name):
        """
        顯示指定頁面，並確保語言同步
        Show the specified page and ensure the language is synchronized
        """
        self.view.show_frame(page_name)
        # 確保新顯示的頁面語言更新
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
        """讓 OrderViewNew 重新加載新分類的數據"""
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
    
    def refreshMyOrder(self):
        myOrderView = self.view.frames.get("MyOrderView")
        if myOrderView:
            myOrderView.refresh()
    def get_table_number(self):
        return self.table_number
    def get_my_orders(self):
        return self.orderModel.merge_orders_to_objects()


    def addItemToMenu(self,menuItem):
        theItem=menuItem
        self.menuModel.addItem(theItem)
    
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
    
    def addItemToVIPMenu(self,menuItem):
        theItem=menuItem
        self.menuModel.addVIPItem(theItem)
    
    def removeItemFromVIPMenu(self,index):
        self.menuModel.removeVIPItem(index)