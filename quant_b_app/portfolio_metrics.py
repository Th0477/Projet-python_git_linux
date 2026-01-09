import pandas as pd
import numpy as np


def portfolio_volatility(returns: pd.Series):
    return returns.std() * np.sqrt(252)


def portfolio_return(portfolio_value: pd.Series):
    return portfolio_value.iloc[-1] / portfolio_value.iloc[0] - 1


def correlation_matrix(returns: pd.DataFrame):
    return returns.corr()
