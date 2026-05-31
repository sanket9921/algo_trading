from datetime import (
    datetime,
    timedelta,
    timezone,
)

import httpx

from app.core.config import (
    get_settings,
)

from app.core.logger import (
    get_logger,
)

from app.history.constants import (
    TIMEFRAME_TO_MINUTES,
    TIMEFRAME_TO_UPSTOX_INTERVAL,
)

from app.history.models import (
    HistoricalCandle,
)

logger = get_logger(__name__)


class UpstoxHistoryClient:

    BASE_URL = (
        "https://api.upstox.com/v2/historical-candle"
    )

    def __init__(self) -> None:

        self.settings = (
            get_settings()
        )

    # =====================================================
    # Public API
    # =====================================================

    async def fetch_candles(
        self,
        instrument_key: str,
        timeframe: str,
        from_date: datetime,
        to_date: datetime,
    ) -> list[HistoricalCandle]:

        self._validate_timeframe(
            timeframe=timeframe,
        )

        upstox_interval = (
            TIMEFRAME_TO_UPSTOX_INTERVAL[
                timeframe
            ]
        )

        logger.info(
            "historical_fetch_started",
            instrument_key=
            instrument_key,

            timeframe=
            timeframe,

            from_date=
            from_date.isoformat(),

            to_date=
            to_date.isoformat(),
        )

        url = self._build_url(
            instrument_key=
            instrument_key,

            interval=
            upstox_interval,

            from_date=
            from_date,

            to_date=
            to_date,
        )

        payload = await self._fetch_payload(
            url=url,
        )

        raw_candles = (
            payload
            .get("data", {})
            .get("candles", [])
        )

        logger.info(
            "historical_candles_fetched",
            candles_count=
            len(raw_candles),

            timeframe=
            timeframe,
        )

        candles = self._parse_candles(
            instrument_key=
            instrument_key,

            timeframe=
            timeframe,

            raw_candles=
            raw_candles,
        )

        logger.info(
            "historical_candle_processing_completed",
            processed_candles=
            len(candles),

            timeframe=
            timeframe,
        )

        return candles

    # =====================================================
    # Internal Helpers
    # =====================================================

    def _build_url(
        self,
        instrument_key: str,
        interval: str,
        from_date: datetime,
        to_date: datetime,
    ) -> str:

        return (
            f"{self.BASE_URL}/"
            f"{instrument_key}/"
            f"{interval}/"
            f"{to_date.strftime('%Y-%m-%d')}/"
            f"{from_date.strftime('%Y-%m-%d')}"
        )

    async def _fetch_payload(
        self,
        url: str,
    ) -> dict:

        headers = {
            "Authorization": (
                f"Bearer "
                f"{self.settings.upstox_access_token}"
            ),
            "Accept": "application/json",
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=headers,
            )

        response.raise_for_status()

        return response.json()

    def _parse_candles(
        self,
        instrument_key: str,
        timeframe: str,
        raw_candles: list,
    ) -> list[HistoricalCandle]:

        results: list[
            HistoricalCandle
        ] = []

        # =========================================
        # Upstox returns newest first
        # Replay/backtesting require oldest first
        # =========================================

        raw_candles.reverse()

        interval_minutes = (
            TIMEFRAME_TO_MINUTES[
                timeframe
            ]
        )

        for candle in raw_candles:

            start_time = (
                datetime.fromisoformat(
                    candle[0].replace(
                        "Z",
                        "+00:00",
                    )
                )
            )

            end_time = (
                start_time
                +
                timedelta(
                    minutes=
                    interval_minutes
                )
            )

            results.append(
                HistoricalCandle(
                    instrument_key=
                    instrument_key,

                    timeframe=
                    timeframe,

                    open=
                    float(candle[1]),

                    high=
                    float(candle[2]),

                    low=
                    float(candle[3]),

                    close=
                    float(candle[4]),

                    volume=
                    int(candle[5]),

                    start_time=
                    start_time,

                    end_time=
                    end_time,

                    is_closed=
                    True,
                )
            )

        return results

    def _validate_timeframe(
        self,
        timeframe: str,
    ) -> None:

        if timeframe not in (
            TIMEFRAME_TO_UPSTOX_INTERVAL
        ):

            raise ValueError(
                f"Unsupported timeframe: "
                f"{timeframe}"
            )

    # =====================================================
    # Utility Helpers
    # =====================================================

    def build_default_date_range(
        self,
        lookback_days: int,
    ) -> tuple[datetime, datetime]:

        to_date = datetime.now(
            tz=timezone.utc,
        )

        from_date = (
            to_date
            -
            timedelta(
                days=lookback_days
            )
        )

        return (
            from_date,
            to_date,
        )