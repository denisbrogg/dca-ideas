from .base import InvestmentStrategy
import pandas as pd
from lib.data_load.fear_and_greed import get_fng_data

class DummyFNGDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float):
        self.dca_amount = dca_amount
            
    def dummy_fng_dca(self, fng: pd.Series):
        """Buy more when there's fear, buy less when there's greed
        """
        return self.dca_amount + self.dca_amount * (50 - fng) / 50
    
    def apply(self, df: pd.DataFrame) -> pd.Series:
        df_fng = get_fng_data(days=len(df))
        df_tmp = df.join(df_fng, how="left").copy()
        return self.dummy_fng_dca(df_tmp.fng)
    
class DummyCategoricFNGDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float):
        self.dca_amount = dca_amount
            
    def categorical_fng_dca(self, fng_class: pd.Series):
        """Buy more when there's fear, buy less when there's greed
        """
        fng_class_map = fng_class.map({
            "Extreme Fear": 1,
            "Fear": 0.5,
            "Neutral": 0, 
            "Greed": -0.5, 
            "Extreme Greed": -1
        })
        return self.dca_amount + self.dca_amount * fng_class_map
    
    def apply(self, df: pd.DataFrame) -> pd.Series:
        df_fng = get_fng_data(days=len(df))
        df_tmp = df.join(df_fng, how="left").copy()
        return self.categorical_fng_dca(df_tmp.fng_class)
    
class DummyRollingFNGDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, window: int=7):
        self.dca_amount = dca_amount
        self.window = window
            
    def dummy_fng_dca(self, fng: pd.Series):
        """Buy more when there's fear, buy less when there's greed
        """
        return self.dca_amount + self.dca_amount * (50 - fng) / 50
    
    def apply(self, df: pd.DataFrame) -> pd.Series:
        df_fng = get_fng_data(days=len(df))
        df_tmp = df.join(df_fng, how="left").copy()
        
        rolling_fng = df_tmp.fng.rolling(window=self.window).mean().values
        rolling_fng[:(self.window-1)] = df_tmp.fng.values[:(self.window-1)]
        
        return self.dummy_fng_dca(pd.Series(rolling_fng, index=df_tmp.index))

