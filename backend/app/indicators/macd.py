"""
AEGIS AI v2
Moving Average Convergence Divergence
"""

from __future__ import annotations

from app.indicators.ema import EMA


class MACD:

    def __init__(

        self,

        fast=12,

        slow=26,

        signal=9,

    ):

        self.fast = fast

        self.slow = slow

        self.signal = signal

    # -----------------------------------------------------

    def calculate(

        self,

        prices,

    ):

        prices = [

            float(x)

            for x in prices

            if x is not None

        ]

        if len(prices) < self.slow + self.signal:

            return {

                "macd": None,

                "signal": None,

                "histogram": None,

            }

        macd_values = []

        for i in range(self.slow, len(prices) + 1):

            subset = prices[:i]

            fast = EMA(self.fast).calculate(subset)

            slow = EMA(self.slow).calculate(subset)

            if fast is None or slow is None:

                continue

            macd_values.append(fast - slow)

        if len(macd_values) < self.signal:

            return {

                "macd": None,

                "signal": None,

                "histogram": None,

            }

        signal_line = EMA(self.signal).calculate(macd_values)

        macd_line = macd_values[-1]

        histogram = macd_line - signal_line

        return {

            "macd": round(macd_line, 6),

            "signal": round(signal_line, 6),

            "histogram": round(histogram, 6),

        }