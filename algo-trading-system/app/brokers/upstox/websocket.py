import asyncio
from datetime import datetime, timezone

import websockets
from websockets.asyncio.client import ClientConnection

from app.brokers.upstox.constants import (
    DEFAULT_RECONNECT_DELAY,
    MAX_RECONNECT_ATTEMPTS,
    UPSTOX_WS_URL,
)
from app.brokers.upstox.decoder import (
    decode_market_feed,
)
from app.brokers.upstox.models import (
    MarketSubscription,
)
from app.brokers.upstox.subscription import (
    build_subscription_payload,
)
from app.core.config import get_settings
from app.core.logger import get_logger
from app.events.event_bus import EventBus
from app.events.event_models import (
    TickReceivedEvent,
)
from app.market.tick_processor import (
    TickProcessor,
)

logger = get_logger(__name__)


class UpstoxWebSocketClient:
    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self.settings = get_settings()

        self.websocket: (
            ClientConnection | None
        ) = None

        self.event_bus = event_bus

        self.running = False

        self.tick_processor = (
            TickProcessor()
        )

    async def connect(self) -> None:
        reconnect_attempts = 0

        while (
            reconnect_attempts
            < MAX_RECONNECT_ATTEMPTS
        ):
            try:
                logger.info(
                    "upstox_websocket_connecting",
                    attempt=(
                        reconnect_attempts + 1
                    ),
                )

                self.websocket = (
                    await websockets.connect(
                        UPSTOX_WS_URL,
                        additional_headers={
                            "Authorization": (
                                f"Bearer "
                                f"{self.settings.upstox_access_token}"
                            )
                        },
                        ping_interval=20,
                        ping_timeout=20,
                    )
                )

                logger.info(
                    "upstox_websocket_connected",
                )

                await self.subscribe()

                await self.listen()

            except Exception as exc:
                reconnect_attempts += 1

                logger.exception(
                    "upstox_websocket_connection_failed",
                    error=str(exc),
                    reconnect_attempts=(
                        reconnect_attempts
                    ),
                )

                await asyncio.sleep(
                    DEFAULT_RECONNECT_DELAY
                )

    async def subscribe(self) -> None:
        if self.websocket is None:
            return

        subscription = MarketSubscription(
            instrument_keys=[
                # Reliance Industries
                "NSE_INDEX|Nifty 50",
            ],
            mode="ltpc",
        )

        payload = (
            build_subscription_payload(
                subscription
            )
        )

        # ==========================================
        # Upstox V3 requires binary frame
        # ==========================================

        await self.websocket.send(
            payload.encode()
        )

        logger.info(
            "upstox_subscription_sent",
            payload=payload,
        )

    async def listen(self) -> None:
        if self.websocket is None:
            return

        async for message in self.websocket:
            await self.handle_message(
                message
            )

    async def handle_message(
        self,
        raw_message,
    ) -> None:

        try:
            # ==========================================
            # Ignore non-binary messages
            # ==========================================

            if not isinstance(
                raw_message,
                bytes,
            ):
                logger.warning(
                    "non_binary_message_received",
                    message_type=str(
                        type(raw_message)
                    ),
                )
                return

            logger.info(
                "upstox_binary_message_received",
                size=len(raw_message),
            )

            decoded = decode_market_feed(
                raw_message
            )

            logger.info(
                "upstox_message_decoded",
                payload=str(decoded),
            )

            # ==========================================
            # Ignore messages without feeds
            # ==========================================

            if not hasattr(
                decoded,
                "feeds",
            ):
                logger.info(
                    "message_without_feeds_skipped",
                )
                return

            feeds = decoded.feeds

            if not feeds:
                logger.info(
                    "empty_feed_message_received",
                )
                return

            logger.info(
                "live_feed_received",
                feeds_count=len(feeds),
                current_ts=str(
                    decoded.currentTs
                ),
            )

            for (
                instrument_key,
                feed,
            ) in feeds.items():

                logger.info(
                    "upstox_feed_structure",
                    instrument_key=
                    instrument_key,
                    feed=str(feed),
                )

                # ==========================================
                # Ensure LTPC exists
                # ==========================================

                if not feed.HasField(
                    "ltpc"
                ):
                    logger.warning(
                        "ltpc_field_missing",
                        instrument_key=
                        instrument_key,
                    )
                    continue

                ltpc = feed.ltpc

                logger.info(
                    "ltpc_received",
                    instrument_key=
                    instrument_key,
                    ltp=ltpc.ltp,
                )

                tick = (
                    self.tick_processor
                    .process(
                        instrument_key=
                        instrument_key,
                        last_price=
                        ltpc.ltp,
                        volume=0,
                    )
                )

                logger.info(
                    "live_market_tick_received",
                    instrument_key=
                    tick.instrument_key,
                    last_price=
                    tick.last_price,
                )

                await self.event_bus.publish(
                    TickReceivedEvent(
                        timestamp=datetime.now(
                            tz=timezone.utc,
                        ),
                        tick=tick,
                    )
                )

        except Exception as exc:
            logger.exception(
                "upstox_message_processing_failed",
                error=str(exc),
            )

    async def close(self) -> None:
        if self.websocket:
            await self.websocket.close()

            logger.info(
                "upstox_websocket_closed",
            )