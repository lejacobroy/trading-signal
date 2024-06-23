import pandas as pd

def calculate_macd(data):
    short_window = 12
    long_window = 26
    signal_window = 9
    data["short_mavg"] = data["Close"].ewm(span=short_window, adjust=False).mean()
    data["long_mavg"] = data["Close"].ewm(span=long_window, adjust=False).mean()
    data["macd"] = data["short_mavg"] - data["long_mavg"]
    data["signal_line"] = data["macd"].ewm(span=signal_window, adjust=False).mean()
    return data["macd"].iloc[-1] - data["signal_line"].iloc[-1]

def calculate_bb(data):
    window = 20
    data["sma"] = data["Close"].rolling(window=window).mean()
    data["stddev"] = data["Close"].rolling(window=window).std()
    data["upper_band"] = data["sma"] + (data["stddev"] * 2)
    data["lower_band"] = data["sma"] - (data["stddev"] * 2)
    return data["Close"].iloc[-1] - data["upper_band"].iloc[-1]

def calculate_rsi(data):
    window = 14
    delta = data["Close"].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def calculate_sma(data):
    window = 50
    sma = data["Close"].rolling(window=window).mean()
    return sma.iloc[-1]

def calculate_ma_cross(data):
    short_window = 50
    long_window = 200
    data["short_mavg"] = data["Close"].rolling(window=short_window).mean()
    data["long_mavg"] = data["Close"].rolling(window=long_window).mean()
    return data["short_mavg"].iloc[-1] - data["long_mavg"].iloc[-1]



