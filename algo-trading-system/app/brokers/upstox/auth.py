from app.core.config import get_settings
from app.core.exceptions import BrokerError


def validate_upstox_credentials() -> None:
    settings = get_settings()

    required_fields = {
        "UPSTOX_API_KEY": settings.upstox_api_key,
        "UPSTOX_API_SECRET": settings.upstox_api_secret,
        "UPSTOX_ACCESS_TOKEN": settings.upstox_access_token,
    }

    missing = [
        key
        for key, value in required_fields.items()
        if not value
    ]

    if missing:
        raise BrokerError(
            f"Missing required Upstox credentials: {', '.join(missing)}"
        )