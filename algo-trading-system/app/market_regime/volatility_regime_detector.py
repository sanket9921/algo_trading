from app.market_regime.models import (
    VolatilityRegime,
)


class VolatilityRegimeDetector:

    def detect(
        self,
        atr: float,
        close_price: float,
    ) -> VolatilityRegime:

        if close_price <= 0:

            return (
                VolatilityRegime
                .NORMAL_VOLATILITY
            )

        volatility_ratio = (
            atr
            /
            close_price
        )

        # ======================================
        # Low Volatility
        # ======================================

        if volatility_ratio < 0.003:

            return (
                VolatilityRegime
                .LOW_VOLATILITY
            )

        # ======================================
        # High Volatility
        # ======================================

        if volatility_ratio > 0.01:

            return (
                VolatilityRegime
                .HIGH_VOLATILITY
            )

        return (
            VolatilityRegime
            .NORMAL_VOLATILITY
        )