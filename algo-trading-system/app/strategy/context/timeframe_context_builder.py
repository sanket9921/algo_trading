from app.indicators.models import (
    IndicatorSnapshot,
)

from app.strategy.context.models import (
    TimeframeContext,
)


class TimeframeContextBuilder:

    def build(
        self,
        timeframe: str,
        indicators: IndicatorSnapshot,
        close_price: float,
    ) -> TimeframeContext:

        ema_fast = (
            indicators.ema_9
        )

        ema_slow = (
            indicators.ema_21
        )

        adx_value = (
            indicators.adx_14
        )

        vwap = (
            indicators.vwap
        )

        bullish_trend = False

        bearish_trend = False

        strong_trend = False

        above_vwap = False

        if (
            ema_fast is not None
            and
            ema_slow is not None
        ):

            bullish_trend = (
                ema_fast > ema_slow
            )

            bearish_trend = (
                ema_fast < ema_slow
            )

        if adx_value is not None:

            strong_trend = (
                adx_value >= 25
            )

        if vwap is not None:

            above_vwap = (
                close_price > vwap
            )

        return TimeframeContext(

            timeframe=
            timeframe,

            bullish_trend=
            bullish_trend,

            bearish_trend=
            bearish_trend,

            strong_trend=
            strong_trend,

            above_vwap=
            above_vwap,

            adx_value=
            adx_value or 0.0,

            ema_fast=
            ema_fast or 0.0,

            ema_slow=
            ema_slow or 0.0,
        )