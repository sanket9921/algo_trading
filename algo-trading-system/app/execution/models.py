from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class PositionSide(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass(slots=True)
class ExecutedTrade:
    instrument_key: str

    side: OrderSide

    quantity: int

    execution_price: float

    executed_at: datetime

    strategy_name: str


@dataclass(slots=True)
class Position:
    instrument_key: str

    side: PositionSide

    quantity: int

    average_price: float

    stop_loss: float

    take_profit: float

    is_open: bool = True

    unrealized_pnl: float = 0.0

    realized_pnl: float = 0.0