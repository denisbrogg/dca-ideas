import pandas as pd

days_of_week = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thurstday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

def get_btcusdt_data(start:str, end: str):
    
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    
    df = pd.read_csv("../data/Binance_BTCUSDT_d.csv")
    df["date"] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    
    df = df.assign(dayofweek=[days_of_week[x.dayofweek] for x in df.index])
    df = df[(df.index >= start) & (df.index <= end)]
    
    return df