"""
AEGIS AI v3
Order Manager
"""

from __future__ import annotations

from uuid import uuid4
from datetime import datetime


class OrderManager:

    def __init__(self):

        self.pending_orders = []

        self.executed_orders = []

        self.cancelled_orders = []

    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create(

        self,

        direction,

        symbol,

        entry,

        stop_loss,

        take_profit,

        lot_size,

    ):

        order = {

            "id": str(uuid4()),

            "direction": direction,

            "symbol": symbol,

            "entry": float(entry),

            "stop_loss": float(stop_loss),

            "take_profit": float(take_profit),

            "lot_size": float(lot_size),

            "status": "PENDING",

            "created_at": datetime.utcnow(),

        }

        self.pending_orders.append(order)

        return order

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(

        self,

        order,

    ):

        if order["lot_size"] <= 0:

            return False

        if order["entry"] <= 0:

            return False

        if order["direction"] == "BUY":

            return (

                order["stop_loss"]

                <

                order["entry"]

                <

                order["take_profit"]

            )

        return (

            order["take_profit"]

            <

            order["entry"]

            <

            order["stop_loss"]

        )

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(

        self,

        order,

    ):

        if not self.validate(order):

            return None

        if order not in self.pending_orders:

            return None

        self.pending_orders.remove(order)

        order["status"] = "EXECUTED"

        order["executed_at"] = datetime.utcnow()

        self.executed_orders.append(order)

        return order

    # =====================================================
    # CANCEL
    # =====================================================

    def cancel(

        self,

        order,

    ):

        if order not in self.pending_orders:

            return None

        self.pending_orders.remove(order)

        order["status"] = "CANCELLED"

        order["cancelled_at"] = datetime.utcnow()

        self.cancelled_orders.append(order)

        return order

    # =====================================================
    # FIND
    # =====================================================

    def get(

        self,

        order_id,

    ):

        for order in (

            self.pending_orders

            +

            self.executed_orders

            +

            self.cancelled_orders

        ):

            if order["id"] == order_id:

                return order

        return None

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        return {

            "pending": len(self.pending_orders),

            "executed": len(self.executed_orders),

            "cancelled": len(self.cancelled_orders),

        }

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.pending_orders.clear()

        self.executed_orders.clear()

        self.cancelled_orders.clear()