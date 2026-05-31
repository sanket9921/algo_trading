from dataclasses import dataclass


@dataclass(slots=True)
class TimeframeContext:

    timeframe: str

    bullish_trend: bool

    bearish_trend: bool

    strong_trend: bool

    above_vwap: bool

    adx_value: float

    ema_fast: float

    ema_slow: float