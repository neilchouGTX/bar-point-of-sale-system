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
        # Title
        title_label = tk.Label(self, text="Staff Panel", font=("Georgia", 24, "bold"), bg="#A7C7E7", fg="#000435")
        title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Navigation buttons
        nav_frame = tk.Frame(self, bg="#A7C7E7")
        nav_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")

        self.buttons = {}
        for idx, page in enumerate(["order", "stock", "reservation", "menu", "VIP_menu"]):
            btn = tk.Button(nav_frame, text=page.capitalize(), **self.button_style,
                            command=partial(self.switch_page, page))
            btn.grid(row=0, column=idx, padx=10, sticky="news")
            nav_frame.grid_columnconfigure(idx, weight=1)
            self.buttons[page] = btn

        # Table frame
        self.table_frame = tk.Frame(self, bg="white", bd=2, relief="solid", width=235, height=168)
        self.table_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_propagate(False)  # Prevent auto-resizing


        self.highlight_button(self.current_page)


        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def switch_page(self, page):
        #Switch the current page and update the table.
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
        columns = ("table", "beer", "amount", "action")
        self.table["columns"] = columns
        for col in columns:
            if col == "action":
                self.table.heading(col, text=col.capitalize(), anchor="center")
                self.table.column(col, width=200, anchor="center")
            else:
                self.table.heading(col, text=col.capitalize(), anchor="w")
                self.table.column(col, width=150, anchor="w")

        self.controller.orderModel.loadData()
        self.controller.orderModel.jsonToObject()
        orders = self.controller.orderModel.staticData
        for order_index, order in enumerate(orders):
            table_number = order.tableNumber
            for item_index, item in enumerate(order.orderItems):
                beer_data = self.controller.beerModel.getDataById(str(item.id))
                beer_name = beer_data.namn if beer_data else "Unknown"
                amount = item.amount
                # Create an identifier that encodes the order and item indices.
                iid = f"order_{order_index}_item_{item_index}"
                # Combine the two actions into a single cell with a delimiter.
                action_text = "Complete | Cancel"
                self.table.insert("", "end", iid=iid, values=(table_number, beer_name, amount, action_text))

        # Bind clicks to our custom handler.
        self.table.bind("<Button-1>", self.on_order_action_click)


    def on_order_action_click(self, event):
        selected_item = self.table.identify_row(event.y)
        selected_column = self.table.identify_column(event.x)
        if selected_item and selected_column:
            # Determine which column was clicked.
            column_index = int(selected_column[1:]) - 1  # e.g., '#1' -> 0, '#2' -> 1, etc.
            column_name = self.table["columns"][column_index]
            if column_name == "action":
                # Get the bounding box of the clicked cell.
                bbox = self.table.bbox(selected_item, selected_column)
                if bbox:
                    cell_x, cell_y, cell_width, cell_height = bbox
                    # Calculate click position relative to the cell.
                    x_offset = event.x - cell_x
                    # Divide the cell in two halves.
                    if x_offset < cell_width / 2:
                        action = "action1"  # Left half → "Complete"
                    else:
                        action = "action2"  # Right half → "Cancel"
                    
                    # Parse the iid to retrieve order and item indices.
                    parts = selected_item.split("_")
                    if len(parts) == 4 and parts[0] == "order" and parts[2] == "item":
                        order_index = int(parts[1])
                        item_index = int(parts[3])
                        self.order_action(action, order_index, item_index)


    def load_stock(self):
        # Use a single "action" column instead of separate action columns.
        columns = ("id", "beer", "amount", "action")
        self.table["columns"] = columns
        for col in columns:
            if col == "action":
                self.table.heading(col, text=col.capitalize(), anchor="center")
                self.table.column(col, width=200, anchor="center")
            else:
                self.table.heading(col, text=col.capitalize(), anchor="w")
                self.table.column(col, width=150, anchor="w")

        # Get menu and VIP menu IDs to filter stock
        menu_and_vip_ids = self.controller.get_menu_and_vip_menu_ids()

        # Fetch filtered stock data
        total, details, current_page, total_pages = self.controller.stockModel.view_total_stock_page(
            self.stock_page, self.stock_page_size, self.stock_filter, filter_ids=menu_and_vip_ids)
        
        stock_data = []
        for line in details.split("\n"):
            if ":" in line:
                bev, amt = line.rsplit(":", 1)
                bev_id = bev.strip().split(" (nr: ")[1].rstrip(")")
                bev_name = bev.split(" (nr: ")[0].strip()
                stock_data.append({"id": bev_id, "beer": bev_name, "amount": int(amt.strip())})

        for item in stock_data:
            action_text = "Increase | Reduce"
            self.table.insert("", "end", values=(item["id"], item["beer"], item["amount"], action_text))

        self.table.bind("<Button-1>", self.on_stock_action_click)

        # Add filter and pagination controls 
        control_frame = tk.Frame(self.table_frame, bg="white")
        control_frame.pack(pady=5)

        self.filter_label = tk.Label(control_frame, text="Filter by ID or name:", font=self.custom_font, bg="white")
        self.filter_label.grid(row=0, column=0, padx=5)
        self.filter_entry = tk.Entry(control_frame)
        self.filter_entry.grid(row=0, column=1, padx=5)
        self.filter_btn = tk.Button(control_frame, text="Filter", **self.button_style, command=lambda: self.apply_stock_filter(self.filter_entry.get()))
        self.filter_btn.grid(row=0, column=2, padx=5)

        self.prev_btn = tk.Button(control_frame, text="Previous", **self.button_style, command=self.prev_stock_page)
        self.prev_btn.grid(row=0, column=3, padx=5)
        self.next_btn = tk.Button(control_frame, text="Next", **self.button_style, command=self.next_stock_page)
        self.next_btn.grid(row=0, column=4, padx=5)


    def prev_stock_page(self):
        if self.stock_page > 1:
            self.stock_page -= 1
            self.load_page("stock")

    def next_stock_page(self):
        self.stock_page += 1
        self.load_page("stock")

    def apply_stock_filter(self, filter_text):
        self.stock_filter = filter_text
        self.stock_page = 1
        self.load_page("stock")

    def load_reservations(self):
        # Use a single "action" column.
        columns = ("table", "people", "time", "status", "action")
        self.table["columns"] = columns
        for col in columns:
            if col == "action":
                self.table.heading(col, text=col.capitalize(), anchor="center")
                self.table.column(col, width=200, anchor="center")
            else:
                self.table.heading(col, text=col.capitalize(), anchor="w")
                self.table.column(col, width=150 if col in ("table", "people", "time", "status") else 100, anchor="w")

        # Populate with reservation data
        reservations = self.controller.get_reservations()  # List of Reservation objects
        for res_index, res in enumerate(reservations):
            iid = f"res_{res_index}"
            action_text = "Complete | Cancel"
            self.table.insert("", "end", iid=iid, values=(res.table_number, res.people, res.time, res.status, action_text))

        # Bind click event for actions
        self.table.bind("<Button-1>", self.on_reservation_action_click)

        # Add reservation creation frame
        add_frame = tk.Frame(self.table_frame, bg="white")
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Add Reservation", font=self.custom_font, bg="white").pack(pady=5)

        # Table number input
        tk.Label(add_frame, text="Table Number:", bg="white").pack(side="left", padx=5)
        self.table_number_entry = tk.Entry(add_frame, width=10)
        self.table_number_entry.pack(side="left", padx=5)

        # Number of people
        tk.Label(add_frame, text="People:", bg="white").pack(side="left", padx=5)
        self.people_var = tk.IntVar(value=1)
        people_frame = tk.Frame(add_frame, bg="white")
        people_frame.pack(side="left", padx=5)
        tk.Button(people_frame, text="-", command=lambda: self.adjust_people(-1), width=2).pack(side="left")
        tk.Label(people_frame, textvariable=self.people_var, width=3, bg="white").pack(side="left")
        tk.Button(people_frame, text="+", command=lambda: self.adjust_people(1), width=2).pack(side="left")

        # Reservation time
        tk.Label(add_frame, text="Time:", bg="white").pack(side="left", padx=5)
        self.time_var = tk.StringVar(value="12:00")
        time_frame = tk.Frame(add_frame, bg="white")
        time_frame.pack(side="left", padx=5)
        tk.Button(time_frame, text="-30m", command=lambda: self.adjust_time(-30), width=5).pack(side="left")
        tk.Entry(time_frame, textvariable=self.time_var, width=10).pack(side="left")
        tk.Button(time_frame, text="+30m", command=lambda: self.adjust_time(30), width=5).pack(side="left")

        # Add button
        add_btn = tk.Button(add_frame, text="Add", command=self.add_reservation)
        add_btn.pack(side="left", padx=10)


    def on_reservation_action_click(self, event):
        selected_item = self.table.identify_row(event.y)
        selected_column = self.table.identify_column(event.x)
        if selected_item and selected_column:
            column_index = int(selected_column[1:]) - 1  
            column_name = self.table["columns"][column_index]
            if column_name == "action":
                bbox = self.table.bbox(selected_item, selected_column)
                if bbox:
                    cell_x, cell_y, cell_width, cell_height = bbox
                    x_offset = event.x - cell_x
                    if x_offset < cell_width / 2:
                        action = "action1"  # Left half → Complete
                    else:
                        action = "action2"  # Right half → Cancel
                    
                    res_index = int(selected_item.split("_")[1])
                    self.reservation_action(action, res_index)


    def add_reservation(self):
        table_number = self.table_number_entry.get()
        people = self.people_var.get()
        time = self.time_var.get()
        if not table_number or not time:
            mbox.showerror("Error", "Table number and time are required.")
            return
        try:
            self.controller.add_reservation(table_number, people, time)
            self.load_page("reservation")  # Refresh the page
            mbox.showinfo("Success", "Reservation added.")
        except Exception as e:
            mbox.showerror("Error", f"Failed to add reservation: {str(e)}")

    def adjust_people(self, delta):
        # Adjust the number of people for the new reservation.
        current = self.people_var.get()
        new_value = max(1, current + delta)  # Ensure at least 1 person
        self.people_var.set(new_value)

    def adjust_time(self, minutes):
        from datetime import datetime, timedelta
        try:
            current_time = datetime.strptime(self.time_var.get(), "%H:%M")
            new_time = current_time + timedelta(minutes=minutes)
            self.time_var.set(new_time.strftime("%H:%M"))
        except ValueError:
            mbox.showerror("Error", "Invalid time format. Use HH:MM.")

    def load_menu(self):
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

        # menu below the table
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
        
        selected_item = self.table.identify_row(event.y)  # get the position in row 
        selected_column = self.table.identify_column(event.x)  # get the position in col（the formatis #1, #2, #3 ...）

        if selected_item and selected_column == "#3":
            #item_values = self.table.item(selected_item, "values")  
            #id = item_values[0] 
            #name = item_values[1]
            index = self.table.index(selected_item)
            self.controller.removeItemFromMenu(index)
            self.load_page("menu")
            #print(f"id:{id}, name:{name}")
    
    def on_VIP_Menu_Remove_click(self,event):
        selected_item = self.table.identify_row(event.y)  # get the position in row 
        selected_column = self.table.identify_column(event.x)  # get the position in col（the formatis #1, #2, #3 ...）

        if selected_item and selected_column == "#3":
            #item_values = self.table.item(selected_item, "values")
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
                            bg="green" if action == "action1" else "#ADD8E6",
                            fg="white", command=lambda a=action, i=iid: callback(a, i))
            btn.pack(side="left", padx=2)
        # Set the last column's value to the action_frame widget
        self.table.set(iid, column=len(values)-1, value=action_frame)
        self.table.item(iid, values=values)

    def order_action(self, action, order_index, item_index):
        orders = self.controller.orderModel.staticData
        if 0 <= order_index < len(orders):
            order = orders[order_index]
            if 0 <= item_index < len(order.orderItems):
                item = order.orderItems[item_index]
                if action == "action1":  # "Complete" button
                    beverage_id = str(item.id)
                    # Get current stock for this item
                    current_stock = self.controller.stockModel.get_stock(beverage_id)
                    # Check if there’s enough stock
                    if current_stock >= item.amount:
                        # Deduct stock
                        new_stock = current_stock - item.amount
                        self.controller.stockModel.update_stock(beverage_id, new_stock)
                        print(f"Stock updated for {beverage_id}: {new_stock}")
                        # Remove the completed item from the order
                        del order.orderItems[item_index]
                        # If the order has no more items, remove the entire order
                        if not order.orderItems:
                            del orders[order_index]
                    else:
                        # Show error if stock is insufficient
                        beer_data = self.controller.beerModel.getDataById(beverage_id)
                        beer_name = beer_data.namn if beer_data else "Unknown"
                        import tkinter.messagebox as mbox
                        mbox.showerror("Error", f"Insufficient stock for {beer_name}. Available: {current_stock}, Required: {item.amount}")
                elif action == "action2":  # "Cancel" button
                    # Remove item without affecting stock
                    del order.orderItems[item_index]
                    if not order.orderItems:
                        del orders[order_index]
                # Save changes and refresh the page
                self.controller.orderModel.saveData()
                self.load_page("order")


    def on_stock_action_click(self, event):
        selected_item = self.table.identify_row(event.y)
        selected_column = self.table.identify_column(event.x)
        if selected_item and selected_column:
            column_index = int(selected_column[1:]) - 1  # e.g., '#1' -> 0, '#2' -> 1, etc.
            column_name = self.table["columns"][column_index]
            if column_name == "action":
                bbox = self.table.bbox(selected_item, selected_column)
                if bbox:
                    cell_x, cell_y, cell_width, cell_height = bbox
                    x_offset = event.x - cell_x
                    if x_offset < cell_width / 2:
                        action = "action1"  # Left half → Increase
                    else:
                        action = "action2"  # Right half → Reduce
                    bev_id = self.table.item(selected_item, "values")[0]
                    self.stock_action(action, bev_id)


    def stock_action(self, action, bev_id):
        current_amount = self.controller.stockModel.get_stock(bev_id)
        if action == "action1":
            new_amount = current_amount + 1
            self.controller.updateStockData(bev_id, new_amount)
        elif action == "action2":
            if current_amount > 0:
                new_amount = current_amount - 1
                self.controller.updateStockData(bev_id, new_amount)
                if new_amount == 0:
                    self.controller.stockModel.remove_beverage_by_id(bev_id)
        self.load_page("stock")  # Refresh the page

    def reservation_action(self, action, res_index):
        if action == "action1":
            self.controller.complete_reservation(res_index)
        elif action == "action2":
            self.controller.cancel_reservation(res_index)
        self.load_page("reservation")  # Refresh the page

    def menu_action(self, action, iid):
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