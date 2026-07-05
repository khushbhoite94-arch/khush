"""
AEGIS AI
Live Candle Builder
"""

from datetime import datetime


class CandleBuilder:

    def __init__(self):

        self.current = None

    def update(self, price):

        minute = datetime.utcnow().replace(second=0, microsecond=0)

        if self.current is None:

            self.current = {
                "time": minute,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
            }

            return None

        if minute == self.current["time"]:

            self.current["high"] = max(self.current["high"], price)
            self.current["low"] = min(self.current["low"], price)
            self.current["close"] = price

            return None

        finished = self.current.copy()

        self.current = {
            "time": minute,
            "open": price,
            "high": price,
            "low": price,
            "close": price,
        }

        return finished