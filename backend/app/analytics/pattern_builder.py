"""
AEGIS AI v2
Pattern Recognition Engine
"""

from __future__ import annotations


class PatternEngine:

    def __init__(self):

        self.minimum = 5

    # -------------------------------------------------------

    def analyze(self, candles):

        if len(candles) < self.minimum:

            return {

                "pattern": "UNKNOWN",

                "strength": 0,

                "bullish": False,

                "bearish": False,

            }

        closes = [c["close"] for c in candles]

        highs = [c["high"] for c in candles]

        lows = [c["low"] for c in candles]

        return self.detect(

            closes,

            highs,

            lows,

        )

    # -------------------------------------------------------

    def detect(

        self,

        closes,

        highs,

        lows,

    ):

        bullish = 0

        bearish = 0

        pattern = "NONE"

        # ------------------------------------------------

        if closes[-1] > closes[-2] > closes[-3]:

            bullish += 30

            pattern = "Higher High"

        # ------------------------------------------------

        if closes[-1] < closes[-2] < closes[-3]:

            bearish += 30

            pattern = "Lower Low"

        # ------------------------------------------------

        if highs[-1] > highs[-2]:

            bullish += 10

        else:

            bearish += 10

        # ------------------------------------------------

        if lows[-1] > lows[-2]:

            bullish += 10

        else:

            bearish += 10

        strength = max(

            bullish,

            bearish,

        )

        return {

            "pattern": pattern,

            "strength": strength,

            "bullish": bullish > bearish,

            "bearish": bearish > bullish,

        }