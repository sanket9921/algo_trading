from app.brokers.upstox.auth import validate_upstox_credentials
from app.brokers.upstox.websocket import UpstoxWebSocketClient
from app.events.event_bus import EventBus


class UpstoxBrokerClient:
    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        validate_upstox_credentials()

        self.websocket_client = UpstoxWebSocketClient(
            event_bus=event_bus,
        )

    async def start(self) -> None:
        await self.websocket_client.connect()

    async def stop(self) -> None:
        await self.websocket_client.close()