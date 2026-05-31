from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
    Index, 
)
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.base import Base


# =========================================================
# Candle Storage
# =========================================================

class CandleEntity(Base):
    __tablename__ = "candles"

    __table_args__ = (

        UniqueConstraint(
            "instrument_key",
            "timeframe",
            "start_time",
            name="uq_candle_identity",
        ),

        Index(
            "idx_candle_lookup",
            "instrument_key",
            "timeframe",
            "start_time",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    instrument_key: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    timeframe: Mapped[str] = mapped_column(
        String(20),
        index=True,
    )

    open: Mapped[float] = mapped_column(
        Float,
    )

    high: Mapped[float] = mapped_column(
        Float,
    )

    low: Mapped[float] = mapped_column(
        Float,
    )

    close: Mapped[float] = mapped_column(
        Float,
    )

    volume: Mapped[int] = mapped_column(
        Integer,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    is_closed: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )


# =========================================================
# Historical Sync State
# =========================================================

class SyncStateEntity(Base):
    __tablename__ = "sync_state"

    instrument_key: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    timeframe: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    last_candle_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# =========================================================
# Signals
# =========================================================

class SignalEntity(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    instrument_key: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    signal_type: Mapped[str] = mapped_column(
        String(20),
    )

    strategy_name: Mapped[str] = mapped_column(
        String(100),
    )

    price: Mapped[float] = mapped_column(
        Float,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )


# =========================================================
# Risk Decisions
# =========================================================

class RiskDecisionEntity(Base):
    __tablename__ = "risk_decisions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    instrument_key: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    approved: Mapped[bool] = mapped_column(
        Boolean,
    )

    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    suggested_quantity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )


# =========================================================
# Live Trades
# =========================================================

class TradeEntity(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    instrument_key: Mapped[str] = mapped_column(
        String(100),
    )

    side: Mapped[str] = mapped_column(
        String(20),
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
    )

    execution_price: Mapped[float] = mapped_column(
        Float,
    )

    strategy_name: Mapped[str] = mapped_column(
        String(100),
    )

    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )


# =========================================================
# Closed Positions
# =========================================================

class ClosedPositionEntity(Base):
    __tablename__ = "closed_positions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    instrument_key: Mapped[str] = mapped_column(
        String(100),
    )

    side: Mapped[str] = mapped_column(
        String(20),
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
    )

    average_price: Mapped[float] = mapped_column(
        Float,
    )

    realized_pnl: Mapped[float] = mapped_column(
        Float,
    )

    closed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )


# =========================================================
# Backtest Trades
# =========================================================

class BacktestTradeEntity(Base):
    __tablename__ = "backtest_trades"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    instrument_key: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    strategy_name: Mapped[str] = mapped_column(
        String(100),
    )

    side: Mapped[str] = mapped_column(
        String(20),
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
    )

    entry_price: Mapped[float] = mapped_column(
        Float,
    )

    exit_price: Mapped[float] = mapped_column(
        Float,
    )

    realized_pnl: Mapped[float] = mapped_column(
        Float,
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    closed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    is_replay: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
 

class OptionChainSnapshotEntity(Base):

    __tablename__ = (
        "option_chain_snapshots"
    )

    __table_args__ = (

        UniqueConstraint(

            "instrument_key",

            "expiry",

            "strike_price",

            "snapshot_time",

            name=
            "uq_option_chain_snapshot",
        ),

        Index(
            "idx_option_chain_lookup",

            "instrument_key",

            "expiry",

            "strike_price",

            "snapshot_time",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ==========================================
    # Core Context
    # ==========================================

    instrument_key: Mapped[str] = (
        mapped_column(
            String(100),
            index=True,
        )
    )

    expiry: Mapped[str] = (
        mapped_column(
            String(30),
        )
    )

    strike_price: Mapped[float] = (
        mapped_column(
            Float,
        )
    )

    snapshot_time: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            index=True,
        )
    )

    underlying_spot_price: Mapped[float] = (
        mapped_column(
            Float,
        )
    )

    # ==========================================
    # Call Side
    # ==========================================

    call_ltp: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    call_volume: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    call_oi: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    call_prev_oi: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    call_iv: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    call_theta: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    call_delta: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    # ==========================================
    # Put Side
    # ==========================================

    put_ltp: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    put_volume: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    put_oi: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    put_prev_oi: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    put_iv: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    put_theta: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    put_delta: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )
    
class OptionAnalyticsSnapshotEntity(
    Base
):

    __tablename__ = (
        "option_analytics_snapshots"
    )

    __table_args__ = (

        UniqueConstraint(

            "instrument_key",

            "expiry",

            "strike_price",

            "snapshot_time",

            name=
            "uq_option_analytics_snapshot",
        ),

        Index(
            "idx_option_analytics_lookup",

            "instrument_key",

            "expiry",

            "strike_price",

            "snapshot_time",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ==========================================
    # Core Context
    # ==========================================

    instrument_key: Mapped[str] = (
        mapped_column(
            String(100),
            index=True,
        )
    )

    expiry: Mapped[str] = (
        mapped_column(
            String(30),
        )
    )

    strike_price: Mapped[float] = (
        mapped_column(
            Float,
        )
    )

    snapshot_time: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            index=True,
        )
    )

    # ==========================================
    # OI Intelligence
    # ==========================================

    call_oi_change: Mapped[int] = (
        mapped_column(
            Integer,
        )
    )

    put_oi_change: Mapped[int] = (
        mapped_column(
            Integer,
        )
    )

    # ==========================================
    # Behavioral Classification
    # ==========================================

    call_buildup: Mapped[str] = (
        mapped_column(
            String(50),
        )
    )

    put_buildup: Mapped[str] = (
        mapped_column(
            String(50),
        )
    )