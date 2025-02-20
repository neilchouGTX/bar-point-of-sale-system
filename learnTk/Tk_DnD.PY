import tkinter as tk

class DraggableButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        x = self.winfo_x() + (event.x - self.start_x)
        y = self.winfo_y() + (event.y - self.start_y)
        self.place(x=x, y=y)

# build main window
root = tk.Tk()
root.geometry("400x300")
root.title("Tkinter Drag and Drop Button")

# build button
btn = DraggableButton(root, text="Drag Me", bg="lightblue")
btn.place(x=50, y=50)

root.mainloop()