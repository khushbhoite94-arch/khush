"""
AEGIS AI v2
Breakout Strategy
"""

from __future__ import annotations


class Breakout:

    def __init__(

        self,

        lookback=20,

    ):

        self.lookback = lookback

    # ----------------------------------------------------

    def signal(

        self,

        candles,

    ):

        if candles is None:

            return {

                "signal": "WAIT",

                "confidence": 0,

                "reason": "No candles",

            }

        if len(candles) < self.lookback + 1:

            return {

                "signal": "WAIT",

                "confidence": 0,

                "reason": "Not enough candles",

            }

        recent = candles[-self.lookback:]

        last = recent[-1]

        previous = recent[:-1]

        highest = max(

            c["high"]

            for c in previous

        )

        lowest = min(

            c["low"]

            for c in previous

        )

        close = last["close"]

        # -------------------------------------

        if close > highest:

            return {

                "strategy": "BREAKOUT",

                "signal": "BUY",

                "confidence": 82,

                "reason": [

                    "Price broke previous high",

                ],

            }

        # -------------------------------------

        if close < lowest:

            return {

                "strategy": "BREAKOUT",

                "signal": "SELL",

                "confidence": 82,

                "reason": [

                    "Price broke previous low",

                ],

            }

        return {

            "strategy": "BREAKOUT",

            "signal": "WAIT",

            "confidence": 0,

            "reason": "Inside range",

        }