import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def get_price(ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    Fetch the closing price data from Yahoo finance for a ticker.
    """
    
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, progress=False)

    if df.empty:
        print(f"No data found for the ticker '{ticker}' between {start_date} and {end_date}.")
        return pd.DataFrame()

    close_data = df['Close']
    if isinstance(close_data, pd.Series):
        df_close = close_data.to_frame(name=ticker)
    else:
        df_close = close_data.copy()

    return df_close