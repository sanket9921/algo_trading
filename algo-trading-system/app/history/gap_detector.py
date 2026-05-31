from app.history.models import (
    HistoricalCandle,
)


class GapDetector:
    def calculate_missing_candles(
        self,
        existing_candles: list[
            HistoricalCandle
        ],
        required_count: int,
    ) -> int:

        existing_count = len(
            existing_candles
        )

        if (
            existing_count
            >= required_count
        ):
            return 0

        return (
            required_count
            - existing_count
        )