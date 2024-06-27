import pandas as pd
import numpy as np

def calculate_macd(data):
    short_window = 12
    long_window = 26
    signal_window = 9
    data["short_mavg"] = data["Close"].ewm(span=short_window, adjust=False).mean()
    data["long_mavg"] = data["Close"].ewm(span=long_window, adjust=False).mean()
    data["macd"] = data["short_mavg"] - data["long_mavg"]
    data["signal_line"] = data["macd"].ewm(span=signal_window, adjust=False).mean()
    
    # Calculate the difference between MACD and signal line
    diff = data["macd"] - data["signal_line"]
    
    # Check if the sign of the difference changes (crossover occurred)
    crossover = np.diff(np.sign(diff))
    
    # Get the last values of MACD and signal line
    macd_value = data["macd"].iloc[-1]
    signal_value = data["signal_line"].iloc[-1]
    
    # Determine the crossover flag
    if len(crossover) > 0:
        if crossover[-1] == 2:  # MACD crossed above signal line
            crossed = 1
        elif crossover[-1] == -2:  # MACD crossed below signal line
            crossed = -1
        else:
            crossed = 0
    else:
        crossed = 0
    
    return macd_value, signal_value, crossed

def calculate_bb(data):
    window = 20
    data["sma"] = data["Close"].rolling(window=window).mean()
    data["stddev"] = data["Close"].rolling(window=window).std()
    data["upper_band"] = data["sma"] + (data["stddev"] * 2)
    data["lower_band"] = data["sma"] - (data["stddev"] * 2)
    
    # Calculate the difference between price and upper/lower bands
    diff_upper = data["Close"] - data["upper_band"]
    diff_lower = data["Close"] - data["lower_band"]
    
    # Check if the sign of the differences changes (crossover occurred)
    crossover_upper = np.diff(np.sign(diff_upper))
    crossover_lower = np.diff(np.sign(diff_lower))
    
    # Get the last values of upper and lower bands
    upper_band_value = data["upper_band"].iloc[-1]
    lower_band_value = data["lower_band"].iloc[-1]
    
    # Determine the crossover flags
    if len(crossover_upper) > 0:
        if crossover_upper[-1] == 2:  # Price crossed above upper band
            crossed_upper = 1
        elif crossover_upper[-1] == -2:  # Price crossed below upper band
            crossed_upper = -1
        else:
            crossed_upper = 0
    else:
        crossed_upper = 0
        
    if len(crossover_lower) > 0:
        if crossover_lower[-1] == 2:  # Price crossed above lower band
            crossed_lower = 1
        elif crossover_lower[-1] == -2:  # Price crossed below lower band
            crossed_lower = -1
        else:
            crossed_lower = 0
    else:
        crossed_lower = 0
    
    return upper_band_value, lower_band_value, crossed_upper, crossed_lower

def calculate_rsi(data):
    window = 14
    delta = data["Close"].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Calculate the difference between RSI and threshold
    diff = rsi - 30  # Assuming a threshold of 30 for overbought/oversold
    
    # Check if the sign of the difference changes (crossover occurred)
    crossover = np.diff(np.sign(diff))
    
    # Get the last value of RSI
    rsi_value = rsi.iloc[-1]
    
    # Determine the crossover flag
    if len(crossover) > 0:
        if crossover[-1] == 2:  # RSI crossed above threshold
            crossed = 1
        elif crossover[-1] == -2:  # RSI crossed below threshold
            crossed = -1
        else:
            crossed = 0
    else:
        crossed = 0
    
    return rsi_value, crossed

def calculate_sma(data, window):
    sma = data["Close"].rolling(window=window).mean()
    
    # Calculate the difference between price and SMA
    diff = data["Close"] - sma
    
    # Check if the sign of the difference changes (crossover occurred)
    crossover = np.diff(np.sign(diff))
    
    # Get the last value of SMA
    sma_value = sma.iloc[-1]
    
    # Determine the crossover flag
    if len(crossover) > 0:
        if crossover[-1] == 2:  # Price crossed above SMA
            crossed = 1
        elif crossover[-1] == -2:  # Price crossed below SMA
            crossed = -1
        else:
            crossed = 0
    else:
        crossed = 0
    
    return sma_value, crossed

def calculate_ma_cross(data, short_window, long_window):
    data["short_mavg"] = data["Close"].rolling(window=short_window).mean()
    data["long_mavg"] = data["Close"].rolling(window=long_window).mean()

    # Calculate the difference between short and long moving averages
    diff = data["short_mavg"] - data["long_mavg"]

    # Check if the sign of the difference changes (crossover occurred)
    crossover = np.diff(np.sign(diff))

    # Get the last values of short and long moving averages
    short_mavg = data["short_mavg"].iloc[-1]
    long_mavg = data["long_mavg"].iloc[-1]

    # Determine the crossover flag
    if len(crossover) > 0:
        if crossover[-1] == 2:  # Short MA crossed above Long MA
            crossed = 1
        elif crossover[-1] == -2:  # Short MA crossed below Long MA
            crossed = -1
        else:
            crossed = 0
    else:
        crossed = 0

    return short_mavg, long_mavg, crossed



