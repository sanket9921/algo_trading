from app.backtest.candle_loader import (
    CandleLoader,
)

from app.backtest.performance_analyzer import (
    PerformanceAnalyzer,
)

from app.backtest.replay_engine import (
    ReplayEngine,
)

from app.core.logger import (
    get_logger,
)

from app.events.event_bus import (
    EventBus,
)

from app.execution.runtime import (
    ExecutionRuntime,
)

logger = get_logger(__name__)


class BacktestRuntime:

    def __init__(
        self,
        event_bus: EventBus,
        execution_runtime: ExecutionRuntime,
    ) -> None:

        self.event_bus = event_bus

        self.execution_runtime = (
            execution_runtime
        )

        self.loader = CandleLoader()

        self.replay_engine = ReplayEngine(
            event_bus=event_bus,
        )

        self.performance_analyzer = (
            PerformanceAnalyzer()
        )

    async def run_backtest(
        self,
        instrument_key: str,
    ) -> None:

        candles = (
            await self.loader
            .load_candles(
                instrument_key=
                instrument_key,
            )
        )

        logger.info(
            "historical_candles_loaded",
            candles_count=
            len(candles),
        )

        # ======================================
        # Replay Historical Candles
        # ======================================

        await self.replay_engine.replay_candles(
            candles=candles,
        )

        # ======================================
        # Collect Closed Position PnLs
        # ======================================

        realized_pnls = []

        for position in (
            self.execution_runtime
            .portfolio_manager
            .positions
            .values()
        ):

            if (
                position.realized_pnl
                != 0
            ):

                realized_pnls.append(
                    position.realized_pnl
                )

        # ======================================
        # Analyze Performance
        # ======================================

        result = (
            self.performance_analyzer
            .analyze(
                realized_pnls=
                realized_pnls
            )
        )

        logger.info(
            "backtest_completed",

            total_trades=
            result.total_trades,

            winning_trades=
            result.winning_trades,

            losing_trades=
            result.losing_trades,

            total_pnl=
            result.total_pnl,

            win_rate=
            result.win_rate,

            expectancy=
            result.expectancy,

            max_drawdown=
            result.max_drawdown,
        )