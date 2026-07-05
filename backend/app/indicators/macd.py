"""
AEGIS AI
MACD Indicator
"""

from app.indicators.ema import EMA


class MACD:

    def __init__(self):

        self.fast = EMA(12)
        self.slow = EMA(26)

    def calculate(self, prices):

        if len(prices) < 26:
            return None

        fast = self.fast.calculate(prices)
        slow = self.slow.calculate(prices)

        macd = fast - slow

        signal_prices = []

        for i in range(26, len(prices) + 1):

            f = self.fast.calculate(prices[:i])
            s = self.slow.calculate(prices[:i])

            if f is not None and s is not None:
                signal_prices.append(f - s)

        signal = EMA(9).calculate(signal_prices)

        histogram = None

        if signal is not None:
            histogram = macd - signal

        return {
            "macd": round(macd, 5),
            "signal": round(signal, 5) if signal is not None else None,
            "histogram": round(histogram, 5) if histogram is not None else None,
        }