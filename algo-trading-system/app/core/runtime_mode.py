from enum import Enum


class RuntimeMode(str, Enum):
    DEVELOPMENT = "development"

    PAPER = "paper"

    BACKTEST = "backtest"

    LIVE = "live"