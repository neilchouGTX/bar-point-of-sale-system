from tkinter import *
from tkinter import ttk
from styles.style_config import *
from tkinter import messagebox
import json
from Controller_translations import languages

class ReservationView(Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        self.reservations = []
        
        self.display()
    
         #初始化語言 /initialize language
        self.languages = languages
        self.current_language = self.controller.current_language


    def display(self):
        self.title = tk.Label(self, text="Reservations", font=("Georgia", 24, "bold"), bg="#A7C7E7", fg="#000435")
        self.title.pack(pady=20)

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

        self.add_rsv_btn = Button(btn_frame, text="Add Reservation", **self.button_style, width=10, command=self.reservation_form)
        self.add_rsv_btn.grid(row=0, column=0, padx=10, pady=10)

        self.cancel_rsv_btn = Button(btn_frame, text="Cancel Reservation", **self.button_style, width=10, command=self.cancel_reservation)
        self.cancel_rsv_btn.grid(row=0, column=1, padx=10, pady=10)

    def reservation_form(self):
        rsv_window = Toplevel(self)
        rsv_window.title("New Reservation")
        rsv_window.geometry("375x250")

        # Name entry
        name_label = Label(rsv_window, text="Name:", font=self.custom_font)
        name_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        name_entry = Entry(rsv_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Table entry
        table_label = Label(rsv_window, text="Table:", font=self.custom_font)
        table_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        table_entry = Entry(rsv_window)
        table_entry.grid(row=1, column=1, padx=10, pady=10)

        # Date Entry
        date_label = Label(rsv_window, text="Date (DD-MM-YYYY):", font=self.custom_font)
        date_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        date_entry = Entry(rsv_window)
        date_entry.grid(row=2, column=1, padx=10, pady=10)

        # Time Entry
        time_label = Label(rsv_window, text="Time (HH:MM):", font=self.custom_font)
        time_label.grid(row=3, column=0, sticky="e", padx=10, pady=10)
        time_entry = Entry(rsv_window)
        time_entry.grid(row=3, column=1, padx=10, pady=10)

        # Submit button
        submit_btn = Button(rsv_window, text="Submit", **self.button_style, command=lambda: self.add_reservation(name_entry, table_entry, date_entry, time_entry, rsv_window))
        submit_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_reservation(self, name_entry, table_entry, date_entry, time_entry, rsv_window):
        name = name_entry.get()
        table = table_entry.get()
        date = date_entry.get()
        time = time_entry.get()

        self.tree.insert('', 'end', values=(name, table, date, time))

        # Closing form after submit button is pressed
        rsv_window.destroy()

    def cancel_reservation(self):
        rsv_selection = self.tree.selection()

        if not rsv_selection:
            messagebox.showerror("Error", "No reservation selected")
            return

        result = tk.messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this reservation?")
        if result:
            self.tree.delete(rsv_selection)
    
    def update_language(self, lang_code):
        """
        更新 ReservationView 的語言，僅更新標題和按鈕文字。
        Update the language of the ReservationView, focusing only on the title and buttons.
        """
        # 取得當前語言的字典 / Get the current language dictionary
        ldict = self.controller.languages[lang_code]



        # 更新標題文字 / Update the title label
        self.title.config(text=ldict['reservation_page'])

        # 更新按鈕文字 / Update button texts
        self.add_rsv_btn.config(text=ldict['add_reservation'])
        self.cancel_rsv_btn.config(text=ldict['cancel_reservation'])