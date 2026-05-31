from app.market_regime.models import (
    TrendRegime,
)


class TrendRegimeDetector:

    def detect(
        self,
        ema_fast: float,
        ema_slow: float,
        adx: float,
        close_price: float,
        vwap: float,
    ) -> TrendRegime:

        # ======================================
        # Strong Bullish Trend
        # ======================================

        if (

            ema_fast > ema_slow

            and

            close_price > vwap

            and

            adx >= 25

        ):

            return (
                TrendRegime
                .TRENDING_BULLISH
            )

        # ======================================
        # Strong Bearish Trend
        # ======================================

        if (

            ema_fast < ema_slow

            and

            close_price < vwap

            and

            adx >= 25

        ):

            return (
                TrendRegime
                .TRENDING_BEARISH
            )

        # ======================================
        # Sideways / Weak Trend
        # ======================================

        return (
            TrendRegime
            .SIDEWAYS
        )