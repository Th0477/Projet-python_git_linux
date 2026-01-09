import yfinance as yf
import pandas as pd


def get_multi_asset_data(tickers, start, end):
    """
    Récupère les prix ajustés de plusieurs actifs.
    Retourne un DataFrame : dates x tickers
    """
    data = yf.download(
        tickers,
        start=start,
        end=end,
        group_by="ticker",
        auto_adjust=False
    )

    # Multi-actifs
    if isinstance(tickers, list) and len(tickers) > 1:
        adj_close = pd.DataFrame(
            {ticker: data[ticker]["Adj Close"] for ticker in tickers}
        )
    else:
        # Mono-actif
        adj_close = data["Adj Close"].to_frame(name=tickers[0])

    return adj_close
