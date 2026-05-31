import asyncio
from app.alerts.runtime import (
    AlertRuntime,
)

from app.api.websocket.market_stream import (
    MarketStreamRuntime,
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
)

from app.core.runtime_mode import (
    RuntimeMode,
)

from app.core.runtime_settings import (
    get_runtime_settings,
)

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

from app.replay.runtime import (
    ReplayRuntime,
)

from app.options.runtime import (
    OptionChainRuntime,
)

logger = get_logger(__name__)

INSTRUMENT_KEY = (
    "NSE_INDEX|Nifty 50"
)


class ApplicationBootstrap:

    def __init__(self) -> None:

        self.settings = (
            get_settings()
        )

        self.runtime_settings = (
            get_runtime_settings(
                self.settings.runtime_mode
            )
        )

        self.event_bus = EventBus()

    async def initialize(
        self,
    ) -> None:

        logger.info(
            "application_bootstrap_started"
        )

        logger.info(
            "runtime_mode_loaded",
            mode=self.settings.runtime_mode.value,
        )

        # ==========================================
        # Database
        # ==========================================

        await initialize_database()

        logger.info(
            "database_initialized"
        )

        # ==========================================
        # Recovery Runtime
        # ==========================================

        bootstrap_runtime = (
            BootstrapRuntime(
                event_bus=self.event_bus,
            )
        )

        # ==========================================
        # Core Runtimes
        # ==========================================

        market_runtime = (
            MarketRuntime(
                event_bus=self.event_bus,
                runtime_settings=
                self.runtime_settings,
            )
        )

        indicator_runtime = (
            IndicatorRuntime(
                event_bus=self.event_bus,
            )
        )

        strategy_runtime = (
            StrategyRuntime(
                event_bus=self.event_bus,
            )
        )

        risk_runtime = (
            RiskRuntime(
                event_bus=self.event_bus,
            )
        )

        execution_runtime = (
            ExecutionRuntime(
                event_bus=self.event_bus,
                runtime_settings=
                self.runtime_settings,
            )
        )

        storage_runtime = (
            StorageRuntime()
        )

        alert_runtime = (
            AlertRuntime()
        )
        
        option_chain_runtime = (
            OptionChainRuntime()
        )

        backtest_runtime = (
            BacktestRuntime(
                event_bus=self.event_bus,
                execution_runtime=
                execution_runtime,
            )
        )
        
        replay_runtime = (
            ReplayRuntime(
                event_bus=self.event_bus,

                replay_speed=
                self.settings.replay_speed_seconds,

                replay_candle_limit=
                self.settings.replay_candle_limit,
            )
        )
        
        market_stream_runtime = (
            MarketStreamRuntime()
        )

        logger.info(
            "all_runtimes_initialized"
        )

        # ==========================================
        # Event Subscriptions
        # ==========================================

        self.event_bus.subscribe(
            TickReceivedEvent,
            market_runtime.handle_tick,
        )

        self.event_bus.subscribe(
            TickReceivedEvent,
            market_stream_runtime.handle_tick_event,
        )
        
        self.event_bus.subscribe(
            CandleClosedEvent,
            market_stream_runtime.handle_replay_candle,
        )
        
        self.event_bus.subscribe(
            TradingSignalEvent,
            market_stream_runtime.handle_signal_event,
        )

        self.event_bus.subscribe(
            CandleClosedEvent,
            indicator_runtime.handle_closed_candle,
        )

        self.event_bus.subscribe(
            IndicatorCalculatedEvent,
            strategy_runtime.handle_indicator_event,
        )

        self.event_bus.subscribe(
            TradingSignalEvent,
            risk_runtime.handle_signal_event,
        )

        self.event_bus.subscribe(
            TradingSignalEvent,
            alert_runtime.handle_signal_event,
        )

        self.event_bus.subscribe(
            TradingSignalEvent,
            storage_runtime.handle_signal_generated,
        )

        self.event_bus.subscribe(
            RiskValidatedEvent,
            execution_runtime.handle_risk_event,
        )

        self.event_bus.subscribe(
            RiskValidatedEvent,
            alert_runtime.handle_risk_event,
        )

        self.event_bus.subscribe(
            RiskValidatedEvent,
            storage_runtime.handle_risk_validated,
        )

        self.event_bus.subscribe(
            CandleClosedEvent,
            storage_runtime.handle_candle_closed,
        )

        self.event_bus.subscribe(
            CandleClosedEvent,
            execution_runtime.handle_candle_event,
        )

        self.event_bus.subscribe(
            TradeExecutedEvent,
            storage_runtime.handle_trade_executed,
        )

        self.event_bus.subscribe(
            PositionClosedEvent,
            storage_runtime.handle_position_closed,
        )
        

        logger.info(
            "all_event_subscriptions_registered"
        )

        # ==========================================
        # Data Sources
        # ==========================================

        simulator = (
            MarketDataSimulator(
                event_bus=self.event_bus,
            )
        )

        broker_client = (
            UpstoxBrokerClient(
                event_bus=self.event_bus,
            )
        )

        logger.info(
            "data_sources_initialized"
        )

        # ==========================================
        # Startup Notification
        # ==========================================

        await alert_runtime.client.send_message(
            (
                "🚀 Algo Trading System Started\n"
                f"Mode: "
                f"{self.settings.runtime_mode.value}"
            )
        )

        logger.info(
            "startup_alert_sent"
        )

        # ==========================================
        # Runtime Modes
        # ==========================================

        if (
            self.settings.runtime_mode
            == RuntimeMode.BACKTEST
        ):

            logger.info(
                "backtest_mode_started"
            )

            await (
                backtest_runtime.run_backtest(
                    instrument_key=
                    INSTRUMENT_KEY,
                )
            )

            return


        # ==========================================
        # Market Data Modes
        # ==========================================

        if (
            self.settings.market_data_mode
            == "REPLAY"
        ):

            logger.info(
                "replay_mode_started"
            )

            asyncio.create_task(
                replay_runtime.replay_market(
                    instrument_key=
                    INSTRUMENT_KEY,
                )
            )

        elif (
            self.settings.market_data_mode
            == "LIVE"
        ):

            logger.info(
                "live_market_mode_started"
            )

            await (
                bootstrap_runtime
                .warmup_market_state(
                    instrument_key=
                    INSTRUMENT_KEY,
                )
            )

            logger.info(
                "historical_state_recovered"
            )
            from app.history.runtime import (
                HistoryRuntime,
            )
            history_runtime = (
                HistoryRuntime()
            )
            
            asyncio.create_task(
                history_runtime.start()
            )
            
            asyncio.create_task(
                option_chain_runtime.start()
            )

            logger.info(
                "history_runtime_started"
            )
            
            asyncio.create_task(
                broker_client.start()
            )

        elif (
            self.settings.market_data_mode
            == "SIMULATOR"
        ):

            logger.info(
                "simulator_mode_started"
            )

            asyncio.create_task(
                simulator.start()
            )

        else:

            raise ValueError(
                (
                    "Unsupported market "
                    "data mode: "
                    f"{self.settings.market_data_mode}"
                )
            )