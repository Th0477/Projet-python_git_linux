import yfinance as yf
import pandas as pd

def get_price(ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    Récupère les prix de clôture pour un ticker donné.

    Args:
        ticker (str): Symbole de l'action, ex: "AAPL"
        start_date (str, optional): Date de début au format 'YYYY-MM-DD'
        end_date (str, optional): Date de fin au format 'YYYY-MM-DD'

    Returns:
        pandas.DataFrame: DataFrame avec les dates comme index et une colonne pour le ticker
    """
    # Télécharger les données depuis Yahoo Finance
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

    if df.empty:
        print(f"Aucune donnée trouvée pour le ticker '{ticker}' entre {start_date} et {end_date}.")
        return pd.DataFrame()

    # Extraire les prix de clôture et s'assurer que c'est un DataFrame
    close_data = df['Close']
    if isinstance(close_data, pd.Series):
        df_close = close_data.to_frame(name=ticker)
    else:
        df_close = close_data.copy()

    return df_close


