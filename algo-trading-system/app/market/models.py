from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Tick:
    instrument_key: str
    last_price: float
    volume: int
    timestamp: datetime


@dataclass(slots=True)
class Candle:
    instrument_key: str

    timeframe: str

    open: float
    high: float
    low: float
    close: float

    volume: int

    start_time: datetime
    end_time: datetime

    is_closed: bool = False