from datetime import (
    datetime,
    timedelta,
    timezone,
)

from app.core.config import (
    get_settings,
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

from app.history.candle_merger import (
    CandleMerger,
)

from app.history.database_loader import (
    DatabaseCandleLoader,
)

from app.history.gap_detector import (
    GapDetector,
)

from app.history.upstox_history_client import (
    UpstoxHistoryClient,
)

from app.market.models import (
    Candle,
)

logger = get_logger(__name__)


class BootstrapRuntime:

    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:

        self.settings = (
            get_settings()
        )

        self.event_bus = event_bus

        self.history_client = (
            UpstoxHistoryClient()
        )

        self.database_loader = (
            DatabaseCandleLoader()
        )

        self.gap_detector = (
            GapDetector()
        )

        self.candle_merger = (
            CandleMerger()
        )

    async def warmup_market_state(
        self,
        instrument_key: str,
        required_candles: int = 100,
    ) -> None:

        logger.info(
            "historical_warmup_started",
            instrument_key=
            instrument_key,
        )

        # ==========================================
        # Load Existing DB Candles
        # ==========================================

        database_candles = (
            await self.database_loader
            .load_recent_candles(
                instrument_key=
                instrument_key,

                limit=
                required_candles,
            )
        )

        missing_candles = (
            self.gap_detector
            .calculate_missing_candles(
                existing_candles=
                database_candles,

                required_count=
                required_candles,
            )
        )

        logger.info(
            "historical_gap_analysis_completed",
            existing_candles=
            len(database_candles),

            missing_candles=
            missing_candles,
        )

        historical_candles = []

        # ==========================================
        # Fetch Missing History
        # ==========================================

        if missing_candles > 0:

            to_date = datetime.now(
                tz=timezone.utc,
            )

            from_date = (
                to_date
                -
                timedelta(days=7)
            )

            historical_candles = (
                await self.history_client
                .fetch_candles(
                    instrument_key=
                    instrument_key,

                    timeframe=
                    self.settings.default_timeframe,

                    from_date=
                    from_date,

                    to_date=
                    to_date,
                )
            )

        # ==========================================
        # Merge DB + Historical
        # ==========================================

        merged_candles = (
            self.candle_merger
            .merge_candles(
                historical_candles=
                historical_candles,

                database_candles=
                database_candles,
            )
        )

        # ==========================================
        # Keep Latest Required Candles
        # ==========================================

        merged_candles = (
            merged_candles[
                -required_candles:
            ]
        )

        logger.info(
            "historical_candle_merge_completed",
            total_candles=
            len(merged_candles),
        )

        # ==========================================
        # Replay Into Runtime
        # ==========================================

        for candle in merged_candles:

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

                    is_replay=True,
                )
            )

        logger.info(
            "historical_warmup_completed",
            candles_loaded=
            len(merged_candles),
        )