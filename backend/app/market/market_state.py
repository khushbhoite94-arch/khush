"""
AEGIS AI
Market State
"""

from collections import deque

from app.market.candles import Candle


class MarketState:

    def __init__(self, history=1000):

        self.candles = deque(maxlen=history)

    def add(self, candle: Candle):

        self.candles.append(candle)

    def latest(self):

        if not self.candles:
            return None

        return self.candles[-1]

    def previous(self):

        if len(self.candles) < 2:
            return None

        return self.candles[-2]

    def last(self, n):

        return list(self.candles)[-n:]

    def clear(self):

        self.candles.clear()

    def size(self):

        return len(self.candles)