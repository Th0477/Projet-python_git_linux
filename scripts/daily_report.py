#scripts/daily_reports
import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from quant_app.data.market_data import get_price 
from quant_app.strategies.buy_and_hold import buy_and_hold
from quant_app.backtesting.metrics import compute_metrics
import config

# Parameters
TARGET_TICKER = config.DEFAULT_TICKER 
REPORT_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'daily_reports.txt')

def run_daily_job():
    print(f"⏰ Starting computation for the report of : {datetime.datetime.now()}")
    
    # 1. Dates
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365)
    
    try:
        # 2. Download
        print(f"📥 Downloading data for {TARGET_TICKER}...")
        df = get_price(TARGET_TICKER, str(start_date), str(today))
        
        if df.empty:
            print("⚠️ Error : No data.")
            return

        # 3. COmputation
        current_price = df.iloc[-1]
        
        # B&H simulation to have the metrics
        cum_bh = buy_and_hold(df)
        metrics = compute_metrics(cum_bh)
        
        # 4. Report writing
        with open(REPORT_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n========================================\n")
            f.write(f"📅 DAILY REPORT - {today}\n")
            f.write(f"========================================\n")
            f.write(f"🔹 Asset            : {TARGET_TICKER}\n")
            f.write(f"💰 Closing price  : {current_price:.2f} $\n")
            f.write(f"📈 Performance (1Y) : {metrics.get('Total Return', 'N/A')}\n")
            f.write(f"📉 Max Drawdown     : {metrics.get('Max Drawdown', 'N/A')}\n")
            f.write(f"📊 Volatility       : {metrics.get('Volatility', 'N/A')}\n")
            f.write(f"----------------------------------------\n")
            
        print(f"✅ Report wrote with success in {REPORT_FILE_PATH}")
        
    except Exception as e:
        print(f"❌ Critical Error : {e}")

if __name__ == "__main__":
    run_daily_job()