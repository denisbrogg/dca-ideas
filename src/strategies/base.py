from abc import ABC, abstractmethod
import pandas as pd

class InvestmentStrategy(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute / collect additional data that will be used by the strategy

        Args:
            df (pd.DataFrame): historical data candles

        Returns:
            pd.DataFrame: historical data with additional information
        """
        pass
    
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply strategy to the historical data

        Args:
            df (pd.DataFrame): output from preprocess()

        Returns:
            pd.DataFrame: determine strategy operations
        """
        pass
    
    def backtest(self, df: pd.DataFrame) -> pd.DataFrame:
        
        if any([c not in df.columns for c in ["buyday", "fiat_invested"]]):
            raise ValueError("fiat_invested not in df.columns")
        
        df_tmp = df.copy()
        df_tmp = df_tmp.assign(asset_position = df_tmp.fiat_invested / df_tmp.Close)
        
        last_price = df_tmp.loc[df_tmp.index.max()].Close
                        
        total_fiat_invested = df_tmp.fiat_invested.sum()
        
        strategy_asset_position = df_tmp.asset_position.sum()
        strategy_fiat_value = strategy_asset_position * last_price
        strategy_fiat_gain_absolute = strategy_fiat_value - total_fiat_invested
        strategy_fiat_gain_percent = strategy_fiat_gain_absolute / total_fiat_invested * 100.0
        strategy_average_asset_price = total_fiat_invested / strategy_asset_position
        
        report = {
            "strategy": self.name,
            "params": self.params,
            "total_operations": df_tmp.buyday.sum(),
            "total_fiat_invested": total_fiat_invested,
            "strategy_asset_position": strategy_asset_position,
            "strategy_fiat_value": strategy_fiat_value,
            "strategy_fiat_gain_absolute": strategy_fiat_gain_absolute,
            "strategy_fiat_gain_percent": strategy_fiat_gain_percent,
            "strategy_average_asset_price": strategy_average_asset_price,           
        }
        
        
        return report