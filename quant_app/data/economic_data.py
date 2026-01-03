import yfinance as yf
import config

def get_risk_free_rate(ticker="^TNX"):
    """
    Fetch the risk free rate from Yahoo finance (Treasury Yield).
    If an error occurs we take the config.py risk free rate.
    """
    try:
        df = yf.download(ticker, period="5d", progress=False)['Close']
        if df.empty:
            return config.RISK_FREE_RATE
        return float(df.iloc[-1]) / 100.0
    except:
        return config.RISK_FREE_RATE