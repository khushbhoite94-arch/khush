"""
AEGIS AI v2
Global Runtime State
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Any


@dataclass
class Position:

    symbol: str

    side: str

    quantity: float

    entry: float

    stop_loss: float

    take_profit: float

    open_time: datetime = field(default_factory=datetime.utcnow)

    close_time: datetime | None = None

    exit_price: float | None = None

    pnl: float = 0.0

    closed: bool = False


class RuntimeState:

    def __init__(self):

        self._lock = Lock()

        self.connected = False

        self.symbol = ""

        self.timeframe = ""

        self.current_price = 0.0

        self.bid = 0.0

        self.ask = 0.0

        self.spread = 0.0

        self.candles = []

        self.history_loaded = False

        self.last_candle = None

        self.position: Position | None = None

        self.balance = 100000.0

        self.equity = 100000.0

        self.realized_pnl = 0.0

        self.unrealized_pnl = 0.0

        self.total_trades = 0

        self.wins = 0

        self.losses = 0

        self.last_signal = "WAIT"

        self.last_ai = {}

        self.last_update = datetime.utcnow()

    # --------------------------------------------------------

    @property
    def winrate(self):

        total = self.wins + self.losses

        if total == 0:

            return 0.0

        return round((self.wins / total) * 100, 2)

    # --------------------------------------------------------

    def update_price(

        self,

        bid,

        ask,

    ):

        with self._lock:

            self.bid = bid

            self.ask = ask

            self.current_price = (bid + ask) / 2

            self.spread = ask - bid

            self.last_update = datetime.utcnow()

    # --------------------------------------------------------

    def set_history(

        self,

        candles,

    ):

        with self._lock:

            self.candles = candles

            self.history_loaded = True

    # --------------------------------------------------------

    def append_candle(

        self,

        candle,

    ):

        with self._lock:

            self.candles.append(candle)

            self.last_candle = candle

    # --------------------------------------------------------

    def open_position(

        self,

        position: Position,

    ):

        with self._lock:

            self.position = position

            self.total_trades += 1

    # --------------------------------------------------------

    def close_position(

        self,

        price,

    ):

        if self.position is None:

            return

        p = self.position

        p.closed = True

        p.exit_price = price

        p.close_time = datetime.utcnow()

        if p.side == "BUY":

            pnl = (price - p.entry) * p.quantity

        else:

            pnl = (p.entry - price) * p.quantity

        p.pnl = pnl

        self.realized_pnl += pnl

        self.balance += pnl

        self.equity = self.balance

        if pnl >= 0:

            self.wins += 1

        else:

            self.losses += 1

        self.position = None

    # --------------------------------------------------------

    def snapshot(self) -> dict[str, Any]:

        return {

            "connected": self.connected,

            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "price": self.current_price,

            "bid": self.bid,

            "ask": self.ask,

            "spread": self.spread,

            "balance": self.balance,

            "equity": self.equity,

            "wins": self.wins,

            "losses": self.losses,

            "winrate": self.winrate,

            "trades": self.total_trades,

            "position": self.position,

            "signal": self.last_signal,

            "updated": self.last_update,

        }


state = RuntimeState()