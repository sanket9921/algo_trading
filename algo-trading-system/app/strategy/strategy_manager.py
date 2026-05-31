from app.core.logger import (
    get_logger,
)

from app.indicators.models import (
    IndicatorSnapshot,
)

from app.market.models import (
    Candle,
)

from app.options.analytics.models import (
    OIChangeAnalysis,
)

from app.strategy.context.models import (
    TimeframeContext,
)

from app.strategy.ema_rsi_vwap import (
    EmaRsiVwapStrategy,
)

from app.strategy.models import (
    TradingSignal,
)

logger = get_logger(__name__)


class StrategyManager:

    def __init__(
        self,
    ) -> None:

        self.strategies = [

            EmaRsiVwapStrategy(),
        ]

    def generate_signals(
        self,
        candle: Candle,

        indicators: IndicatorSnapshot,

        contexts: dict[
            str,
            TimeframeContext,
        ],

        option_analysis:
        OIChangeAnalysis | None,
    ) -> list[
        TradingSignal
    ]:

        signals: list[
            TradingSignal
        ] = []

        for strategy in (
            self.strategies
        ):

            signal = (
                strategy
                .generate_signal(

                    candle=
                    candle,

                    indicators=
                    indicators,

                    contexts=
                    contexts,

                    option_analysis=
                    option_analysis,
                )
            )

            if signal:

                logger.info(
                    "trading_signal_generated",

                    instrument_key=
                    signal.instrument_key,

                    signal_type=
                    signal.signal_type,

                    strategy=
                    signal.strategy_name,

                    price=
                    signal.price,
                )

                signals.append(
                    signal
                )

        return signals

    def reset_positions(
        self,
    ) -> None:

        for strategy in (
            self.strategies
        ):

            strategy.reset_position_state()