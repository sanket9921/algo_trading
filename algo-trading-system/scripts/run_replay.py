import asyncio

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
    TradingSignalEvent,
    RiskValidatedEvent,
    TradeExecutedEvent,
    PositionClosedEvent,
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

from app.risk.runtime import (
    RiskRuntime,
)

from app.strategy.runtime import (
    StrategyRuntime,
)


async def main() -> None:

    event_bus = EventBus()

    runtime_settings = (
        get_runtime_settings(
            RuntimeMode.BACKTEST
        )
    )

    # ======================================
    # Runtime Initialization
    # ======================================

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

    risk_runtime = (
        RiskRuntime(
            event_bus=event_bus,
        )
    )

    execution_runtime = (
        ExecutionRuntime(
            event_bus=event_bus,
            runtime_settings=
            runtime_settings,
        )
    )

    # ======================================
    # Event Wiring
    # ======================================

    event_bus.subscribe(
        CandleClosedEvent,
        indicator_runtime.handle_closed_candle,
    )

    event_bus.subscribe(
        CandleClosedEvent,
        execution_runtime.handle_candle_event,
    )

    event_bus.subscribe(
        IndicatorCalculatedEvent,
        strategy_runtime.handle_indicator_event,
    )

    event_bus.subscribe(
        TradingSignalEvent,
        risk_runtime.handle_signal_event,
    )

    event_bus.subscribe(
        RiskValidatedEvent,
        execution_runtime.handle_risk_event,
    )

    # ======================================
    # Optional Debug Logs
    # ======================================

    async def log_trade(
        event: TradeExecutedEvent,
    ) -> None:

        print(
            "\nTRADE EXECUTED:",
            event.trade.side.value,
            event.trade.instrument_key,
            event.trade.execution_price,
        )

    async def log_position_close(
        event: PositionClosedEvent,
    ) -> None:

        print(
            "\nPOSITION CLOSED:",
            event.position.instrument_key,
            "PNL:",
            event.realized_pnl,
        )

    event_bus.subscribe(
        TradeExecutedEvent,
        log_trade,
    )

    event_bus.subscribe(
        PositionClosedEvent,
        log_position_close,
    )

    # ======================================
    # Historical Replay
    # ======================================

    bootstrap_runtime = (
        BootstrapRuntime(
            event_bus=event_bus,
        )
    )

    await bootstrap_runtime.warmup_market_state(
        instrument_key=
        "NSE_INDEX|Nifty 50",

        required_candles=
        500,
    )

    # ======================================
    # Replay Summary
    # ======================================

    print("\nReplay completed.\n")

    print(
        "Executed trades:",
        len(
            execution_runtime
            .executed_trades
        )
    )


if __name__ == "__main__":

    asyncio.run(main())