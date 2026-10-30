"""
AEGIS AI v3
Performance Analytics
"""

from __future__ import annotations


class Performance:

    def __init__(self):

        self.trades = []

    # =====================================================
    # LOAD
    # =====================================================

    def load(self, trades):

        self.trades = list(trades)

    # =====================================================
    # TOTAL
    # =====================================================

    def total_trades(self):

        return len(self.trades)

    # =====================================================
    # WINS
    # =====================================================

    def wins(self):

        return len(

            [

                t

                for t in self.trades

                if t.get("profit", 0) > 0

            ]

        )

    # =====================================================
    # LOSSES
    # =====================================================

    def losses(self):

        return len(

            [

                t

                for t in self.trades

                if t.get("profit", 0) < 0

            ]

        )

    # =====================================================
    # WIN RATE
    # =====================================================

    def win_rate(self):

        total = self.total_trades()

        if total == 0:

            return 0

        return round(

            self.wins() / total * 100,

            2,

        )

    # =====================================================
    # GROSS PROFIT
    # =====================================================

    def gross_profit(self):

        return round(

            sum(

                t.get("profit", 0)

                for t in self.trades

                if t.get("profit", 0) > 0

            ),

            2,

        )

    # =====================================================
    # GROSS LOSS
    # =====================================================

    def gross_loss(self):

        return round(

            abs(

                sum(

                    t.get("profit", 0)

                    for t in self.trades

                    if t.get("profit", 0) < 0

                )

            ),

            2,

        )

    # =====================================================
    # NET PROFIT
    # =====================================================

    def net_profit(self):

        return round(

            sum(

                t.get("profit", 0)

                for t in self.trades

            ),

            2,

        )

    # =====================================================
    # AVERAGE WIN
    # =====================================================

    def average_win(self):

        wins = [

            t.get("profit", 0)

            for t in self.trades

            if t.get("profit", 0) > 0

        ]

        if not wins:

            return 0

        return round(

            sum(wins) / len(wins),

            2,

        )

    # =====================================================
    # AVERAGE LOSS
    # =====================================================

    def average_loss(self):

        losses = [

            abs(t.get("profit", 0))

            for t in self.trades

            if t.get("profit", 0) < 0

        ]

        if not losses:

            return 0

        return round(

            sum(losses) / len(losses),

            2,

        )

    # =====================================================
    # PROFIT FACTOR
    # =====================================================

    def profit_factor(self):

        loss = self.gross_loss()

        if loss == 0:

            return 0

        return round(

            self.gross_profit() / loss,

            2,

        )

    # =====================================================
    # EXPECTANCY
    # =====================================================

    def expectancy(self):

        total = self.total_trades()

        if total == 0:

            return 0

        return round(

            self.net_profit() / total,

            2,

        )

    # =====================================================
    # BEST TRADE
    # =====================================================

    def best_trade(self):

        if not self.trades:

            return None

        return max(

            self.trades,

            key=lambda t: t.get("profit", 0),

        )

    # =====================================================
    # WORST TRADE
    # =====================================================

    def worst_trade(self):

        if not self.trades:

            return None

        return min(

            self.trades,

            key=lambda t: t.get("profit", 0),

        )

    # =====================================================
    # REPORT
    # =====================================================

    def report(self):

        return {

            "total_trades": self.total_trades(),

            "wins": self.wins(),

            "losses": self.losses(),

            "win_rate": self.win_rate(),

            "gross_profit": self.gross_profit(),

            "gross_loss": self.gross_loss(),

            "net_profit": self.net_profit(),

            "average_win": self.average_win(),

            "average_loss": self.average_loss(),

            "profit_factor": self.profit_factor(),

            "expectancy": self.expectancy(),

            "best_trade": self.best_trade(),

            "worst_trade": self.worst_trade(),

        }