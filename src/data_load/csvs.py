# https://finance.yahoo.com/quote/BTCUSD=X/history?period1=1546300800&period2=1577836800&interval=1d&filter=history&frequency=1d

from multiprocessing.sharedctypes import Value
import pandas as pd


def get_asset_price_history(asset: str, start:str, end: str, fill_weekends: bool = True) -> pd.DataFrame:
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
    
    """
    if fill_weekends:
        # if handling a classic stock and DCA day falls in the weekend/non-working day, move it to the next working day
        
        if "Sunday" not in df.day_of_week.unique():
        
            start_date = df.index.min()
            end_date = df.index.max()
            
            weekend_buffer = []
            for current_day in pd.date_range(start_date, end_date):
                if current_day not in df.index:
                    weekend_buffer.append(current_day)
                else:
                    if len(weekend_buffer):
                        for weekend_day in weekend_buffer:
                            fake_monday_row = df.loc[current_day].copy()
                            fake_monday_row.name = weekend_day
                            fake_monday_row = pd.DataFrame([fake_monday_row])
                            df = pd.concat((df, fake_monday_row))
                        weekend_buffer = []
    """
    
    return df