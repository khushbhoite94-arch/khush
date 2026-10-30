"""
AEGIS AI v2
Average True Range
"""

from __future__ import annotations


class ATR:

    def __init__(

        self,

        period=14,

    ):

        self.period = period

    # -----------------------------------------------------

    def calculate(

        self,

        candles,

    ):

        if candles is None:

            return None

        if len(candles) < self.period + 1:

            return None

        trs = []

        for i in range(1, len(candles)):

            current = candles[i]

            previous = candles[i - 1]

            high = float(current["high"])

            low = float(current["low"])

            prev_close = float(previous["close"])

            tr = max(

                high - low,

                abs(high - prev_close),

                abs(low - prev_close),

            )

            trs.append(tr)

        atr = sum(

            trs[-self.period:]

        ) / self.period

        return round(

            atr,

            6,

        )