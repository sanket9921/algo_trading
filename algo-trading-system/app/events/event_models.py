from dataclasses import dataclass
from datetime import datetime

from app.market.models import Candle, Tick
from app.indicators.models import (
    IndicatorSnapshot,
)
from app.risk.models import RiskDecision
from app.strategy.models import TradingSignal
from app.execution.models import (
    ExecutedTrade,
    Position,
)

@dataclass(slots=True)
class BaseEvent:
    timestamp: datetime


@dataclass(slots=True)
class TickReceivedEvent(BaseEvent):
    tick: Tick


@dataclass(slots=True)
class CandleClosedEvent(BaseEvent):
    candle: Candle
    is_replay: bool = False
    
@dataclass(slots=True)
class IndicatorCalculatedEvent(
    BaseEvent
):
    candle: Candle
    indicators: IndicatorSnapshot   

@dataclass(slots=True)
class TradingSignalEvent(
    BaseEvent
):
    signal: TradingSignal

@dataclass(slots=True)
class RiskValidatedEvent(
    BaseEvent
):
    signal: TradingSignal
    decision: RiskDecision
    
@dataclass(slots=True)
class TradeExecutedEvent(
    BaseEvent
):
    trade: ExecutedTrade
    position: Position
    is_replay: bool = False

@dataclass(slots=True)
class PositionClosedEvent(
    BaseEvent
):
    position: Position

    realized_pnl: float
    is_replay: bool = False