from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TrendRegime(str, Enum):

    TRENDING_BULLISH = (
        "TRENDING_BULLISH"
    )

    TRENDING_BEARISH = (
        "TRENDING_BEARISH"
    )

    SIDEWAYS = (
        "SIDEWAYS"
    )


class VolatilityRegime(
    str,
    Enum,
):

    LOW_VOLATILITY = (
        "LOW_VOLATILITY"
    )

    NORMAL_VOLATILITY = (
        "NORMAL_VOLATILITY"
    )

    HIGH_VOLATILITY = (
        "HIGH_VOLATILITY"
    )


@dataclass(slots=True)
class MarketRegime:

    timestamp: datetime

    trend_regime: TrendRegime

    volatility_regime: VolatilityRegime

    adx_value: float

    atr_value: float