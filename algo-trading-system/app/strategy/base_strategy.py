from abc import ABC
from abc import abstractmethod

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

from app.strategy.models import (
    TradingSignal,
)


class BaseStrategy(ABC):

    @abstractmethod
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

        raise NotImplementedError

    def reset_position_state(
        self,
    ) -> None:

        return