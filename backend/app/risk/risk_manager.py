"""
AEGIS AI v2
Risk Manager
"""

from __future__ import annotations


class RiskManager:

    def __init__(

        self,

        risk_percent=1.0,

        reward_ratio=2.0,

        max_daily_loss=5.0,

        max_open_positions=1,

    ):

        self.risk_percent = risk_percent

        self.reward_ratio = reward_ratio

        self.max_daily_loss = max_daily_loss

        self.max_open_positions = max_open_positions

        self.daily_loss = 0.0

    # ----------------------------------------------------

    def calculate_position_size(

        self,

        balance,

        entry,

        stop_loss,

    ):

        risk_amount = balance * (self.risk_percent / 100)

        stop_distance = abs(entry - stop_loss)

        if stop_distance == 0:

            return 0

        lot = risk_amount / stop_distance

        return round(lot, 4)

    # ----------------------------------------------------

    def calculate_take_profit(

        self,

        entry,

        stop_loss,

        side,

    ):

        distance = abs(entry - stop_loss)

        reward = distance * self.reward_ratio

        if side == "BUY":

            return round(entry + reward, 6)

        return round(entry - reward, 6)

    # ----------------------------------------------------

    def can_open_trade(

        self,

        open_positions,

    ):

        return open_positions < self.max_open_positions

    # ----------------------------------------------------

    def register_loss(

        self,

        amount,

    ):

        self.daily_loss += abs(amount)

    # ----------------------------------------------------

    def reset_day(self):

        self.daily_loss = 0

    # ----------------------------------------------------

    def trading_allowed(

        self,

        balance,

    ):

        if balance <= 0:

            return False

        percent_loss = (self.daily_loss / balance) * 100

        return percent_loss < self.max_daily_loss

    # ----------------------------------------------------

    def evaluate(

        self,

        balance,

        entry,

        stop_loss,

        side,

        open_positions,

    ):

        if not self.can_open_trade(open_positions):

            return {

                "allowed": False,

                "reason": "Maximum open positions reached",

            }

        if not self.trading_allowed(balance):

            return {

                "allowed": False,

                "reason": "Daily loss limit reached",

            }

        lot = self.calculate_position_size(

            balance,

            entry,

            stop_loss,

        )

        tp = self.calculate_take_profit(

            entry,

            stop_loss,

            side,

        )

        return {

            "allowed": True,

            "lot_size": lot,

            "take_profit": tp,

            "risk_percent": self.risk_percent,

        }