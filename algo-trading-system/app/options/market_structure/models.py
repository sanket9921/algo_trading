from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class OptionMarketStructure:

    snapshot_time: datetime

    strongest_support: float

    strongest_resistance: float

    highest_put_oi: int

    highest_call_oi: int

    bullish_strength: float

    bearish_strength: float