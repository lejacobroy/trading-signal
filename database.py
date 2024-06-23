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
            stock_id INTEGER,
            indicator TEXT NOT NULL,
            threshold REAL NOT NULL
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
    rows = cursor.fetchall()
    stocks = []
    for row in rows:
        stocks.append({
            "id": row[0],
            "symbol": row[1]
        })
    conn.close()
    return stocks

def add_stock(symbol):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stock (symbol) VALUES (?)", (symbol,))
    conn.commit()
    conn.close()
    
def get_stock(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock where id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    stock = {
            "id": row[0],
            "symbol": row[1]
        }
    return stock

def del_stock(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alert where stock_id = ? and stock_id IS NOT NULL", (id,))
    cursor.execute("DELETE FROM stock where id = ?", (id,))
    conn.close()
    return True

def get_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alert")
    rows = cursor.fetchall()
    alerts = []
    for row in rows:
        alerts.append({
            "id": row[0],
            "stock_id": row[1],
            "indicator": row[2],
            "threshold": row[3]
        })
    conn.close()
    return alerts

def get_alert(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alert where id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    alert = {
            "id": row[0],
            "stock_id": row[1],
            "indicator": row[2],
            "threshold": row[3]
        }
    return alert

def add_alert(stock_id, indicator, threshold):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO alert (stock_id, indicator, threshold) VALUES (?, ?, ?)",
        (stock_id, indicator, threshold),
    )
    conn.commit()
    conn.close()
    
def del_alert(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alert where id = ?", (id,))
    conn.close()
    return True