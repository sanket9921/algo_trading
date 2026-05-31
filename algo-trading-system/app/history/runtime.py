import asyncio

from app.core.config import (
    get_settings,
)

from app.core.logger import (
    get_logger,
)

from app.history.collectors.incremental_sync import (
    IncrementalHistorySync,
)

logger = get_logger(__name__)


class HistoryRuntime:

    def __init__(self) -> None:

        self.settings = (
            get_settings()
        )

        self.sync_engine = (
            IncrementalHistorySync()
        )

        self._running = False

    # =====================================================
    # Public API
    # =====================================================

    async def start(self) -> None:

        if not (
            self.settings
            .historical_auto_sync
        ):

            logger.info(
                "history_auto_sync_disabled"
            )

            return

        self._running = True

        logger.info(
            "history_runtime_started"
        )

        while self._running:

            try:

                await self._run_sync_cycle()

            except Exception as exc:

                logger.exception(
                    "history_runtime_cycle_failed",
                    error=str(exc),
                )

            await asyncio.sleep(
                self.settings
                .historical_sync_interval_seconds
            )

    async def stop(self) -> None:

        self._running = False

        logger.info(
            "history_runtime_stopped"
        )

    # =====================================================
    # Internal Runtime Logic
    # =====================================================

    async def _run_sync_cycle(
        self,
    ) -> None:

        instrument_key = (
            self.settings
            .default_instrument_key
        )

        try:

            logger.info(
                "history_sync_cycle_started",
                instrument_key=
                instrument_key,
            )

            saved_count = (
                await self.sync_engine
                .sync(
                    instrument_key=
                    instrument_key,
                )
            )

            logger.info(
                "history_sync_cycle_completed",
                instrument_key=
                instrument_key,

                saved_count=
                saved_count,
            )

        except Exception as exc:

            logger.exception(
                "history_sync_failed",
                instrument_key=
                instrument_key,

                error=
                str(exc),
            )