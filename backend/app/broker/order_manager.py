"""
AEGIS AI v2
Order Manager

Broker abstraction layer.
"""

from __future__ import annotations

from datetime import datetime


class OrderManager:

    def __init__(self, executor):

        self.executor = executor

        self.orders = []

    # ---------------------------------------------------------

    def buy(

        self,

        symbol,

        lot,

        entry,

        sl,

        tp,

    ):

        order = {

            "time": datetime.utcnow(),

            "side": "BUY",

            "symbol": symbol,

            "lot": lot,

            "entry": entry,

            "sl": sl,

            "tp": tp,

            "status": "OPEN",

        }

        result = self.executor.buy(

            symbol=symbol,

            lot=lot,

            entry=entry,

            sl=sl,

            tp=tp,

        )

        order["broker_result"] = result

        self.orders.append(order)

        return order

    # ---------------------------------------------------------

    def sell(

        self,

        symbol,

        lot,

        entry,

        sl,

        tp,

    ):

        order = {

            "time": datetime.utcnow(),

            "side": "SELL",

            "symbol": symbol,

            "lot": lot,

            "entry": entry,

            "sl": sl,

            "tp": tp,

            "status": "OPEN",

        }

        result = self.executor.sell(

            symbol=symbol,

            lot=lot,

            entry=entry,

            sl=sl,

            tp=tp,

        )

        order["broker_result"] = result

        self.orders.append(order)

        return order

    # ---------------------------------------------------------

    def close(

        self,

        order,

        price,

    ):

        result = self.executor.close(

            order,

            price,

        )

        order["status"] = "CLOSED"

        order["exit"] = price

        order["closed"] = datetime.utcnow()

        order["close_result"] = result

        return order

    # ---------------------------------------------------------

    def open_orders(self):

        return [

            o

            for o in self.orders

            if o["status"] == "OPEN"

        ]

    # ---------------------------------------------------------

    def closed_orders(self):

        return [

            o

            for o in self.orders

            if o["status"] == "CLOSED"

        ]

    # ---------------------------------------------------------

    def last_order(self):

        if not self.orders:

            return None

        return self.orders[-1]

    # ---------------------------------------------------------

    def statistics(self):

        return {

            "total_orders": len(self.orders),

            "open_orders": len(self.open_orders()),

            "closed_orders": len(self.closed_orders()),

        }

    # ---------------------------------------------------------

    def reset(self):

        self.orders.clear()
        