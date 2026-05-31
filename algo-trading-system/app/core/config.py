from enum import Enum
from functools import lru_cache

from pydantic import (
    Field,
)

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from app.core.runtime_mode import (
    RuntimeMode,
)


# =========================================================
# Market Data Modes
# =========================================================

class MarketDataMode(
    str,
    Enum,
):
    LIVE = "LIVE"

    REPLAY = "REPLAY"

    SIMULATOR = "SIMULATOR"


# =========================================================
# Application Settings
# =========================================================

class Settings(
    BaseSettings
):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    # =====================================================
    # Application
    # =====================================================

    app_name: str = (
        "AlgoTradingSystem"
    )

    app_env: str = (
        "development"
    )

    debug: bool = True

    log_level: str = "INFO"

    # =====================================================
    # Runtime
    # =====================================================

    runtime_mode: RuntimeMode = (
        RuntimeMode.DEVELOPMENT
    )

    market_data_mode: (
        MarketDataMode
    ) = (
        MarketDataMode.REPLAY
    )

    # =====================================================
    # Replay Settings
    # =====================================================

    replay_speed_seconds: float = (
        0.2
    )

    replay_candle_limit: int = (
        500
    )

    # =====================================================
    # Trading Settings
    # =====================================================

    default_instrument_key: str = (
        "NSE_INDEX|Nifty 50"
    )

    default_timeframe: str = (
        "1m"
    )

    supported_timeframes: list[str] = (
        [
            "1m",
            "5m",
            "15m",
        ]
    )

    # =====================================================
    # Historical Data Settings
    # =====================================================

    historical_default_lookback_days: int = (
        30
    )

    historical_sync_interval_seconds: int = (
        60
    )

    historical_batch_days: int = (
        28
    )

    historical_enable_gap_recovery: bool = (
        True
    )

    historical_auto_sync: bool = (
        True
    )

    # =====================================================
    # Upstox
    # =====================================================

    upstox_api_key: str = (
        Field(default="")
    )

    upstox_api_secret: str = (
        Field(default="")
    )

    upstox_access_token: str = (
        Field(default="")
    )

    # =====================================================
    # Telegram
    # =====================================================

    telegram_bot_token: str = (
        Field(default="")
    )

    telegram_chat_id: str = (
        Field(default="")
    )

    # =====================================================
    # Database
    # =====================================================

    database_url: str = (
        "sqlite+aiosqlite:///data/trading.db"
    )

    # =====================================================
    # Risk Management
    # =====================================================

    risk_per_trade: float = (
        1.0
    )

    max_daily_loss: float = (
        3.0
    )

    max_trades_per_day: int = (
        3
    )

    # =====================================================
    # Option Chain Collection
    # =====================================================

    option_chain_enabled: bool = True

    option_chain_sync_interval_seconds: int = 60

    option_chain_instrument_key: str = (
        "NSE_INDEX|Nifty 50"
    )

# =========================================================
# Cached Settings Instance
# =========================================================

@lru_cache
def get_settings() -> Settings:
    return Settings()