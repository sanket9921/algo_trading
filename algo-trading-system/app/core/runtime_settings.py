from dataclasses import dataclass

from app.core.runtime_mode import (
    RuntimeMode,
)


@dataclass(slots=True)
class RuntimeSettings:
    candle_duration_minutes: int

    stop_loss_pct: float

    take_profit_pct: float

    replay_speed: float

    telegram_alerts_enabled: bool

    verbose_logging: bool


def get_runtime_settings(
    mode: RuntimeMode,
) -> RuntimeSettings:

    if mode == RuntimeMode.DEVELOPMENT:
        return RuntimeSettings(
            candle_duration_minutes=1,
            stop_loss_pct=0.001,
            take_profit_pct=0.001,
            replay_speed=0.0,
            telegram_alerts_enabled=True,
            verbose_logging=True,
        )

    if mode == RuntimeMode.PAPER:
        return RuntimeSettings(
            candle_duration_minutes=5,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            replay_speed=0.0,
            telegram_alerts_enabled=True,
            verbose_logging=True,
        )

    if mode == RuntimeMode.BACKTEST:
        return RuntimeSettings(
            candle_duration_minutes=1,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            replay_speed=0.01,
            telegram_alerts_enabled=False,
            verbose_logging=False,
        )

    return RuntimeSettings(
        candle_duration_minutes=1,
        stop_loss_pct=0.01,
        take_profit_pct=0.02,
        replay_speed=0.0,
        telegram_alerts_enabled=True,
        verbose_logging=False,
    )