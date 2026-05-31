import asyncio

from app.history.upstox_history_client import (
    UpstoxHistoryClient,
)

from app.market.models import (
    Candle,
)

from app.storage.repositories.candle_repository import (
    CandleRepository,
)


async def main() -> None:

    client = (
        UpstoxHistoryClient()
    )

    repository = (
        CandleRepository()
    )

    instrument_key = (
        "NSE_INDEX|Nifty 50"
    )

    historical_candles = (
        await client.fetch_candles(
            instrument_key=
            instrument_key,

            interval=
            "5minute",

            days=5,
        )
    )

    candles = []

    for candle in historical_candles:

        candles.append(
            Candle(
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
        )

    saved_count = (
        await repository.bulk_save(
            candles=candles,
        )
    )

    print(
        f"Saved candles: "
        f"{saved_count}"
    )


if __name__ == "__main__":

    asyncio.run(main())