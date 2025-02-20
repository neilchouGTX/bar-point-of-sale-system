import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Modern Combobox Example")

# 用來存放選擇的值
selected_var = tk.StringVar()

# 建立 Combobox，設定可選值
combo = ttk.Combobox(root, textvariable=selected_var, values=["English", "Svenska", "中文"])
combo.pack(padx=20, pady=20)

# 預設選取哪個選項 (索引從 0 開始)
combo.current(0)

root.mainloop()
