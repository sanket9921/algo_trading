from app.execution.models import (
    Position,
)


class ExitManager:
    @staticmethod
    def should_exit(
        position: Position,
        market_price: float,
    ) -> tuple[bool, str | None]:

        # LONG POSITION
        if position.side.value == "LONG":

            if market_price <= (
                position.stop_loss
            ):
                return True, "STOP_LOSS"

            if market_price >= (
                position.take_profit
            ):
                return True, "TAKE_PROFIT"

        # SHORT POSITION
        else:
            if market_price >= (
                position.stop_loss
            ):
                return True, "STOP_LOSS"

            if market_price <= (
                position.take_profit
            ):
                return True, "TAKE_PROFIT"

        return False, None