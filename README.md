# Projet-python_git_linux

**Context:** Python for Finance & Linux Architecture Project

**Role:** Quant A
code located in quant_app
# Single Asset
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


**Role:** Quant B
code located in quant_b_app

# Multi-Asset Portfolio Analysis
## Overview

This module is the Multivariate / Portfolio component of a collaborative quantitative finance dashboard.

It extends the single-asset analysis by enabling multi-asset portfolio construction, allocation control, and diversification analysis, all integrated into the same professional Streamlit interface.

## 🚀 Key Features
### 1. 📦 Multi-Asset Portfolio Dashboard

Multi-Asset Selection: Allows simultaneous analysis of at least three financial assets.

Dynamic Portfolio Construction: Users can build portfolios using either equal-weight or custom-weight allocation schemes.

Interactive Controls: Real-time adjustment of asset weights and portfolio composition via Streamlit widgets.

### 2. ⚖️ Portfolio Allocation & Simulation

Equal-Weight Allocation: Automatic uniform distribution across selected assets.

Custom Weights: User-defined asset weights with strict sum-to-one constraint.

Capital Normalization: Portfolio value is normalized to a base of 100 for intuitive performance comparison.

### 3. 📈 Portfolio Performance Visualization

Comparative Time Series: Displays individual asset price evolutions alongside the cumulative portfolio value.

Unified Main Chart: Combines raw asset prices (base 100) and portfolio performance on a single graph.

Visual Diversification Insight: Highlights the smoothing effect of diversification versus single-asset exposure.

### 4. 📐 Portfolio Risk & Diversification Metrics

Computes professional portfolio-level metrics:

Annualized Portfolio Return

Annualized Volatility

Correlation Matrix: Measures inter-asset relationships and diversification benefits.

Asset Count Indicator: Displays portfolio composition size in real time.

### 5. 🔁 Real-Time Updates & Automation

Auto-Refresh: Portfolio data automatically refreshes every 5 minutes.

Robust Weight Handling: Built-in safeguards prevent invalid allocations (e.g., zero-range sliders).

Linux Deployment Ready: Fully compatible with 24/7 execution on a Linux virtual machine.

### 6. 🤝 Integration with Quant A Module

Shared Infrastructure: Reuses the global configuration, date selection, and market data framework.

Metric Reuse: Designed to leverage existing risk metrics from the Quant A backtesting engine where applicable.

Seamless UX: Both Quant A and Quant B modules coexist within a unified Streamlit dashboard.

---
# ⚙️ Technical Implementation & Deployment

This section details the Linux architecture and automation protocols implemented to meet the 24/7 availability requirement.

### 1. ☁️ AWS Cloud Deployment
The application is deployed on a cloud virtual machine to ensure continuous uptime.
* **Provider:** AWS EC2
* **Instance Type:** t2.micro
* **OS:** Ubuntu 24.04 LTS
* **Process Management:** The app runs inside a `tmux` session, allowing it to persist even when SSH connections are closed.
* **Security:** Ports 8501 (Streamlit) and 22 (SSH) are exposed via AWS Security Groups.

### 2. 🔄 Auto-Refresh Logic (Real-Time)
To respect the requirement of refreshing data every 5 minutes while preserving API quotas:
* **Backend (Caching):** We use `@st.cache_data(ttl=300)` on the `get_price` function. This creates a 5-minute buffer where data is served from memory.
* **Frontend (Trigger):** A dedicated logic in `app.py` checks the "Auto-Refresh" toggle. If active, it executes `time.sleep(300)` followed by `st.rerun()`, forcing a cache invalidation and a fresh data fetch.

### 3. ⏰ Cron Job Automation (Daily Reporting)
A purely Linux-based automation handles daily reporting independently of the web dashboard.
* **Script:** `scripts/daily_report.py` (runs independently of Streamlit).
* **Schedule:** Configured via `crontab` to run daily at 20:00.
* **Crontab Configuration:**
    ```bash
    0 20 * * * /usr/bin/python3 /home/ubuntu/Projet-python_git_linux/scripts/daily_report.py >> /home/ubuntu/Projet-python_git_linux/cron.log 2>&1
    ```

### 4. 🛠️ Installation & Setup
1.  **Clone:** `git clone <repo_url>`
2.  **Install:** `pip install -r requirements.txt --break-system-packages`
3.  **Run:** `streamlit run app.py`


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
├── quant_b_app/ 	     # Quant B module
│ ├── portfolio_data.py
│ ├── portfolio_strategy.py
│ └── portfolio_metrics.py
│
└── scripts/                 # Automation Scripts
    └── daily_report.py      # Standalone script for Cron job


