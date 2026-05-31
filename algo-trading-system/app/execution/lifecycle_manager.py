from app.core.logger import get_logger
from app.execution.exit_manager import (
    ExitManager,
)
from app.execution.models import (
    Position,
)
from app.execution.realized_pnl import (
    RealizedPnLEngine,
)

logger = get_logger(__name__)


class LifecycleManager:
    def evaluate_position(
        self,
        position: Position,
        market_price: float,
    ) -> tuple[bool, float | None]:

        if not position.is_open:
            return False, None

        should_exit, exit_reason = (
            ExitManager.should_exit(
                position=position,
                market_price=market_price,
            )
        )

        if not should_exit:
            return False, None

        pnl = (
            RealizedPnLEngine
            .calculate(
                position=position,
                exit_price=market_price,
            )
        )

        position.is_open = False

        position.realized_pnl = pnl

        logger.info(
            "position_closed",
            instrument_key=(
                position.instrument_key
            ),
            exit_reason=exit_reason,
            realized_pnl=pnl,
        )

        return True, pnl