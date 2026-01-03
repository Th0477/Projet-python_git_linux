# strategies/buy_and_hold.py
import pandas as pd

def buy_and_hold(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate a Buy & Hold strategy for a single stock.

    Args:
        prices (pd.DataFrame): DataFrame with dates as index and one column with stock prices

    Returns:
        pd.DataFrame: DataFrame with cumulative PnL of the Buy & Hold strategy
    """
    if prices.empty:
        raise ValueError("Prices DataFrame is empty")

    # Compute daily returns
    daily_returns = prices.pct_change().fillna(0)

    # Compute cumulative PnL (1 unit invested at start)
    cum_pnl = (1 + daily_returns).cumprod()

    return cum_pnl
