import json
import tkinter as tk
from tkinter import messagebox

# Model - JSON data handling
class Model:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"items": []}

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def add_item(self, item):
        self.data["items"].append(item)
        self.save_data()

    def get_items(self):
        return self.data["items"]

# Base View - For managing multiple pages
class BaseView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.frames = {}

        # 初始化 Frame 頁面
        for F in (HomePage, InputPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self.controller)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """顯示指定頁面"""
        frame = self.frames[page_name]
        frame.tkraise()

# Home Page - View
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Home Page", font=("Arial", 16))
        label.pack(pady=10)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(pady=10)
        self.refresh_list()

        button_go_to_input = tk.Button(self, text="Go to Input Page", command=lambda: controller.show_frame("InputPage"))
        button_go_to_input.pack()

    def refresh_list(self):
        """更新列表內容"""
        self.listbox.delete(0, tk.END)
        for item in self.controller.get_items():
            self.listbox.insert(tk.END, item)

# Input Page - View
class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Input Page", font=("Arial", 16))
        label.pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=10)

        self.add_button = tk.Button(self, text="Add Item", command=self.add_item)
        self.add_button.pack()

        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"))
        self.back_button.pack()

    def add_item(self):
        """添加數據到 Model 並返回首頁"""
        item = self.entry.get()
        if item:
            self.controller.add_item(item)
            self.entry.delete(0, tk.END)
            self.controller.frames["HomePage"].refresh_list()
            self.controller.show_frame("HomePage")
        else:
            messagebox.showwarning("Warning", "Input cannot be empty!")

# Controller - Handles interactions and manages views
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = BaseView(self)

    def show_frame(self, page_name):
        """切換頁面"""
        self.view.show_frame(page_name)

    def add_item(self, item):
        """將數據添加到 Model"""
        self.model.add_item(item)

    def get_items(self):
        """取得 Model 數據"""
        return self.model.get_items()

# Main Application
if __name__ == "__main__":
    controller = Controller()
    controller.view.mainloop()

print("MVCtest")
print("11232313133")
