from database import get_alerts, get_stock, get_stocks, get_indicator, get_period, get_interval, add_alert_result, get_alert_result
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
    value = 0
    
    if indicator["name"] == "RSI":
        print("Checking RSI alert for stock:", stock)
        try:
            rsi_value = calculate_rsi(stock_data)
        except Exception as e:
            print(f"Error calculating RSI for {stock}: {e}")
            return
        if alert.action == "Higher":
            if rsi_value >= alert.threshold:
                result = True
                value = rsi_value.round(2)
        if alert.action == "Lower":
            if rsi_value <= alert.threshold:
                result = True
                value = rsi_value.round(2)
    
    if indicator["name"] == "PRICE":
        print("Checking PRICE alert for stock:", stock)
        try:
            current_price = stock_data["Close"].iloc[-1]
            previous_price = stock_data["Close"].iloc[-2]
        except Exception as e:
            print(f"Error getting PRICE for {stock}: {e}")
            return
        # Calculate the difference between current and previous prices
        diff = current_price - previous_price

        # Check if the sign of the difference changes (crossover occurred)
        crossover = 0
        if diff > 0:
            if alert.action == "Higher":
                crossover = 1  # Price crossed higher
            else:
                crossover = -1  # Price crossed lower
        elif diff < 0:
            if alert.action == "Lower":
                crossover = 1  # Price crossed lower
            else:
                crossover = -1  # Price crossed higher

        if alert.action == "Higher" and crossover == 1 and current_price >= alert.threshold:
                result = True
                value = current_price.round(2)
        if alert.action == "Lower" and crossover == -1 and current_price <= alert.threshold:
                result = True
                value = current_price.round(2)

    
    if indicator["name"] == "SMA50":
        print("Checking SMA50 alert for stock:", stock)
        try:
            sma_value, crossed = calculate_sma(data=stock_data, window=50)
        except Exception as e:
            print(f"Error calculating SMA50 for {stock}: {e}")
            return
        if alert.threshold == "PRICE":
            if alert.action == "Higher" and crossed == 1:
                if sma_value >= stock_data["Close"].iloc[-1]:
                    result = True
                    value = sma_value.round(2)
            if alert.action == "Lower" and crossed == -1:
                if sma_value <= stock_data["Close"].iloc[-1]:
                    result = True
                    value = sma_value.round(2)
        else:
            if alert.action == "Higher" and crossed == 1:
                if sma_value >= alert.threshold:
                    result = True
                    value = sma_value.round(2)
            if alert.action == "Lower" and crossed == -1:
                if sma_value <= alert.threshold:
                    result = True
                    value = sma_value.round(2)
    
    if indicator["name"] == "SMA200":
        print("Checking SMA200 alert for stock:", stock)
        try:
            sma_value, crossed = calculate_sma(data=stock_data, window=200)
        except Exception as e:
            print(f"Error calculating SMA200 for {stock}: {e}")
            return
        if crossed:
            if alert.threshold == "PRICE":
                if alert.action == "Higher":
                    if sma_value >= stock_data["Close"].iloc[-1]:
                        result = True
                        value = sma_value.round(2)
                if alert.action == "Lower":
                    if sma_value <= stock_data["Close"].iloc[-1]:
                        result = True
                        value = sma_value.round(2)
            else:
                if alert.action == "Higher":
                    if sma_value >= alert.threshold:
                        result = True
                        value = sma_value.round(2)
                if alert.action == "Lower":
                    if sma_value <= alert.threshold:
                        result = True
                        value = sma_value.round(2)
        
    if indicator["name"] == "MACD":
        print("Checking MACD alert for stock:", stock)
        try:
            macd_value, signal_value, crossed = calculate_macd(stock_data)
        except Exception as e:
            print(f"Error calculating MACD for {stock}: {e}")
            return
        if alert.action == "Cross":
            if alert.threshold == "BULL" and crossed == 1:
                    result = True
                    value = macd_value.round(2)
            if alert.threshold == "BEAR" and crossed == -1:
                    result = True
                    value = macd_value.round(2)
    
    if indicator["name"] == "BB":
        print("Checking BB alert for stock:", stock)
        try:
            upper_band_value, lower_band_value, crossed_upper, crossed_lower = calculate_bb(stock_data)
        except Exception as e:
            print(f"Error calculating BB for {stock}: {e}")
            return
        if alert.action == "Higher" and crossed_upper and stock_data["Close"].iloc[-1] >= upper_band_value:
            result = True
            value = upper_band_value.round(2)
        if alert.action == "Lower" and crossed_lower and stock_data["Close"].iloc[-1] <= lower_band_value:
            result = True
            value = lower_band_value.round(2)
        
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
                result = True
                value = short_mavg.round(2)
            if crossed == -1:  # Short MA crossed below Long MA
                result = True
                value = short_mavg.round(2)
                
    previous = get_alert_result(id=alert.id, stock=alert.stock_id)
    if previous is None:
        previous = 0

    if str(previous) == str(value):
        return
        
    if result:
        print(previous, value)
        try:
            add_alert_result(id=alert.id, stock=alert.stock_id, result=value)
        except Exception as e:
            print(f"Error adding alert result for {stock}, {alert.id}, {value}: {e}")
            return
        interval = get_interval(alert.interval_id)
        try:
            send_telegram_message(
                f"{indicator['name']} {interval['name']} alert for {stock} is triggered {alert.action} at {value}"
            )
        except Exception as e:
            print(f"Error sending {indicator['name']} alert for {stock}: {e}")
        print(indicator['name']," alert for ", stock, " is triggered ", alert.action, " at ", value)

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