from datetime import datetime, timezone

from app.core.logger import get_logger
from app.events.event_bus import EventBus
from app.events.event_models import (
    RiskValidatedEvent,
    TradeExecutedEvent,
)
from app.execution.paper_broker import (
    PaperBroker,
)
from app.execution.portfolio_manager import (
    PortfolioManager,
)
from app.core.runtime_settings import (
    RuntimeSettings,
)
from datetime import datetime, timezone

from app.events.event_models import (
    CandleClosedEvent,
    PositionClosedEvent,
)
from app.execution.lifecycle_manager import (
    LifecycleManager,
)

from app.storage.repositories.backtest_trade_repository import (
    BacktestTradeRepository,
)


logger = get_logger(__name__)


class ExecutionRuntime:
    def __init__(
        self,
        event_bus: EventBus,
        runtime_settings: RuntimeSettings,
    ) -> None:
        self.event_bus = event_bus

        self.paper_broker = PaperBroker()

        self.portfolio_manager = (
            PortfolioManager(
                runtime_settings=runtime_settings
            )
        )
        
        self.lifecycle_manager = (
            LifecycleManager()
        )
        
        self.backtest_trade_repository = (
            BacktestTradeRepository()
        )
        
        self.executed_trades = []

    async def handle_risk_event(
        self,
        event: RiskValidatedEvent,
    ) -> None:

        if not event.decision.approved:
            logger.warning(
                "trade_execution_skipped",
                reason=event.decision.reason,
            )
            return

        quantity = (
            event.decision
            .suggested_quantity
        )

        if quantity is None:
            logger.warning(
                "trade_execution_missing_quantity"
            )
            return

        trade = (
            await self.paper_broker
            .execute_trade(
                signal=event.signal,
                quantity=quantity,
            )
        )
        
        self.executed_trades.append(
            trade
        )

        position = (
            self.portfolio_manager
            .apply_trade(trade)
        )

        logger.info(
            "paper_trade_executed",
            instrument_key=(
                trade.instrument_key
            ),
            side=trade.side.value,
            quantity=trade.quantity,
            price=trade.execution_price,
        )

        await self.event_bus.publish(
            TradeExecutedEvent(
                timestamp=datetime.now(
                    tz=timezone.utc,
                ),
                trade=trade,
                position=position,

                is_replay=
                event.signal.is_replay,
            )
        )
        
    async def handle_candle_event(
        self,
        event: CandleClosedEvent,
    ) -> None:

        position = (
            self.portfolio_manager
            .positions.get(
                event.candle.instrument_key
            )
        )

        if position is None:
            return

        if not position.is_open:
            return

        closed, pnl = (
            self.lifecycle_manager
            .evaluate_position(
                position=position,
                market_price=(
                    event.candle.close
                ),
            )
        )

        if not closed:
            return

        position.realized_pnl = (
            pnl or 0.0
        )

        await self.backtest_trade_repository.save_closed_position(
            position=position,

            exit_price=
            event.candle.close,

            closed_at=
            event.timestamp,

            is_replay=
            event.is_replay,
        )
        
        await self.event_bus.publish(
            PositionClosedEvent(
                timestamp=datetime.now(
                    tz=timezone.utc,
                ),
                position=position,
                realized_pnl=pnl or 0.0,

                is_replay=
                event.is_replay,
            )
        )