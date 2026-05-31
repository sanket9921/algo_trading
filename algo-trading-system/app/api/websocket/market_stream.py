from app.api.websocket.manager import (
    connection_manager,
)

from app.events.event_models import (
    TickReceivedEvent,
    TradingSignalEvent,
)

from app.events.event_models import (
    CandleClosedEvent,
)


class MarketStreamRuntime:

    async def handle_tick_event(
        self,
        event: TickReceivedEvent,
    ) -> None:

        await connection_manager.broadcast(
            {
                "type": "tick",

                "data": {
                    "instrumentKey":
                    event.tick.instrument_key,

                    "lastPrice":
                    event.tick.last_price,

                    "timestamp":
                    event.timestamp.isoformat(),
                },
            }
        )

    async def handle_signal_event(
        self,
        event: TradingSignalEvent,
    ) -> None:

        await connection_manager.broadcast(
            {
                "type": "signal",

                "data": {
                    "instrumentKey":
                    event.signal.instrument_key,

                    "signalType":
                    event.signal.signal_type,

                    "price":
                    event.signal.price,

                    "strategyName":
                    event.signal.strategy_name,

                    "timestamp":
                    event.signal.timestamp.isoformat(),
                },
            }
        )
        
    async def handle_replay_candle(
        self,
        event: CandleClosedEvent,
    ) -> None:

        candle = event.candle

        await connection_manager.broadcast(
    {
        "type": "candle",

        "data": {
            "time":
            int(
                candle.start_time
                .timestamp()
            ),

            "open":
            candle.open,

            "high":
            candle.high,

            "low":
            candle.low,

            "close":
            candle.close,
        }
    }
)