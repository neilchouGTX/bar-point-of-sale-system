from tkinter import *
from tkinter import ttk
from styles.style_config import *
from datetime import datetime

class ReservationView(Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        self.reservations = []
        self.display()

    def display(self):
        title = tk.Label(self, text="Reservations", font=("Georgia", 24, "bold"), bg="#A7C7E7", fg="#000435")
        title.pack(pady=20)

        # Table UI
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.custom_font)

        # Reservations Table
        self.tree = ttk.Treeview(self, columns=("Name", "Table", "Date", "Time"))
        self.tree.heading("Name", text="Name")
        self.tree.heading("Table", text="Table")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")

        self.tree["show"] = "headings"
        self.tree.pack(pady=20)

        # Reservation functions
        btn_frame = Frame(self, bg="#A7C7E7")
        btn_frame.pack(pady=20)

        add_rsv_btn = Button(btn_frame, text="Add Reservation", **self.button_style, width=10, command=self.reservation_form)
        add_rsv_btn.grid(row=0, column=0, padx=10, pady=10)

        cancel_rsv_btn = Button(btn_frame, text="Cancel Reservation", **self.button_style, width=10)
        cancel_rsv_btn.grid(row=0, column=1, padx=10, pady=10)

    def reservation_form(self):
        rsv_window = Toplevel(self)
        rsv_window.title("New Reservation")
        rsv_window.geometry("300x300")

        # Name entry
        Label(rsv_window, text="Name:", font=self.custom_font).pack()
        name_entry = Entry(rsv_window)
        name_entry.pack()

        # Table entry
        Label(rsv_window, text="Table:", font=self.custom_font).pack()
        table_entry = Entry(rsv_window)
        table_entry.pack()

        # Date Entry
        Label(rsv_window, text="Date (DD-MM-YYYY):", font=self.custom_font).pack()
        date_entry = Entry(rsv_window)
        date_entry.pack()

        # Time Entry
        Label(rsv_window, text="Time (HH:MM):", font=self.custom_font).pack()
        time_entry = Entry(rsv_window)
        time_entry.pack()

        # Submit button
        submit_btn = Button(rsv_window, text="Submit", **self.button_style, command=lambda: self.add_reservation(name_entry, table_entry, date_entry, time_entry, rsv_window))
        submit_btn.pack()

    def add_reservation(self, name_entry, table_entry, date_entry, time_entry, rsv_window):
        name = name_entry.get()
        table = table_entry.get()
        date = date_entry.get()
        time = time_entry.get()

        self.tree.insert('', 'end', values=(name, table, date, time))

        # Closing form after submit button is pressed
        rsv_window.destroy()