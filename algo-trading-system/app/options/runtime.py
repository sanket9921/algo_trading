import asyncio

from app.core.config import (
    get_settings,
)

from app.core.logger import (
    get_logger,
)

from app.options.analytics.oi_change_calculator import (
    OIChangeCalculator,
)

from app.options.option_chain_client import (
    OptionChainClient,
)

from app.storage.repositories.option_analytics_repository import (
    OptionAnalyticsRepository,
)

from app.storage.repositories.option_chain_repository import (
    OptionChainRepository,
)

logger = get_logger(__name__)


class OptionChainRuntime:

    def __init__(self) -> None:

        self.settings = (
            get_settings()
        )

        # ======================================
        # Clients
        # ======================================

        self.client = (
            OptionChainClient()
        )

        # ======================================
        # Analytics
        # ======================================

        self.oi_calculator = (
            OIChangeCalculator()
        )

        # ======================================
        # Repositories
        # ======================================

        self.option_repository = (
            OptionChainRepository()
        )

        self.analytics_repository = (
            OptionAnalyticsRepository()
        )

        self._running = False

    # =====================================================
    # Public Runtime API
    # =====================================================

    async def start(self) -> None:

        if not (
            self.settings
            .option_chain_enabled
        ):

            logger.info(
                "option_chain_runtime_disabled"
            )

            return

        self._running = True

        logger.info(
            "option_chain_runtime_started"
        )

        while self._running:

            try:

                await self._run_collection_cycle()

            except Exception as exc:

                logger.exception(
                    "option_chain_runtime_failed",
                    error=str(exc),
                )

            await asyncio.sleep(
                self.settings
                .option_chain_sync_interval_seconds
            )

    async def stop(self) -> None:

        self._running = False

        logger.info(
            "option_chain_runtime_stopped"
        )

    # =====================================================
    # Internal Collection Logic
    # =====================================================

    async def _run_collection_cycle(
        self,
    ) -> None:

        logger.info(
            "option_chain_collection_started"
        )

        # ==========================================
        # Fetch Raw Option Chain
        # ==========================================

        snapshots = (
            await self.client
            .fetch_option_chain(

                instrument_key=
                self.settings
                .option_chain_instrument_key,
            )
        )

        # ==========================================
        # Save Raw Snapshots
        # ==========================================

        raw_saved_count = (
            await self.option_repository
            .bulk_save(
                snapshots
            )
        )

        logger.info(
            "option_chain_raw_snapshots_saved",

            snapshots_fetched=
            len(snapshots),

            snapshots_saved=
            raw_saved_count,
        )

        # ==========================================
        # Calculate Analytics
        # ==========================================

        analyses = []

        for snapshot in snapshots:

            analysis = (
                self.oi_calculator
                .calculate(
                    snapshot
                )
            )

            analyses.append(
                analysis
            )

        logger.info(
            "option_chain_analytics_calculated",

            analytics_count=
            len(analyses),
        )

        # ==========================================
        # Save Analytics
        # ==========================================

        analytics_saved_count = (
            await self.analytics_repository
            .bulk_save(
                snapshots=
                snapshots,

                analyses=
                analyses,
            )
        )

        logger.info(
            "option_chain_analytics_saved",

            analytics_saved=
            analytics_saved_count,
        )

        logger.info(
            "option_chain_collection_completed"
        )