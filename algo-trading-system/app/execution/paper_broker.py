from datetime import datetime, timezone

from app.execution.models import (
    ExecutedTrade,
    OrderSide,
)
from app.strategy.models import (
    SignalType,
    TradingSignal,
)


class PaperBroker:
    async def execute_trade(
        self,
        signal: TradingSignal,
        quantity: int,
    ) -> ExecutedTrade:

        side = (
            OrderSide.BUY
            if signal.signal_type ==
            SignalType.BUY
            else OrderSide.SELL
        )

        return ExecutedTrade(
            instrument_key=signal.instrument_key,
            side=side,
            quantity=quantity,
            execution_price=signal.price,
            executed_at=datetime.now(
                tz=timezone.utc,
            ),
            strategy_name=signal.strategy_name,
        )