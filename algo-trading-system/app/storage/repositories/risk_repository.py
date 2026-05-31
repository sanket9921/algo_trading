from datetime import datetime, timezone

from app.risk.models import RiskDecision
from app.storage.database import (
    AsyncSessionLocal,
)
from app.storage.models import (
    RiskDecisionEntity,
)
from app.strategy.models import (
    TradingSignal,
)


class RiskRepository:
    async def save(
        self,
        signal: TradingSignal,
        decision: RiskDecision,
    ) -> None:
        async with AsyncSessionLocal() as session:
            entity = RiskDecisionEntity(
                instrument_key=signal.instrument_key,
                approved=decision.approved,
                reason=decision.reason,
                suggested_quantity=(
                    decision.suggested_quantity
                ),
                timestamp=datetime.now(
                    tz=timezone.utc,
                ),
            )

            session.add(entity)

            await session.commit()