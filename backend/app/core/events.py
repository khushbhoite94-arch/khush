"""
AEGIS AI v2
Event Bus
"""

from collections import defaultdict


class EventBus:

    def __init__(self):

        self.events = defaultdict(list)

    # ----------------------------------------------------

    def subscribe(

        self,

        event,

        callback,

    ):

        self.events[event].append(callback)

    # ----------------------------------------------------

    def unsubscribe(

        self,

        event,

        callback,

    ):

        if callback in self.events[event]:

            self.events[event].remove(callback)

    # ----------------------------------------------------

    def emit(

        self,

        event,

        *args,

        **kwargs,

    ):

        for callback in self.events[event]:

            callback(

                *args,

                **kwargs,

            )

    # ----------------------------------------------------

    def clear(self):

        self.events.clear()


events = EventBus()


# ============================================================
# EVENT NAMES
# ============================================================

PRICE_UPDATE = "price_update"

NEW_CANDLE = "new_candle"

AI_SIGNAL = "ai_signal"

ORDER_OPENED = "order_opened"

ORDER_CLOSED = "order_closed"

STOP_LOSS = "stop_loss"

TAKE_PROFIT = "take_profit"

ERROR = "error"

CONNECTED = "connected"

DISCONNECTED = "disconnected"