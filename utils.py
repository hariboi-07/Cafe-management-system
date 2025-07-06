# utils.py
import tkinter as tk

def clear_entries(menu_items, total_var):
    """Clear all input fields and reset total."""
    for _, (_, entry) in menu_items.items():
        entry.delete(0, tk.END)
    total_var.set("0")
