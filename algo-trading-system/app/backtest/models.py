from dataclasses import dataclass


@dataclass(slots=True)
class BacktestResult:
    total_trades: int

    winning_trades: int

    losing_trades: int

    total_pnl: float

    win_rate: float

    average_pnl: float
    
    average_win: float

    average_loss: float

    expectancy: float
    
    max_drawdown: float

    equity_curve: list[float]