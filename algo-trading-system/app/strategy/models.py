from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class PositionState(
    str,
    Enum,
):
    FLAT = "FLAT"

    LONG = "LONG"

    SHORT = "SHORT"


@dataclass(slots=True)
class TradingSignal:
    instrument_key: str

    signal_type: SignalType

    price: float

    timestamp: datetime

    strategy_name: str
    
    is_replay: bool = False