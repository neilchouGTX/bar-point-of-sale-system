import tkinter as tk
from tkinter import font

#this file is for storing the styles of the buttons and fonts

def get_custom_font(root):
    return font.Font(root=root, family="Georgia", size=12, weight="bold")

def get_custom_font_bigger(root):
    return font.Font(root=root, family="Georgia", size=18, weight="bold")

def get_button_style(root):
    custom_font = get_custom_font(root)
    return {
        "padx": 15,
        "pady": 7,
        "bd": 0,
        "fg": "black",
        "bg": "white",
        "activebackground": "gray",
        "activeforeground": "black",
        "font": custom_font,
        "relief": "flat"
    }

def get_button_style2(root):
    custom_font = get_custom_font(root)
    return {
        "padx": 15,
        "pady": 5,
        "bd": 0,
        "fg": "black",
        "bg": "#520a07",
        "activebackground": "#400705",
        "activeforeground": "gray",
        "font": custom_font,
        "relief": "flat"
    }

def get_send_order_button_style(root):
    custom_font = get_custom_font_bigger(root)
    return {
        "padx": 20,
        "pady": 10,
        "bd": 0,
        "fg": "black",
        "bg": "white",
        "activebackground": "white",
        "activeforeground": "black",
        "font": custom_font,
        "relief": "flat"
    }