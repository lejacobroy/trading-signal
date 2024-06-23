from database import get_alerts, get_stock, get_stocks
from indicators import (
    calculate_macd,
    calculate_bb,
    calculate_rsi,
    calculate_sma,
    calculate_ma_cross,
)
import yfinance as yf
import pandas as pd
from telegram import send_telegram_message


def check_alerts():
    alerts = get_alerts()
    for alert in alerts:
        if alert["stock_id"] is None or alert["stock_id"] == "" or alert["stock_id"] == "ANY_ALL":
            print("Checking %s alert for all stocks" % alert['indicator'])
            stocks = get_stocks()
            for stock in stocks:
                check_single_alert(alert, stock['symbol'])
        else:
            stock = get_stock(alert["stock_id"])
            check_single_alert(alert, stock['symbol'])

def check_single_alert(alert, stock):
    stock_data = fetch_stock_data(ticker=stock, interval='1h')
    if alert["indicator"] == "MACD":
        print("Checking MACD alert for stock:", stock)
        data = calculate_macd(stock_data)
        ## cross
        if data > alert["threshold"]:
            send_telegram_message(
                f"MACD alert for {stock} is triggered at {data['macd']}"
            )
            print("MACD alert triggered for stock:", stock)
        else:
            print("MACD alert not triggered for stock:", stock)
    
    if alert["indicator"] == "BB":
        print("Checking BB alert for stock:", stock)
        data = calculate_bb(stock_data)
    
    if alert["indicator"] == "RSI":
        print("Checking RSI alert for stock:", stock)
        data = calculate_rsi(stock_data)
    
    if alert["indicator"] == "SMA":
        print("Checking SMA alert for stock:", stock)
        data = calculate_sma(stock_data)
    
    if alert["indicator"] == "MA Cross":
        print("Checking MA Cross alert for stock:", stock)
        data = calculate_ma_cross(stock_data)
    
    if alert["indicator"] == "MACD":
        print("Checking MACD alert for stock:", stock)
        data = calculate_macd(stock_data)
    print(data)

def fetch_stock_data(ticker, interval):
    # Fetches real-time data for the given ticker
    data = yf.download(tickers=[ticker], period="5d", interval=interval, progress=False)
    df = pd.DataFrame(data)
    return df

def fetch_historic_stock_data(ticker):
    # Fetches real-time data for the given ticker
    data = yf.download(tickers=[ticker], period="1mo", interval="15m", progress=False)
    return pd.DataFrame(data)

if __name__ == "__main__":
    check_alerts()