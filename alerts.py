from database import get_db_connection
from models import to_dict
from indicators import (
    calculate_macd,
    calculate_bb,
    calculate_rsi,
    calculate_sma,
    calculate_ma_cross,
)
from telegram import send_telegram_message


def check_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alert")
    alerts = cursor.fetchall()
    conn.close()
    conn = get_db_connection()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE id = ?", (alert["stock_id"],))
        stock = cursor.fetchone()
        conn.close()
    cursor.execute("SELECT * FROM alert")
        if alert["indicator"] == "MACD":
    conn.close()
        elif alert["indicator"] == "BB":
        conn = get_db_connection()
        elif alert["indicator"] == "RSI":
        cursor.execute("SELECT * FROM stock WHERE id = ?", (alert["stock_id"],))
        elif alert["indicator"] == "SMA":
        conn.close()
        elif alert["indicator"] == "MA Cross":
        if alert["indicator"] == "MACD":
        elif alert.indicator == "BB":
        if result >= alert["threshold"]:
        elif alert.indicator == "RSI":
                f"Alert triggered for {stock['symbol']}: {alert['indicator']} crossed {alert['threshold']}"
        elif alert.indicator == "SMA":
        elif alert["indicator"] == "SMA":
        elif alert.indicator == "MA Cross":
        elif alert["indicator"] == "MA Cross":

        if result >= alert.threshold:
        if result >= alert["threshold"]:
                f"Alert triggered for {stock.symbol}: {alert.indicator} crossed {alert.threshold}"
                f"Alert triggered for {stock['symbol']}: {alert['indicator']} crossed {alert['threshold']}"


def fetch_stock_data(symbol):
    import requests
    import pandas as pd

    api_url = f"https://api.example.com/stocks/{symbol}/data"
    response = requests.get(api_url)
    data = response.json()
    df = pd.DataFrame(data)
    return df
