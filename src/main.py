import pandas as pd
import numpy as np

from data_load.csvs import get_btcusdt_data
from strategies import DummyFNGDCA, DummyRollingFNGDCA

START = "2020-01-01"
END = "2022-05-01"
WEEKLY_INVESTMENT = 100
PRICE_TODAY = 39_500

df = get_btcusdt_data(START, END)

df = df.assign(dummy_fng_dca=DummyFNGDCA(WEEKLY_INVESTMENT).apply(df))
df = df.assign(dummy_rolling_fng_dca=DummyRollingFNGDCA(WEEKLY_INVESTMENT, 7).apply(df))

def test_strategy(column_name, price_today):
    
    print(f"{column_name} strategy:")
    
    results = []
    
    for day_of_week, df_dow in df.groupby("dayofweek"):
        
        df_dow = df_dow.assign(cripto_obtained=df_dow[column_name] / df_dow.close)
        
        results.append({
            "dayofweek": day_of_week,
            "fiat_invested": df_dow[column_name].sum(),
            "btc_obtained": df_dow.cripto_obtained.sum(),
            "fiat_value": df_dow.cripto_obtained.sum() * price_today,        
        
    })
    
    df_results = pd.DataFrame(results)
    
    df_results = df_results.assign(performance=100.0 * df_results.fiat_value / df_results.fiat_invested)
    
    return df_results

print(test_strategy("dummy_fng_dca", PRICE_TODAY))
print("______________________________________________________________")
print(test_strategy("dummy_rolling_fng_dca", PRICE_TODAY))