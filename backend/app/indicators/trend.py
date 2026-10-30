"""
AEGIS AI v2
Trend Analyzer

Determines market trend using EMA alignment
and market structure.

Returns:
    BULLISH
    BEARISH
    SIDEWAYS
"""

from __future__ import annotations

from app.indicators.ema import EMA


class Trend:

    def __init__(

        self,

        fast=20,

        slow=50,

    ):

        self.fast = fast
        self.slow = slow

    # --------------------------------------------------

    def calculate(

        self,

        prices,

    ):

        prices = [

            float(x)

            for x in prices

            if x is not None

        ]

        if len(prices) < self.slow:

            return {

                "trend": None,

                "strength": 0,

                "ema_fast": None,

                "ema_slow": None,

            }

        ema_fast = EMA(self.fast).calculate(prices)

        ema_slow = EMA(self.slow).calculate(prices)

        latest = prices[-1]

        if ema_fast > ema_slow and latest > ema_fast:

            trend = "BULLISH"

        elif ema_fast < ema_slow and latest < ema_fast:

            trend = "BEARISH"

        else:

            trend = "SIDEWAYS"

        distance = abs(ema_fast - ema_slow)

        strength = min(

            100,

            round(distance * 100000)

        )

        return {

            "trend": trend,

            "strength": strength,

            "ema_fast": round(ema_fast, 6),

            "ema_slow": round(ema_slow, 6),

        }

    # --------------------------------------------------

    def bullish(

        self,

        prices,

    ):

        result = self.calculate(prices)

        return result["trend"] == "BULLISH"

    # --------------------------------------------------

    def bearish(

        self,

        prices,

    ):

        result = self.calculate(prices)

        return result["trend"] == "BEARISH"

    # --------------------------------------------------

    def sideways(

        self,

        prices,

    ):

        result = self.calculate(prices)

        return result["trend"] == "SIDEWAYS"