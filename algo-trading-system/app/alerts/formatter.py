from app.risk.models import RiskDecision
from app.strategy.models import (
    TradingSignal,
)


class AlertFormatter:
    @staticmethod
    def format_signal_alert(
        signal: TradingSignal,
    ) -> str:
        return (
            "🚨 Trading Signal\n\n"
            f"Instrument: "
            f"{signal.instrument_key}\n"
            f"Signal: "
            f"{signal.signal_type.value}\n"
            f"Price: "
            f"{signal.price}\n"
            f"Strategy: "
            f"{signal.strategy_name}"
        )

    @staticmethod
    def format_risk_alert(
        signal: TradingSignal,
        decision: RiskDecision,
    ) -> str:
        status = (
            "✅ APPROVED"
            if decision.approved
            else "❌ REJECTED"
        )

        return (
            "🛡 Risk Validation\n\n"
            f"Status: {status}\n"
            f"Instrument: "
            f"{signal.instrument_key}\n"
            f"Signal: "
            f"{signal.signal_type.value}\n"
            f"Quantity: "
            f"{decision.suggested_quantity}\n"
            f"Reason: "
            f"{decision.reason}"
        )

    @staticmethod
    def format_system_alert(
        message: str,
    ) -> str:
        return (
            "⚙️ System Alert\n\n"
            f"{message}"
        )