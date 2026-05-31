from datetime import datetime, timezone

from app.core.logger import get_logger
from app.events.event_bus import EventBus
from app.events.event_models import (
    CandleClosedEvent,
    IndicatorCalculatedEvent,
)
from app.indicators.indicator_manager import (
    IndicatorManager,
)

logger = get_logger(__name__)


class IndicatorRuntime:
    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self.event_bus = event_bus

        self.manager = IndicatorManager()

    async def handle_closed_candle(
        self,
        event: CandleClosedEvent,
    ) -> None:
        snapshot = (
            self.manager.process_candle(
                event.candle
            )
        )

        logger.info(
            "indicator_runtime_processed_candle",
            instrument_key=snapshot.instrument_key,
        )

        await self.event_bus.publish(
            IndicatorCalculatedEvent(
                timestamp=datetime.now(
                    tz=timezone.utc,
                ),
                candle=event.candle,
                indicators=snapshot,
            )
        )