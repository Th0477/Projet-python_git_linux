# strategies/momentum.py
import pandas as pd

def momentum(prices: pd.DataFrame, window_fast: int = 20, window_slow: int = 50) -> pd.DataFrame:
    """
    Simple momentum strategy:
    - Long if rolling mean fast > rolling mean slow 
    - Cash (0 position) otherwise
    - Returns cumulative PnL
    """
    if prices.empty:
        raise ValueError("Prices DataFrame is empty")

    # Compute rolling mean
    rolling_mean_fast = prices.rolling(window=window_fast).mean()
    rolling_mean_slow = prices.rolling(window = window_slow).mean()

    # Signal: 1 if rolling mean fast > rolling mean slow, else 0
    signal = (rolling_mean_fast > rolling_mean_slow).astype(int)

    # Compute daily returns
    daily_returns = prices.pct_change().fillna(0)

    # Apply signal on next day
    strategy_returns = signal.shift(1) * daily_returns

    # Cumulative PnL
    cum_pnl = (1 + strategy_returns).cumprod()

    return cum_pnl
