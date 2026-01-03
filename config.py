#config.py
import datetime

# General Configuration
APP_TITLE = "Quantitative Strategy Analyzer"
DEFAULT_TICKER = "AAPL"
DEFAULT_START_DATE = datetime.date(2020, 1, 1)
DEFAULT_END_DATE = datetime.date.today()

# Applications's default parameters
# 1. Momentum
MOMENTUM_WINDOW_FAST = 20
MOMENTUM_WINDOW_SLOW = 50

# 2. Mean Reversion
MEAN_REVERSION_WINDOW = 20
MEAN_REVERSION_THRESHOLD = 2.0  

# 3. Regime Switching
REGIME_TREND_WINDOW = 200

# Analysis Parameters
TRADING_DAYS = 252 
RISK_FREE_RATE = 0.4