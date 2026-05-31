from fastapi import (
    APIRouter,
)

from sqlalchemy import (
    select,
)

from app.api.schemas.signal import (
    SignalResponse,
)

from app.storage.database import (
    AsyncSessionLocal,
)

from app.storage.models import (
    SignalEntity,
)

router = APIRouter()


@router.get(
    "/signals",
    response_model=
    list[SignalResponse],
)
async def get_signals():

    async with (
        AsyncSessionLocal()
        as session
    ):

        statement = (
            select(
                SignalEntity
            )
            .order_by(
                SignalEntity.timestamp.asc()
            )
            .limit(500)
        )

        result = (
            await session.execute(
                statement
            )
        )

        signals = (
            result.scalars().all()
        )

        return [
            SignalResponse(
                signal_type=
                signal.signal_type,

                strategy_name=
                signal.strategy_name,

                price=
                signal.price,

                timestamp=int(
                    signal.timestamp
                    .timestamp()
                ),
            )
            for signal
            in signals
        ]