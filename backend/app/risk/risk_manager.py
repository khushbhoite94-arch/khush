"""
AEGIS AI
Risk Manager
"""


class RiskManager:

    def __init__(

        self,

        risk_percent=1.0,
        min_lot=0.01,
        max_lot=10.0

    ):

        self.risk_percent = risk_percent
        self.min_lot = min_lot
        self.max_lot = max_lot

    # --------------------------------------------------

    def calculate_lot(

        self,

        balance,
        stop_loss_points,
        pip_value=1.0,

    ):

        if stop_loss_points <= 0:
            return self.min_lot

        risk_amount = balance * (self.risk_percent / 100)

        lot = risk_amount / (stop_loss_points * pip_value)

        lot = round(lot, 2)

        if lot < self.min_lot:
            lot = self.min_lot

        if lot > self.max_lot:
            lot = self.max_lot

        return lot