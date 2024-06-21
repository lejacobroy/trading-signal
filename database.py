import sqlite3
import os

DATABASE_PATH = os.path.join(os.getcwd(), "database.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alert (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER NOT NULL,
            indicator TEXT NOT NULL,
            threshold REAL NOT NULL,
            FOREIGN KEY (stock_id) REFERENCES stock (id)
        )
    ''')
    conn.commit()
    conn.close()

def to_dict(row):
    return dict(row)

def get_stocks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock")
    stocks = cursor.fetchall()
    conn.close()
    return to_dict(stocks)

def add_stock(symbol):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stock (symbol) VALUES (?)", (symbol,))
    conn.commit()
    conn.close()

def add_alert(stock_id, indicator, threshold):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO alert (stock_id, indicator, threshold) VALUES (?, ?, ?)",
        (stock_id, indicator, threshold),
    )
    conn.commit()
    conn.close()