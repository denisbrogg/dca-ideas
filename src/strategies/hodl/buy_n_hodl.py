import pandas as pd
import numpy as np
from strategies.base import InvestmentStrategy


class BuyNHodl(InvestmentStrategy):
    
    def __init__(self, dca_amount: float):
        self.name = "BuyNHodl"
        self.params = {}
        self.dca_amount = dca_amount
        
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
                
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:            
        df_tmp = df.copy()
        lump_sum = self.dca_amount * len(df_tmp)//7
        buydays = np.zeros(len(df_tmp))
        buydays[0] = 1
        df_tmp = df_tmp.assign(buyday=buydays)
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * lump_sum)
        return df_tmp