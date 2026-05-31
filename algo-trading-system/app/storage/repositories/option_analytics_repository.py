from sqlalchemy.dialects.sqlite import (
    insert,
)

from app.options.analytics.models import (
    OIChangeAnalysis,
)

from app.options.models import (
    OptionChainSnapshot,
)

from app.storage.database import (
    AsyncSessionLocal,
)

from app.storage.models import (
    OptionAnalyticsSnapshotEntity,
)


class OptionAnalyticsRepository:

    async def bulk_save(
        self,
        snapshots: list[
            OptionChainSnapshot
        ],
        analyses: list[
            OIChangeAnalysis
        ],
    ) -> int:

        if not snapshots:
            return 0

        async with (
            AsyncSessionLocal()
            as session
        ):

            values = []

            for (
                snapshot,
                analysis,
            ) in zip(
                snapshots,
                analyses,
            ):

                values.append(
                    {

                        # ==================
                        # Core Context
                        # ==================

                        "instrument_key":
                        snapshot.instrument_key,

                        "expiry":
                        snapshot.expiry,

                        "strike_price":
                        snapshot.strike_price,

                        "snapshot_time":
                        snapshot.snapshot_time,

                        # ==================
                        # OI Intelligence
                        # ==================

                        "call_oi_change":
                        analysis.call_oi_change,

                        "put_oi_change":
                        analysis.put_oi_change,

                        # ==================
                        # Behavioral State
                        # ==================

                        "call_buildup":
                        analysis.call_buildup,

                        "put_buildup":
                        analysis.put_buildup,
                    }
                )

            statement = (
                insert(
                    OptionAnalyticsSnapshotEntity
                )
                .values(values)
                .on_conflict_do_nothing(
                    index_elements=[

                        "instrument_key",

                        "expiry",

                        "strike_price",

                        "snapshot_time",
                    ]
                )
            )

            result = (
                await session.execute(
                    statement
                )
            )

            await session.commit()

            return (
                result.rowcount
                or 0
            )