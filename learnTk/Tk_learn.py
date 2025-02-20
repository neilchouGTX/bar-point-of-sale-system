import tkinter as tk
from tkinter import ttk
window = tk.Tk()
greeting = tk.Label(text="Hello, Tkinter",
                    foreground="white",  # Set the text color to white
                    background="black",   # Set the background color to black
                    width=10,
                    height=10 
                    )
button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)
greeting.pack()
button.pack()

label = tk.Label(text="Name")
entry = tk.Entry()
label.pack()
entry.pack()
#name = entry.get()
#print(name)

text_box = tk.Text()
text_box.insert(tk.END, "\nPut me on a new line!")
text_box.pack()

ttk_button = ttk.Button(text="Styled Button")
ttk_button.pack()

def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)

# Bind keypress event to handle_keypress()
window.bind("<Key>", handle_keypress)
window.mainloop()