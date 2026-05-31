from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class MarketTick:
    instrument_key: str
    last_price: float
    volume: int
    timestamp: datetime


@dataclass(slots=True)
class MarketSubscription:
    instrument_keys: list[str]
    mode: str = "ltpc"