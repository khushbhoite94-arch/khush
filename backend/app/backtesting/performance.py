"""
AEGIS AI v2
Performance Analyzer
"""

from __future__ import annotations

import math


class Performance:

    def __init__(self):

        self.trades = []

    # -------------------------------------------------

    def add_trade(self, trade):

        self.trades.append(trade)

    # -------------------------------------------------

    @property
    def total(self):

        return len(self.trades)

    # -------------------------------------------------

    @property
    def wins(self):

        return len(

            [

                t

                for t in self.trades

                if t["pnl"] > 0

            ]

        )

    # -------------------------------------------------

    @property
    def losses(self):

        return len(

            [

                t

                for t in self.trades

                if t["pnl"] <= 0

            ]

        )

    # -------------------------------------------------

    @property
    def winrate(self):

        if self.total == 0:

            return 0

        return round(

            self.wins / self.total * 100,

            2,

        )

    # -------------------------------------------------

    @property
    def profit(self):

        return round(

            sum(

                t["pnl"]

                for t in self.trades

            ),

            2,

        )

    # -------------------------------------------------

    @property
    def average(self):

        if self.total == 0:

            return 0

        return round(

            self.profit / self.total,

            2,

        )

    # -------------------------------------------------

    @property
    def max_win(self):

        if self.total == 0:

            return 0

        return max(

            t["pnl"]

            for t in self.trades

        )

    # -------------------------------------------------

    @property
    def max_loss(self):

        if self.total == 0:

            return 0

        return min(

            t["pnl"]

            for t in self.trades

        )

    # -------------------------------------------------

    @property
    def sharpe(self):

        if self.total < 2:

            return 0

        returns = [

            t["pnl"]

            for t in self.trades

        ]

        avg = sum(returns) / len(returns)

        variance = sum(

            (x - avg) ** 2

            for x in returns

        ) / len(returns)

        std = math.sqrt(variance)

        if std == 0:

            return 0

        return round(

            avg / std,

            3,

        )

    # -------------------------------------------------

    def report(self):

        return {

            "Trades": self.total,

            "Wins": self.wins,

            "Losses": self.losses,

            "WinRate": self.winrate,

            "NetProfit": self.profit,

            "AverageTrade": self.average,

            "MaxWin": self.max_win,

            "MaxLoss": self.max_loss,

            "Sharpe": self.sharpe,

        }