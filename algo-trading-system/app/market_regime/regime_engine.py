from datetime import (
    datetime,
    timezone,
)

from app.market_regime.models import (
    MarketRegime,
)

from app.market_regime.trend_regime_detector import (
    TrendRegimeDetector,
)

from app.market_regime.volatility_regime_detector import (
    VolatilityRegimeDetector,
)


class RegimeEngine:

    def __init__(self) -> None:

        self.trend_detector = (
            TrendRegimeDetector()
        )

        self.volatility_detector = (
            VolatilityRegimeDetector()
        )

    # =====================================================
    # Public API
    # =====================================================

    def analyze(
        self,
        ema_fast: float,
        ema_slow: float,
        adx: float,
        atr: float,
        close_price: float,
        vwap: float,
    ) -> MarketRegime:

        trend_regime = (
            self.trend_detector
            .detect(

                ema_fast=
                ema_fast,

                ema_slow=
                ema_slow,

                adx=
                adx,

                close_price=
                close_price,

                vwap=
                vwap,
            )
        )

        volatility_regime = (
            self.volatility_detector
            .detect(

                atr=
                atr,

                close_price=
                close_price,
            )
        )

        return MarketRegime(

            timestamp=
            datetime.now(
                tz=timezone.utc,
            ),

            trend_regime=
            trend_regime,

            volatility_regime=
            volatility_regime,

            adx_value=
            adx,

            atr_value=
            atr,
        )