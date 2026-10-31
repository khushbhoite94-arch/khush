"""Risk controls for paper-trading position sizing and trade validation."""

from __future__ import annotations

from math import isfinite


class RiskManager:
    def __init__(
        self,
        risk_percent=1.0,
        reward_ratio=2.0,
        max_daily_loss=5.0,
        max_open_positions=1,
        contract_size=100000,
    ):
        self.risk_percent = risk_percent
        self.reward_ratio = reward_ratio
        self.max_daily_loss = max_daily_loss
        self.max_open_positions = max_open_positions
        self.contract_size = contract_size
        self.daily_loss = 0.0

    def calculate_position_size(self, balance, entry, stop_loss):
        values = (balance, entry, stop_loss, self.contract_size, self.risk_percent)
        if any(not isinstance(value, (int, float)) or not isfinite(value) for value in values):
            return 0.0
        if balance <= 0 or entry <= 0 or stop_loss <= 0 or self.contract_size <= 0 or self.risk_percent <= 0:
            return 0.0
        stop_distance = abs(entry - stop_loss)
        if stop_distance == 0:
            return 0.0
        risk_amount = balance * (self.risk_percent / 100)
        # PaperExecutor converts price movement to P&L using this same
        # contract multiplier. Include it here or position risk is overstated.
        lot = risk_amount / (stop_distance * self.contract_size)
        return round(lot, 4)

    def calculate_take_profit(self, entry, stop_loss, side):
        distance = abs(entry - stop_loss)
        reward = distance * self.reward_ratio
        if side == "BUY":
            return round(entry + reward, 6)
        if side == "SELL":
            return round(entry - reward, 6)
        raise ValueError("Side must be BUY or SELL")

    def can_open_trade(self, open_positions):
        return open_positions < self.max_open_positions

    def register_loss(self, amount):
        self.daily_loss += abs(amount)

    def reset_day(self):
        self.daily_loss = 0.0

    def trading_allowed(self, balance):
        if balance <= 0:
            return False
        percent_loss = (self.daily_loss / balance) * 100
        return percent_loss < self.max_daily_loss

    def evaluate(self, balance, entry, stop_loss, side, open_positions):
        values = (balance, entry, stop_loss)
        if any(not isinstance(value, (int, float)) or not isfinite(value) for value in values):
            return {"allowed": False, "reason": "Trade prices and balance must be finite numbers"}
        if side not in ("BUY", "SELL"):
            return {"allowed": False, "reason": "Side must be BUY or SELL"}
        if balance <= 0 or entry <= 0 or stop_loss <= 0:
            return {"allowed": False, "reason": "Balance, entry, and stop loss must be positive"}
        if (side == "BUY" and stop_loss >= entry) or (side == "SELL" and stop_loss <= entry):
            return {"allowed": False, "reason": "Stop loss is on the wrong side of entry"}
        if not self.can_open_trade(open_positions):
            return {"allowed": False, "reason": "Maximum open positions reached"}
        if not self.trading_allowed(balance):
            return {"allowed": False, "reason": "Daily loss limit reached"}

        lot = self.calculate_position_size(balance, entry, stop_loss)
        if lot <= 0:
            return {"allowed": False, "reason": "Calculated position size is zero"}
        tp = self.calculate_take_profit(entry, stop_loss, side)
        return {
            "allowed": True,
            "lot_size": lot,
            "take_profit": tp,
            "risk_percent": self.risk_percent,
            "contract_size": self.contract_size,
        }
