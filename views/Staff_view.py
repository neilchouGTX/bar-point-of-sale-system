import tkinter as tk
from tkinter import ttk
from functools import partial
from styles.style_config import * 
import tkinter.simpledialog as sd
import tkinter.messagebox as mbox
from Controller_translations import languages
from Model import MenuItem

class StaffView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.current_page = "order"  # Default page
        self.stock_page = 1
        self.stock_page_size = 20
        self.stock_filter = ""
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)

        self.setup_ui()
        self.load_page(self.current_page)

        #初始化語言 /initialize language
        self.languages = languages
        self.current_language = self.controller.current_language
       


    def setup_ui(self):
        """Set up the UI with grid layout."""
        # Title
        title_label = tk.Label(self, text="Staff Panel", font=("Georgia", 24, "bold"), bg="#A7C7E7", fg="#000435")
        title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Navigation buttons
        nav_frame = tk.Frame(self, bg="#A7C7E7")
        nav_frame.grid(row=1, column=0, columnspan=4, pady=10)

        self.buttons = {}
        for idx, page in enumerate(["order", "stock", "reservation", "menu", "VIP_menu"]):
            btn = tk.Button(nav_frame, text=page.capitalize(), **self.button_style,
                            command=partial(self.switch_page, page))
            btn.grid(row=0, column=idx, padx=10)
            self.buttons[page] = btn

        # Table frame
        self.table_frame = tk.Frame(self, bg="white", bd=2, relief="solid", width=235, height=168)
        self.table_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_propagate(False)  # Prevent auto-resizing


        self.highlight_button(self.current_page)


        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def switch_page(self, page):
        """Switch the current page and update the table."""
        self.current_page = page
        self.stock_page = 1  
        self.stock_filter = ""  #
        self.highlight_button(page)
        self.load_page(page)
        self.update_language(self.controller.current_language)

    def highlight_button(self, page):
        
        for btn_page, btn in self.buttons.items():
            if btn_page == page:
                btn.config(bg="#FFC107")  # Yellow for active
            else:
                btn.config(**self.button_style)  # Default style for inactive

    def load_page(self, page):
        # Clear table_frame completely to prevent layout shifts
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Create a new treeview for the table
        self.table = ttk.Treeview(self.table_frame, style="Custom.Treeview")
        self.table.pack(fill="both", expand=True)

        # Reset columns and heading for treeview
        self.table["columns"] = ()
        self.table.heading("#0", text="", anchor="w")
        self.table.unbind("<Button-1>")

        if page == "order":
            self.load_orders()
        elif page == "stock":
            self.load_stock()
        elif page == "reservation":
            self.load_reservations()
        elif page == "menu":
            self.load_menu()
        elif page == "VIP_menu":
            self.load_VIP_Menu()

    def load_orders(self):
        "Populate table with order data."
        columns = ("table_number", "beer", "amount", "action")
        self.table["columns"] = columns
        for col in columns:
            self.table.heading(col, text=col.capitalize(), anchor="w")
            self.table.column(col, width=150, anchor="w")

        self.controller.orderModel.loadData()
        self.controller.orderModel.jsonToObject()
        orders = self.controller.orderModel.staticData
        for order in orders:
            table_number = order.tableNumber
            for item in order.orderItems:
                # Convert item.id to string to match BeerModel's data format
                beer_data = self.controller.beerModel.getDataById(str(item.id))
                beer_name = beer_data.namn if beer_data else "Unknown"
                amount = item.amount
                self.table.insert("", "end", values=(table_number, beer_name, amount, ""), tags=("action_row",))

        for iid in self.table.get_children():
            self.action_buttons(iid, ["complete", "cancel"], self.order_action)

    def load_stock(self):
        columns = ("id", "beer", "amount", "action")
        self.table["columns"] = columns
        for col in columns:
            self.table.heading(col, text=col.capitalize(), anchor="w")
            self.table.column(col, width=150, anchor="w")

        # Fetch paginated stock data with lazy loading
        total, details, current_page, total_pages = self.controller.stockModel.view_total_stock_page(
            self.stock_page, self.stock_page_size, self.stock_filter)
        stock_data = []
        for line in details.split("\n"):
            if ":" in line:
                bev, amt = line.split(":")
                bev_id = bev.strip().split(" (nr: ")[1].rstrip(")")
                bev_name = bev.split(" (nr: ")[0].strip()
                stock_data.append({"id": bev_id, "beer": bev_name, "amount": int(amt.strip())})

        for item in stock_data:
            self.table.insert("", "end", values=(item["id"], item["beer"], item["amount"], ""), tags=("action_row",))

        for iid in self.table.get_children():
            self.action_buttons(iid, ["edit"], self.stock_action)

        # Add filter and pagination controls using grid inside a control frame
        control_frame = tk.Frame(self.table_frame, bg="white")
        control_frame.pack(pady=5)

        # Filter controls
        self.filter_label = tk.Label(control_frame, text="Filter by ID or name:", font=self.custom_font, bg="white")
        self.filter_label.grid(row=0, column=0, padx=5)
        self.filter_entry = tk.Entry(control_frame)
        self.filter_entry.grid(row=0, column=1, padx=5)
        self.filter_btn = tk.Button(control_frame, text="Filter", **self.button_style, command=lambda: self.apply_stock_filter(self.filter_entry.get()))
        self.filter_btn.grid(row=0, column=2, padx=5)

        # Pagination buttons
        self.prev_btn = tk.Button(control_frame, text="Previous", **self.button_style, command=self.prev_stock_page)
        self.prev_btn.grid(row=0, column=3, padx=5)
        self.next_btn = tk.Button(control_frame, text="Next", **self.button_style, command=self.next_stock_page)
        self.next_btn.grid(row=0, column=4, padx=5)

    def prev_stock_page(self):
        """Go to the previous stock page."""
        if self.stock_page > 1:
            self.stock_page -= 1
            self.load_page("stock")

    def next_stock_page(self):
        """Go to the next stock page."""
        self.stock_page += 1
        self.load_page("stock")

    def apply_stock_filter(self, filter_text):
        """Apply filter to stock data and reload."""
        self.stock_filter = filter_text
        self.stock_page = 1
        self.load_page("stock")

    def load_reservations(self):
        """Populate table with reservation data (placeholder)."""
        columns = ("table_number", "time", "status", "action")
        self.table["columns"] = columns
        for col in columns:
            self.table.heading(col, text=col.capitalize(), anchor="w")
            self.table.column(col, width=150, anchor="w")

        # Placeholder data
        reservations = [{"id": "1", "table_number": "3", "time": "18:00", "status": "Pending"}]
        for res in reservations:
            self.table.insert("", "end", text=res["id"], values=(res["table_number"], res["time"], res["status"], ""), tags=("action_row",))

        for iid in self.table.get_children():
            self.action_buttons(iid, ["confirm", "cancel"], self.reservation_action)

    def load_menu(self):
        """Populate table with menu data from dutchman_menu.json and add menu addition section."""
        columns = ("id", "name", "action")
        self.table["columns"] = columns
        for col in columns:
            self.table.heading(col, text=col.capitalize(), anchor="w")
            self.table.column(col, width=150, anchor="w")

        menu_data = self.controller.getBeerDataFromMenu()
        for item in menu_data:
            self.table.insert("", "end", values=(item.nr, item.namn, "Remove"), tags=("action_row",))

        self.table.bind("<Button-1>", self.on_Menu_Remove_click)
        ##for iid in self.table.get_children():
            #self.action_buttons(iid, ["remove"], self.menu_action)

        # Add menu addition frame below the table
        add_frame = tk.Frame(self.table_frame, bg="white")
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Add Menu Item", font=self.custom_font, bg="white").pack(pady=5)

        # Combobox for selecting beverage
        beers = self.controller.beerModel.staticData
        print("Number of beers available:", len(beers))  # Debug: Check beer data
        values = [f"{beer.nr}, {beer.namn}" for beer in beers[:30]]  # Limit to first 30
        self.combo = ttk.Combobox(add_frame, values=values, width=50)
        self.combo.pack(padx=10, pady=5)

        add_btn = tk.Button(add_frame, text="Add", **self.button_style, command=self.add_menu_item)
        add_btn.pack(pady=10)
    def load_VIP_Menu(self):
        """Populate table with menu data from dutchman_menu.json and add menu addition section."""
        columns = ("id", "name", "action")
        self.table["columns"] = columns
        for col in columns:
            self.table.heading(col, text=col.capitalize(), anchor="w")
            self.table.column(col, width=150, anchor="w")

        menu_data = self.controller.getBeerDataFromVIPMenu()
        for item in menu_data:
            self.table.insert("", "end", values=(item.nr, item.namn, "Remove"), tags=("action_row",))

        self.table.bind("<Button-1>", self.on_VIP_Menu_Remove_click)
        ##for iid in self.table.get_children():
            #self.action_buttons(iid, ["remove"], self.menu_action)

        # Add menu addition frame below the table
        add_frame = tk.Frame(self.table_frame, bg="white")
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Add Menu Item", font=self.custom_font, bg="white").pack(pady=5)

        # Combobox for selecting beverage
        beers = self.controller.beerModel.staticData
        print("Number of beers available:", len(beers))  # Debug: Check beer data
        values = [f"{beer.nr}, {beer.namn}" for beer in beers[:20]]  # Limit to first 20
        self.combo = ttk.Combobox(add_frame, values=values, width=50)
        self.combo.pack(padx=10, pady=5)

        add_btn = tk.Button(add_frame, text="Add", **self.button_style, command=self.add_VIP_menu_item)
        add_btn.pack(pady=10)

    def on_Menu_Remove_click(self,event):
        
        selected_item = self.table.identify_row(event.y)  # 獲取被點擊的行 ID
        selected_column = self.table.identify_column(event.x)  # 獲取被點擊的列 ID（格式為 #1, #2, #3 ...）

        if selected_item and selected_column == "#3":
            #item_values = self.table.item(selected_item, "values")  # 獲取該行的所有值
            #id = item_values[0] 
            #name = item_values[1]
            index = self.table.index(selected_item)
            self.controller.removeItemFromMenu(index)
            self.load_page("menu")
            #print(f"id:{id}, name:{name}")
    
    def on_VIP_Menu_Remove_click(self,event):
        selected_item = self.table.identify_row(event.y)  # 獲取被點擊的行 ID
        selected_column = self.table.identify_column(event.x)  # 獲取被點擊的列 ID（格式為 #1, #2, #3 ...）

        if selected_item and selected_column == "#3":
            #item_values = self.table.item(selected_item, "values")  # 獲取該行的所有值
            #id = item_values[0] 
            #name = item_values[1]
            index = self.table.index(selected_item)
            self.controller.removeItemFromVIPMenu(index)
            self.load_page("VIP_menu")
            #print(f"id:{id}, name:{name}")      
     
    def add_menu_item(self):
        """Add a new item to the menu using the combobox selection."""
        selected = self.combo.get()
        print("Selected value:", selected)  # Debug: Check combobox selection
        if selected:
            try:
                nr, namn = selected.split(", ", 1)
                print("Parsed - nr:", nr, "namn:", namn)  # Debug: Check split result
                menu_item = MenuItem(nr.strip(), namn.strip())
                self.controller.addItemToMenu(menu_item)
                self.load_page("menu")  # Refresh the menu page
                mbox.showinfo("Menu Update", f"Added {namn.strip()} to menu.")
            except Exception as e:
                mbox.showerror("Error", f"Failed to add item: {str(e)}")
        else:
            mbox.showerror("Error", "Please select a beer.")
    
    def add_VIP_menu_item(self):
        """Add a new item to the menu using the combobox selection."""
        selected = self.combo.get()
        print("Selected value:", selected)  # Debug: Check combobox selection
        if selected:
            try:
                nr, namn = selected.split(", ", 1)
                print("Parsed - nr:", nr, "namn:", namn)  # Debug: Check split result
                menu_item = MenuItem(nr.strip(), namn.strip())
                self.controller.addItemToVIPMenu(menu_item)
                self.load_page("VIP_menu")  # Refresh the menu page
                mbox.showinfo("VIP Menu Update", f"Added {namn.strip()} to menu.")
            except Exception as e:
                mbox.showerror("Error", f"Failed to add item: {str(e)}")
        else:
            mbox.showerror("Error", "Please select a beer.")

    def action_buttons(self, iid, actions, callback):
        values = list(self.table.item(iid, "values"))
        action_frame = tk.Frame(self.table)
        for action in actions:
            btn = tk.Button(action_frame, text=action.capitalize(),
                            bg="green" if action == "complete" else "#ADD8E6",
                            fg="white", command=lambda a=action, i=iid: callback(a, i))
            btn.pack(side="left", padx=2)
        # Set the last column's value to the action_frame widget
        self.table.set(iid, column=len(values)-1, value=action_frame)
        self.table.item(iid, values=values)

    def order_action(self, action, iid):
        "Handle order actions."
        table_number = self.table.item(iid, "values")[0]
        if action == "complete":
            self.controller.orderModel.staticData = [
                order for order in self.controller.orderModel.staticData
                if order.tableNumber != table_number
            ]
            self.controller.orderModel.saveData()
            self.load_page("order")
        elif action == "cancel":
            print(f"Cancel order for table {table_number}")

    def stock_action(self, action, iid):
        "Handle stock actions."
        if action == "edit":
            bev_id = self.table.item(iid, "values")[0]
            new_amount = tk.simpledialog.askinteger("Edit Stock", f"New amount for {bev_id}:")
            if new_amount is not None:
                self.controller.updateStockData(bev_id, new_amount)
                self.load_page("stock")

    def reservation_action(self, action, iid):
        """Handle reservation actions (placeholder)."""
        print(f"Reservation action: {action} on item {iid}")

    def menu_action(self, action, iid):
        """Handle menu actions."""
        if action == "remove":
            item_id = self.table.item(iid, "values")[0]
            self.controller.removeItemFromMenu(item_id)
            self.load_page("menu")

    def update_language(self, lang_code):
        """
        只更新導航按鈕的語言，而不改變表格標題。
        Update only the navigation buttons' text without modifying table headers.
        """
        # 獲取當前語言字典 / Get the current language dictionary
        ldict = self.controller.languages[lang_code]

        # 對應關鍵字與語言字典中的翻譯 / Map button keys to their translated text
        button_map = {
            "order": ldict['order_page'],
            "stock": ldict['stock_page'],
            "reservation": ldict['reservation_page'],
            "menu": ldict['menu_page']
        }

        # 逐一更新導航按鈕文字 / Update the text of each navigation button
        for key, button in self.buttons.items():
            if key in button_map:
                button.config(text=button_map[key])
        
        # 僅在切換到 “stock” 頁時，才更新 filter_label, prev_btn, next_btn
        if self.current_page == "stock":
            # 確保這些屬性已在 load_stock() 中被建立
                self.filter_label.config(text=ldict['filter_label'])
                self.filter_btn.config(text=ldict['filter'])
                self.prev_btn.config(text=ldict['previous'])
                self.next_btn.config(text=ldict['next'])