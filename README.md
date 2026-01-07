# Projet-python_git_linux
# 📈 Quantitative Asset Analysis Platform (Quant A Module)

**Role:** Quant A - Univariate / Single Asset Analysis  
**Context:** Python for Finance & Linux Architecture Project

## 📖 Overview

This module is the **Univariate component** of a collaborative quantitative analysis platform. It is designed to analyze single financial assets (stocks, forex, commodities) by providing real-time data visualization, advanced backtesting engines, and machine learning forecasting tools.

The application allows users to test various trading strategies against a Buy & Hold benchmark and export daily performance reports automatically.

## 🚀 Key Features

### 1. 📊 Interactive Dashboard
* **Real-time Data:** Fetches financial OHLCV data using `yfinance` with optimized caching (TTL 5 min) to respect API rate limits.
* **Dynamic Visualization:** Interactive charts plotting raw asset prices against strategy performance (Cumulative Return).
* **User Controls:** Sidebar widgets to adjust rolling windows, thresholds, and date ranges dynamically.

### 2. 🧠 Algorithmic Strategies
The module includes 4 distinct backtesting strategies:
* **🟢 Buy & Hold:** Benchmark strategy (Baseline performance).
* **🔴 Momentum:** Trend-following logic using Fast/Slow SMA crossovers.
* **🔵 Mean Reversion:** Statistical arbitrage strategy based on Z-Score deviations (> 2σ) from the moving average.
* **🟣 Regime Switching:** A meta-strategy that detects market regimes (Bull/Bear via SMA 200) to switch automatically between Momentum and Mean Reversion logic.

### 3. 📉 Performance Metrics
Automatically calculates professional risk-adjusted metrics:
* **Sharpe Ratio:** Computed using a dynamic Risk-Free Rate fetched from US Treasury Yields (`^TNX`).
* **Max Drawdown:** Measures the maximum observed loss from a peak to a trough.
* **CAGR:** Compound Annual Growth Rate.
* **Volatility:** Annualized standard deviation of returns.

### 4. 🔮 Predictive Modeling (Bonus)
* **Auto-ARIMA:** Implements an automated time-series forecasting model that calibrates parameters $(p,d,q)$ on the fly.
* **Confidence Tunnel:** Visualizes the 95% confidence interval for future price projections (30-day forecast).

### 5. 🤖 Automation (Linux/Cron)
* **Daily Reporter:** Includes a standalone script (`scripts/daily_report.py`) designed to run via CRON.
* **Logging:** Automatically appends key asset metrics (Price, Volatility, Returns) to a local log file every day at a fixed time.

---

## 📂 Project Architecture

The project follows a modular architecture separating data, logic, and visualization.

```text
PROJET_ROOT/
├── app.py                   # Main Streamlit Dashboard entry point
├── config.py                # Global configuration (Constants, Tickers, Params)
├── requirements.txt         # Python dependencies
├── README.md                # Project Documentation
│
├── quant_app/               # Core Python Package
│   ├── __init__.py
│   ├── data/                # Data Access Layer
│   │   ├── market_data.py   # Stock data fetching + Caching
│   │   └── economic_data.py # Macro data (Risk-free rates)
│   │
│   ├── strategies/          # Trading Algorithms
│   │   ├── buy_and_hold.py
│   │   ├── momentum.py
│   │   ├── mean_reversion.py
│   │   └── regime_switching.py
│   │
│   ├── backtesting/         # Performance Analysis
│   │   └── metrics.py       # Math engine for Sharpe, Drawdown, etc.
│   │
│   └── models/              # Machine Learning
│       └── forecasting.py   # ARIMA Model implementation
│
└── scripts/                 # Automation Scripts
    └── daily_report.py      # Standalone script for Cron job