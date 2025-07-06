# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import connect_to_database, setup_database
from utils import clear_entries

class CafeManagement:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Cafe Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#F5F5F5")

        self.conn = connect_to_database()
        self.cursor = self.conn.cursor()
        setup_database(self.cursor)
        self.conn.commit()

        self.menu_items = {}
        self.total_cost = tk.StringVar(value="0")

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        tk.Label(self.root, text="Cafe Management System",
                 font=("Arial", 24, "bold"), bg="#F5F5F5", fg="#2E8B57").pack(pady=10)

        datetime_label = tk.Label(self.root,
            text=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Arial", 14), bg="#F5F5F5", fg="#2E8B57")
        datetime_label.pack()

        menu_frame = ttk.LabelFrame(self.root, text="Menu", padding=(20, 10))
        menu_frame.pack(side=tk.LEFT, padx=20, pady=20)

        billing_frame = ttk.LabelFrame(self.root, text="Billing", padding=(20, 10))
        billing_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        self.load_menu(menu_frame)
        self.create_billing_ui(billing_frame)

        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(side=tk.BOTTOM, pady=10)

    def load_menu(self, parent):
        self.cursor.execute("SELECT name, price FROM menu")
        menu_items = self.cursor.fetchall()

        for idx, (name, price) in enumerate(menu_items):
            tk.Label(parent, text=f"{name} - ₹{price}", font=("Arial", 14)).grid(row=idx, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(parent, width=5)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.menu_items[name] = (price, entry)

    def create_billing_ui(self, frame):
        tk.Label(frame, text="Total:", font=("Arial", 16)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        total_entry = ttk.Entry(frame, textvariable=self.total_cost, font=("Arial", 16), state="readonly")
        total_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Calculate Total", command=self.calculate_total).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Complete Payment", command=self.complete_payment).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Clear All", command=self.clear).grid(row=3, column=0, columnspan=2, pady=10)

    def calculate_total(self):
        total = 0
        for name, (price, entry) in self.menu_items.items():
            try:
                quantity = int(entry.get())
                total += price * quantity
            except ValueError:
                continue
        self.total_cost.set(f"{total:.2f}")

    def complete_payment(self):
        total = float(self.total_cost.get())
        if total == 0:
            messagebox.showwarning("Payment", "Please select items to calculate the total.")
            return

        timestamp = datetime.now()
        self.cursor.execute("INSERT INTO transactions (total, timestamp) VALUES (%s, %s)", (total, timestamp))
        self.conn.commit()

        messagebox.showinfo("Payment", f"Payment of ₹{total:.2f} completed successfully!")
        self.clear()

    def clear(self):
        clear_entries(self.menu_items, self.total_cost)

    def __del__(self):
        self.conn.close()
