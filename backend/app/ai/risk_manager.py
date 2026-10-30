"""
AEGIS AI v3
Institutional Risk Manager
"""

from __future__ import annotations


class RiskManager:

    def __init__(

        self,

        account_balance=10000,

        risk_per_trade=0.01,

        max_daily_loss=0.05,

        max_open_positions=3,

        max_drawdown=0.20,

    ):

        self.account_balance = float(account_balance)

        self.risk_per_trade = risk_per_trade

        self.max_daily_loss = max_daily_loss

        self.max_open_positions = max_open_positions

        self.max_drawdown = max_drawdown

    # =====================================================
    # ACCOUNT RISK
    # =====================================================

    def risk_amount(self):

        return round(

            self.account_balance

            * self.risk_per_trade,

            2,

        )

    # =====================================================
    # MAXIMUM RISK
    # =====================================================

    def maximum_risk(self):

        return self.risk_amount()

    # =====================================================
    # POSITION SIZE
    # =====================================================

    def position_size(

        self,

        entry,

        stop,

        pip_value=1,

    ):

        risk = abs(

            float(entry)

            - float(stop)

        )

        if risk <= 0:

            return 0

        amount = self.risk_amount()

        size = amount / (

            risk * pip_value

        )

        return max(

            round(size, 2),

            0,

        )

    # =====================================================
    # LOT SIZE
    # =====================================================

    def lot_size(

        self,

        entry,

        stop,

        pip_value=100000,

    ):

        lots = self.position_size(

            entry,

            stop,

            pip_value,

        )

        return max(

            round(lots, 2),

            0.01,

        )

    # =====================================================
    # RISK REWARD
    # =====================================================

    def risk_reward(

        self,

        entry,

        stop,

        target,

    ):

        risk = abs(

            entry - stop

        )

        reward = abs(

            target - entry

        )

        if risk <= 0:

            return 0

        return round(

            reward / risk,

            2,

        )

    # =====================================================
    # VALIDATE RR
    # =====================================================

    def valid_rr(

        self,

        rr,

        minimum=2,

    ):

        return rr >= minimum

    # =====================================================
    # DAILY LOSS LIMIT
    # =====================================================

    def daily_limit(

        self,

        daily_loss,

    ):

        limit = (

            self.account_balance

            * self.max_daily_loss

        )

        return daily_loss < limit

    # =====================================================
    # DRAWDOWN
    # =====================================================

    def drawdown(

        self,

        peak,

        current,

    ):

        if peak <= 0:

            return 0

        return (

            peak - current

        ) / peak

    # =====================================================
    # VALID DRAWDOWN
    # =====================================================

    def valid_drawdown(

        self,

        peak,

        current,

    ):

        return (

            self.drawdown(

                peak,

                current,

            )

            < self.max_drawdown

        )

    # =====================================================
    # OPEN POSITIONS
    # =====================================================

    def can_open(

        self,

        current_positions,

    ):

        return (

            current_positions

            < self.max_open_positions

        )

    # =====================================================
    # UPDATE BALANCE
    # =====================================================

    def update_balance(

        self,

        pnl,

    ):

        self.account_balance = round(

            self.account_balance + pnl,

            2,

        )

        return self.account_balance

    # =====================================================
    # COMPOUND SIZE
    # =====================================================

    def compound_size(

        self,

        entry,

        stop,

        pip_value=100000,

    ):

        return self.lot_size(

            entry,

            stop,

            pip_value,

        )

    # =====================================================
    # MARGIN
    # =====================================================

    def margin_required(

        self,

        lot,

        leverage=100,

        contract=100000,

    ):

        margin = (

            lot

            * contract

        ) / leverage

        return round(

            margin,

            2,

        )

    # =====================================================
    # FREE MARGIN
    # =====================================================

    def free_margin(

        self,

        used,

    ):

        return round(

            self.account_balance

            - used,

            2,

        )

    # =====================================================
    # SAFE TRADE
    # =====================================================

    def safe_trade(

        self,

        trade,

        current_positions,

        daily_loss,

        peak_balance,

    ):

        rr = self.risk_reward(

            trade["entry"],

            trade["stop_loss"],

            trade["take_profit"],

        )

        if not self.valid_rr(rr):

            return False

        if not self.can_open(

            current_positions,

        ):

            return False

        if not self.daily_limit(

            daily_loss,

        ):

            return False

        if not self.valid_drawdown(

            peak_balance,

            self.account_balance,

        ):

            return False

        return True

    # =====================================================
    # BUILD RISK REPORT
    # =====================================================

    def report(

        self,

        trade,

        current_positions,

        daily_loss,

        peak_balance,

    ):

        rr = self.risk_reward(

            trade["entry"],

            trade["stop_loss"],

            trade["take_profit"],

        )

        lot = self.lot_size(

            trade["entry"],

            trade["stop_loss"],

        )

        margin = self.margin_required(

            lot,

        )

        return {

            "balance": self.account_balance,

            "maximum_risk": self.maximum_risk(),

            "risk_amount": self.risk_amount(),

            "lot_size": lot,

            "risk_reward": rr,

            "margin": margin,

            "free_margin": self.free_margin(

                margin,

            ),

            "approved": self.safe_trade(

                trade,

                current_positions,

                daily_loss,

                peak_balance,

            ),

        }