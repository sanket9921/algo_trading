import httpx

from app.core.config import (
    get_settings,
)

from app.core.logger import (
    get_logger,
)

logger = get_logger(__name__)


class OptionExpiryResolver:

    BASE_URL = (
        "https://api.upstox.com/v2/"
        "option/contract"
    )

    def __init__(self) -> None:

        self.settings = (
            get_settings()
        )

    async def get_nearest_expiry(
        self,
        instrument_key: str,
    ) -> str:

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
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.BASE_URL,
                headers=headers,
                params=params,
            )

        logger.info(
            "option_contract_response",
            status_code=
            response.status_code,

            response_text=
            response.text,
        )

        response.raise_for_status()

        payload = response.json()

        contracts = (
            payload
            .get("data", [])
        )

        expiries = sorted(
            {

                contract.get(
                    "expiry"
                )

                for contract
                in contracts

                if contract.get(
                    "expiry"
                )
            }
        )

        if not expiries:

            raise ValueError(
                (
                    "No active option "
                    "expiries found"
                )
            )

        nearest_expiry = (
            expiries[0]
        )

        logger.info(
            "nearest_option_expiry_resolved",
            expiry=
            nearest_expiry,
        )

        return nearest_expiry