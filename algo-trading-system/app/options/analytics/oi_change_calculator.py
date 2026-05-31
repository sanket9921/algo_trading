from app.options.analytics.models import (
    OIChangeAnalysis,
)

from app.options.models import (
    OptionChainSnapshot,
)


class OIChangeCalculator:

    def calculate(
        self,
        snapshot: OptionChainSnapshot,
    ) -> OIChangeAnalysis:

        # ======================================
        # OI Delta
        # ======================================

        call_oi_change = (
            (
                snapshot.call_oi
                or 0
            )
            -
            (
                snapshot.call_prev_oi
                or 0
            )
        )

        put_oi_change = (
            (
                snapshot.put_oi
                or 0
            )
            -
            (
                snapshot.put_prev_oi
                or 0
            )
        )

        # ======================================
        # Buildup Classification
        # ======================================

        call_buildup = (
            self._classify_buildup(
                oi_change=
                call_oi_change,

                premium=
                snapshot.call_ltp,
            )
        )

        put_buildup = (
            self._classify_buildup(
                oi_change=
                put_oi_change,

                premium=
                snapshot.put_ltp,
            )
        )

        return OIChangeAnalysis(

            strike_price=
            snapshot.strike_price,

            call_oi_change=
            call_oi_change,

            put_oi_change=
            put_oi_change,

            call_buildup=
            call_buildup,

            put_buildup=
            put_buildup,
        )

    # ==================================================
    # Internal Helpers
    # ==================================================

    def _classify_buildup(
        self,
        oi_change: int,
        premium: float | None,
    ) -> str:

        if premium is None:

            return "UNKNOWN"

        # ==========================================
        # OI Increasing
        # ==========================================

        if oi_change > 0:

            if premium > 0:

                return "LONG_BUILDUP"

            return "SHORT_BUILDUP"

        # ==========================================
        # OI Decreasing
        # ==========================================

        if oi_change < 0:

            if premium > 0:

                return "SHORT_COVERING"

            return "LONG_UNWINDING"

        return "NEUTRAL"