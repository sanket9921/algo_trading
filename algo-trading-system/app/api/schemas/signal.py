from pydantic import (
    BaseModel,
)


class SignalResponse(
    BaseModel
):

    signal_type: str

    strategy_name: str

    price: float

    timestamp: int