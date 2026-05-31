from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class OptionChainSnapshot:

    # ==========================================
    # Core Context
    # ==========================================

    instrument_key: str

    expiry: str

    strike_price: float

    snapshot_time: datetime

    underlying_spot_price: float

    # ==========================================
    # Call Side
    # ==========================================

    call_ltp: float | None = None

    call_volume: int | None = None

    call_oi: int | None = None

    call_prev_oi: int | None = None

    call_iv: float | None = None

    call_theta: float | None = None

    call_delta: float | None = None

    # ==========================================
    # Put Side
    # ==========================================

    put_ltp: float | None = None

    put_volume: int | None = None

    put_oi: int | None = None

    put_prev_oi: int | None = None

    put_iv: float | None = None

    put_theta: float | None = None

    put_delta: float | None = None