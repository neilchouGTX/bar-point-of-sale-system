import tkinter as tk
import os
from tkinter import PhotoImage
class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 創建 Canvas
        self.canvas = tk.Canvas(self,height=200,width=150)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # 配置 Canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 佈局
        self.canvas.pack(side="left",)
        self.scrollbar.pack(side="left", fill="y")

root = tk.Tk()
root.geometry("400x300") 
root.title("可滾動 Frame")

scroll_frame = ScrollableFrame(root)
scroll_frame.pack(fill="both", expand=True)

folder_path = os.getcwd()  
images_path=os.path.join(folder_path, "images")
image = PhotoImage(file=os.path.join(images_path,"shopping-cart.png"))
image=image.subsample(10,10)
# 在可滾動的 Frame 內添加內容
for y in range(30):
    for x in range(5): 
    
        text=tk.Text(scroll_frame.scrollable_frame, height=5,width=10)
        text.image_create(tk.END, image=image)
        text.insert(tk.END, f"  圖片 {y}\n")
        text.grid(row=y,column=x)

root.mainloop()