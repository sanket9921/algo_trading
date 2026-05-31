import asyncio

from app.alerts.runtime import (
    AlertRuntime,
)

from app.backtest.runtime import (
    BacktestRuntime,
)

from app.brokers.upstox.client import (
    UpstoxBrokerClient,
)

from app.core.config import (
    get_settings,
)

from app.core.logger import (
    get_logger,
    setup_logger,
)

from app.core.runtime_mode import (
    RuntimeMode,
)

from app.core.runtime_settings import get_runtime_settings

from app.events.event_bus import (
    EventBus,
)

from app.events.event_models import (
    CandleClosedEvent,
    IndicatorCalculatedEvent,
    PositionClosedEvent,
    RiskValidatedEvent,
    TickReceivedEvent,
    TradeExecutedEvent,
    TradingSignalEvent,
)

from app.execution.runtime import (
    ExecutionRuntime,
)

from app.history.bootstrap_runtime import (
    BootstrapRuntime,
)

from app.indicators.runtime import (
    IndicatorRuntime,
)

from app.market.runtime import (
    MarketRuntime,
)

from app.market.simulator import (
    MarketDataSimulator,
)

from app.risk.runtime import (
    RiskRuntime,
)

from app.storage.database import (
    initialize_database,
)

from app.storage.runtime import (
    StorageRuntime,
)

from app.strategy.runtime import (
    StrategyRuntime,
)

from app.api.websocket.market_stream import (
    MarketStreamRuntime,
)

from app.replay.runtime import (
    ReplayRuntime,
)

logger = get_logger(__name__)


# INSTRUMENT_KEY = (
#     "NSE_INDEX|Nifty 50"
# )


async def bootstrap() -> None:

    logger.info(
        "application_bootstrap_started"
    )

    # ==================================================
    # Load Settings
    # ==================================================

    settings = get_settings()

    runtime_settings = (
        get_runtime_settings(
            settings.runtime_mode
        )
    )

    logger.info(
        "runtime_mode_loaded",
        mode=settings.runtime_mode.value,
    )

    # ==================================================
    # Core Infrastructure
    # ==================================================

    event_bus = EventBus()

    await initialize_database()

    logger.info(
        "database_initialized"
    )

    # ==================================================
    # Recovery / Warmup Runtime
    # ==================================================

    bootstrap_runtime = (
        BootstrapRuntime(
            event_bus=event_bus,
        )
    )

    logger.info(
        "bootstrap_runtime_initialized"
    )

    # ==================================================
    # Core Trading Runtimes
    # ==================================================

    market_runtime = MarketRuntime(
        event_bus=event_bus,
        runtime_settings=runtime_settings,
    )

    indicator_runtime = (
        IndicatorRuntime(
            event_bus=event_bus,
        )
    )

    strategy_runtime = (
        StrategyRuntime(
            event_bus=event_bus,
        )
    )

    risk_runtime = RiskRuntime(
        event_bus=event_bus,
    )

    execution_runtime = (
        ExecutionRuntime(
            event_bus=event_bus,
            runtime_settings=runtime_settings,
        )
    )

    storage_runtime = (
        StorageRuntime()
    )

    alert_runtime = (
        AlertRuntime()
    )

    backtest_runtime = (
        BacktestRuntime(
            event_bus=event_bus,
            execution_runtime=
            execution_runtime,
        )
    )
    
    market_stream_runtime = (
        MarketStreamRuntime()
    )
    replay_runtime = (
        ReplayRuntime(
            event_bus=event_bus,
            replay_speed=
            settings.replay_speed_seconds,
        )
    )

    logger.info(
        "all_runtimes_initialized"
    )

    # ==================================================
    # Event Subscriptions
    # ==================================================

    # ------------------------------------------
    # Tick → Market
    # ------------------------------------------

    event_bus.subscribe(
        TickReceivedEvent,
        market_runtime.handle_tick,
    )

    # ------------------------------------------
    # Candle → Indicators
    # ------------------------------------------

    event_bus.subscribe(
        CandleClosedEvent,
        indicator_runtime
        .handle_closed_candle,
    )

    # ------------------------------------------
    # Indicators → Strategy
    # ------------------------------------------

    event_bus.subscribe(
        IndicatorCalculatedEvent,
        strategy_runtime
        .handle_indicator_event,
    )

    # ------------------------------------------
    # Strategy → Risk
    # ------------------------------------------

    event_bus.subscribe(
        TradingSignalEvent,
        risk_runtime
        .handle_signal_event,
    )

    # ------------------------------------------
    # Strategy → Alerts
    # ------------------------------------------

    event_bus.subscribe(
        TradingSignalEvent,
        alert_runtime
        .handle_signal_event,
    )

    # ------------------------------------------
    # Strategy → Storage
    # ------------------------------------------

    event_bus.subscribe(
        TradingSignalEvent,
        storage_runtime
        .handle_signal_generated,
    )

    # ------------------------------------------
    # Risk → Execution
    # ------------------------------------------

    event_bus.subscribe(
        RiskValidatedEvent,
        execution_runtime
        .handle_risk_event,
    )

    # ------------------------------------------
    # Risk → Alerts
    # ------------------------------------------

    event_bus.subscribe(
        RiskValidatedEvent,
        alert_runtime
        .handle_risk_event,
    )

    # ------------------------------------------
    # Risk → Storage
    # ------------------------------------------

    event_bus.subscribe(
        RiskValidatedEvent,
        storage_runtime
        .handle_risk_validated,
    )

    # ------------------------------------------
    # Candle → Storage
    # ------------------------------------------

    event_bus.subscribe(
        CandleClosedEvent,
        storage_runtime
        .handle_candle_closed,
    )

    # ------------------------------------------
    # Candle → Execution Runtime
    # ------------------------------------------

    event_bus.subscribe(
        CandleClosedEvent,
        execution_runtime
        .handle_candle_event,
    )

    # ------------------------------------------
    # Trade → Storage
    # ------------------------------------------

    event_bus.subscribe(
        TradeExecutedEvent,
        storage_runtime
        .handle_trade_executed,
    )

    # ------------------------------------------
    # Position Closed → Storage
    # ------------------------------------------

    event_bus.subscribe(
        PositionClosedEvent,
        storage_runtime
        .handle_position_closed,
    )
    
    event_bus.subscribe(
        TickReceivedEvent,
        market_stream_runtime.handle_tick_event,
    )

    logger.info(
        "all_event_subscriptions_registered"
    )

    # ==================================================
    # Data Sources
    # ==================================================

    simulator = (
        MarketDataSimulator(
            event_bus=event_bus,
        )
    )

    broker_client = (
        UpstoxBrokerClient(
            event_bus=event_bus,
        )
    )

    logger.info(
        "data_sources_initialized"
    )

    # ==================================================
    # Startup Notification
    # ==================================================

    await alert_runtime.client.send_message(
        (
            "🚀 Algo Trading System Started\n"
            f"Mode: "
            f"{settings.runtime_mode.value}"
        )
    )

    logger.info(
        "startup_alert_sent"
    )

    # ==================================================
    # Runtime Mode Selection
    # ==================================================

    # ------------------------------------------
    # BACKTEST MODE
    # ------------------------------------------

    # if (
    #     settings.runtime_mode
    #     == RuntimeMode.BACKTEST
    # ):

    #     logger.info(
    #         "backtest_mode_started"
    #     )

    #     await backtest_runtime.run_backtest(
    #         instrument_key=
    #         INSTRUMENT_KEY,
    #     )

    # # ------------------------------------------
    # # LIVE MODE
    # # ------------------------------------------

    # elif (
    #     settings.runtime_mode
    #     == RuntimeMode.LIVE
    # ):

    #     logger.info(
    #         "live_mode_started"
    #     )

    #     # ======================================
    #     # Warmup Historical State
    #     # ======================================

    #     await (
    #         bootstrap_runtime
    #         .warmup_market_state(
    #             instrument_key=
    #             INSTRUMENT_KEY,
    #         )
    #     )

    #     logger.info(
    #         "historical_state_recovered"
    #     )

    #     # ======================================
    #     # Start Live Feed
    #     # ======================================

    #     await broker_client.start()

    # # ------------------------------------------
    # # PAPER MODE
    # # ------------------------------------------

    # elif (
    #     settings.runtime_mode
    #     == RuntimeMode.PAPER
    # ):

    #     logger.info(
    #         "paper_mode_started"
    #     )

    #     # ======================================
    #     # Recover Historical State
    #     # ======================================

    #     await (
    #         bootstrap_runtime
    #         .warmup_market_state(
    #             instrument_key=
    #             INSTRUMENT_KEY,
    #         )
    #     )

    #     logger.info(
    #         "historical_state_recovered"
    #     )

    #     # ======================================
    #     # Start Live Market Feed
    #     # ======================================

    #     await broker_client.start()

    # # ------------------------------------------
    # # DEVELOPMENT MODE
    # # ------------------------------------------

    # else:

        # logger.info(
        #     "development_mode_started"
        # )

        # await simulator.start()
        
    if settings.market_data_mode:

        logger.info(
            "replay_mode_started"
        )

        await replay_runtime.replay_market(
            instrument_key=
            settings.default_instrument_key,
        )

    else:

        logger.info(
            "live_mode_started"
        )

        await broker_client.start()


async def main() -> None:

    setup_logger()

    try:

        await bootstrap()

    except KeyboardInterrupt:

        logger.warning(
            "application_shutdown_requested"
        )

    except Exception as exc:

        logger.exception(
            "application_crashed",
            error=str(exc),
        )

        raise


if __name__ == "__main__":
    asyncio.run(main())