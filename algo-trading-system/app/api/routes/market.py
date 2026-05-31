from datetime import datetime

from fastapi import (
    APIRouter,
    Query,
)

from sqlalchemy import (
    and_,
    select,
)

from app.api.schemas.candle import (
    CandleResponse,
)

from app.storage.database import (
    AsyncSessionLocal,
)

from app.storage.models import (
    CandleEntity,
)

router = APIRouter()


@router.get(
    "/candles",
    response_model=
    list[CandleResponse],
)
async def get_candles(

    instrument_key: str,

    timeframe: str = "1m",

    from_date: datetime | None = None,

    to_date: datetime | None = None,

    limit: int = Query(
        default=1000,
        le=20000,
    ),
):

    async with (
        AsyncSessionLocal()
        as session
    ):

        filters = [

            CandleEntity.instrument_key
            ==
            instrument_key,

            CandleEntity.timeframe
            ==
            timeframe,
        ]

        if from_date:

            filters.append(

                CandleEntity.start_time
                >=
                from_date
            )

        if to_date:

            filters.append(

                CandleEntity.start_time
                <=
                to_date
            )

        statement = (
            select(
                CandleEntity
            )
            .where(
                and_(*filters)
            )
            .order_by(
                CandleEntity.start_time.asc()
            )
            .limit(limit)
        )

        result = (
            await session.execute(
                statement
            )
        )

        candles = (
            result.scalars().all()
        )

        return [

            CandleResponse(
                time=int(
                    candle.start_time
                    .timestamp()
                ),

                open=candle.open,

                high=candle.high,

                low=candle.low,

                close=candle.close,

                volume=candle.volume,
            )

            for candle
            in candles
        ]