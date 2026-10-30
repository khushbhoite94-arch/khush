"""
AEGIS AI v2
Exponential Moving Average
"""

from __future__ import annotations


class EMA:

    def __init__(

        self,

        period: int,

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

        if len(prices) < self.period:

            return None

        multiplier = 2 / (self.period + 1)

        ema = sum(

            prices[: self.period]

        ) / self.period

        for price in prices[self.period:]:

            ema = (

                price - ema

            ) * multiplier + ema

        return round(

            ema,

            6,

        )