from abc import ABC, abstractmethod
import pandas as pd

class InvestmentStrategy(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.Series:
        pass