from .base import InvestmentStrategy
import numpy as np
import pandas as pd

class DCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float):
        self.dca_amount = dca_amount
                
    def apply(self, df: pd.DataFrame) -> pd.Series:
        return pd.Series(self.dca_amount * np.ones(len(df)), index=df.index)