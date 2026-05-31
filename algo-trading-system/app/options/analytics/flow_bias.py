from app.options.analytics.models import (
    OptionAnalyticsSnapshot,
)


class OptionFlowBias:

    def is_bullish(
        self,
        analytics:
        OptionAnalyticsSnapshot,
    ) -> bool:

        # ======================================
        # Bullish Conditions
        # ======================================

        bullish_put_buildup = (

            analytics.put_oi_change
            >
            analytics.call_oi_change
        )

        call_unwinding = (

            analytics.call_oi_change
            < 0
        )

        return (

            bullish_put_buildup

            or

            call_unwinding
        )

    def is_bearish(
        self,
        analytics:
        OptionAnalyticsSnapshot,
    ) -> bool:

        # ======================================
        # Bearish Conditions
        # ======================================

        bearish_call_buildup = (

            analytics.call_oi_change
            >
            analytics.put_oi_change
        )

        put_unwinding = (

            analytics.put_oi_change
            < 0
        )

        return (

            bearish_call_buildup

            or

            put_unwinding
        )