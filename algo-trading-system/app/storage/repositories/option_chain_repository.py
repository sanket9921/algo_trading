from sqlalchemy.dialects.sqlite import (
    insert,
)

from app.options.models import (
    OptionChainSnapshot,
)

from app.storage.database import (
    AsyncSessionLocal,
)

from app.storage.models import (
    OptionChainSnapshotEntity,
)


class OptionChainRepository:

    async def bulk_save(
        self,
        snapshots: list[
            OptionChainSnapshot
        ],
    ) -> int:

        if not snapshots:
            return 0

        async with (
            AsyncSessionLocal()
            as session
        ):

            values = []

            for snapshot in snapshots:

                values.append(
                    {

                        # ======================
                        # Core Context
                        # ======================

                        "instrument_key":
                        snapshot.instrument_key,

                        "expiry":
                        snapshot.expiry,

                        "strike_price":
                        snapshot.strike_price,

                        "snapshot_time":
                        snapshot.snapshot_time,

                        "underlying_spot_price":
                        snapshot.underlying_spot_price,

                        # ======================
                        # Call Side
                        # ======================

                        "call_ltp":
                        snapshot.call_ltp,

                        "call_volume":
                        snapshot.call_volume,

                        "call_oi":
                        snapshot.call_oi,

                        "call_prev_oi":
                        snapshot.call_prev_oi,

                        "call_iv":
                        snapshot.call_iv,

                        "call_theta":
                        snapshot.call_theta,

                        "call_delta":
                        snapshot.call_delta,

                        # ======================
                        # Put Side
                        # ======================

                        "put_ltp":
                        snapshot.put_ltp,

                        "put_volume":
                        snapshot.put_volume,

                        "put_oi":
                        snapshot.put_oi,

                        "put_prev_oi":
                        snapshot.put_prev_oi,

                        "put_iv":
                        snapshot.put_iv,

                        "put_theta":
                        snapshot.put_theta,

                        "put_delta":
                        snapshot.put_delta,
                    }
                )

            statement = (
                insert(
                    OptionChainSnapshotEntity
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