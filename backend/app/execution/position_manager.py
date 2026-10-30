"""
AEGIS AI v3
Position Manager

Central manager for all open and closed positions.
"""

from __future__ import annotations

from datetime import datetime


class PositionManager:

    def __init__(self):

        self.open_positions = []

        self.closed_positions = []

    # =====================================================
    # OPEN POSITION
    # =====================================================

    def open(self, trade):

        position = trade.copy()

        position["status"] = "OPEN"

        position["opened_at"] = datetime.utcnow()

        position["closed_at"] = None

        position["exit_price"] = None

        position["profit"] = 0.0

        self.open_positions.append(position)

        return position

    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close(self, trade_id, exit_price):

        for position in self.open_positions:

            if position["id"] != trade_id:
                continue

            if position["direction"] == "BUY":

                pnl = exit_price - position["entry"]

            else:

                pnl = position["entry"] - exit_price

            pnl *= position.get("lot_size", 1)

            position["profit"] = round(pnl, 5)

            position["exit_price"] = exit_price

            position["closed_at"] = datetime.utcnow()

            position["status"] = "CLOSED"

            self.open_positions.remove(position)

            self.closed_positions.append(position)

            return position

        return None

    # =====================================================
    # FIND POSITION
    # =====================================================

    def get(self, trade_id):

        for position in self.open_positions:

            if position["id"] == trade_id:

                return position

        return None

    # =====================================================
    # FLOATING PNL
    # =====================================================

    def floating_profit(self, current_price):

        total = 0.0

        for position in self.open_positions:

            if position["direction"] == "BUY":

                pnl = current_price - position["entry"]

            else:

                pnl = position["entry"] - current_price

            pnl *= position.get("lot_size", 1)

            total += pnl

        return round(total, 5)

    # =====================================================
    # TOTAL CLOSED PNL
    # =====================================================

    def realized_profit(self):

        return round(

            sum(

                p["profit"]

                for p in self.closed_positions

            ),

            5,

        )

    # =====================================================
    # WIN RATE
    # =====================================================

    def win_rate(self):

        if not self.closed_positions:

            return 0.0

        wins = len(

            [

                p

                for p in self.closed_positions

                if p["profit"] > 0

            ]

        )

        return round(

            wins / len(self.closed_positions) * 100,

            2,

        )

    # =====================================================
    # EXPOSURE
    # =====================================================

    def exposure(self):

        return round(

            sum(

                p.get("lot_size", 0)

                for p in self.open_positions

            ),

            2,

        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        return {

            "open_positions": len(self.open_positions),

            "closed_positions": len(self.closed_positions),

            "realized_profit": self.realized_profit(),

            "win_rate": self.win_rate(),

            "exposure": self.exposure(),

        }

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.open_positions.clear()

        self.closed_positions.clear()