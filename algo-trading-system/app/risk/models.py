from dataclasses import dataclass


@dataclass(slots=True)
class RiskDecision:
    approved: bool

    reason: str | None = None

    risk_amount: float | None = None

    suggested_quantity: int | None = None