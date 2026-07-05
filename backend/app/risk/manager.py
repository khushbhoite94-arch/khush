"""
AEGIS AI
Risk Manager
"""

from dataclasses import dataclass


@dataclass
class RiskSettings:

    risk_percent: float = 1.0
    max_daily_loss_percent: float = 5.0
    max_drawdown_percent: float = 10.0
    max_open_trades: int = 3
    min_lot: float = 0.01
    max_lot: float = 5.00
    pip_value_per_lot: float = 10.0


class RiskManager:

    def __init__(self, settings: RiskSettings | None = None):

        self.settings = settings or RiskSettings()

    def calculate_lot_size(
        self,
        balance: float,
        stop_loss_pips: float,
    ) -> float:

        if stop_loss_pips <= 0:
            raise ValueError("Stop loss must be greater than zero.")

        risk_amount = balance * (self.settings.risk_percent / 100)

        lot = risk_amount / (
            stop_loss_pips * self.settings.pip_value_per_lot
        )

        lot = round(lot, 2)

        lot = max(lot, self.settings.min_lot)
        lot = min(lot, self.settings.max_lot)

        return lot

    def can_open_trade(
        self,
        open_positions: int,
    ) -> bool:

        return (
            open_positions
            < self.settings.max_open_trades
        )

    def daily_loss_limit(
        self,
        balance: float,
    ) -> float:

        return (
            balance
            * self.settings.max_daily_loss_percent
            / 100
        )

    def drawdown_limit(
        self,
        balance: float,
    ) -> float:

        return (
            balance
            * self.settings.max_drawdown_percent
            / 100
        )