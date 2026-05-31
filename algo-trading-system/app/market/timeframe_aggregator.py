from collections import defaultdict
from datetime import datetime

from app.market.models import (
    Candle,
)


class TimeframeAggregator:

    def __init__(self) -> None:

        self.buffers: dict[
            tuple[str, str, datetime],
            list[Candle],
        ] = defaultdict(list)

        self.timeframe_minutes = {
            "5m": 5,
            "15m": 15,
        }

    # =====================================================
    # Public API
    # =====================================================

    def process_candle(
        self,
        candle: Candle,
    ) -> list[Candle]:

        aggregated = []

        # ==========================================
        # Only aggregate from 1m candles
        # ==========================================

        if candle.timeframe != "1m":
            return aggregated

        for timeframe, minutes in (
            self.timeframe_minutes.items()
        ):

            boundary = (
                self._calculate_boundary(
                    timestamp=
                    candle.start_time,

                    timeframe_minutes=
                    minutes,
                )
            )

            key = (
                candle.instrument_key,
                timeframe,
                boundary,
            )

            self.buffers[key].append(
                candle
            )

            # ======================================
            # Wait until candle closes
            # ======================================

            if len(self.buffers[key]) < minutes:
                continue

            aggregated.append(
                self._build_candle(
                    candles=
                    self.buffers[key],

                    timeframe=
                    timeframe,
                )
            )

            del self.buffers[key]

        return aggregated

    # =====================================================
    # Boundary Calculation
    # =====================================================

    def _calculate_boundary(
        self,
        timestamp: datetime,
        timeframe_minutes: int,
    ) -> datetime:

        aligned_minute = (
            timestamp.minute
            //
            timeframe_minutes
        ) * timeframe_minutes

        return timestamp.replace(
            minute=
            aligned_minute,

            second=0,

            microsecond=0,
        )

    # =====================================================
    # Candle Builder
    # =====================================================

    def _build_candle(
        self,
        candles: list[Candle],
        timeframe: str,
    ) -> Candle:

        first = candles[0]

        last = candles[-1]

        return Candle(
            instrument_key=
            first.instrument_key,

            timeframe=
            timeframe,

            open=
            first.open,

            high=
            max(
                candle.high
                for candle in candles
            ),

            low=
            min(
                candle.low
                for candle in candles
            ),

            close=
            last.close,

            volume=
            sum(
                candle.volume
                for candle in candles
            ),

            start_time=
            first.start_time,

            end_time=
            last.end_time,

            is_closed=
            True,
        )