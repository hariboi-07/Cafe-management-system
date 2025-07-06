# database.py
import mysql.connector
from tkinter import messagebox

def connect_to_database():
    """Connect to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1410",
            database="cafe_db"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
        exit()

def setup_database(cursor):
    """Set up the MySQL database tables."""
    cursor.execute("CREATE DATABASE IF NOT EXISTS cafe_db")
    cursor.execute("USE cafe_db")

    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
                        item_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) UNIQUE NOT NULL,
                        price FLOAT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        trans_id INT AUTO_INCREMENT PRIMARY KEY,
                        total FLOAT NOT NULL,
                        timestamp DATETIME NOT NULL)''')

    default_items = [("Tea", 10), ("Coffee", 20), ("Sandwich", 50),
                     ("Cake", 100), ("Burger", 50), ("Pizza", 150),
                     ("Fries", 80), ("Pepsi", 80)]
    cursor.executemany('''INSERT IGNORE INTO menu (name, price) VALUES (%s, %s)''', default_items)
