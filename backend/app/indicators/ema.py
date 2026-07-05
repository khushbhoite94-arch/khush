"""
AEGIS AI
EMA Indicator
"""


class EMA:

    def __init__(self, period=20):

        self.period = period

    def calculate(self, prices):

        if len(prices) < self.period:
            return None

        multiplier = 2 / (self.period + 1)

        ema = sum(prices[:self.period]) / self.period

        for price in prices[self.period:]:

            ema = (price - ema) * multiplier + ema

        return round(ema, 5)