import pandas as pd
import pmdarima as pm
from datetime import timedelta

def forecast_arima(price_series, n_days=30):
    """
    Train an Auto-ARIMA model on the price series and forecast the future n_days
    """
    
    # 1. Configuration and training of the Auto-ARIMA
    model = pm.auto_arima(price_series, 
                          start_p=1, start_q=1,
                          max_p=5, max_q=5, 
                          d=None,           
                          seasonal=False,   
                          stepwise=True,
                          suppress_warnings=True, 
                          error_action="ignore",
                          trace=False)

    # 2. Forecasting with a confidence interval
    forecast, conf_int = model.predict(n_periods=n_days, return_conf_int=True, alpha=0.05)
    
    # 3. Generation of the future dates for the index
    last_date = price_series.index[-1]
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=n_days)
    
    # 4. Results
    forecast_values = forecast.values if hasattr(forecast, 'values') else forecast
    forecast_df = pd.DataFrame({
        "Forecast": forecast_values,       
        "Lower_CI": conf_int[:, 0],
        "Upper_CI": conf_int[:, 1]
    }, index=future_dates)
    
    # We keep the order to show it
    model_desc = str(model.order) 
    
    return forecast_df, model_desc