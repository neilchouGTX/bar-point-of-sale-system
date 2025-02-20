import tkinter as tk
from tkinter import font

#this file is for storing the styles of the buttons and fonts

def get_custom_font(root):
    return font.Font(root=root, family="Helvetica", size=12, weight="bold")

def get_button_style(root):
    custom_font = get_custom_font(root)
    return {
        "padx": 15,
        "pady": 5,
        "bd": 0,
        "fg": "white",
        "bg": "#38042c",
        "activebackground": "#26031e",
        "activeforeground": "white",
        "font": custom_font,
        "relief": "flat"
    }

def get_button_style2(root):
    custom_font = get_custom_font(root)
    return {
        "padx": 15,
        "pady": 5,
        "bd": 0,
        "fg": "white",
        "bg": "#520a07",
        "activebackground": "#400705",
        "activeforeground": "white",
        "font": custom_font,
        "relief": "flat"
    }