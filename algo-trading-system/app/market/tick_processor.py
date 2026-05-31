from datetime import datetime, timezone

from app.core.logger import get_logger
from app.market.models import Tick

logger = get_logger(__name__)


class TickProcessor:
    def process(
        self,
        instrument_key: str,
        last_price: float,
        volume: int,
    ) -> Tick:
        tick = Tick(
            instrument_key=instrument_key,
            last_price=last_price,
            volume=volume,
            timestamp=datetime.now(
                tz=timezone.utc
            ),
        )

        logger.info(
            "tick_processed",
            instrument_key=tick.instrument_key,
            last_price=tick.last_price,
        )

        return tick