import asyncio

from datetime import (
    datetime,
    timezone,
)

from app.core.logger import (
    get_logger,
)

from app.events.event_bus import (
    EventBus,
)

from app.events.event_models import (
    CandleClosedEvent,
)

from app.history.database_loader import (
    DatabaseCandleLoader,
)

from app.market.models import (
    Candle,
)

logger = get_logger(__name__)


class ReplayRuntime:

    def __init__(
        self,
        event_bus: EventBus,
        replay_speed: float,
        replay_candle_limit: int,
    ) -> None:

        self.event_bus = event_bus

        self.replay_speed = (
            replay_speed
        )

        self.replay_candle_limit = (
            replay_candle_limit
        )

        self.loader = (
            DatabaseCandleLoader()
        )

    async def replay_market(
        self,
        instrument_key: str,
    ) -> None:

        logger.info(
            "replay_started",
            instrument_key=
            instrument_key,
        )

        candles = (
            await self.loader
            .load_recent_candles(
                instrument_key=
                instrument_key,

                limit=self.replay_candle_limit,
            )
        )

        logger.info(
            "replay_candles_loaded",
            candles_count=
            len(candles),
        )

        for candle in candles:

            await self.event_bus.publish(
                CandleClosedEvent(
                    timestamp=datetime.now(
                        tz=timezone.utc,
                    ),

                    candle=Candle(
                        instrument_key=
                        candle.instrument_key,

                        timeframe=
                        candle.timeframe,

                        open=
                        candle.open,

                        high=
                        candle.high,

                        low=
                        candle.low,

                        close=
                        candle.close,

                        volume=
                        candle.volume,

                        start_time=
                        candle.start_time,

                        end_time=
                        candle.end_time,

                        is_closed=
                        candle.is_closed,
                    ),
                )
            )

            logger.info(
                "replay_candle_emitted",
                timestamp=
                candle.start_time,
                close=
                candle.close,
            )

            await asyncio.sleep(
                self.replay_speed
            )

        logger.info(
            "replay_completed",
        )