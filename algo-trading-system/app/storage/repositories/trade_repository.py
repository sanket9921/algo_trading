from app.execution.models import (
    ExecutedTrade,
)
from app.storage.database import (
    AsyncSessionLocal,
)
from app.storage.models import (
    TradeEntity,
)


class TradeRepository:
    async def save(
        self,
        trade: ExecutedTrade,
    ) -> None:
        async with AsyncSessionLocal() as session:
            entity = TradeEntity(
                instrument_key=(
                    trade.instrument_key
                ),
                side=trade.side.value,
                quantity=trade.quantity,
                execution_price=(
                    trade.execution_price
                ),
                strategy_name=(
                    trade.strategy_name
                ),
                executed_at=trade.executed_at,
            )

            session.add(entity)

            await session.commit()