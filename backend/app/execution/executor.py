"""
AEGIS AI
Paper Trading Engine
"""

from datetime import datetime
from uuid import uuid4

from app.risk.manager import RiskManager


class PaperExecutor:

    def __init__(self, starting_balance: float = 10000.0):

        self.balance = starting_balance
        self.equity = starting_balance

        self.risk = RiskManager()

        self.open_positions = []
        self.closed_positions = []

    # --------------------------------------------------

    def buy(
        self,
        symbol: str,
        entry: float,
        stop_loss: float,
        take_profit: float,
    ):

        sl_pips = abs(entry - stop_loss) * 10000

        lot = self.risk.calculate_lot_size(
            self.balance,
            sl_pips,
        )

        if not self.risk.can_open_trade(
            len(self.open_positions)
        ):
            raise Exception("Maximum open trades reached.")

        trade = self._create_trade(
            "BUY",
            symbol,
            lot,
            entry,
            stop_loss,
            take_profit,
        )

        self.open_positions.append(trade)

        return trade

    # --------------------------------------------------

    def sell(
        self,
        symbol: str,
        entry: float,
        stop_loss: float,
        take_profit: float,
    ):

        sl_pips = abs(stop_loss - entry) * 10000

        lot = self.risk.calculate_lot_size(
            self.balance,
            sl_pips,
        )

        if not self.risk.can_open_trade(
            len(self.open_positions)
        ):
            raise Exception("Maximum open trades reached.")

        trade = self._create_trade(
            "SELL",
            symbol,
            lot,
            entry,
            stop_loss,
            take_profit,
        )

        self.open_positions.append(trade)

        return trade

    # --------------------------------------------------

    def close_trade(
        self,
        trade_id: str,
        close_price: float,
    ):

        for trade in self.open_positions:

            if trade["id"] != trade_id:
                continue

            pnl = self.calculate_pnl(
                trade,
                close_price,
            )

            trade["close_price"] = close_price
            trade["close_time"] = datetime.utcnow().isoformat()
            trade["pnl"] = round(pnl, 2)

            self.balance += pnl
            self.equity = self.balance

            self.closed_positions.append(trade)

            self.open_positions.remove(trade)

            return trade

        return None

    # --------------------------------------------------

    def calculate_pnl(
        self,
        trade,
        close_price,
    ):

        multiplier = 100000

        if trade["type"] == "BUY":

            return (
                close_price
                - trade["entry"]
            ) * multiplier * trade["lot"]

        return (
            trade["entry"]
            - close_price
        ) * multiplier * trade["lot"]

    # --------------------------------------------------

    def _create_trade(
        self,
        trade_type,
        symbol,
        lot,
        entry,
        sl,
        tp,
    ):

        return {

            "id": str(uuid4()),

            "type": trade_type,

            "symbol": symbol,

            "lot": lot,

            "entry": entry,

            "sl": sl,

            "tp": tp,

            "time": datetime.utcnow().isoformat(),
        }

    # --------------------------------------------------

    def get_balance(self):

        return round(self.balance, 2)

    def get_equity(self):

        return round(self.equity, 2)

    def get_open_positions(self):

        return self.open_positions

    def get_closed_positions(self):

        return self.closed_positions