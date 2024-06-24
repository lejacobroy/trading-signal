import sqlite3
import os
from models import Alert

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
            indicator_id INTEGER NOT NULL,
            period_id TEXT NOT NULL,
            interval_id TEXT NOT NULL,
            action TEXT NOT NULL,
            threshold REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS indicator (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            dispaly_name TEXT NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS period (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interval (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def seed_db():
    indicators = [
        {
            "name": "MACD",
            "display_name": "Moving Average Convergence Divergence",
            "type": "TREND"
        },
        {
            "name": "BB",
            "display_name": "Bollinger Bands",
            "type": "TREND"
        },
        {
            "name": "RSI",
            "display_name": "Relative Strength Index",
            "type": "TREND"
        },
        {
            "name": "SMA200",
            "display_name": "Simple Moving Average 200 periods",
            "type": "Price"
        },
        {
            "name": "SMA50",
            "display_name": "Simple Moving Average 50 periods",
            "type": "Price"
        },
        {
            "name": "MA_CROSS_9_21",
            "display_name": "MA Cross 9-21",
            "type": "CROSS"
        },
        {
            "name": "MA_CROSS_50_200",
            "display_name": "MA Cross 50-200",
            "type": "CROSS"
        },
        {
            "name": "PRICE",
            "display_name": "Price",
            "type": "Price"
        },
        {
            "name": "PRICE_CHANGE",
            "display_name": "Price change (%)",
            "type": "Price"
        }
    ]
    # accepted by yfinance: 1d, 5d, 1mo, 3mo, 6mo,
    # 1y, 2y, 5y, 10y, ytd, max
    periods = [{
        "name": "1d",
        "display_name": "1 Day"
    }, {
        "name": "5d",
        "display_name": "5 Days"
    }, {
        "name": "1mo",
        "display_name": "1 Month"
    }, {
        "name": "3mo",
        "display_name": "3 Months"
    }, {
        "name": "6mo",
        "display_name": "6 Months"
    }, {
        "name": "1y",
        "display_name": "1 Year"
    }, {
        "name": "2y",
        "display_name": "2 Years"
    }, {
        "name": "5y",
        "display_name": "5 Years"
    }, {
        "name": "10y",
        "display_name": "10 Years"
    }, {
        "name": "ytd",
        "display_name": "Year to Date"
    }, {
        "name": "max",
        "display_name": "Max"
    }]
    
    # accepted by yfinance: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h,
    # 1d, 5d, 1wk, 1mo, 3mo
    intervals = [{
        "name": "1m",
        "display_name": "1 Minute"
    }, {
        "name": "2m",
        "display_name": "2 Minutes"
    }, {
        "name": "5m",
        "display_name": "5 Minutes"
    }, {
        "name": "15m",
        "display_name": "15 Minutes"
    }, {
        "name": "30m",
        "display_name": "30 Minutes"
    },{
        "name": "60m",
        "display_name": "60 Minutes"
    }, {
        "name": "90m",
        "display_name": "90 Minutes"
    }, {
        "name": "1h",
        "display_name": "1 Hour"
    },{
        "name": "1d",
        "display_name": "1 Day"
    },{
        "name": "5d",
        "display_name": "5 Days"
    },{
        "name": "1wk",
        "display_name": "1 Week"
    },{
        "name": "1mo",
        "display_name": "1 Month"
    },{
        "name": "3mo",
        "display_name": "3 Months"
    }]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    for indicator in indicators:
        cursor.execute('''
            INSERT OR IGNORE INTO indicator (name, dispaly_name, type) VALUES (?, ?, ?)
        ''', (indicator["name"], indicator["display_name"], indicator["type"]))
    for period in periods:
        cursor.execute('''
            INSERT OR IGNORE INTO period (name, display_name) VALUES (?, ?)
        ''', (period["name"], period["display_name"]))
    for interval in intervals:
        cursor.execute('''
            INSERT OR IGNORE INTO interval (name, display_name) VALUES (?, ?)
        ''', (interval["name"], interval["display_name"]))
    conn.commit()
    conn.close()

def get_indicators():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM indicator")
    rows = cursor.fetchall()
    indicators = []
    for row in rows:
        indicators.append({
            "id": row[0],
            "name": row[1],
            "display_name": row[2],
            "type": row[3]
        })
    conn.close()
    return indicators

def get_indicator(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM indicator where id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    indicator = {
        "id": row[0],
        "name": row[1],
        "display_name": row[2],
        "type": row[3]
    }
    return indicator

def get_periods():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM period")
    rows = cursor.fetchall()
    periods = []
    for row in rows:
        periods.append({
            "id": row[0],
            "name": row[1],
            "display_name": row[2]
        })
    conn.close()
    return periods

def get_period(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM period where id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    period = {
            "id": row[0],
            "name": row[1],
            "display_name": row[2]
        }
    return period

def get_intervals():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interval")
    rows = cursor.fetchall()
    intervals = []
    for row in rows:
        intervals.append({
            "id": row[0],
            "name": row[1],
            "display_name": row[2]
        })
    conn.close()
    return intervals

def get_interval(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interval where id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    interval = {
            "id": row[0],
            "name": row[1],
            "display_name": row[2]
        }
    return interval

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
        alerts.append(Alert(
            id= row[0],
            stock_id= row[1],
            indicator_id= row[2],
            period_id= row[3],
            interval_id= row[4],
            action= row[5],
            threshold= row[6]
        ))
    conn.close()
    return alerts

def get_alert(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alert where id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    alert = Alert(
            id= row[0],
            stock_id= row[1],
            indicator_id= row[2],
            period_id= row[3],
            interval_id= row[4],
            action= row[5],
            threshold= row[6]
        )
    return alert

def add_alert(alert=Alert):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO alert (stock_id, indicator_id, period_id, interval_id, action, threshold) VALUES (?, ?, ?, ?, ?, ?)",
        (alert.stock_id, alert.indicator_id, alert.period_id, alert.interval_id, alert.action, alert.threshold),
    )
    conn.commit()
    conn.close()
    
def del_alert(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alert where id = ?", (id,))
    conn.close()
    return True