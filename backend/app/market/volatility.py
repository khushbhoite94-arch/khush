"""
AEGIS AI
Volatility Analyzer
"""


class Volatility:

    def __init__(self):

        self.values = []

    def update(self, candle):

        value = candle.high - candle.low

        self.values.append(value)

        if len(self.values) > 100:

            self.values.pop(0)

    @property
    def current(self):

        if not self.values:

            return 0

        return self.values[-1]

    @property
    def average(self):

        if not self.values:

            return 0

        return sum(self.values) / len(self.values)

    @property
    def high(self):

        return self.current > self.average * 1.5

    @property
    def low(self):

        return self.current < self.average * 0.5