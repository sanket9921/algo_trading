import pandas as pd

from app.market.models import Candle


class EMACalculator:
    @staticmethod
    def calculate(
        candles: list[Candle],
        period: int,
    ) -> float | None:
        if len(candles) < period:
            return None

        closes = pd.Series(
            [c.close for c in candles]
        )

        ema = closes.ewm(
            span=period,
            adjust=False,
        ).mean()

        return float(ema.iloc[-1])