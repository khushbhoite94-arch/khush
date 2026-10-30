"""
AEGIS AI v2
Smart Money Strategy
"""

from __future__ import annotations


class SmartMoney:

    def __init__(self, lookback=10):

        self.lookback = lookback

    # ----------------------------------------------------

    def signal(self, candles):

        if candles is None or len(candles) < self.lookback + 2:

            return {

                "strategy": "SMART_MONEY",

                "signal": "WAIT",

                "confidence": 0,

                "reason": "Not enough candles",

            }

        previous = candles[-self.lookback-1:-1]

        last = candles[-1]

        highest = max(c["high"] for c in previous)
        lowest = min(c["low"] for c in previous)

        # ------------------------
        # Liquidity sweep above
        # ------------------------

        if (

            last["high"] > highest

            and

            last["close"] < highest

        ):

            return {

                "strategy": "SMART_MONEY",

                "signal": "SELL",

                "confidence": 90,

                "reason": [

                    "Liquidity sweep above highs",

                ],

            }

        # ------------------------
        # Liquidity sweep below
        # ------------------------

        if (

            last["low"] < lowest

            and

            last["close"] > lowest

        ):

            return {

                "strategy": "SMART_MONEY",

                "signal": "BUY",

                "confidence": 90,

                "reason": [

                    "Liquidity sweep below lows",

                ],

            }

        return {

            "strategy": "SMART_MONEY",

            "signal": "WAIT",

            "confidence": 0,

            "reason": "No smart money setup",

        }