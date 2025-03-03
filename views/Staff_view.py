import tkinter as tk
from tkinter import ttk
from functools import partial
from styles.style_config import *  # Assuming this provides fonts and styles
import tkinter.simpledialog as sd
import tkinter.messagebox as mbox

# Assuming MenuItem is defined somewhere accessible
class MenuItem:
    def __init__(self, nr, namn):
        self.nr = nr
        self.namn = namn

class StaffView(tk.Frame):
    def __init__(self, root, controller):  # Changed 'parent' to 'root'
        super().__init__(root)  # Updated parameter name
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

    def setup_ui(self):
        """Set up the UI with grid layout."""
        # Title
        title_label = tk.Label(self, text="Staff Panel", font=("Georgia", 24, "bold"), bg="#A7C7E7", fg="#000435")
        title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Navigation buttons
        nav_frame = tk.Frame(self, bg="#A7C7E7")
        nav_frame.grid(row=1, column=0, columnspan=4, pady=10)

        self.buttons = {}
        for idx, page in enumerate(["order", "stock", "reservation", "menu"]):
            btn = tk.Button(nav_frame, text=page.capitalize(), **self.button_style,
                            command=partial(self.switch_page, page))
            btn.grid(row=0, column=idx, padx=10)
            self.buttons[page] = btn

        # Table frame with fixed size (70% of previous size)
        self.table_frame = tk.Frame(self, bg="white", bd=2, relief="solid", width=392, height=280)
        self.table_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_propagate(False)  # Prevent auto-resizing

        # Highlight default button
        self.highlight_button(self.current_page)

        # Configure grid weights for responsiveness
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def switch_page(self, page):
        """Switch the current page and update the table."""
        self.current_page = page
        self.stock_page = 1  # Reset stock page on switch
        self.stock_filter = ""  # Reset filter
        self.highlight_button(page)
        self.load_page(page)

    def highlight_button(self, page):
        """Highlight the active button with yellow, others with button_style."""
        for btn_page, btn in self.buttons.items():
            if btn_page == page:
                btn.config(bg="#FFC107")  # Yellow for active
            else:
                btn.config(**self.button_style)  # Default style for inactive

    def load_page(self, page):
        """Clear and repopulate the table based on the selected page."""
        # Clear table_frame completely to prevent layout shifts
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Create a new treeview for the table
        self.table = ttk.Treeview(self.table_frame, style="Custom.Treeview")
        self.table.pack(fill="both", expand=True)

        # Reset columns and heading for treeview
        self.table["columns"] = ()
        self.table.heading("#0", text="", anchor="w")

        if page == "order":
            self.load_orders()
        elif page == "stock":
            self.load_stock()
        elif page == "reservation":
            self.load_reservations()
        elif page == "menu":
            self.load_menu()

    def load_orders(self):
        """Populate table with order data."""
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
            self.add_action_buttons(iid, ["complete", "cancel"], self.order_action)

    def load_stock(self):
        """Populate table with stock data, using pagination and filtering."""
        columns = ("id", "beer", "amount", "action")
        self.table["columns"] = columns
        for col in columns:
            self.table.heading(col, text=col.capitalize(), anchor="w")
            self.table.column(col, width=150, anchor="w")

        # Fetch paginated stock data
        total, details, current_page, total_pages = self.controller.stockModel.view_total_stock_page(
            self.stock_page, self.stock_page_size, self.stock_filter)
        stock_data = []
        for line in details.split("\n"):
            if ":" in line:
                bev, amt = line.split(":")
                bev_id = bev.strip().replace("Beverage ", "").split(" (nr: ")[1].rstrip(")")
                bev_name = bev.split(" (nr: ")[0].replace("Beverage ", "").strip()
                stock_data.append({"id": bev_id, "beer": bev_name, "amount": int(amt.strip())})

        for item in stock_data:
            self.table.insert("", "end", values=(item["id"], item["beer"], item["amount"], ""), tags=("action_row",))

        for iid in self.table.get_children():
            self.add_action_buttons(iid, ["edit"], self.stock_action)

        # Add filter and pagination controls using grid inside a control frame
        control_frame = tk.Frame(self.table_frame, bg="white")
        control_frame.pack(pady=5)

        # Filter controls
        filter_label = tk.Label(control_frame, text="Filter by ID or name:", font=self.custom_font, bg="white")
        filter_label.grid(row=0, column=0, padx=5)
        filter_entry = tk.Entry(control_frame)
        filter_entry.grid(row=0, column=1, padx=5)
        filter_btn = tk.Button(control_frame, text="Filter", **self.button_style, command=lambda: self.apply_stock_filter(filter_entry.get()))
        filter_btn.grid(row=0, column=2, padx=5)

        # Pagination buttons
        prev_btn = tk.Button(control_frame, text="Previous", **self.button_style, command=self.prev_stock_page)
        prev_btn.grid(row=0, column=3, padx=5)
        next_btn = tk.Button(control_frame, text="Next", **self.button_style, command=self.next_stock_page)
        next_btn.grid(row=0, column=4, padx=5)

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

        # Placeholder data (no reservation model provided)
        reservations = [{"id": "1", "table_number": "3", "time": "18:00", "status": "Pending"}]
        for res in reservations:
            self.table.insert("", "end", text=res["id"], values=(res["table_number"], res["time"], res["status"], ""), tags=("action_row",))

        for iid in self.table.get_children():
            self.add_action_buttons(iid, ["confirm", "cancel"], self.reservation_action)

    def load_menu(self):
        """Populate table with menu data from dutchman_menu.json."""
        columns = ("id", "name", "action")
        self.table["columns"] = columns
        for col in columns:
            self.table.heading(col, text=col.capitalize(), anchor="w")
            self.table.column(col, width=150, anchor="w")

        menu_data = self.controller.getBeerDataFromMenu()
        for item in menu_data:
            self.table.insert("", "end", values=(item.nr, item.namn, ""), tags=("action_row",))

        for iid in self.table.get_children():
            self.add_action_buttons(iid, ["remove"], self.menu_action)

        # Add "ADD" button below the table
        add_btn = tk.Button(self.table_frame, text="ADD", **self.button_style, command=self.add_menu_item)
        add_btn.pack(pady=5)

    def add_menu_item(self):
        """Add a new item to the menu with a combo box selection."""
        dialog = tk.Toplevel(self)
        dialog.title("Add Menu Item")
        
        # Fetch all available beers from the beer model
        beers = self.controller.beerModel.staticData
        values = [f"{beer.nr}, {beer.namn}" for beer in beers]
        
        # Combo box setup
        tk.Label(dialog, text="Select Beer:").pack(padx=10, pady=5)
        combo = ttk.Combobox(dialog, values=values, width=50)
        combo.pack(padx=10, pady=5)
        
        def on_add():
            selected = combo.get()
            if selected:
                nr, namn = selected.split(", ", 1)
                menu_item = MenuItem(nr.strip(), namn.strip())
                self.controller.addItemToMenu(menu_item)
                self.load_page("menu")
                dialog.destroy()
                mbox.showinfo("Menu Update", f"Added {namn.strip()} to menu.")
            else:
                mbox.showerror("Error", "Please select a beer.")
        
        tk.Button(dialog, text="Add", command=on_add).pack(pady=10)

    def add_action_buttons(self, iid, actions, callback):
        """Add action buttons to a table row."""
        values = list(self.table.item(iid, "values"))
        action_frame = tk.Frame(self.table)
        for action in actions:
            btn = tk.Button(action_frame, text=action.capitalize(),
                            bg="green" if action == "complete" else "#ADD8E6",
                            fg="white", command=lambda a=action, i=iid: callback(a, i))
            btn.pack(side="left", padx=2)
        # Here we set the last column's value to the action_frame widget.
        self.table.set(iid, column=len(values)-1, value=action_frame)
        self.table.item(iid, values=values)

    def order_action(self, action, iid):
        """Handle order actions."""
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
        """Handle stock actions."""
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
