import pandas as pd

from app.market.models import (
    Candle,
)


class ADXCalculator:

    @staticmethod
    def calculate(
        candles: list[Candle],
        period: int = 14,
    ) -> float | None:

        if len(candles) < (
            period + 1
        ):
            return None

        dataframe = pd.DataFrame(
            {
                "high": [
                    c.high
                    for c in candles
                ],

                "low": [
                    c.low
                    for c in candles
                ],

                "close": [
                    c.close
                    for c in candles
                ],
            }
        )

        dataframe["previous_close"] = (
            dataframe["close"]
            .shift(1)
        )

        dataframe["+dm"] = (
            dataframe["high"]
            .diff()
        )

        dataframe["-dm"] = (
            dataframe["low"]
            .diff()
            .abs()
        )

        dataframe["+dm"] = dataframe[
            "+dm"
        ].where(
            (
                dataframe["+dm"]
                >
                dataframe["-dm"]
            )
            &
            (
                dataframe["+dm"]
                > 0
            ),
            0,
        )

        dataframe["-dm"] = dataframe[
            "-dm"
        ].where(
            (
                dataframe["-dm"]
                >
                dataframe["+dm"]
            )
            &
            (
                dataframe["-dm"]
                > 0
            ),
            0,
        )

        tr_components = pd.concat(
            [
                (
                    dataframe["high"]
                    -
                    dataframe["low"]
                ),

                (
                    dataframe["high"]
                    -
                    dataframe[
                        "previous_close"
                    ]
                ).abs(),

                (
                    dataframe["low"]
                    -
                    dataframe[
                        "previous_close"
                    ]
                ).abs(),
            ],
            axis=1,
        )

        dataframe["tr"] = (
            tr_components.max(
                axis=1
            )
        )

        atr = (
            dataframe["tr"]
            .rolling(period)
            .mean()
        )

        plus_di = (
            100
            *
            (
                dataframe["+dm"]
                .rolling(period)
                .mean()
                /
                atr
            )
        )

        minus_di = (
            100
            *
            (
                dataframe["-dm"]
                .rolling(period)
                .mean()
                /
                atr
            )
        )

        dx = (
            (
                (
                    plus_di
                    -
                    minus_di
                ).abs()
            )
            /
            (
                plus_di
                +
                minus_di
            )
        ) * 100

        adx = (
            dx.rolling(period)
            .mean()
        )

        latest_adx = (
            adx.iloc[-1]
        )

        if pd.isna(
            latest_adx
        ):
            return None

        return float(
            latest_adx
        )