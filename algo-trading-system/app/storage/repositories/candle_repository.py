from sqlalchemy import (
    insert,
    select,
)

from app.market.models import (
    Candle,
)

from app.storage.database import (
    AsyncSessionLocal,
)

from app.storage.models import (
    CandleEntity,
)


class CandleRepository:

    async def save(
        self,
        candle: Candle,
    ) -> None:

        await self.bulk_save(
            [candle]
        )

    async def bulk_save(
        self,
        candles: list[Candle],
    ) -> int:

        if not candles:
            return 0

        async with AsyncSessionLocal() as session:

            values = []

            for candle in candles:

                values.append(
                    {
                        "instrument_key":
                        candle.instrument_key,

                        "timeframe":
                        candle.timeframe,

                        "open":
                        candle.open,

                        "high":
                        candle.high,

                        "low":
                        candle.low,

                        "close":
                        candle.close,

                        "volume":
                        candle.volume,

                        "start_time":
                        candle.start_time,

                        "end_time":
                        candle.end_time,

                        "is_closed":
                        candle.is_closed,
                    }
                )

            statement = (
                insert(CandleEntity)
                .prefix_with(
                    "OR IGNORE"
                )
                .values(values)
            )

            result = await session.execute(
                statement
            )

            await session.commit()

            return result.rowcount or 0

    async def get_latest_candle(
        self,
        instrument_key: str,
        timeframe: str,
    ) -> Candle | None:

        async with AsyncSessionLocal() as session:

            query = (
                select(CandleEntity)
                .where(
                    CandleEntity.instrument_key
                    == instrument_key
                )
                .where(
                    CandleEntity.timeframe
                    == timeframe
                )
                .order_by(
                    CandleEntity.start_time.desc()
                )
                .limit(1)
            )

            result = await session.execute(
                query
            )

            entity = (
                result
                .scalars()
                .first()
            )

            if not entity:
                return None

            return Candle(
                instrument_key=
                entity.instrument_key,

                timeframe=
                entity.timeframe,

                open=
                entity.open,

                high=
                entity.high,

                low=
                entity.low,

                close=
                entity.close,

                volume=
                entity.volume,

                start_time=
                entity.start_time,

                end_time=
                entity.end_time,

                is_closed=
                entity.is_closed,
            )