# from .fear_and_greed_dca import DummyFNGDCA, DummyRollingFNGDCA, DummyCategoricFNGDCA
from .dca.simple import WeeklyDCA, MonthlyDCA
from .dca.fng import WeeklyFNGDCA, WeeklyCategoricalFNGDCA
from .dca.ta import WeeklyRollingZScoreDCA, WeeklyCategoricalZScoreDCA, WeeklyRSIDCA
from .dca.experimental import WeeklyZFNGDCA