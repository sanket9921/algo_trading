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
    TickReceivedEvent,
)

from app.market.candle_engine import (
    CandleEngine,
)

from app.market.timeframe_aggregator import (
    TimeframeAggregator,
)

logger = get_logger(__name__)


class MarketRuntime:

    def __init__(
        self,
        event_bus: EventBus,
        runtime_settings,
    ) -> None:

        self.event_bus = (
            event_bus
        )

        # ======================================
        # ALWAYS BUILD 1m BASE CANDLES
        # ======================================

        self.candle_engine = (
            CandleEngine()
        )

        # ======================================
        # Higher Timeframe Aggregation
        # ======================================

        self.aggregator = (
            TimeframeAggregator()
        )

    async def handle_tick(
        self,
        event: TickReceivedEvent,
    ) -> None:

        # ======================================
        # Generate ONLY 1m Candle
        # ======================================

        closed_candle = (

            self.candle_engine
            .process_tick(

                event.tick,

                timeframe_minutes=1,
            )
        )

        if not closed_candle:

            return

        logger.info(
            "closed_candle_generated",

            instrument_key=
            closed_candle
            .instrument_key,

            timeframe=
            closed_candle
            .timeframe,

            close=
            closed_candle.close,
        )

        # ======================================
        # Publish 1m Candle
        # ======================================

        await self._publish_candle(
            closed_candle
        )

        # ======================================
        # Aggregate 5m / 15m
        # ======================================

        aggregated_candles = (

            self.aggregator
            .process_candle(
                closed_candle
            )
        )

        for aggregated in (
            aggregated_candles
        ):

            logger.info(
                "aggregated_candle_generated",

                timeframe=
                aggregated.timeframe,

                close=
                aggregated.close,
            )

            await self._publish_candle(
                aggregated
            )

    async def _publish_candle(
        self,
        candle,
    ) -> None:

        await self.event_bus.publish(

            CandleClosedEvent(

                timestamp=
                datetime.now(
                    tz=timezone.utc,
                ),

                candle=
                candle,
            )
        )