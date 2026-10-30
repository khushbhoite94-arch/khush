"""
AEGIS AI v2
Relative Strength Index
"""

from __future__ import annotations


class RSI:

    def __init__(

        self,

        period=14,

    ):

        self.period = period

    # ----------------------------------------------------

    def calculate(

        self,

        prices,

    ):

        prices = [

            float(x)

            for x in prices

            if x is not None

        ]

        if len(prices) < self.period + 1:

            return None

        gains = []

        losses = []

        for i in range(1, len(prices)):

            change = prices[i] - prices[i - 1]

            if change >= 0:

                gains.append(change)

                losses.append(0)

            else:

                gains.append(0)

                losses.append(abs(change))

        avg_gain = sum(

            gains[-self.period:]

        ) / self.period

        avg_loss = sum(

            losses[-self.period:]

        ) / self.period

        if avg_loss == 0:

            return 100

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return round(

            rsi,

            2,

        )