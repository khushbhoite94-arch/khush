"""
AEGIS AI v3
Trade Journal
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime


class Journal:

    def __init__(self):

        self.trades = []

    # =====================================================
    # ADD TRADE
    # =====================================================

    def add_trade(self, trade):

        if trade is None:
            return

        record = deepcopy(trade)

        record.setdefault(
            "recorded_at",
            datetime.utcnow(),
        )

        self.trades.append(record)

    # =====================================================
    # LATEST
    # =====================================================

    def latest_trade(self):

        if not self.trades:
            return None

        return self.trades[-1]

    # =====================================================
    # TOTAL
    # =====================================================

    def total_trades(self):

        return len(self.trades)

    # =====================================================
    # WINNERS
    # =====================================================

    def winning_trades(self):

        return [

            trade

            for trade in self.trades

            if trade.get("profit", 0) > 0

        ]

    # =====================================================
    # LOSERS
    # =====================================================

    def losing_trades(self):

        return [

            trade

            for trade in self.trades

            if trade.get("profit", 0) < 0

        ]

    # =====================================================
    # BREAKEVEN
    # =====================================================

    def breakeven_trades(self):

        return [

            trade

            for trade in self.trades

            if trade.get("profit", 0) == 0

        ]

    # =====================================================
    # WIN RATE
    # =====================================================

    def win_rate(self):

        total = self.total_trades()

        if total == 0:
            return 0

        wins = len(

            self.winning_trades()

        )

        return round(

            (wins / total) * 100,

            2,

        )

    # =====================================================
    # TOTAL PROFIT
    # =====================================================

    def total_profit(self):

        return round(

            sum(

                trade.get("profit", 0)

                for trade in self.trades

            ),

            2,

        )

    # =====================================================
    # AVERAGE PROFIT
    # =====================================================

    def average_profit(self):

        total = self.total_trades()

        if total == 0:
            return 0

        return round(

            self.total_profit() / total,

            2,

        )

    # =====================================================
    # FILTER
    # =====================================================

    def by_symbol(self, symbol):

        return [

            trade

            for trade in self.trades

            if trade.get("symbol") == symbol

        ]

    # =====================================================
    # FILTER STRATEGY
    # =====================================================

    def by_strategy(self, strategy):

        return [

            trade

            for trade in self.trades

            if trade.get("strategy") == strategy

        ]

    # =====================================================
    # EXPORT
    # =====================================================

    def export(self):

        return deepcopy(

            self.trades

        )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.trades.clear()

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "total_trades": self.total_trades(),

            "wins": len(

                self.winning_trades()

            ),

            "losses": len(

                self.losing_trades()

            ),

            "breakeven": len(

                self.breakeven_trades()

            ),

            "win_rate": self.win_rate(),

            "total_profit": self.total_profit(),

            "average_profit": self.average_profit(),

        }