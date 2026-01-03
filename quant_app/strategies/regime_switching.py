# strategies/regime_switching.py
import pandas as pd
import numpy as np

def regime_switching(prices: pd.DataFrame, trend_window: int = 200, mom_window: int = 20, mr_window: int = 20, mr_threshold: float = 2.0) -> pd.DataFrame:
    """
    Regime Switching strategy (hybrid):
    - Determines Market Regime using a Long Term Moving Average (trend_window)
    - BULL REGIME (Price > Long MA): Uses Momentum logic
    - BEAR REGIME (Price < Long MA): Uses Mean Reversion logic 
    - Returns cumulative PnL
    """
    if prices.empty:
        raise ValueError("Prices DataFrame is empty")

    # 1. COMPUTE INDICATORS

    # Regime Filter
    regime_ma = prices.rolling(window=trend_window).mean()

    # Momentum Indicator
    mom_ma = prices.rolling(window=mom_window).mean()

    # Mean Reversion Indicators 
    mr_ma = prices.rolling(window=mr_window).mean()
    mr_std = prices.rolling(window=mr_window).std()
    z_score = (prices - mr_ma) / mr_std


    # 2. GENERATE SIGNALS

    # A. Momentum Signal 
    # 1 if Price > Fast MA, else 0
    sig_momentum = (prices > mom_ma).astype(int)
    
    # B. Mean Reversion Signal
    # Buy at -threshold times sigma, hold, sell at Mean (0 sigma)
    sig_mean_reversion = pd.DataFrame(np.nan, index=prices.index, columns=prices.columns)
    sig_mean_reversion[z_score < -mr_threshold] = 1.0  
    sig_mean_reversion[z_score >= 0] = 0.0             
    sig_mean_reversion = sig_mean_reversion.ffill().fillna(0)


    # 3. COMBINE SIGNALS BASED ON REGIME
    
    # Define Regime
    is_bull_regime = (prices > regime_ma)
    
    # Vectorized condition
    final_signal = np.where(is_bull_regime, sig_momentum, sig_mean_reversion)
    final_signal = pd.DataFrame(final_signal, index=prices.index, columns=prices.columns)


    # 4. COMPUTE RETURNS

    # Compute daily returns
    daily_returns = prices.pct_change().fillna(0)

    # Apply signal on next day
    strategy_returns = final_signal.shift(1) * daily_returns

    # Cumulative PnL
    cum_pnl = (1 + strategy_returns).cumprod()

    return cum_pnl