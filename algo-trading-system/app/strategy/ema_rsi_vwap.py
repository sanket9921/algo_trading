from app.indicators.models import (
    IndicatorSnapshot,
)

from app.market.models import (
    Candle,
)

from app.options.analytics.models import (
    OIChangeAnalysis,
)

from app.strategy.base_strategy import (
    BaseStrategy,
)

from app.strategy.context.models import (
    TimeframeContext,
)

from app.strategy.models import (
    SignalType,
    TradingSignal,
)


class EmaRsiVwapStrategy(
    BaseStrategy
):

    def __init__(
        self,
    ) -> None:

        self.active_position: (
            SignalType | None
        ) = None

    def generate_signal(
        self,
        candle: Candle,
        indicators: IndicatorSnapshot,

        contexts: dict[
            str,
            TimeframeContext,
        ],

        option_analysis:
        OIChangeAnalysis | None,
    ) -> TradingSignal | None:

        # ==========================================
        # Execute ONLY On 1m Candle
        # ==========================================

        if candle.timeframe != "1m":

            return None

        # ==========================================
        # Indicator Validation
        # ==========================================

        if (
            indicators.ema_9 is None
            or indicators.ema_21 is None
            or indicators.rsi_14 is None
            or indicators.adx_14 is None
        ):

            return None

        # ==========================================
        # Strong Trend Required
        # ==========================================

        if indicators.adx_14 < 25:

            return None

        # ==========================================
        # Trend Direction
        # ==========================================

        bullish_trend = (
            indicators.ema_9
            >
            indicators.ema_21
        )

        bearish_trend = (
            indicators.ema_9
            <
            indicators.ema_21
        )

        # ==========================================
        # Pullback Zones
        # ==========================================

        bullish_pullback = (

            indicators.rsi_14 >= 45

            and

            indicators.rsi_14 <= 60
        )

        bearish_pullback = (

            indicators.rsi_14 <= 55

            and

            indicators.rsi_14 >= 40
        )

        # ==========================================
        # Candle Confirmation
        # ==========================================

        bullish_candle = (
            candle.close >
            candle.open
        )

        bearish_candle = (
            candle.close <
            candle.open
        )

        # ==========================================
        # Candle Strength
        # ==========================================

        candle_body = abs(
            candle.close
            -
            candle.open
        )

        minimum_body = (
            candle.close * 0.00012
        )

        if candle_body < minimum_body:

            return None

        # ==========================================
        # BUY SIGNAL
        # ==========================================

        if (

            bullish_trend

            and

            bullish_pullback

            and

            bullish_candle
        ):

            # ======================================
            # Prevent Signal Spam
            # ======================================

            if (
                self.active_position
                ==
                SignalType.BUY
            ):

                return None

            self.active_position = (
                SignalType.BUY
            )

            return TradingSignal(

                instrument_key=
                candle.instrument_key,

                signal_type=
                SignalType.BUY,

                price=
                candle.close,

                timestamp=
                candle.end_time,

                strategy_name=
                "PULLBACK_CONTINUATION_V2",

                is_replay=
                False,
            )

        # ==========================================
        # SELL SIGNAL
        # ==========================================

        if (

            bearish_trend

            and

            bearish_pullback

            and

            bearish_candle
        ):

            # ======================================
            # Prevent Signal Spam
            # ======================================

            if (
                self.active_position
                ==
                SignalType.SELL
            ):

                return None

            self.active_position = (
                SignalType.SELL
            )

            return TradingSignal(

                instrument_key=
                candle.instrument_key,

                signal_type=
                SignalType.SELL,

                price=
                candle.close,

                timestamp=
                candle.end_time,

                strategy_name=
                "PULLBACK_CONTINUATION_V2",

                is_replay=
                False,
            )

        return None

    def reset_position_state(
        self,
    ) -> None:

        self.active_position = None