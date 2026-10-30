"""
AEGIS AI v2
Range Trading Strategy
"""

from __future__ import annotations


class RangeStrategy:

    def __init__(

        self,

        lookback=20,

        tolerance=0.0002,

    ):

        self.lookback = lookback
        self.tolerance = tolerance

    # ----------------------------------------------------

    def signal(

        self,

        candles,

    ):

        if candles is None or len(candles) < self.lookback:

            return {

                "strategy": "RANGE",

                "signal": "WAIT",

                "confidence": 0,

                "reason": "Not enough candles",

            }

        recent = candles[-self.lookback:]

        high = max(c["high"] for c in recent)

        low = min(c["low"] for c in recent)

        close = recent[-1]["close"]

        # Buy near support

        if close <= low + self.tolerance:

            return {

                "strategy": "RANGE",

                "signal": "BUY",

                "confidence": 78,

                "reason": [

                    "Near range support",

                ],

            }

        # Sell near resistance

        if close >= high - self.tolerance:

            return {

                "strategy": "RANGE",

                "signal": "SELL",

                "confidence": 78,

                "reason": [

                    "Near range resistance",

                ],

            }

        return {

            "strategy": "RANGE",

            "signal": "WAIT",

            "confidence": 0,

            "reason": "Middle of range",

        }