from dataclasses import dataclass


@dataclass(slots=True)
class OIChangeAnalysis:

    strike_price: float

    call_oi_change: int

    put_oi_change: int

    call_buildup: str

    put_buildup: str