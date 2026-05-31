from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class IndicatorSnapshot:
    instrument_key: str

    ema_9: float | None = None
    ema_21: float | None = None

    rsi_14: float | None = None

    vwap: float | None = None

    adx_14: float | None = None
    
    timestamp: datetime | None = None