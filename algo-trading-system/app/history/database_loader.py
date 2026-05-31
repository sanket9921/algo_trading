from sqlalchemy import select

from app.core.logger import (
    get_logger,
)

from app.storage.database import (
    AsyncSessionLocal,
)

from app.storage.models import (
    CandleEntity,
)

from app.history.models import (
    HistoricalCandle,
)

logger = get_logger(__name__)


class DatabaseCandleLoader:
    async def load_recent_candles(
        self,
        instrument_key: str,
        timeframe: str = "1m",
        limit: int = 100,
    ) -> list[HistoricalCandle]:

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
                .limit(limit)
            )

            result = await session.execute(
                query
            )

            candles = (
                result.scalars().all()
            )

        candles.reverse()

        logger.info(
            "database_candles_loaded",
            candles_count=len(candles),
            instrument_key=
            instrument_key,
        )

        return [
            HistoricalCandle(
                instrument_key=
                candle.instrument_key,

                timeframe=
                candle.timeframe,

                open=
                candle.open,

                high=
                candle.high,

                low=
                candle.low,

                close=
                candle.close,

                volume=
                candle.volume,

                start_time=
                candle.start_time,

                end_time=
                candle.end_time,

                is_closed=
                candle.is_closed,
            )
            for candle in candles
        ]