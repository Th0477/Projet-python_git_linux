# data_loader.py
import yfinance as yf
import pandas as pd

class DataLoader:
    """
    Classe pour récupérer les données financières depuis Yahoo Finance.
    """

    def __init__(self):
        pass  # On pourrait ajouter des configs ici plus tard (API keys, etc.)

    def get_prices(self, tickers, start_date=None, end_date=None):
        """
        Récupère les prix de clôture pour un ou plusieurs tickers.

        Args:
            tickers (str ou list): Symbole(s) des actifs, ex: "AAPL" ou ["AAPL", "MSFT"]
            start_date (str, optional): Date de début 'YYYY-MM-DD'
            end_date (str, optional): Date de fin 'YYYY-MM-DD'

        Returns:
            pandas.DataFrame: Prix de clôture avec les dates comme index
                              et les tickers comme colonnes.
        """
        if isinstance(tickers, str):
            tickers = [tickers]

        all_data = pd.DataFrame()

        for ticker in tickers:
            df = yf.download(ticker, start=start_date, end=end_date)
            if df.empty:
                print(f"Aucune donnée trouvée pour le ticker '{ticker}'")
                continue
            all_data[ticker] = df['Close']

        if all_data.empty:
            raise ValueError("Aucune donnée récupérée pour les tickers fournis.")
