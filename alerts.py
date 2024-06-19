from database import get_db
from models import Alert, Stock
from indicators import calculate_macd, calculate_bb, calculate_rsi, calculate_sma, calculate_ma_cross
from telegram import send_telegram_message

def check_alerts():
    db = get_db()
    alerts = Alert.query.all()
    for alert in alerts:
        stock = Stock.query.get(alert.stock_id)
        data = fetch_stock_data(stock.symbol)
        if alert.indicator == 'MACD':
            result = calculate_macd(data)
        elif alert.indicator == 'BB':
            result = calculate_bb(data)
        elif alert.indicator == 'RSI':
            result = calculate_rsi(data)
        elif alert.indicator == 'SMA':
            result = calculate_sma(data)
        elif alert.indicator == 'MA Cross':
            result = calculate_ma_cross(data)
        
        if result >= alert.threshold:
            send_telegram_message(f"Alert triggered for {stock.symbol}: {alert.indicator} crossed {alert.threshold}")

def fetch_stock_data(symbol):
    # Fetch stock data logic
    pass