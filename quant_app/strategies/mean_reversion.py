# strategies/mean_reversion.py
import pandas as pd
import numpy as np

def mean_reversion(prices: pd.DataFrame, window: int = 20, threshold: float = 2.0) -> pd.DataFrame:
    """
    Mean Reversion strategy:
    - Buy when the price is very low (-threshold times the rolling std)
    - Sell when the price is back at the rolling mean
    - Returns cumulative PnL
    """
    if prices.empty:
        raise ValueError("Prices DataFrame is empty")

    # Indicators
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()
    z_score = (prices - rolling_mean) / rolling_std

    # Signal, buy when very low, sell when it's back at rolling mean
    signal = pd.DataFrame(np.nan, index=prices.index, columns=prices.columns)
    signal[z_score < -threshold] = 1.0
    signal[z_score >= 0] = 0.0
    signal = signal.ffill().fillna(0)

    # Compute daily returns
    daily_returns = prices.pct_change().fillna(0)

    # Apply signal on next day
    strategy_returns = signal.shift(1) * daily_returns

    # Cumulative PnL
    cum_pnl = (1 + strategy_returns).cumprod()

    return cum_pnl