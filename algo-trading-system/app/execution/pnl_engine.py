from app.execution.models import (
    Position,
)


class PnLEngine:
    @staticmethod
    def calculate_unrealized_pnl(
        position: Position,
        market_price: float,
    ) -> float:

        if position.side.value == "LONG":
            return (
                market_price -
                position.average_price
            ) * position.quantity

        return (
            position.average_price -
            market_price
        ) * position.quantity