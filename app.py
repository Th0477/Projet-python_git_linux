#app.py
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import config
import time
from quant_app.data.market_data import get_price
from quant_app.data.economic_data import get_risk_free_rate
from quant_app.strategies import buy_and_hold, momentum, mean_reversion, regime_switching
from quant_app.backtesting import metrics
from quant_app.models import forecasting

#import quant b functions
from quant_b_app.portfolio_data import get_multi_asset_data
from quant_b_app.portfolio_strategy import (
    compute_returns,
    compute_portfolio_returns,
    compute_portfolio_value
)
from quant_b_app.portfolio_metrics import (
    portfolio_volatility,
    portfolio_return,
    correlation_matrix
)

# Streamlit configuration
st.set_page_config(layout="wide")
st.title(config.APP_TITLE)

mode = st.radio(
    "Choose analysis mode",
    ["Single Asset (Quant A)", "Portfolio (Quant B)"]
)

if "last_mode" not in st.session_state:
    st.session_state.last_mode = mode

if st.session_state.last_mode != mode:
    st.session_state.clear()
    st.session_state.last_mode = mode
    st.rerun()


selected_assets = []
weights = {}

# Layout 
col_left, col_right = st.columns([3, 1], gap="large")

# Rigth column : Parameters
with col_right: 
    params_placeholder = st.empty()
    with params_placeholder.container():
        st.header("⚙️ Parameters")
        auto_refresh = st.checkbox("🔄 Auto-Refresh (5 min)", value=True)
        st.markdown("---")
        # Dates
        start_date = st.date_input("Start Date", config.DEFAULT_START_DATE)
        end_date = st.date_input("End Date", config.DEFAULT_END_DATE)
        if mode == "Portfolio (Quant B)":
            st.subheader("📦 Portfolio parameters")

            selected_assets = st.multiselect(
                "Select assets",
                options=config.PORTFOLIO_TICKERS,
                default=config.PORTFOLIO_TICKERS[:3],
                key="quant_b_assets"
            )

            weight_mode = st.radio(
                "Weighting scheme",
                ["Equal weights", "Custom weights"],
                key="quant_b_weight_mode"
            )

            if selected_assets:
                    if weight_mode == "Equal weights":
                        w = 1 / len(selected_assets)
                        weights = {asset: w for asset in selected_assets}

                    else:
                        st.caption("Custom asset weights (must sum to 1)")
                        remaining = 1.0

                        for i, asset in enumerate(selected_assets):
                            if i < len(selected_assets) - 1:
                                max_weight=round(remaining, 4)
                                if max_weight <= 0:
                                    weights[asset]=0.0
                                else:
                                    weights[asset]=st.slider(
                                        f"Weight {asset}",
                                        0.0,
                                        max_weight,
                                        max_weight,
                                        key=f"weight_{asset}"
                                    )
                                remaining-=weights[asset]
                            else:
                                weights[asset] = round(remaining, 4)

                        st.write("Final weights:", weights)

        elif mode == "Single Asset (Quant A)" :
            ticker = st.text_input("Ticker :", config.DEFAULT_TICKER, key="quant_a_ticker")
            
            st.markdown("---")
            st.subheader("Strategies")
            
            # Momentum Parameters
            st.caption("Momentum")
            mom_fast = st.slider("Fast Window", 5, 50, config.MOMENTUM_WINDOW_FAST, key="mom_fast")
            mom_slow = st.slider("Slow Window", 20, 200, config.MOMENTUM_WINDOW_SLOW, key="mom_slow")
            
            # Mean Reversion Parameters
            st.caption("Mean Reversion")
            mr_window = st.slider("Window", 10, 50, config.MEAN_REVERSION_WINDOW, key="mr_window")
            mr_thresh = st.slider("Threshold", 1.0, 4.0, config.MEAN_REVERSION_THRESHOLD, step=0.1, key="mr_thresh")
            
            # Regime Switching Parameters
            st.caption("Regime Switching")
            rs_trend = st.slider("Trend Filter", 100, 300, config.REGIME_TREND_WINDOW, key="rs_trend")

            # Forecast
            st.markdown("---")
            st.header("Auto-ARIMA Forecast")
            enable_forecast = st.checkbox("Enable the ARIMA forecasting", key="enable_forecast")
            forecast_days = st.slider("Forecast horizon (days)", 7, 90, 30, key="forecast_days")

        fetch_data = st.button("Start the analysis", type="primary")

# Left column : Results
with col_left:
    if fetch_data and mode=="Single Asset (Quant A)":
        try:
            # 1. Data laoding
            with st.spinner('Téléchargement des données...'):
                df = get_price(ticker, str(start_date), str(end_date))

            current_rf = get_risk_free_rate()
            st.info(f"ℹ️ Risk free rate (US 10Y) : {current_rf:.2%}")

            if df.empty:
                st.warning("⚠️ No data available. Check the ticker or the dates.")
            else:
                st.success(f"Data fetched for {ticker} ({len(df)} days)")
            

                # 2. Strategies computation
                cum_bh = buy_and_hold.buy_and_hold(df)
                cum_mom = momentum.momentum(df, window_fast=mom_fast, window_slow=mom_slow)
                cum_mr = mean_reversion.mean_reversion(df, window=mr_window, threshold=mr_thresh)
                cum_rs = regime_switching.regime_switching(df, trend_window=rs_trend, mom_window=mom_fast, mr_window=mr_window, mr_threshold=mr_thresh)

                # 3. Metrics computation
                st.subheader("🏆 Performance comparison")
                
                strategies_data = {
                    "Buy & Hold": metrics.compute_metrics(cum_bh),
                    "Momentum": metrics.compute_metrics(cum_mom),
                    "Mean Reversion": metrics.compute_metrics(cum_mr),
                    "Regime Switching": metrics.compute_metrics(cum_rs)
                }
                
                metrics_df = pd.DataFrame(strategies_data).T 
                st.table(metrics_df)

                # 4. Graphic visualization
                st.subheader("📈 Évolution du Portefeuille (Base 1.0)")
                
                fig2, ax2 = plt.subplots(figsize=(12, 6))

                ax2.plot(cum_bh.index, cum_bh[ticker], label="Buy & Hold", color="green", linewidth=2, alpha=0.6)
                ax2.plot(cum_mom.index, cum_mom[ticker], label="Momentum", color="red", linewidth=1.5)
                ax2.plot(cum_mr.index, cum_mr[ticker], label="Mean Reversion", color="blue", linewidth=1.5)
                ax2.plot(cum_rs.index, cum_rs[ticker], label="Regime Switching", color="purple", linewidth=1.5) 
                
                ax2.set_ylabel("Portfolio value")
                ax2.set_title(f"Comparative Performance : {ticker}")
                ax2.legend()
                ax2.grid(True, linestyle='--', alpha=0.3)
                
                st.pyplot(fig2)

                # 5. Gross price
                with st.expander("See the gross price chart"):
                    fig1, ax1 = plt.subplots(figsize=(12, 4))
                    ax1.plot(df.index, df[ticker], color="black", linewidth=1)
                    ax1.set_title(f"{ticker} Stock price")
                    ax1.grid(True, alpha=0.3)
                    st.pyplot(fig1)

                # ARIMA Forecasting
                if enable_forecast:
                    with st.spinner(f"Auto-ARIMA model calibration in progress..."):
                        price_series = df[ticker]
                        
                        # 1. Prediction computing
                        pred_df, model_order = forecasting.forecast_arima(price_series, n_days=forecast_days)
                        
                        st.success(f"Calibrated model : ARIMA{model_order}")

                        # Prediction graphic
                        st.subheader(f"ARIMA prediction at {forecast_days} days")
                        fig_pred, ax_pred = plt.subplots(figsize=(12, 5))
                        
                        # Historical data
                        display_hist = price_series.iloc[-180:]
                        
                        last_real_date = display_hist.index[-1]
                        last_real_price = display_hist.iloc[-1]
                        
                        plot_pred_dates = [last_real_date] + list(pred_df.index)
                        plot_pred_values = [last_real_price] + list(pred_df['Forecast'])
                        
                        plot_lower = [last_real_price] + list(pred_df['Lower_CI'])
                        plot_upper = [last_real_price] + list(pred_df['Upper_CI'])

                        # 2. Tracing historic
                        ax_pred.plot(display_hist.index, display_hist, label="Historic", color="black", linewidth=1.5)
                        
                        # 3. Tracing prediction
                        ax_pred.plot(plot_pred_dates, plot_pred_values, label="Prediction", color="darkorange", linestyle="-", linewidth=2)
                        
                        # 4. Confidence interval
                        ax_pred.fill_between(plot_pred_dates, 
                                             plot_lower, 
                                             plot_upper, 
                                             color='orange', alpha=0.2, label="Intervalle de Confiance (95%)")
                        
                        ax_pred.set_title(f"Projection du prix {ticker} (Modèle ARIMA {model_order})")
                        ax_pred.legend(loc="upper left")
                        ax_pred.grid(True, linestyle='--', alpha=0.3)
                        
                        st.pyplot(fig_pred)

        except Exception as e:
            st.error(f"An error occured : {e}")


    if fetch_data and mode=="Portfolio (Quant B)" and selected_assets:
        st.subheader("Portfolio Performance")
        # 1. Data
        prices = get_multi_asset_data(
        selected_assets,
        str(start_date),
        str(end_date)
        )

        # 2. Returns
        returns = compute_returns(prices)

        # 3. Portfolio returns
        port_ret = compute_portfolio_returns(returns, weights)

        # 4. Portfolio value (base 100)
        port_val = compute_portfolio_value(port_ret)

        fig, ax = plt.subplots(figsize=(12, 6))

        # Assets
        for asset in selected_assets:
            ax.plot(
                prices.index,
                prices[asset] / prices[asset].iloc[0] * 100,
                alpha=0.5,
                label=asset
            )

        # Portfolio
        ax.plot(
            port_val.index,
            port_val,
            color="black",
            linewidth=2.5,
            label="Portfolio"
        )

        ax.set_title("Multi-Asset Portfolio vs Individual Assets (Base 100)")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.3)

        st.pyplot(fig)

        st.subheader("📐 Portfolio Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Annual Return", f"{portfolio_return(port_ret):.2%}")

        with col2:
            st.metric("Volatility", f"{portfolio_volatility(port_ret):.2%}")

        with col3:
            st.metric("Nb Assets", len(selected_assets))

        st.subheader("🔗 Correlation Matrix")
        corr = correlation_matrix(returns)
        st.dataframe(corr)
# Automated refresh every 5min
if auto_refresh:
    time.sleep(300)
    st.rerun





