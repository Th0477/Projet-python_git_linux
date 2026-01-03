#backtesting/metrics.py
import numpy as np

def compute_metrics(cum_returns_df):
    """
    Compute perfomance metrics:
    - Total Returns
    - Compound Annual Growth Rate (CAGR)
    - Volatility
    - Sharpe Ratio
    - Max Drawdown
    """
    
    # Security checks
    series = cum_returns_df.iloc[:, 0].fillna(1.0)
    if series.empty or len(series) < 2:
        return {k: "N/A" for k in ["Total Return", "CAGR", "Volatility", "Sharpe Ratio", "Max Drawdown"]}

    # 1. Total Return
    total_return = series.iloc[-1] - 1
    
    # 2. CAGR
    start_date = series.index[0]
    end_date = series.index[-1]
    days = (end_date - start_date).days
    years = days / 365.25
    if years > 0.1: 
        cagr = (series.iloc[-1] / series.iloc[0]) ** (1 / years) - 1
    else:
        cagr = 0

    # 3. Vol
    daily_rets = series.pct_change().fillna(0)
    volatility = daily_rets.std() * np.sqrt(252)
    
    # 4. Sharpe Ratio
    if volatility > 0:
        sharpe = (daily_rets.mean() * 252) / volatility
    else:
        sharpe = 0
        
    # 5. Max Drawdown
    running_max = series.cummax()
    drawdown = (series - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        "Total Return": f"{total_return:.2%}",
        "CAGR": f"{cagr:.2%}",
        "Volatility": f"{volatility:.2%}",
        "Sharpe Ratio": f"{sharpe:.2f}",
        "Max Drawdown": f"{max_drawdown:.2%}"
    }