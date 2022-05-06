import requests
import pandas as pd


def get_fng_data(days=365*3):
    api_url = f"https://api.alternative.me/fng/?limit={days}&date_format=us"
    raw = requests.get(api_url)
    df = pd.DataFrame(raw.json()["data"])
    df = df.assign(date=pd.to_datetime(df.timestamp))
    df = df.assign(fng=pd.to_numeric(df.value))
    df = df.assign(fng_class=df.value_classification)
    df = df[["date", "fng", "fng_class"]]
    df.set_index("date", inplace=True)
    return df