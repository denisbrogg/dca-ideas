import pandas as pd
from strategies.base import InvestmentStrategy


class WeeklyDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, day_of_week: str = 6):
        
        self.week = { 0: "Monday", 1: "Tuesday", 2: "Wednesday",  3: "Thurstday", 4: "Friday", 5: "Saturday", 6: "Sunday", }
        self.name = f"Weekly DCA"
        self.params = {"dca_amount": dca_amount, "day_of_week": day_of_week}
        self.dca_amount = dca_amount
        self.day_of_week = day_of_week
        
        if day_of_week not in self.week.values():
            raise ValueError(f"Day of week not supported. Please choose from {self.week.values()}")
        
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(day_of_week=df_tmp.index.day_name())
        return df_tmp
                
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:            
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(buyday=(df_tmp.day_of_week == self.day_of_week).astype(int))
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * self.dca_amount)
        return df_tmp
    
class MonthlyDCA(InvestmentStrategy):
    
    def __init__(self, dca_amount: float, day_of_month: int = 31):
        self.name = f"Monthly DCA"
        self.params = {"dca_amount": dca_amount, "day_of_month": day_of_month}
        self.dca_amount = dca_amount
        self.day_of_month = day_of_month
        
        self.debug = []
        
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:        
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(dayofmonth=[x.day for x in df_tmp.index])
        df_tmp = df_tmp.assign(daysinmonth=[x.days_in_month for x in df_tmp.index])
        df_tmp = df_tmp.assign(day_of_week=df_tmp.index.day_name())
                
        return df_tmp
                
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        
        def is_buy_day(row):
            if self.day_of_month > row.daysinmonth:
                return row.dayofmonth == row.daysinmonth
            return self.day_of_month == row.dayofmonth
        
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(buyday=df.apply(lambda row: is_buy_day(row), axis=1).astype(int))
        df_tmp = df_tmp.assign(fiat_invested = df_tmp.buyday * self.dca_amount)
        return df_tmp
