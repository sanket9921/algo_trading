from datetime import datetime, timedelta, timezone

from app.core.logger import get_logger
from app.market.models import Candle, Tick

logger = get_logger(__name__)


class CandleEngine:
    def __init__(self) -> None:
        self.current_candles: dict[
            tuple[str, str],
            Candle,
        ] = {}

    def process_tick(
        self,
        tick: Tick,
        timeframe_minutes: int = 5,
    ) -> Candle | None:
        candle_start = self._get_candle_start(
            tick.timestamp,
            timeframe_minutes,
        )

        candle_end = (
            candle_start +
            timedelta(minutes=timeframe_minutes)
        )

        key = (
            tick.instrument_key,
            str(timeframe_minutes),
        )

        current_candle = self.current_candles.get(key)

        if current_candle is None:
            candle = Candle(
                instrument_key=tick.instrument_key,
                timeframe=f"{timeframe_minutes}m",
                open=tick.last_price,
                high=tick.last_price,
                low=tick.last_price,
                close=tick.last_price,
                volume=tick.volume,
                start_time=candle_start,
                end_time=candle_end,
            )

            self.current_candles[key] = candle

            logger.info(
                "new_candle_created",
                instrument_key=tick.instrument_key,
                timeframe=f"{timeframe_minutes}m",
            )

            return None

        if tick.timestamp >= current_candle.end_time:
            closed_candle = current_candle

            closed_candle.is_closed = True

            new_candle = Candle(
                instrument_key=tick.instrument_key,
                timeframe=f"{timeframe_minutes}m",
                open=tick.last_price,
                high=tick.last_price,
                low=tick.last_price,
                close=tick.last_price,
                volume=tick.volume,
                start_time=candle_start,
                end_time=candle_end,
            )

            self.current_candles[key] = new_candle

            logger.info(
                "candle_closed",
                instrument_key=closed_candle.instrument_key,
                close=closed_candle.close,
            )

            return closed_candle

        current_candle.high = max(
            current_candle.high,
            tick.last_price,
        )

        current_candle.low = min(
            current_candle.low,
            tick.last_price,
        )

        current_candle.close = tick.last_price

        current_candle.volume += tick.volume

        return None

    @staticmethod
    def _get_candle_start(
        timestamp: datetime,
        timeframe_minutes: int,
    ) -> datetime:
        minute = (
            timestamp.minute //
            timeframe_minutes
        ) * timeframe_minutes

        return timestamp.replace(
            minute=minute,
            second=0,
            microsecond=0,
            tzinfo=timezone.utc,
        )