class PositionSizer:
    @staticmethod
    def calculate_quantity(
        capital: float,
        risk_percent: float,
        entry_price: float,
        stop_loss_price: float,
    ) -> int:
        risk_amount = (
            capital *
            risk_percent
        ) / 100

        per_share_risk = abs(
            entry_price -
            stop_loss_price
        )

        if per_share_risk <= 0:
            return 0

        quantity = int(
            risk_amount /
            per_share_risk
        )

        return max(quantity, 0)