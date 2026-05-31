from datetime import datetime, timezone

from app.execution.models import (
    Position,
)
from app.storage.database import (
    AsyncSessionLocal,
)
from app.storage.models import (
    ClosedPositionEntity,
)


class ClosedPositionRepository:
    async def save(
        self,
        position: Position,
    ) -> None:

        async with AsyncSessionLocal() as session:
            entity = ClosedPositionEntity(
                instrument_key=(
                    position.instrument_key
                ),
                side=position.side.value,
                quantity=position.quantity,
                average_price=(
                    position.average_price
                ),
                realized_pnl=(
                    position.realized_pnl
                ),
                closed_at=datetime.now(
                    tz=timezone.utc,
                ),
            )

            session.add(entity)

            await session.commit()