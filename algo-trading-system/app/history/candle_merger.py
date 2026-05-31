from app.history.models import (
    HistoricalCandle,
)


class CandleMerger:
    def merge_candles(
        self,
        historical_candles: list[
            HistoricalCandle
        ],
        database_candles: list[
            HistoricalCandle
        ],
    ) -> list[HistoricalCandle]:

        merged: dict[
            str,
            HistoricalCandle,
        ] = {}

        for candle in (
            historical_candles
            + database_candles
        ):

            key = (
                candle.start_time
                .isoformat()
            )

            merged[key] = candle

        return sorted(
            merged.values(),
            key=lambda candle:
            candle.start_time,
        )