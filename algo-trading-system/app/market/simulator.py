import asyncio
import random
from datetime import datetime, timezone

from app.core.logger import get_logger
from app.events.event_bus import EventBus
from app.events.event_models import TickReceivedEvent
from app.market.models import Tick

logger = get_logger(__name__)


class MarketDataSimulator:
    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self.event_bus = event_bus

        self.base_price = 22500.0

        self.instrument_key = "NSE_INDEX|Nifty 50"

    async def start(self) -> None:
        logger.info(
            "market_data_simulator_started"
        )

        while True:
            simulated_move = random.uniform(
                -20,
                20,
            )

            self.base_price += simulated_move

            tick = Tick(
                instrument_key=self.instrument_key,
                last_price=round(
                    self.base_price,
                    2,
                ),
                volume=random.randint(
                    100,
                    1000,
                ),
                timestamp=datetime.now(
                    tz=timezone.utc,
                ),
            )

            logger.info(
                "simulated_tick_generated",
                instrument_key=tick.instrument_key,
                last_price=tick.last_price,
            )

            await self.event_bus.publish(
                TickReceivedEvent(
                    timestamp=datetime.now(
                        tz=timezone.utc,
                    ),
                    tick=tick,
                )
            )

            await asyncio.sleep(1)