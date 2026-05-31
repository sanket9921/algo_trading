class AppError(Exception):
    """Base application exception."""


class BrokerError(AppError):
    """Broker-related exception."""


class MarketDataError(AppError):
    """Market data processing exception."""


class StrategyError(AppError):
    """Strategy processing exception."""


class RiskError(AppError):
    """Risk validation exception."""


class ExecutionError(AppError):
    """Execution-related exception."""