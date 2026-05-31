from app.execution.models import (
    Position,
)


class RealizedPnLEngine:
    @staticmethod
    def calculate(
        position: Position,
        exit_price: float,
    ) -> float:

        if position.side.value == "LONG":
            return (
                exit_price -
                position.average_price
            ) * position.quantity

        return (
            position.average_price -
            exit_price
        ) * position.quantity