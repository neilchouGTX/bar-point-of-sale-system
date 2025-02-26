from tkinter import *
from tkinter import ttk
from styles.style_config import *

class ReservationView(Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.configure(bg="#A7C7E7")
        self.custom_font = get_custom_font(self)
        self.button_style = get_button_style(self)
        self.display()

    def display(self):
        title = tk.Label(self, text="Reservations", font=("Georgia", 24, "bold"), bg="#A7C7E7", fg="#000435")
        title.pack(pady=20)