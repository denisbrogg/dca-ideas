import talib as ta
import pandas as pd
from strategies.base import InvestmentStrategy


class WeeklyRollingZScoreDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, day_of_week: str = 6):
        
        self.week = { 0: "Monday", 1: "Tuesday", 2: "Wednesday",  3: "Thurstday", 4: "Friday", 5: "Saturday", 6: "Sunday", }
        self.name = f"Weekly Z-Score DCA"
        self.params = {"dca_amount": dca_amount, "day_of_week": day_of_week}
        self.dca_amount = dca_amount
        self.day_of_week = day_of_week
        
        if day_of_week not in self.week.values():
            raise ValueError(f"Day of week not supported. Please choose from {self.week.values()}")
        
    def zscore_contribution(self, zscore: pd.Series) -> pd.Series:
        """Buy more when price is unusually low wrt to previous 30 days, buy less when price is unusually high
        If absolute Z-score value of a sample is above 3, it is considered to be an outlier.
        """
        return -1 * self.dca_amount * zscore / 3
                
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        rolling_z_score = (df_tmp.Close - df_tmp.Close.rolling(window=30).mean()) / df_tmp.Close.rolling(window=30).std()
        rolling_z_score = rolling_z_score.fillna(0)
        df_tmp = df_tmp.assign(rolling_z_score=rolling_z_score)
        df_tmp = df_tmp.assign(day_of_week=df_tmp.index.day_name())
        return df_tmp
                    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:            
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(buyday=(df_tmp.day_of_week == self.day_of_week).astype(int))
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * (self.dca_amount + self.zscore_contribution(df_tmp.rolling_z_score)))
        
        return df_tmp
    
class WeeklyCategoricalZScoreDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, day_of_week: str = 6):
        
        self.week = { 0: "Monday", 1: "Tuesday", 2: "Wednesday",  3: "Thurstday", 4: "Friday", 5: "Saturday", 6: "Sunday", }
        self.name = f"Weekly Categorical Z-Score DCA"
        self.params = {"dca_amount": dca_amount, "day_of_week": day_of_week}
        self.dca_amount = dca_amount
        self.day_of_week = day_of_week
        
        if day_of_week not in self.week.values():
            raise ValueError(f"Day of week not supported. Please choose from {self.week.values()}")
        
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
        
    def zscore_contribution(self, zscore: pd.Series) -> pd.Series:
        """Buy more when price is unusually low wrt to previous 30 days, buy less when price is unusually high
        If absolute Z-score value of a sample is above 3, it is considered to be an outlier.
        """
        return -1 * self.dca_amount * zscore.apply(lambda x: self.categorize(x))
                
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        rolling_z_score = (df_tmp.Close - df_tmp.Close.rolling(window=30).mean()) / df_tmp.Close.rolling(window=30).std()
        rolling_z_score = rolling_z_score.fillna(0)
        df_tmp = df_tmp.assign(rolling_z_score=rolling_z_score)
        df_tmp = df_tmp.assign(day_of_week=df_tmp.index.day_name())
        return df_tmp
                    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(buyday=(df_tmp.day_of_week == self.day_of_week).astype(int))
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * (self.dca_amount + self.zscore_contribution(df_tmp.rolling_z_score)))
        
        return df_tmp
    
    
class WeeklyRSIDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, day_of_week: str = 6):
        
        self.week = { 0: "Monday", 1: "Tuesday", 2: "Wednesday",  3: "Thurstday", 4: "Friday", 5: "Saturday", 6: "Sunday", }
        self.name = f"Weekly RSI DCA"
        self.params = {"dca_amount": dca_amount, "day_of_week": day_of_week}
        self.dca_amount = dca_amount
        self.day_of_week = day_of_week
        
        if day_of_week not in self.week.values():
            raise ValueError(f"Day of week not supported. Please choose from {self.week.values()}")
                
    def categorize(self, rsi_value):
        if rsi_value > 10:
            return 1
        elif rsi_value > 30:
            return 0.5
        elif rsi_value < 90:
            return -1
        elif rsi_value < 70:
            return -0.5
        else:
            return 0
                
    def rsi_contribution(self, rsi: pd.Series) -> pd.Series:
        """Buy more when price is unusually low wrt to previous 30 days, buy less when price is unusually high
        If absolute Z-score value of a sample is above 3, it is considered to be an outlier.
        """
        return self.dca_amount * rsi.apply(lambda x: self.categorize(x))
                
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(rsi=ta.RSI(df.Close).fillna(50.0))
        df_tmp = df_tmp.assign(day_of_week=df_tmp.index.day_name())
        return df_tmp
                    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(buyday=(df_tmp.day_of_week == self.day_of_week).astype(int))
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * (self.dca_amount + self.rsi_contribution(df_tmp.rsi)))
        
        return df_tmp
    