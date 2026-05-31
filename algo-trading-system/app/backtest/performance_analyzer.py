from app.backtest.models import (
    BacktestResult,
)


class PerformanceAnalyzer:

    def analyze(
        self,
        realized_pnls: list[float],
    ) -> BacktestResult:

        if not realized_pnls:

            return BacktestResult(
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                total_pnl=0.0,
                win_rate=0.0,
                average_pnl=0.0,
                average_win=0.0,
                average_loss=0.0,
                expectancy=0.0,
                max_drawdown=0.0,
                equity_curve=[],
            )

        winning_trade_pnls = []

        losing_trade_pnls = []

        equity_curve = []

        running_equity = 0.0

        peak_equity = 0.0

        max_drawdown = 0.0

        # ======================================
        # Process Real PnLs
        # ======================================

        for pnl in realized_pnls:

            # ======================================
            # Equity Curve
            # ======================================

            running_equity += pnl

            equity_curve.append(
                running_equity
            )

            peak_equity = max(
                peak_equity,
                running_equity,
            )

            current_drawdown = (
                peak_equity
                -
                running_equity
            )

            max_drawdown = max(
                max_drawdown,
                current_drawdown,
            )

            # ======================================
            # Winner / Loser Split
            # ======================================

            if pnl > 0:

                winning_trade_pnls.append(
                    pnl
                )

            elif pnl < 0:

                losing_trade_pnls.append(
                    abs(pnl)
                )

        total_trades = len(
            realized_pnls
        )

        winning_trades = len(
            winning_trade_pnls
        )

        losing_trades = len(
            losing_trade_pnls
        )

        total_pnl = sum(
            realized_pnls
        )

        average_pnl = (
            total_pnl
            /
            total_trades
        )

        average_win = (
            sum(
                winning_trade_pnls
            )
            /
            len(
                winning_trade_pnls
            )
            if winning_trade_pnls
            else 0.0
        )

        average_loss = (
            sum(
                losing_trade_pnls
            )
            /
            len(
                losing_trade_pnls
            )
            if losing_trade_pnls
            else 0.0
        )

        win_rate = (
            (
                winning_trades
                /
                total_trades
            )
            * 100
        )

        # ======================================
        # Expectancy
        # ======================================

        win_rate_decimal = (
            winning_trades
            /
            total_trades
        )

        loss_rate_decimal = (
            1 -
            win_rate_decimal
        )

        expectancy = (
            (
                win_rate_decimal
                * average_win
            )
            -
            (
                loss_rate_decimal
                * average_loss
            )
        )

        return BacktestResult(
            total_trades=
            total_trades,

            winning_trades=
            winning_trades,

            losing_trades=
            losing_trades,

            total_pnl=
            total_pnl,

            win_rate=
            win_rate,

            average_pnl=
            average_pnl,

            average_win=
            average_win,

            average_loss=
            average_loss,

            expectancy=
            expectancy,

            max_drawdown=
            max_drawdown,

            equity_curve=
            equity_curve,
        )