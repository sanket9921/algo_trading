from app.options.market_structure.models import (
    OptionMarketStructure,
)

from app.options.models import (
    OptionChainSnapshot,
)


class StrikeStrengthCalculator:

    def calculate(
        self,
        snapshots: list[
            OptionChainSnapshot
        ],
    ) -> OptionMarketStructure:

        if not snapshots:

            raise ValueError(
                (
                    "Cannot calculate "
                    "market structure "
                    "from empty snapshots"
                )
            )

        # ======================================
        # Strongest Put OI
        # Support Zone
        # ======================================

        strongest_put_snapshot = max(

            snapshots,

            key=lambda snapshot:
            snapshot.put_oi or 0,
        )

        # ======================================
        # Strongest Call OI
        # Resistance Zone
        # ======================================

        strongest_call_snapshot = max(

            snapshots,

            key=lambda snapshot:
            snapshot.call_oi or 0,
        )

        # ======================================
        # Aggregate Market Pressure
        # ======================================

        total_put_oi = sum(

            snapshot.put_oi or 0

            for snapshot
            in snapshots
        )

        total_call_oi = sum(

            snapshot.call_oi or 0

            for snapshot
            in snapshots
        )

        total_oi = (
            total_put_oi
            +
            total_call_oi
        )

        bullish_strength = 0.0

        bearish_strength = 0.0

        if total_oi > 0:

            bullish_strength = (
                total_put_oi
                /
                total_oi
            )

            bearish_strength = (
                total_call_oi
                /
                total_oi
            )

        return OptionMarketStructure(

            snapshot_time=
            snapshots[0]
            .snapshot_time,

            strongest_support=
            strongest_put_snapshot
            .strike_price,

            strongest_resistance=
            strongest_call_snapshot
            .strike_price,

            highest_put_oi=
            strongest_put_snapshot
            .put_oi or 0,

            highest_call_oi=
            strongest_call_snapshot
            .call_oi or 0,

            bullish_strength=
            round(
                bullish_strength,
                4,
            ),

            bearish_strength=
            round(
                bearish_strength,
                4,
            ),
        )