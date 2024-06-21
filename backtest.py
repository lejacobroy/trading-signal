from indicators import (
    calculate_macd,
    calculate_bb,
    calculate_rsi,
    calculate_sma,
    calculate_ma_cross,
)


def backtest_strategy(data, indicator, threshold):
    if indicator == "MACD":
        result = calculate_macd(data)
    elif indicator == "BB":
        result = calculate_bb(data)
    elif indicator == "RSI":
        result = calculate_rsi(data)
    elif indicator == "SMA":
        result = calculate_sma(data)
    elif indicator == "MA Cross":
        result = calculate_ma_cross(data)

    # Backtesting logic
    if result >= threshold:
        return True
    return False


if __name__ == "__main__":
    import pandas as pd

    data = pd.read_csv("historical_stock_data.csv")
    print(backtest_strategy(data, "MACD", 0.5))
