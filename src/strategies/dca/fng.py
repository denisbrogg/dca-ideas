import pandas as pd
from strategies.base import InvestmentStrategy
from data_load.fear_and_greed import get_fng_data


class WeeklyFNGDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, day_of_week: str = 6):
        
        self.week = { 0: "Monday", 1: "Tuesday", 2: "Wednesday",  3: "Thurstday", 4: "Friday", 5: "Saturday", 6: "Sunday", }
        self.name = f"Weekly FNG DCA"
        self.params = {"dca_amount": dca_amount, "day_of_week": day_of_week}
        self.dca_amount = dca_amount
        self.day_of_week = day_of_week
        
        if day_of_week not in self.week.values():
            raise ValueError(f"Day of week not supported. Please choose from {self.week.values()}")
        
    def fng_contribution(self, fng: pd.Series) -> pd.Series:
        """Buy more when there's fear, buy less when there's greed
        """
        return self.dca_amount * (50 - fng) / 50
                
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        if "FNG" not in df_tmp.columns:
            df_fng = get_fng_data(days=len(df))
            df_tmp = df_tmp.join(df_fng, how="left").copy()
            df_tmp = df_tmp.assign(FNG=df_tmp.FNG.fillna(50.0))
            df_tmp = df_tmp.assign(FNGClass=df_tmp.FNGClass.fillna("Neutral"))
            df_tmp = df_tmp.assign(day_of_week=df_tmp.index.day_name())
        return df_tmp
                    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(buyday=(df_tmp.day_of_week == self.day_of_week).astype(int))
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * (self.dca_amount + self.fng_contribution(df_tmp.FNG)))
        
        return df_tmp
    
    
class WeeklyCategoricalFNGDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, day_of_week: str = 6):
        
        self.week = { 0: "Monday", 1: "Tuesday", 2: "Wednesday",  3: "Thurstday", 4: "Friday", 5: "Saturday", 6: "Sunday", }
        self.name = f"Weekly FNG Categorical DCA"
        self.params = {"dca_amount": dca_amount, "day_of_week": day_of_week}
        self.dca_amount = dca_amount
        self.day_of_week = day_of_week
        
        if day_of_week not in self.week.values():
            raise ValueError(f"Day of week not supported. Please choose from {self.week.values()}")
        
    def fng_contribution(self, fngclass: pd.Series) -> pd.Series:
        """Buy more when there's fear, buy less when there's greed
        """
        fng_class_map = fngclass.map({
            "Extreme Fear": 1,
            "Fear": 0.5,
            "Neutral": 0, 
            "Greed": -0.5, 
            "Extreme Greed": -1
        })
        return self.dca_amount * fng_class_map
                
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        if "FNG" not in df_tmp.columns:
            df_fng = get_fng_data(days=len(df))
            df_tmp = df_tmp.join(df_fng, how="left").copy()
            df_tmp = df_tmp.assign(FNG=df_tmp.FNG.fillna(50.0))
            df_tmp = df_tmp.assign(FNGClass=df_tmp.FNGClass.fillna("Neutral"))
            df_tmp = df_tmp.assign(day_of_week=df_tmp.index.day_name())
        return df_tmp
                    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        
        # Classic stocks do not have weekend data
        if self.day_of_week not in df.day_of_week.unique():
            self.day_of_week = "Monday"
            
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(buyday=(df_tmp.day_of_week == self.day_of_week).astype(int))
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * (self.dca_amount + self.fng_contribution(df_tmp.FNGClass)))
        
        return df_tmp
