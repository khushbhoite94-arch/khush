"""
AEGIS AI
EMA Crossover Strategy
"""

from app.indicators.ema import EMA


class EMACrossover:

    def __init__(self):

        self.fast = EMA(9)
        self.slow = EMA(21)

    def signal(self, closes):

        if len(closes) < 21:
            return "WAIT"

        fast = self.fast.calculate(closes)
        slow = self.slow.calculate(closes)

        if fast is None or slow is None:
            return "WAIT"

        if fast > slow:
            return "BUY"

        if fast < slow:
            return "SELL"

        return "WAIT"