from app.execution.models import (
    Position,
)

from app.storage.database import (
    AsyncSessionLocal,
)

from app.storage.models import (
    BacktestTradeEntity,
)


class BacktestTradeRepository:

    async def save_closed_position(
        self,
        position: Position,
        exit_price: float,
        closed_at,
        is_replay: bool,
    ) -> None:

        async with AsyncSessionLocal() as session:

            entity = BacktestTradeEntity(
                instrument_key=
                position.instrument_key,

                strategy_name=
                "EMA_RSI_VWAP",

                side=
                position.side.value,

                quantity=
                position.quantity,

                entry_price=
                position.average_price,

                exit_price=
                exit_price,

                realized_pnl=
                position.realized_pnl,

                opened_at=
                closed_at,

                closed_at=
                closed_at,

                is_replay=
                is_replay,
            )

            session.add(entity)

            await session.commit()