"""
AEGIS AI v3
Paper Trading Engine
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.execution.position_manager import PositionManager
from app.execution.break_even import BreakEven
from app.execution.trailing_stop import TrailingStop
from app.execution.partial_close import PartialClose


class PaperExecutor:

    def __init__(

        self,

        starting_balance: float = 10000.0,

    ):

        self.balance = starting_balance

        self.equity = starting_balance

        self.positions = PositionManager()

        self.break_even = BreakEven()

        self.trailing = TrailingStop(

            distance=0.0010,

        )

        self.partial = PartialClose()

    # =====================================================
    # CREATE TRADE
    # =====================================================

    def _create_trade(

        self,

        direction,

        symbol,

        lot,

        entry,

        sl,

        tp,

    ):

        return {

            "id": str(uuid4()),

            "direction": direction,

            "symbol": symbol,

            "entry": entry,

            "stop_loss": sl,

            "take_profit": tp,

            "lot_size": lot,

            "opened_at": datetime.utcnow(),

            "status": "OPEN",

            "profit": 0.0,

            "breakeven": False,

            "partial_closed": False,

        }

    # =====================================================
    # BUY
    # =====================================================

    def buy(

        self,

        symbol,

        lot,

        entry,

        sl,

        tp,

    ):

        trade = self._create_trade(

            "BUY",

            symbol,

            lot,

            entry,

            sl,

            tp,

        )

        return self.positions.open(trade)

    # =====================================================
    # SELL
    # =====================================================

    def sell(

        self,

        symbol,

        lot,

        entry,

        sl,

        tp,

    ):

        trade = self._create_trade(

            "SELL",

            symbol,

            lot,

            entry,

            sl,

            tp,

        )

        return self.positions.open(trade)

    # =====================================================
    # UPDATE MARKET PRICE
    # =====================================================

    def update(

        self,

        current_price,

    ):

        finished = []

        for trade in list(self.positions.open_positions):

            self.break_even.apply(

                trade,

                current_price,

            )

            self.trailing.apply(

                trade,

                current_price,

            )

            if trade["direction"] == "BUY":

                if current_price <= trade["stop_loss"]:

                    closed = self.positions.close(

                        trade["id"],

                        trade["stop_loss"],

                    )

                elif current_price >= trade["take_profit"]:

                    closed = self.positions.close(

                        trade["id"],

                        trade["take_profit"],

                    )

                else:

                    continue

            else:

                if current_price >= trade["stop_loss"]:

                    closed = self.positions.close(

                        trade["id"],

                        trade["stop_loss"],

                    )

                elif current_price <= trade["take_profit"]:

                    closed = self.positions.close(

                        trade["id"],

                        trade["take_profit"],

                    )

                else:

                    continue

            pnl = closed["profit"] * 100000

            self.balance += pnl

            self.equity = self.balance

            closed["profit"] = pnl

            finished.append(closed)

        return finished

    # =====================================================
    # PARTIAL CLOSE
    # =====================================================

    def partial_close(

        self,

        trade_id,

        percentage=0.5,

    ):

        trade = self.positions.get(trade_id)

        if trade is None:

            return None

        return self.partial.apply(

            trade,

            percentage,

        )

    # =====================================================
    # MANUAL CLOSE
    # =====================================================

    def close_trade(

        self,

        trade_id,

        price,

    ):

        trade = self.positions.close(

            trade_id,

            price,

        )

        if trade is None:

            return None

        pnl = trade["profit"] * 100000

        trade["profit"] = pnl

        self.balance += pnl

        self.equity = self.balance

        return trade

    # =====================================================
    # BALANCE
    # =====================================================

    def get_balance(self):

        return self.balance

    # =====================================================
    # EQUITY
    # =====================================================

    def get_equity(self):

        return self.equity

    # =====================================================
    # OPEN POSITIONS
    # =====================================================

    def get_open_positions(self):

        return self.positions.open_positions

    # =====================================================
    # CLOSED POSITIONS
    # =====================================================

    def get_closed_positions(self):

        return self.positions.closed_positions

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        stats = self.positions.statistics()

        stats["balance"] = self.balance

        stats["equity"] = self.equity

        return stats

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.positions.reset()

        self.balance = self.equity