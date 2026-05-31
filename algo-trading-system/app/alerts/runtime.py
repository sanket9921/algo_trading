from app.alerts.client import (
    TelegramClient,
)
from app.alerts.formatter import (
    AlertFormatter,
)
from app.core.logger import get_logger
from app.events.event_models import (
    RiskValidatedEvent,
    TradingSignalEvent,
)

logger = get_logger(__name__)


class AlertRuntime:
    def __init__(self) -> None:
        self.client = TelegramClient()

    async def handle_signal_event(
        self,
        event: TradingSignalEvent,
    ) -> None:
        message = (
            AlertFormatter
            .format_signal_alert(
                event.signal
            )
        )

        await self.client.send_message(
            message
        )

        logger.info(
            "signal_alert_sent"
        )

    async def handle_risk_event(
        self,
        event: RiskValidatedEvent,
    ) -> None:

        # Ignore ordinary rejections
        if not event.decision.approved:
            logger.info(
                "risk_alert_skipped_for_rejection",
                reason=event.decision.reason,
            )
            return

        message = (
            AlertFormatter
            .format_risk_alert(
                signal=event.signal,
                decision=event.decision,
            )
        )

        await self.client.send_message(
            message
        )

        logger.info(
            "risk_alert_sent"
        )