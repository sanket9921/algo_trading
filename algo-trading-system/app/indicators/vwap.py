import pandas as pd

from app.market.models import (
    Candle,
)


class VWAPCalculator:

    @staticmethod
    def calculate(
        candles: list[Candle],
    ) -> float | None:

        if not candles:
            return None

        dataframe = pd.DataFrame(
            {
                "high": [
                    c.high
                    for c in candles
                ],

                "low": [
                    c.low
                    for c in candles
                ],

                "close": [
                    c.close
                    for c in candles
                ],

                "volume": [
                    c.volume
                    for c in candles
                ],
            }
        )

        # ======================================
        # Prevent invalid VWAP
        # ======================================

        total_volume = (
            dataframe["volume"]
            .sum()
        )

        if total_volume <= 0:
            return None

        typical_price = (
            dataframe["high"]
            +
            dataframe["low"]
            +
            dataframe["close"]
        ) / 3

        cumulative_tpv = (
            typical_price
            *
            dataframe["volume"]
        ).cumsum()

        cumulative_volume = (
            dataframe["volume"]
        ).cumsum()

        # ======================================
        # Safe division
        # ======================================

        vwap = (
            cumulative_tpv
            /
            cumulative_volume
        )

        latest_vwap = (
            vwap.iloc[-1]
        )

        if pd.isna(
            latest_vwap
        ):
            return None

        return float(
            latest_vwap
        )