import pandas as pd
from strategies.base import InvestmentStrategy
from data_load.fear_and_greed import get_fng_data
from strategies.dca.fng import WeeklyCategoricalFNGDCA
from strategies.dca.ta import WeeklyCategoricalZScoreDCA

class WeeklyZFNGDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, day_of_week: str = 6):
        self.name = "Weekly Z+FNG DCA"
        self.dca_amount = dca_amount
        self.params = {"dca_amount": dca_amount, "day_of_week": day_of_week}
        self.day_of_week = day_of_week
        self.fng_strategy = WeeklyCategoricalFNGDCA(dca_amount, day_of_week)
        self.zscore_strategy = WeeklyCategoricalZScoreDCA(dca_amount, day_of_week)
        
        
    def combined_contribution(self, fng: pd.Series, zscore:pd.Series) -> pd.Series:
        """Buy more when there's fear, buy less when there's greed
        """
        contribution = self.fng_strategy.fng_contribution(fng) + self.zscore_strategy.zscore_contribution(zscore)
        return contribution.fillna(0.0)
                
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        df_tmp = self.fng_strategy.preprocess(df_tmp)
        df_tmp = self.zscore_strategy.preprocess(df_tmp)
        return df_tmp
                    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:            
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(buyday=(df_tmp.day_of_week == self.day_of_week).astype(int))
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * (self.dca_amount + self.combined_contribution(df_tmp.FNGClass, df_tmp.rolling_z_score)))
        
        return df_tmp
