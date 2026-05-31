from datetime import (
    datetime,
    timezone,
)

import httpx

from app.core.config import (
    get_settings,
)

from app.core.logger import (
    get_logger,
)

from app.options.expiry_resolver import (
    OptionExpiryResolver,
)

from app.options.models import (
    OptionChainSnapshot,
)

logger = get_logger(__name__)


class OptionChainClient:

    BASE_URL = (
        "https://api.upstox.com/v2/"
        "option/chain"
    )

    def __init__(self) -> None:

        self.settings = (
            get_settings()
        )

        self.expiry_resolver = (
            OptionExpiryResolver()
        )

    # =====================================================
    # Public API
    # =====================================================

    async def fetch_option_chain(
        self,
        instrument_key: str,
    ) -> list[
        OptionChainSnapshot
    ]:

        expiry_date = (
            await self.expiry_resolver
            .get_nearest_expiry(
                instrument_key
            )
        )

        logger.info(
            "option_chain_fetch_started",
            instrument_key=
            instrument_key,

            expiry_date=
            expiry_date,
        )

        headers = {

            "Accept":
            "application/json",

            "Authorization":
            (
                f"Bearer "
                f"{self.settings.upstox_access_token}"
            ),
        }

        params = {

            "instrument_key":
            instrument_key,

            "expiry_date":
            expiry_date,
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.BASE_URL,
                headers=headers,
                params=params,
            )

        logger.info(
            "option_chain_http_response",
            status_code=
            response.status_code,

            response_text=
            response.text,
        )

        response.raise_for_status()

        payload = response.json()

        raw_data = (
            payload
            .get("data", [])
        )

        logger.info(
            "option_chain_fetch_completed",
            strikes_count=
            len(raw_data),
        )

        # ==========================================
        # Normalize Snapshot Time
        # Prevent Duplicate Snapshots
        # ==========================================

        current_time = datetime.now(
            tz=timezone.utc,
        )

        snapshot_time = current_time.replace(
            second=0,
            microsecond=0,
        )

        snapshots: list[
            OptionChainSnapshot
        ] = []

        for item in raw_data:

            call_options = (
                item.get(
                    "call_options",
                    {}
                )
            )

            put_options = (
                item.get(
                    "put_options",
                    {}
                )
            )

            call_market_data = (
                call_options.get(
                    "market_data",
                    {}
                )
            )

            put_market_data = (
                put_options.get(
                    "market_data",
                    {}
                )
            )

            snapshots.append(
                OptionChainSnapshot(

                    # ==================================
                    # Core Context
                    # ==================================

                    instrument_key=
                    instrument_key,

                    expiry=
                    item.get(
                        "expiry",
                        expiry_date,
                    ),

                    strike_price=
                    float(
                        item.get(
                            "strike_price",
                            0,
                        )
                    ),

                    snapshot_time=
                    snapshot_time,

                    underlying_spot_price=
                    self._safe_float(
                        item.get(
                            "underlying_spot_price"
                        )
                    ) or 0.0,

                    # ==================================
                    # Call Side
                    # ==================================

                    call_ltp=
                    self._safe_float(
                        call_market_data.get(
                            "ltp"
                        )
                    ),

                    call_volume=
                    self._safe_int(
                        call_market_data.get(
                            "volume"
                        )
                    ),

                    call_oi=
                    self._safe_int(
                        call_market_data.get(
                            "oi"
                        )
                    ),

                    call_prev_oi=
                    self._safe_int(
                        call_market_data.get(
                            "prev_oi"
                        )
                    ),

                    call_iv=
                    self._safe_float(
                        call_options
                        .get(
                            "option_greeks",
                            {}
                        )
                        .get("iv")
                    ),

                    call_theta=
                    self._safe_float(
                        call_options
                        .get(
                            "option_greeks",
                            {}
                        )
                        .get("theta")
                    ),

                    call_delta=
                    self._safe_float(
                        call_options
                        .get(
                            "option_greeks",
                            {}
                        )
                        .get("delta")
                    ),

                    # ==================================
                    # Put Side
                    # ==================================

                    put_ltp=
                    self._safe_float(
                        put_market_data.get(
                            "ltp"
                        )
                    ),

                    put_volume=
                    self._safe_int(
                        put_market_data.get(
                            "volume"
                        )
                    ),

                    put_oi=
                    self._safe_int(
                        put_market_data.get(
                            "oi"
                        )
                    ),

                    put_prev_oi=
                    self._safe_int(
                        put_market_data.get(
                            "prev_oi"
                        )
                    ),

                    put_iv=
                    self._safe_float(
                        put_options
                        .get(
                            "option_greeks",
                            {}
                        )
                        .get("iv")
                    ),

                    put_theta=
                    self._safe_float(
                        put_options
                        .get(
                            "option_greeks",
                            {}
                        )
                        .get("theta")
                    ),

                    put_delta=
                    self._safe_float(
                        put_options
                        .get(
                            "option_greeks",
                            {}
                        )
                        .get("delta")
                    ),
                )
            )

        logger.info(
            "option_chain_normalization_completed",
            snapshots_count=
            len(snapshots),
        )

        return snapshots

    # =====================================================
    # Internal Helpers
    # =====================================================

    def _safe_float(
        self,
        value: object,
    ) -> float | None:

        if value is None:
            return None

        try:

            return float(value)

        except (
            TypeError,
            ValueError,
        ):

            return None

    def _safe_int(
        self,
        value: object,
    ) -> int | None:

        if value is None:
            return None

        try:

            return int(value)

        except (
            TypeError,
            ValueError,
        ):

            return None