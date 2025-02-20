import tkinter as tk

def on_button_click():
    label.config(text="Button Clicked!")

# Create the main window
root = tk.Tk()
root.title("Tkinter Frames Example")

# Create a frame
frame = tk.Frame(root, padx=20, pady=20,bg="red",width=300,height=300)  
frame.grid(row=2,column=0,padx=10, pady=10,sticky="nwes",) 

# Create widgets inside the frame
label = tk.Label(frame, text="Hello, Tkinter!")
label.grid(row=0,column=0)
#label.pack()


# 創建三個 Label
label1 = tk.Label(root, text="Label 1", bg="lightblue")
label2 = tk.Label(root, text="Label 2", bg="lightgreen")
label3 = tk.Label(root, text="Label 3", bg="lightcoral")

# 放入 grid 佈局
label1.grid(row=0, column=0, sticky="nsew")
label2.grid(row=0, column=1, sticky="nsew")
label3.grid(row=1, column=0, columnspan=2, sticky="nsew")

# 讓 Grid 隨視窗縮放
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)  # 權重 2 表示比 row=0 佔更多空間
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
"""
button = tk.Button(frame, text="Click me!", command=on_button_click)
button.pack(side="left")

# Create another frame
frame2 = tk.Frame(root, bg="lightblue",padx=10,pady=10)
frame2.pack()

label2 = tk.Label(frame2, text="This is another frame.")
label2.pack()
"""
# Run the Tkinter event loop
root.mainloop()