import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from indicators import calculate_full_macd, calculate_full_bb, calculate_full_rsi, calculate_full_sma, calculate_full_ma_cross
import yfinance as yf

def round_series(series, decimals=2):
    """Round all values in a pandas Series or DataFrame to specified decimal places"""
    if isinstance(series, pd.Series) or isinstance(series, pd.DataFrame):
        return series.round(decimals)
    elif isinstance(series, np.ndarray):
        return np.round(series, decimals)
    else:
        return series  # Return as is if not a known type
    
def create_stock_graph(stock, alerts, limited=False):
    # alerts : 'id': row[0],
            # 'stock_id': row[1],
            # 'stock_symbol': row[2],
            # 'indicator_id': row[3],
            # 'indicator_name': row[4],
            # 'period_id': row[5],
            # 'period_name': row[6],
            # 'interval_id': row[7],
            # 'interval_name': row[8],
            # 'action': row[9],
            # 'threshold': row[10]
    # Fetch data (you may want to adjust the period and interval)
    data = yf.download(stock['symbol'], period="1y", interval="1d", auto_adjust=True, multi_level_index=False, progress=False)

    # Create subplot structure
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.005,
                        row_heights=[0.55, 0.15, 0.15, 0.15])
    # Add candlestick chart
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'].astype(float),
                                 high=data['High'].astype(float),
                                 low=data['Low'].astype(float),
                                 close=data['Close'].astype(float),
                                 name='Price',
                                 opacity=1.0,
                                visible=True,
                                increasing_line_color='green',  # Make increasing candles clearly visible
                                decreasing_line_color='red' ),
                  row=1, col=1)
   
    # Add Bollinger Bands, if they are present in the alerts
    bb_present = True
    if limited:
        bb_present = any(alert['indicator_name'] == "BB" for alert in alerts)
    if bb_present:
        bb_data = calculate_full_bb(data)
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=round_series(bb_data['upper_band']), 
            name='Upper BB', 
            line=dict(color='rgba(0, 170,255, 0.75)')), row=1, col=1)    
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=bb_data['lower_band'], 
            name='Lower BB', 
            line=dict(color='rgba(0, 170,255, 0.75)')), row=1, col=1)

    # Add SMA, if it is present in the alerts
    sma_present = True
    if limited:
        sma_present = any(alert['indicator_name'] == "SMA50" or alert['indicator_name'] == "SMA200" for alert in alerts)
    if sma_present:
        sma_data_50 = calculate_full_sma(data,50)
        sma_data_200 = calculate_full_sma(data,200)
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=round_series(sma_data_50), 
            name='SMA 50', 
            line=dict(color='rgba(119,0,179,0.75)')), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=round_series(sma_data_200), 
            name='SMA 200', 
            line=dict(color='rgba(77,64,0,0.75)')), row=1, col=1)

    # Add MACD if it is present in the alerts
    macd_present = True
    if limited:
        macd_present = any(alert['indicator_name'] == "MACD" for alert in alerts)
    if macd_present:
        macd_data = calculate_full_macd(data)
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=round_series(macd_data['macd']), 
            name='MACD', 
            line=dict(color='blue')), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=round_series(macd_data['signal_line']), 
            name='Signal Line', 
            line=dict(color='orange')), row=2, col=1)

    # Add MA Cross, if it is present in the alerts
    ma_cross_present = True
    if limited:
        ma_cross_present = any(alert['indicator_name'] == "MA_CROSS_9_21" for alert in alerts)
    if ma_cross_present:
        mac_data = calculate_full_ma_cross(data, 9, 21)
        # Calculate the difference between short and long moving averages
        mac_data['diff'] = data["short_mavg"] - data["long_mavg"]
        # Create a new column for crossover points
        mac_data['crossover'] = None
        # Iterate through the data to find crossover points
        for i in range(1, len(mac_data)):
            if (mac_data['diff'].iloc[i-1] <= 0 and mac_data['diff'].iloc[i] > 0) or \
               (mac_data['diff'].iloc[i-1] >= 0 and mac_data['diff'].iloc[i] < 0):
                mac_data.loc[mac_data.index[i], 'crossover'] = mac_data["short_mavg"].iloc[i]
        
        # Add traces for MA lines and crossover points
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=round_series(mac_data['short_mavg']), 
            name='MA 9', 
            line=dict(color='rgba(25,102,255,0.75)')), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=round_series(mac_data['long_mavg']), 
            name='MA 21', 
            line=dict(color='rgba(255,140,25,0.75)')), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=data[mac_data['crossover'].notnull()].index, 
            y=data[data['crossover'].notnull()]['crossover'], 
            name='MA Cross', mode='markers', 
            marker=dict(size=10, color='black', symbol='cross')), row=1, col=1)  
          
    # Add RSI, if it is present in the alerts
    rsi_present = True
    if limited:
        rsi_present = any(alert['indicator_name'] == "RSI" for alert in alerts)
    if rsi_present:
        rsi_data = calculate_full_rsi(data)
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=round_series(rsi_data), 
            name='RSI', 
            line=dict(color='orange')), row=3, col=1)

    # Add volume bar chart
    fig.add_trace(go.Bar(
        x=data.index, 
        y=round_series(data['Volume']), 
        name='Volume',
        marker=dict(color='red')), row=4, col=1)

    # Update layout
    fig.update_layout(title='Stock Price with Indicators',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      height=1000,
                      showlegend=True)
    
        # Update x-axis properties for each subplot
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_xaxes(rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    ), row=1, col=1)

    # After adding all traces, add this code:
    fig.update_yaxes(
        title_text="Price",
        row=1, col=1,
        autorange=True  # Force autorange to include all data
    )

    # Ensure only the bottom subplot has a visible x-axis
    for i in range(1, 4):
        fig.update_xaxes(visible=False, row=i, col=1)
    fig.update_xaxes(visible=True, row=4, col=1)

    return fig