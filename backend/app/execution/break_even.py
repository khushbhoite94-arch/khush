"""
AEGIS AI v3
Break Even Manager
"""

from __future__ import annotations


class BreakEven:

    def __init__(

        self,

        trigger_rr=1.0,

    ):

        self.trigger_rr = trigger_rr

    # =====================================================
    # RISK
    # =====================================================

    def risk(

        self,

        trade,

    ):

        return abs(

            trade["entry"]

            - trade["stop_loss"]

        )

    # =====================================================
    # REWARD
    # =====================================================

    def reward(

        self,

        trade,

        current_price,

    ):

        if trade["direction"] == "BUY":

            return current_price - trade["entry"]

        return trade["entry"] - current_price

    # =====================================================
    # READY
    # =====================================================

    def ready(

        self,

        trade,

        current_price,

    ):

        risk = self.risk(trade)

        if risk == 0:

            return False

        rr = self.reward(

            trade,

            current_price,

        ) / risk

        return rr >= self.trigger_rr

    # =====================================================
    # APPLY
    # =====================================================

    def apply(

        self,

        trade,

        current_price,

    ):

        if not self.ready(

            trade,

            current_price,

        ):

            return trade

        trade["stop_loss"] = trade["entry"]

        trade["breakeven"] = True

        return trade