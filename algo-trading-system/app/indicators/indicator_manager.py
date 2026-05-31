from collections import defaultdict

from app.core.logger import get_logger

from app.indicators.adx import (
    ADXCalculator,
)

from app.indicators.ema import (
    EMACalculator,
)

from app.indicators.models import (
    IndicatorSnapshot,
)

from app.indicators.rsi import (
    RSICalculator,
)

from app.indicators.vwap import (
    VWAPCalculator,
)

from app.market.models import (
    Candle,
)

logger = get_logger(__name__)


class IndicatorManager:

    def __init__(
        self,
    ) -> None:

        self.candle_history: dict[
            tuple[str, str],
            list[Candle],
        ] = defaultdict(list)

    def process_candle(
        self,
        candle: Candle,
    ) -> IndicatorSnapshot:

        key = (
            candle.instrument_key,
            candle.timeframe,
        )

        history = (
            self.candle_history[key]
        )

        history.append(candle)

        # ==========================================
        # Rolling Window
        # ==========================================

        if len(history) > 500:

            history.pop(0)

        # ==========================================
        # Indicator Calculations
        # ==========================================

        ema_9 = (
            EMACalculator.calculate(
                history,
                9,
            )
        )

        ema_21 = (
            EMACalculator.calculate(
                history,
                21,
            )
        )

        rsi_14 = (
            RSICalculator.calculate(
                history,
            )
        )

        vwap = (
            VWAPCalculator.calculate(
                history,
            )
        )

        adx_14 = (
            ADXCalculator.calculate(
                history,
            )
        )

        snapshot = IndicatorSnapshot(

            instrument_key=
            candle.instrument_key,

            ema_9=
            ema_9,

            ema_21=
            ema_21,

            rsi_14=
            rsi_14,

            vwap=
            vwap,

            adx_14=
            adx_14,

            timestamp=
            candle.end_time,
        )

        logger.info(
            "indicator_snapshot_generated",

            instrument_key=
            snapshot.instrument_key,

            ema_9=
            snapshot.ema_9,

            ema_21=
            snapshot.ema_21,

            rsi_14=
            snapshot.rsi_14,

            vwap=
            snapshot.vwap,

            adx_14=
            snapshot.adx_14,
        )

        return snapshot