from datetime import datetime

from sqlalchemy import (
    select,
)

from app.storage.database import (
    AsyncSessionLocal,
)

from app.storage.models import (
    SyncStateEntity,
)


class SyncStateRepository:

    async def get_last_candle_time(
        self,
        instrument_key: str,
        timeframe: str,
    ) -> datetime | None:

        async with AsyncSessionLocal() as session:

            query = (
                select(SyncStateEntity)
                .where(
                    SyncStateEntity.instrument_key
                    == instrument_key
                )
                .where(
                    SyncStateEntity.timeframe
                    == timeframe
                )
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

            return entity.last_candle_start

    async def update_sync_state(
        self,
        instrument_key: str,
        timeframe: str,
        last_candle_start: datetime,
    ) -> None:

        async with AsyncSessionLocal() as session:

            query = (
                select(SyncStateEntity)
                .where(
                    SyncStateEntity.instrument_key
                    == instrument_key
                )
                .where(
                    SyncStateEntity.timeframe
                    == timeframe
                )
            )

            result = await session.execute(
                query
            )

            entity = (
                result
                .scalars()
                .first()
            )

            now = datetime.utcnow()

            if entity:

                entity.last_candle_start = (
                    last_candle_start
                )

                entity.last_synced_at = now

            else:

                entity = SyncStateEntity(
                    instrument_key=
                    instrument_key,

                    timeframe=
                    timeframe,

                    last_candle_start=
                    last_candle_start,

                    last_synced_at=
                    now,
                )

                session.add(entity)

            await session.commit()