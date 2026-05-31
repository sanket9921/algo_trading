from app.core.logger import get_logger
from app.events.event_models import (
    CandleClosedEvent,
    RiskValidatedEvent,
    TradingSignalEvent,
)
from app.storage.repositories.candle_repository import (
    CandleRepository,
)
from app.storage.repositories.risk_repository import (
    RiskRepository,
)
from app.storage.repositories.signal_repository import (
    SignalRepository,
)

from app.events.event_models import (
    TradeExecutedEvent,
)
from app.storage.repositories.trade_repository import (
    TradeRepository,
)

from app.events.event_models import (
    PositionClosedEvent,
)
from app.storage.repositories.closed_position_repository import (
    ClosedPositionRepository,
)
logger = get_logger(__name__)


class StorageRuntime:
    def __init__(self) -> None:
        self.candle_repository = (
            CandleRepository()
        )

        self.signal_repository = (
            SignalRepository()
        )

        self.risk_repository = (
            RiskRepository()
        )
        self.trade_repository = (
            TradeRepository()
        )
        self.closed_position_repository = (
            ClosedPositionRepository()
        )
        
    async def handle_candle_closed(
        self,
        event: CandleClosedEvent,
    ) -> None:
        if event.is_replay:
            return
        
        await self.candle_repository.save(
            event.candle
        )

        logger.info(
            "candle_persisted",
            instrument_key=event.candle.instrument_key,
        )

    async def handle_signal_generated(
        self,
        event: TradingSignalEvent,
    ) -> None:
        await self.signal_repository.save(
            event.signal
        )

        logger.info(
            "signal_persisted",
            instrument_key=event.signal.instrument_key,
        )

    async def handle_risk_validated(
        self,
        event: RiskValidatedEvent,
    ) -> None:
        await self.risk_repository.save(
            signal=event.signal,
            decision=event.decision,
        )

        logger.info(
            "risk_decision_persisted",
            instrument_key=event.signal.instrument_key,
        )
        
    async def handle_trade_executed(
        self,
        event: TradeExecutedEvent,
    ) -> None:
        await self.trade_repository.save(
            event.trade
        )

        logger.info(
            "trade_persisted",
            instrument_key=(
                event.trade.instrument_key
            ),
        )
    
    async def handle_position_closed(
        self,
        event: PositionClosedEvent,
    ) -> None:

        await (
            self.closed_position_repository
            .save(event.position)
        )

        logger.info(
            "closed_position_persisted",
            instrument_key=(
                event.position
                .instrument_key
            ),
            realized_pnl=(
                event.realized_pnl
            ),
        )