from pydantic import (
    BaseModel,
)


class CandleResponse(
    BaseModel
):
    time: int

    open: float

    high: float

    low: float

    close: float

    volume: int