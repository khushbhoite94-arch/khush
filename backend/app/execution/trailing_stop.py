"""
AEGIS AI v3
Trailing Stop Manager
"""

from __future__ import annotations


class TrailingStop:

    def __init__(

        self,

        distance,

    ):

        self.distance = distance

    # =====================================================
    # NEW STOP
    # =====================================================

    def new_stop(

        self,

        trade,

        current_price,

    ):

        if trade["direction"] == "BUY":

            return current_price - self.distance

        return current_price + self.distance

    # =====================================================
    # SHOULD MOVE
    # =====================================================

    def should_move(

        self,

        trade,

        current_price,

    ):

        stop = self.new_stop(

            trade,

            current_price,

        )

        if trade["direction"] == "BUY":

            return stop > trade["stop_loss"]

        return stop < trade["stop_loss"]

    # =====================================================
    # APPLY
    # =====================================================

    def apply(

        self,

        trade,

        current_price,

    ):

        if self.should_move(

            trade,

            current_price,

        ):

            trade["stop_loss"] = self.new_stop(

                trade,

                current_price,

            )

        return trade

    # =====================================================
    # RESET
    # =====================================================

    def reset(

        self,

    ):

        return True