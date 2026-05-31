import asyncio
from datetime import datetime, timezone

from app.core.logger import get_logger
from app.events.event_bus import EventBus
from app.events.event_models import (
    CandleClosedEvent,
)
from app.market.models import Candle

logger = get_logger(__name__)


class ReplayEngine:
    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self.event_bus = event_bus

    async def replay_candles(
        self,
        candles: list[Candle],
        replay_speed: float = 0.01,
    ) -> None:

        logger.info(
            "backtest_replay_started",
            candles_count=len(candles),
        )

        for candle in candles:
            await self.event_bus.publish(
                CandleClosedEvent(
                    timestamp=datetime.now(
                        tz=timezone.utc,
                    ),
                    candle=candle,
                )
            )

            await asyncio.sleep(
                replay_speed
            )

        logger.info(
            "backtest_replay_completed"
        )