"""
AEGIS AI v3
Trade Executor
"""

from __future__ import annotations

import uuid
from datetime import datetime


class TradeExecutor:

    def __init__(

        self,

        mode="paper",

    ):

        self.mode = mode

        self.orders = []

        self.executed = []

    # =====================================================
    # BUILD ORDER
    # =====================================================

    def build_order(

        self,

        trade,

    ):

        order = {

            "id": str(

                uuid.uuid4()

            ),

            "direction":

                trade["direction"],

            "entry":

                trade["entry"],

            "stop_loss":

                trade["stop_loss"],

            "take_profit":

                trade["take_profit"],

            "lot_size":

                trade.get(

                    "lot_size",

                    0.01,

                ),

            "status": "PENDING",

            "created": datetime.utcnow(),

        }

        return order

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(

        self,

        trade,

    ):

        required = [

            "direction",

            "entry",

            "stop_loss",

            "take_profit",

        ]

        for field in required:

            if field not in trade:

                raise ValueError(

                    f"Missing {field}"

                )

        return True

    # =====================================================
    # PAPER EXECUTION
    # =====================================================

    def paper_execute(

        self,

        trade,

    ):

        self.validate(trade)

        order = self.build_order(

            trade,

        )

        order["status"] = "FILLED"

        order["mode"] = "PAPER"

        order["filled"] = datetime.utcnow()

        self.executed.append(order)

        return order

    # =====================================================
    # LIVE EXECUTION
    # =====================================================

    def live_execute(

        self,

        trade,

    ):

        self.validate(trade)

        order = self.build_order(

            trade,

        )

        order["status"] = "SENT"

        order["mode"] = "LIVE"

        self.orders.append(order)

        return order

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(

        self,

        trade,

    ):

        if self.mode.lower() == "paper":

            return self.paper_execute(

                trade,

            )

        return self.live_execute(

            trade,

        )

    # =====================================================
    # CANCEL
    # =====================================================

    def cancel(

        self,

        order_id,

    ):

        for order in self.orders:

            if order["id"] == order_id:

                order["status"] = "CANCELLED"

                return order

        return None

    # =====================================================
    # COMPLETE
    # =====================================================

    def complete(

        self,

        order_id,

    ):

        for order in self.orders:

            if order["id"] == order_id:

                order["status"] = "FILLED"

                order["filled"] = datetime.utcnow()

                self.executed.append(order)

                self.orders.remove(order)

                return order

        return None

    # =====================================================
    # GET
    # =====================================================

    def get(

        self,

        order_id,

    ):

        for order in (

            self.orders +

            self.executed

        ):

            if order["id"] == order_id:

                return order

        return None

    # =====================================================
    # OPEN
    # =====================================================

    def open_orders(

        self,

    ):

        return self.orders

    # =====================================================
    # HISTORY
    # =====================================================

    def history(

        self,

    ):

        return self.executed

    # =====================================================
    # STATS
    # =====================================================

    def statistics(

        self,

    ):

        return {

            "mode": self.mode,

            "pending": len(

                self.orders

            ),

            "executed": len(

                self.executed

            ),

        }

    # =====================================================
    # RESET
    # =====================================================

    def reset(

        self,

    ):

        self.orders.clear()

        self.executed.clear()

    # =====================================================
    # SWITCH MODE
    # =====================================================

    def set_mode(

        self,

        mode,

    ):

        self.mode = mode