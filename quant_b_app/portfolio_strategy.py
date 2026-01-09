import pandas as pd
import numpy as np


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les rendements journaliers à partir des prix.
    """
    return prices.pct_change().dropna()


def compute_portfolio_returns(returns: pd.DataFrame, weights: dict) -> pd.Series:
    """
    Calcule le rendement du portefeuille à partir des poids.
    weights = {"AAPL": 0.4, "MSFT": 0.3, "GOOGL": 0.3}
    """
    w = pd.Series(weights)
    return returns.dot(w)

def compute_portfolio_value(portfolio_returns: pd.Series, initial_value=100):
    portfolio_value = (1 + portfolio_returns).cumprod()
    portfolio_value.iloc[0] = 1.0
    return initial_value * portfolio_value
