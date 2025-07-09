import streamlit as st
from twelvedata import TDClient
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import ta

# ------------------ Data Pull and Feature Engineering --------------
## --------- Credentials --------
def configure():
    load_dotenv()

## ----------- Data Pull ----------
def data_get():
    configure()
    td = TDClient(apikey=os.getenv('api_key'))      # Initialize client - apikey parameter is requiered
    ts = td.time_series(                            # Construct the necessary time series
        symbol="USD/JPY",
        interval="1day",
        outputsize=5000,
        timezone="UTC",
        )
    usdjpy_daily_df = ts.as_pandas()                
    return usdjpy_daily_df                          # Returns pandas.DataFrame

## ------------ Data Transform --------
def transform():
    df = data_get()
    df = df.sort_index(ascending=True)
    df['tomorrow'] = df['close'].shift(-1)
    df['target'] = (df['tomorrow'] > df['close']).astype(int)
    return df                                                                   # Return Transformed DataFrame

## ------------ Feature Engineering -------
def feature_engineering():
    df = transform()
    horizons = [2, 5, 60, 250, 1000]
    predictors = []
    for horizon in horizons:
        rolling_averages = df.rolling(horizon).mean()

        ratio_column = f'Close_Ratio{horizon}'
        df[ratio_column] = df['close'] / rolling_averages['close']

        trend_column = f'Trend_{horizon}'
        df[trend_column] = df.shift(1).rolling(horizon).sum()['target']

        predictors += [ratio_column, trend_column]
    
    df = df.dropna()
    return df                                                          # Returns Featured DataFrame

## -------- Price Overtime Chart -----------------
def price_overtime(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['close'], label='USDJPY Close', linewidth=1)
    ax.set_title('USDJPY Close Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close')
    ax.legend()
    return fig

## ----------- Candlestick ------------
def candlestick(df):
    # Only use the last 30 rows (i.e. last 30 days)
    df_last30 = df.tail(30)
    
    fig = go.Figure(data = [go.Candlestick(
        x = df_last30.index,
        open = df_last30['open'],
        high = df_last30['high'],
        low = df_last30['low'],
        close = df_last30['close']
    )])

    fig.update_layout(
        title="USD/JPY - Last 30 Days",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )
    return fig

## -------- Moving Average -------
def moving_average(df):
    ma50 = df.close.rolling(50).mean()
    ma20 = df.close.rolling(20).mean()
    ma15 = df.close.rolling(15).mean()

    df_last30 = df.tail(30)
    ma50_last30 = ma50.tail(30)
    ma20_last30 = ma20.tail(30)
    ma15_last30 = ma15.tail(30)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_last30['close'], label='USDJPY Close Price')
    ax.plot(ma50_last30, label ='Moving Average 50 Price')
    ax.plot(ma20_last30, label ='Moving Average 20 Price')
    ax.plot(ma15_last30, label ='Moving Average 15 Price')
    ax.set_title('Moving Average and Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close')
    ax.legend()
    return fig

## ------------ RSI --------------
def rsi_plot(df):
    rsi = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
    df_last30 = df.tail(30)
    rsi_last30 = rsi.tail(30)

    # Plotting RSI
    fig, axs = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # ---- Subplot 1: close ----
    axs[0].plot(df_last30.index, df_last30['close'], label='USDJPY close', color='blue')
    axs[0].set_title('USDJPY Close')
    axs[0].set_ylabel('Close Price')
    axs[0].legend()
    axs[0].grid(True)

    # ---- Subplot 2: RSI ----
    axs[1].plot(df_last30.index, rsi_last30, label='RSI (14)', color='orange')
    axs[1].axhline(70, color='red', linestyle='--', label='Overbought (70)')
    axs[1].axhline(30, color='green', linestyle='--', label='Oversold (30)')
    axs[1].axhline(50, color='gray', linestyle='--', alpha=0.5)
    axs[1].set_title('Relative Strength Index (RSI)')
    axs[1].set_ylabel('RSI Value')
    axs[1].set_ylim(0, 100)
    axs[1].legend()
    axs[1].grid(True)

    fig.tight_layout()
    return fig

def render():
    df = feature_engineering()
    ## ------- Dataset Overview -----------
    st.header('Data Overview')
    st.dataframe(df.tail(10))

    # Price Overtime Chart
    st.header("USD/JPY Price Overtime", divider=True)
    st.pyplot(price_overtime(df))

    # Candlestick
    st.header("Candlestick Last 30 Days", divider=True)
    st.plotly_chart(candlestick(df), theme=None, use_container_width=True)

    # Moving Average
    st.header("Moving Average", divider=True)
    st.pyplot(moving_average(df))

    # RSI
    st.header("Relative Strength Index in Last 30 Days", divider=True)
    st.pyplot(rsi_plot(df))







