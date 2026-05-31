import pandas as pd
from ta.momentum import RSIIndicator

from app.market.models import Candle


class RSICalculator:
    @staticmethod
    def calculate(
        candles: list[Candle],
        period: int = 14,
    ) -> float | None:
        if len(candles) < period:
            return None

        closes = pd.Series(
            [c.close for c in candles]
        )

        rsi = RSIIndicator(
            close=closes,
            window=period,
        ).rsi()

        return float(rsi.iloc[-1])