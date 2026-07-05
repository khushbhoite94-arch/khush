"""
AEGIS AI
Candle History
"""


class MarketHistory:

    def __init__(self, max_candles=500):

        self.candles = []
        self.max_candles = max_candles

    # -----------------------------------------------------

    def add(self, candle):

        if candle is None:
            return

        self.candles.append(candle)

        if len(self.candles) > self.max_candles:
            self.candles.pop(0)

    # -----------------------------------------------------

    def closes(self):

        return [
            c["close"]
            for c in self.candles
            if c.get("close") is not None
        ]

    # -----------------------------------------------------

    def highs(self):

        return [
            c["high"]
            for c in self.candles
            if c.get("high") is not None
        ]

    # -----------------------------------------------------

    def lows(self):

        return [
            c["low"]
            for c in self.candles
            if c.get("low") is not None
        ]

    # -----------------------------------------------------

    def opens(self):

        return [
            c["open"]
            for c in self.candles
            if c.get("open") is not None
        ]

    # -----------------------------------------------------

    def latest(self):

        if not self.candles:
            return None

        return self.candles[-1]

    # -----------------------------------------------------

    def count(self):

        return len(self.candles)