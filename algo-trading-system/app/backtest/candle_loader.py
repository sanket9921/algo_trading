from sqlalchemy import select

from app.market.models import Candle
from app.storage.database import (
    AsyncSessionLocal,
)
from app.storage.models import (
    CandleEntity,
)


class CandleLoader:
    async def load_candles(
        self,
        instrument_key: str,
        timeframe: str = "1m",
    ) -> list[Candle]:

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
                    CandleEntity.start_time
                )
            )

            result = await session.execute(
                query
            )

            entities = result.scalars().all()

            return [
                Candle(
                    instrument_key=(
                        entity.instrument_key
                    ),
                    timeframe=(
                        entity.timeframe
                    ),
                    open=entity.open,
                    high=entity.high,
                    low=entity.low,
                    close=entity.close,
                    volume=entity.volume,
                    start_time=(
                        entity.start_time
                    ),
                    end_time=entity.end_time,
                    is_closed=entity.is_closed,
                )
                for entity in entities
            ]