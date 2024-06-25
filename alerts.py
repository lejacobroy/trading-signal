from database import get_alerts, get_stock, get_stocks, get_indicator, get_period, get_interval
from indicators import (
    calculate_macd,
    calculate_bb,
    calculate_rsi,
    calculate_sma,
    calculate_ma_cross,
)
import yfinance as yf
import pandas as pd
from models import Alert
from telegram import send_telegram_message


def check_alerts():
    alerts = get_alerts()
    for alert in alerts:
        if alert.stock_id is None or alert.stock_id == "" or alert.stock_id == "ANY_ALL":
            print("Checking alert %s for all stocks" % alert.indicator_id)
            stocks = get_stocks()
            for stock in stocks:
                check_single_alert(alert, stock['symbol'])
        else:
            stock = get_stock(alert.stock_id)
            check_single_alert(alert, stock['symbol'])

def check_single_alert(alert, stock):
    indicator = get_indicator(alert.indicator_id)
    period = get_period(alert.period_id)
    interval = get_interval(alert.interval_id)
    try:
        stock_data = fetch_stock_data(ticker=stock, period=period['name'], interval=interval['name'])
    except Exception as e:
        print(f"Error fetching stock data for {stock}: {e}")
        return
    result = False
    
    if indicator["name"] == "RSI":
        print("Checking RSI alert for stock:", stock)
        try:
            data = calculate_rsi(stock_data)
        except Exception as e:
            print(f"Error calculating RSI for {stock}: {e}")
            return
        print("RSI ", data)
        if alert.action == "Higher":
            if data >= alert.threshold:
                result = True
        if alert.action == "Lower":
            if data <= alert.threshold:
                result = True
    
    if indicator["name"] == "PRICE":
        print("Checking PRICE alert for stock:", stock)
        try:
            data = stock_data["Close"].iloc[-1]
        except Exception as e:
            print(f"Error getting PRICE for {stock}: {e}")
            return
        print("PRICE ", data)
        if alert.action == "Higher":
            if data >= alert.threshold:
                result = True
        if alert.action == "Lower":
            if data <= alert.threshold:
                result = True
    
    if indicator["name"] == "SMA50":
        print("Checking SMA50 alert for stock:", stock)
        try:
            data = calculate_sma(data=stock_data, window=50)
        except Exception as e:
            print(f"Error calculating SMA50 for {stock}: {e}")
            return
        if alert.threshold == "PRICE":
            if alert.action == "Higher":
                try:
                    if data >= stock_data["Close"].iloc[-1]:
                        result = True
                except Exception as e:
                    print(f"Error comparing SMA50 and PRICE for {stock}: {e}")
                    return
            if alert.action == "Lower":
                try:
                    if data <= stock_data["Close"].iloc[-1]:
                        result = True
                except Exception as e:
                    print(f"Error comparing SMA50 and PRICE for {stock}: {e}")
                    return
        print("SMA50 ", data)
    
    if indicator["name"] == "SMA200":
        print("Checking SMA200 alert for stock:", stock)
        try:
            data = calculate_sma(data=stock_data, window=200)
        except Exception as e:
            print(f"Error calculating SMA200 for {stock}: {e}")
            return
        print("SMA200 ", data)
        
    if indicator["name"] == "MACD":
        print("Checking MACD alert for stock:", stock)
        try:
            data = calculate_macd(stock_data)
        except Exception as e:
            print(f"Error calculating MACD for {stock}: {e}")
            return
        ## cross
        if data > alert.threshold:
            try:
                send_telegram_message(
                    f"MACD alert for {stock} is triggered at {data['macd']}"
                )
            except Exception as e:
                print(f"Error sending MACD alert for {stock}: {e}")
            print("MACD alert triggered for stock:", stock)
        else:
            print("MACD alert not triggered for stock:", stock)
    
    if indicator["name"] == "BB":
        print("Checking BB alert for stock:", stock)
        try:
            data = calculate_bb(stock_data)
        except Exception as e:
            print(f"Error calculating BB for {stock}: {e}")
            return
        print("BB ", data)
        if data > 0:
            # MACD is positive
            pass
        
    if indicator["name"] == "MA_CROSS_9_21":
        print("Checking MA Cross alert for stock:", stock)
        try:
            short_mavg, long_mavg, crossed = calculate_ma_cross(data=stock_data, short_window=9, long_window=21)
        except Exception as e:
            print(f"Error calculating MA Cross for {stock}: {e}")
            return
        print("MA Cross Short:", short_mavg, "Long:", long_mavg, "Crossed:", crossed)
        if alert.action == 'Cross':
            if crossed == 1:  # Short MA crossed above Long MA
                try:
                    send_telegram_message(
                        f"Bullish MA Cross alert for {stock}: Short MA ({short_mavg}) crossed above Long MA ({long_mavg})"
                    )
                except Exception as e:
                    print(f"Error sending Bullish MA Cross alert for {stock}: {e}")
                print("Bullish MA Cross alert triggered for stock:", stock)

            if crossed == -1:  # Short MA crossed below Long MA
                try:
                    send_telegram_message(
                        f"Bearish MA Cross alert for {stock}: Short MA ({short_mavg}) crossed below Long MA ({long_mavg})"
                    )
                except Exception as e:
                    print(f"Error sending Bearish MA Cross alert for {stock}: {e}")
                print("Bearish MA Cross alert triggered for stock:", stock)
            
    if result:
        try:
            send_telegram_message(
                f"{indicator['name']} alert for {stock} is triggered at {data}"
            )
        except Exception as e:
            print(f"Error sending {indicator['name']} alert for {stock}: {e}")
        print(indicator['name']," alert triggered for stock:", stock)

def fetch_stock_data(ticker, period, interval):
    # Fetches real-time data for the given ticker
    # Period is the length of data, interval is the timeframe
    try:
        data = yf.download(tickers=[ticker], period=period, interval=interval, progress=False)
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return None

def fetch_historic_stock_data(ticker):
    # Fetches real-time data for the given ticker
    try:
        data = yf.download(tickers=[ticker], period="1mo", interval="15m", progress=False)
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching historic stock data for {ticker}: {e}")
        return None

if __name__ == "__main__":
    check_alerts()