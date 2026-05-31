from app.storage.database import (
    AsyncSessionLocal,
)
from app.storage.models import SignalEntity
from app.strategy.models import TradingSignal


class SignalRepository:
    async def save(
        self,
        signal: TradingSignal,
    ) -> None:
        async with AsyncSessionLocal() as session:
            entity = SignalEntity(
                instrument_key=signal.instrument_key,
                signal_type=signal.signal_type.value,
                strategy_name=signal.strategy_name,
                price=signal.price,
                timestamp=signal.timestamp,
            )

            session.add(entity)

            await session.commit()