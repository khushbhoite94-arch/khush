"""
AEGIS AI v3
Trade Lifecycle Manager
"""

from __future__ import annotations

from datetime import datetime


class TradeManager:

    def __init__(self):

        self.open_trades = []

        self.closed_trades = []

    # =====================================================
    # OPEN TRADE
    # =====================================================

    def open_trade(

        self,

        trade,

    ):

        trade = trade.copy()

        trade.setdefault("lot_size", 1.0)

        trade["status"] = "OPEN"

        trade["opened_at"] = datetime.utcnow()

        trade["closed_at"] = None

        trade["exit_price"] = None

        trade["profit"] = 0.0

        trade["breakeven"] = False

        trade["partial_closed"] = False

        trade["remaining_size"] = 1.0

        self.open_trades.append(

            trade,

        )

        return trade

    # =====================================================
    # CLOSE TRADE
    # =====================================================

    def close_trade(

        self,

        trade,

        price,

    ):

        if trade not in self.open_trades:

            return None

        trade["status"] = "CLOSED"

        trade["closed_at"] = datetime.utcnow()

        trade["exit_price"] = price

        if trade["direction"] == "BUY":

            pnl = price - trade["entry"]

        else:

            pnl = trade["entry"] - price

        trade["profit"] = round(

            pnl,

            5,

        )

        self.open_trades.remove(

            trade,

        )

        self.closed_trades.append(

            trade,

        )

        return trade

    # =====================================================
    # MOVE TO BREAKEVEN
    # =====================================================

    def move_to_breakeven(

        self,

        trade,

    ):

        if trade["breakeven"]:

            return trade

        trade["stop_loss"] = trade["entry"]

        trade["breakeven"] = True

        return trade

    # =====================================================
    # TRAILING STOP
    # =====================================================

    def trail(

        self,

        trade,

        current_price,

        distance,

    ):

        if trade["direction"] == "BUY":

            stop = current_price - distance

            if stop > trade["stop_loss"]:

                trade["stop_loss"] = stop

        else:

            stop = current_price + distance

            if stop < trade["stop_loss"]:

                trade["stop_loss"] = stop

        return trade

    # =====================================================
    # PARTIAL CLOSE
    # =====================================================

    def partial_close(

        self,

        trade,

        percentage=0.50,

    ):

        if trade["partial_closed"]:

            return trade

        trade["remaining_size"] *= (

            1 - percentage

        )

        trade["partial_closed"] = True

        return trade

    # =====================================================
    # SCALE IN
    # =====================================================

    def scale_in(

        self,

        trade,

        lots,

    ):

        trade["lot_size"] += lots

        return trade

    # =====================================================
    # SCALE OUT
    # =====================================================

    def scale_out(

        self,

        trade,

        lots,

    ):

        trade["lot_size"] = max(

            trade["lot_size"] - lots,

            0,

        )

        return trade

    # =====================================================
    # STOP HIT
    # =====================================================

    def hit_stop(

        self,

        trade,

        price,

    ):

        if trade["direction"] == "BUY":

            return price <= trade["stop_loss"]

        return price >= trade["stop_loss"]

    # =====================================================
    # TARGET HIT
    # =====================================================

    def hit_target(

        self,

        trade,

        price,

    ):

        if trade["direction"] == "BUY":

            return price >= trade["take_profit"]

        return price <= trade["take_profit"]

    # =====================================================
    # UPDATE
    # =====================================================

    def update(

        self,

        price,

    ):

        closed = []

        for trade in list(

            self.open_trades,

        ):

            if self.hit_stop(

                trade,

                price,

            ):

                closed.append(

                    self.close_trade(

                        trade,

                        trade["stop_loss"],

                    )

                )

                continue

            if self.hit_target(

                trade,

                price,

            ):

                closed.append(

                    self.close_trade(

                        trade,

                        trade["take_profit"],

                    )

                )

        return closed

    # =====================================================
    # TOTAL PROFIT
    # =====================================================

    def total_profit(

        self,

    ):

        return round(

            sum(

                t["profit"]

                for t in self.closed_trades

            ),

            5,

        )

    # =====================================================
    # WIN RATE
    # =====================================================

    def win_rate(

        self,

    ):

        if not self.closed_trades:

            return 0

        wins = sum(

            1

            for trade in self.closed_trades

            if trade["profit"] > 0

        )

        return round(

            wins

            / len(

                self.closed_trades,

            )

            * 100,

            2,

        )

    # =====================================================
    # LOSSES
    # =====================================================

    def losses(

        self,

    ):

        return len(

            [

                t

                for t in self.closed_trades

                if t["profit"] <= 0

            ]

        )

    # =====================================================
    # WINS
    # =====================================================

    def wins(

        self,

    ):

        return len(

            [

                t

                for t in self.closed_trades

                if t["profit"] > 0

            ]

        )

    # =====================================================
    # RESET
    # =====================================================

    def reset(

        self,

    ):

        self.open_trades.clear()

        self.closed_trades.clear()

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(

        self,

    ):

        return {

            "open": len(

                self.open_trades,

            ),

            "closed": len(

                self.closed_trades,

            ),

            "wins": self.wins(),

            "losses": self.losses(),

            "profit": self.total_profit(),

            "win_rate": self.win_rate(),

        }

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(

        self,

    ):

        return self.statistics()