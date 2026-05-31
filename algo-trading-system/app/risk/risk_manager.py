from app.core.config import get_settings
from app.core.logger import get_logger
from app.risk.models import RiskDecision
from app.risk.position_sizing import (
    PositionSizer,
)
from app.risk.trade_limits import (
    TradeLimitManager,
)
from app.strategy.models import (
    TradingSignal,
)

logger = get_logger(__name__)


class RiskManager:
    def __init__(self) -> None:
        self.settings = get_settings()

        self.trade_limits = (
            TradeLimitManager()
        )

        self.account_capital = 100000.0

    def validate_signal(
        self,
        signal: TradingSignal,
    ) -> RiskDecision:

        if not self.trade_limits.can_trade():
            logger.warning(
                "risk_rejected_max_trades_reached",
                instrument_key=signal.instrument_key,
            )

            return RiskDecision(
                approved=False,
                reason="Max daily trades reached",
            )

        stop_loss_price = (
            signal.price * 0.99
        )

        quantity = (
            PositionSizer.calculate_quantity(
                capital=self.account_capital,
                risk_percent=self.settings.risk_per_trade,
                entry_price=signal.price,
                stop_loss_price=stop_loss_price,
            )
        )

        if quantity <= 0:
            return RiskDecision(
                approved=False,
                reason="Invalid quantity calculated",
            )

        self.trade_limits.register_trade()

        logger.info(
            "risk_signal_approved",
            instrument_key=signal.instrument_key,
            quantity=quantity,
        )

        return RiskDecision(
            approved=True,
            risk_amount=(
                self.account_capital *
                self.settings.risk_per_trade
            ) / 100,
            suggested_quantity=quantity,
        )