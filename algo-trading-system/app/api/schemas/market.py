from pydantic import BaseModel


class TickStreamMessage(
    BaseModel,
):
    instrument_key: str

    last_price: float

    timestamp: str