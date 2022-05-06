import pandas as pd
from .base import InvestmentStrategy
from lib.data_load.fear_and_greed import get_fng_data


class MeanFNGDCA(InvestmentStrategy):
    """Combine fear and greed with relative mean
    """
    
    def __init__(self, dca_amount: float):
        self.dca_amount = dca_amount
        
    def categorize_mean(self, relative_mean):
        if relative_mean > 1.5:
            return -1.0
        elif relative_mean > 0.5:
            return -0.5
        elif 0.5 > relative_mean > -0.5:
            return 0.0
        elif relative_mean > -1.5:
            return 0.5
        else:
            return 1.0
        
    def categorize_fng(self, fng_class):
        """Buy more when there's fear, buy less when there's greed
        """
        d = {
            "Extreme Fear": 1.0,
            "Fear": 0.5,
            "Neutral": 0, 
            "Greed": -0.5, 
            "Extreme Greed": -1.0
        }
        return d.get(fng_class, 0.0)
    
    def combine_fng_mean(self, fng, mean):
        fng_cat = fng.apply(lambda x: self.categorize_fng(x))
        mean_cat = mean.apply(lambda x: self.categorize_mean(x))
        return self.dca_amount + self.dca_amount * (fng_cat + mean_cat)
    
    def apply(self, df: pd.DataFrame) -> pd.Series:
        df_tmp = df.assign(relative_mean=(df.close - df.close.rolling(window=30).mean()) / df.close.rolling(window=30).std())
        df_fng = get_fng_data(days=len(df))
        df_tmp = df_tmp.join(df_fng, how="left").copy()
        return self.combine_fng_mean(df_tmp.fng_class, df_tmp.relative_mean)