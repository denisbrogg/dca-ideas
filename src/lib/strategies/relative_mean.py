import pandas as pd
from .base import InvestmentStrategy


class RelativeMean(InvestmentStrategy):
    
    def __init__(self, dca_amount: float):
        self.dca_amount = dca_amount
    
    def relative_mean(self, relative_mean: pd.Series) -> pd.Series:
        return self.dca_amount - self.dca_amount * relative_mean / 3
    
    def apply(self, df: pd.DataFrame) -> pd.Series:
        df_tmp = df.assign(relative_mean=(df.close - df.close.rolling(window=30).mean()) / df.close.rolling(window=30).std())
        return self.relative_mean(df_tmp.relative_mean)

    
class RelativeCategoricalMean(InvestmentStrategy):
    
    def __init__(self, dca_amount: float):
        self.dca_amount = dca_amount
        
    def categorize(self, relative_mean):
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
    
    def relative_mean(self, relative_mean: pd.Series) -> pd.Series:
        relative_mean_categorized = relative_mean.apply(lambda x: self.categorize(x))
        return self.dca_amount + self.dca_amount * relative_mean_categorized
    
    def apply(self, df: pd.DataFrame) -> pd.Series:
        df_tmp = df.assign(relative_mean=(df.close - df.close.rolling(window=30).mean()) / df.close.rolling(window=30).std())
        return self.relative_mean(df_tmp.relative_mean)