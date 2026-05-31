from app.core.logger import get_logger
from app.execution.models import (
    ExecutedTrade,
    Position,
    PositionSide,
)

from app.core.runtime_settings import (
    RuntimeSettings,
)


logger = get_logger(__name__)

class PortfolioManager:
    def __init__(
        self,
        runtime_settings: RuntimeSettings,
    ) -> None:
        self.positions: dict[
            str,
            Position,
        ] = {}
        self.runtime_settings = runtime_settings

    def apply_trade(
        self,
        trade: ExecutedTrade,
    ) -> Position:

        existing_position = (
            self.positions.get(
                trade.instrument_key
            )
        )

        if existing_position is None:
            position = Position(
                instrument_key=(
                    trade.instrument_key
                ),
                side=(
                    PositionSide.LONG
                    if trade.side.value == "BUY"
                    else PositionSide.SHORT
                ),
                quantity=trade.quantity,
                average_price=(
                    trade.execution_price
                ),

                # 1% stop loss
                stop_loss=(
                    trade.execution_price * (1 - self.runtime_settings.stop_loss_pct)
                ),

                # 2% take profit
                take_profit=(
                    trade.execution_price * (1 + self.runtime_settings.take_profit_pct)
                ),
            )

            self.positions[
                trade.instrument_key
            ] = position

            logger.info(
                "new_position_opened",
                instrument_key=(
                    trade.instrument_key
                ),
                quantity=trade.quantity,
            )

            return position

        total_quantity = (
            existing_position.quantity +
            trade.quantity
        )

        weighted_price = (
            (
                existing_position.average_price *
                existing_position.quantity
            ) +
            (
                trade.execution_price *
                trade.quantity
            )
        ) / total_quantity

        existing_position.quantity = (
            total_quantity
        )

        existing_position.average_price = (
            weighted_price
        )

        logger.info(
            "position_updated",
            instrument_key=(
                existing_position
                .instrument_key
            ),
            quantity=(
                existing_position.quantity
            ),
        )

        return existing_position