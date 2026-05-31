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
    IndicatorCalculatedEvent,
    PositionClosedEvent,
    TradingSignalEvent,
)

from app.options.analytics.models import (
    OIChangeAnalysis,
)

from app.strategy.context.models import (
    TimeframeContext,
)

from app.strategy.context.timeframe_context_builder import (
    TimeframeContextBuilder,
)

from app.strategy.strategy_manager import (
    StrategyManager,
)

logger = get_logger(__name__)


class StrategyRuntime:

    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:

        self.event_bus = (
            event_bus
        )

        self.manager = (
            StrategyManager()
        )

        self.context_builder = (
            TimeframeContextBuilder()
        )

        self.contexts: dict[
            str,
            TimeframeContext,
        ] = {}

        self.latest_option_analysis: (
            OIChangeAnalysis | None
        ) = None

    async def handle_indicator_event(
        self,
        event:
        IndicatorCalculatedEvent,
    ) -> None:

        candle = (
            event.candle
        )

        indicators = (
            event.indicators
        )

        timeframe = (
            candle.timeframe
        )

        context = (
            self.context_builder
            .build(

                timeframe=
                timeframe,

                indicators=
                indicators,

                close_price=
                candle.close,
            )
        )

        self.contexts[
            timeframe
        ] = context

        logger.info(
            "timeframe_context_updated",

            timeframe=
            timeframe,

            bullish=
            context.bullish_trend,

            bearish=
            context.bearish_trend,

            strong_trend=
            context.strong_trend,
        )

        signals = (
            self.manager
            .generate_signals(

                candle=
                candle,

                indicators=
                indicators,

                contexts=
                self.contexts,

                option_analysis=
                self.latest_option_analysis,
            )
        )

        for signal in signals:

            await self.event_bus.publish(

                TradingSignalEvent(

                    timestamp=
                    datetime.now(
                        tz=timezone.utc,
                    ),

                    signal=
                    signal,
                )
            )

        if not signals:

            logger.info(
                "no_trading_signal_generated",

                instrument_key=
                candle.instrument_key,

                timeframe=
                candle.timeframe,
            )

    async def handle_option_analysis(
        self,
        analysis: OIChangeAnalysis,
    ) -> None:

        self.latest_option_analysis = (
            analysis
        )

        logger.info(
            "option_analysis_updated",

            strike_price=
            analysis.strike_price,

            call_oi_change=
            analysis.call_oi_change,

            put_oi_change=
            analysis.put_oi_change,
        )

    async def handle_position_closed(
        self,
        event:
        PositionClosedEvent,
    ) -> None:

        self.manager.reset_positions()

        logger.info(
            "strategy_position_reset",

            instrument_key=
            event.position
            .instrument_key,
        )