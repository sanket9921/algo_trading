from datetime import datetime, timezone

from app.core.logger import get_logger
from app.events.event_bus import EventBus
from app.events.event_models import (
    RiskValidatedEvent,
    TradingSignalEvent,
)
from app.risk.risk_manager import (
    RiskManager,
)

logger = get_logger(__name__)


class RiskRuntime:
    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self.event_bus = event_bus

        self.manager = RiskManager()

    async def handle_signal_event(
        self,
        event: TradingSignalEvent,
    ) -> None:
        decision = (
            self.manager.validate_signal(
                event.signal
            )
        )

        logger.info(
            "risk_validation_completed",
            approved=decision.approved,
            reason=decision.reason,
        )

        await self.event_bus.publish(
            RiskValidatedEvent(
                timestamp=datetime.now(
                    tz=timezone.utc,
                ),
                signal=event.signal,
                decision=decision,
            )
        )