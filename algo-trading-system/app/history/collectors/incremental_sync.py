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

from app.history.upstox_history_client import (
    UpstoxHistoryClient,
)

from app.market.models import (
    Candle,
)

from app.market.timeframe_aggregator import (
    TimeframeAggregator,
)

from app.storage.repositories.candle_repository import (
    CandleRepository,
)

from app.storage.repositories.sync_state_repository import (
    SyncStateRepository,
)

logger = get_logger(__name__)


class IncrementalHistorySync:

    def __init__(self) -> None:

        self.settings = (
            get_settings()
        )

        self.history_client = (
            UpstoxHistoryClient()
        )

        self.candle_repository = (
            CandleRepository()
        )

        self.sync_repository = (
            SyncStateRepository()
        )

        self.aggregator = (
            TimeframeAggregator()
        )

    # =====================================================
    # Public API
    # =====================================================

    async def sync(
        self,
        instrument_key: str,
    ) -> int:

        logger.info(
            "incremental_sync_started",
            instrument_key=
            instrument_key,
        )

        from_date, to_date = (
            await self._calculate_sync_range(
                instrument_key=
                instrument_key,
            )
        )

        # ==========================================
        # Fetch ONLY 1m candles
        # ==========================================

        candles = (
            await self.history_client
            .fetch_candles(
                instrument_key=
                instrument_key,

                timeframe=
                "1m",

                from_date=
                from_date,

                to_date=
                to_date,
            )
        )

        if not candles:

            logger.info(
                "no_new_candles_found",
                instrument_key=
                instrument_key,
            )

            return 0

        # ==========================================
        # Save Raw 1m Candles
        # ==========================================

        saved_1m = (
            await self.candle_repository
            .bulk_save(
                candles
            )
        )

        # ==========================================
        # Aggregate Higher Timeframes
        # ==========================================

        aggregated_candles = []

        for candle in candles:

            generated = (
                self.aggregator
                .process_candle(
                    Candle(
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
                    )
                )
            )

            aggregated_candles.extend(
                generated
            )

        saved_aggregated = 0

        if aggregated_candles:

            saved_aggregated = (
                await self.candle_repository
                .bulk_save(
                    aggregated_candles
                )
            )

        # ==========================================
        # Update Sync States
        # ==========================================

        latest_candle = candles[-1]

        await self.sync_repository.update_sync_state(
            instrument_key=
            instrument_key,

            timeframe=
            "1m",

            last_candle_start=
            latest_candle.start_time,
        )

        # ==========================================
        # Update Aggregated Timeframe States
        # ==========================================

        grouped = {}

        for candle in aggregated_candles:

            grouped[
                candle.timeframe
            ] = candle

        for timeframe, candle in (
            grouped.items()
        ):

            await (
                self.sync_repository
                .update_sync_state(
                    instrument_key=
                    instrument_key,

                    timeframe=
                    timeframe,

                    last_candle_start=
                    candle.start_time,
                )
            )

        total_saved = (
            saved_1m
            +
            saved_aggregated
        )

        logger.info(
            "incremental_sync_completed",
            instrument_key=
            instrument_key,

            fetched=
            len(candles),

            saved_1m=
            saved_1m,

            saved_aggregated=
            saved_aggregated,

            total_saved=
            total_saved,
        )

        return total_saved

    # =====================================================
    # Internal Helpers
    # =====================================================

    async def _calculate_sync_range(
        self,
        instrument_key: str,
    ) -> tuple[datetime, datetime]:

        latest_synced = (
            await self.sync_repository
            .get_last_candle_time(
                instrument_key=
                instrument_key,

                timeframe=
                "1m",
            )
        )

        to_date = datetime.now(
            tz=timezone.utc,
        )

        # ==========================================
        # Initial Sync
        # ==========================================

        if latest_synced is None:

            from_date = (
                to_date
                -
                timedelta(
                    days=
                    self.settings
                    .historical_default_lookback_days
                )
            )

            logger.info(
                "initial_history_sync",
                instrument_key=
                instrument_key,

                lookback_days=
                self.settings
                .historical_default_lookback_days,
            )

            return (
                from_date,
                to_date,
            )

        # ==========================================
        # Incremental Sync
        # ==========================================

        from_date = (
            latest_synced
            -
            timedelta(minutes=1)
        )

        logger.info(
            "incremental_history_sync",
            instrument_key=
            instrument_key,

            latest_synced=
            latest_synced.isoformat(),
        )

        return (
            from_date,
            to_date,
        )