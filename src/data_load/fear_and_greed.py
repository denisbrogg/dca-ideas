import requests
import pandas as pd


def get_fng_data(days: int) -> pd.DataFrame:
    api_url = f"https://api.alternative.me/fng/?limit={days}&date_format=us"
    raw = requests.get(api_url)
    df = pd.DataFrame(raw.json()["data"])
    df = df.assign(Date=pd.to_datetime(df.timestamp))
    df = df.assign(FNG=pd.to_numeric(df.value))
    df = df.assign(FNGClass=df.value_classification)
    df = df[["Date", "FNG", "FNGClass"]]
    df.set_index("Date", inplace=True)
    return df