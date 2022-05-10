# https://finance.yahoo.com/quote/BTCUSD=X/history?period1=1546300800&period2=1577836800&interval=1d&filter=history&frequency=1d

from multiprocessing.sharedctypes import Value
import pandas as pd


def get_asset_price_history(asset: str, start:str, end: str):
    """Load asset data from csv for offline analysis
    """
    
    if asset not in ["BTC", "ETH", "TSLA", "AMZN"]:
        raise ValueError("Asset not supported. Please choose from BTC, ETH, TSLA, AMZN")
    
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    
    df = pd.read_csv(f"../data/{asset}.csv")
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index('Date')
        
    df = df[(df.index >= start) & (df.index <= end)]
    
    return df