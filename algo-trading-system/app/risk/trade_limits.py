from datetime import date

from app.core.config import get_settings


class TradeLimitManager:
    def __init__(self) -> None:
        self.settings = get_settings()

        self.current_day = date.today()

        self.daily_trade_count = 0

    def can_trade(self) -> bool:
        self._reset_if_new_day()

        return (
            self.daily_trade_count <
            self.settings.max_trades_per_day
        )

    def register_trade(self) -> None:
        self._reset_if_new_day()

        self.daily_trade_count += 1

    def _reset_if_new_day(self) -> None:
        today = date.today()

        if today != self.current_day:
            self.current_day = today
            self.daily_trade_count = 0