# strategies/momentum.py
import pandas as pd

def momentum(prices: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Simple momentum strategy:
    - Long if price > rolling mean (window)
    - Cash (0 position) otherwise
    - Returns cumulative PnL

    Args:
        prices (pd.DataFrame): DataFrame with stock prices (dates as index)
        window (int): Rolling window for moving average

    Returns:
        pd.DataFrame: Cumulative PnL of the strategy
    """
    if prices.empty:
        raise ValueError("Prices DataFrame is empty")

    # Compute rolling mean
    rolling_mean = prices.rolling(window=window).mean()

    # Signal: 1 if price > rolling mean, else 0
    signal = (prices > rolling_mean).astype(int)

    # Compute daily returns
    daily_returns = prices.pct_change().fillna(0)

    # Apply signal on next day (shift)
    strategy_returns = signal.shift(1) * daily_returns

    # Cumulative PnL
    cum_pnl = (1 + strategy_returns).cumprod()

    return cum_pnl
