"""
AEGIS AI v2
Pullback Strategy
"""

from __future__ import annotations

from app.indicators.trend import Trend
from app.indicators.ema import EMA


class Pullback:

    def __init__(self):

        self.trend = Trend()

        self.ema20 = EMA(20)

    # ----------------------------------------------------

    def signal(self, closes):

        closes = [float(x) for x in closes if x is not None]

        if len(closes) < 50:

            return {

                "strategy": "PULLBACK",

                "signal": "WAIT",

                "confidence": 0,

                "reason": "Not enough candles",

            }

        trend = self.trend.calculate(closes)

        ema = self.ema20.calculate(closes)

        last = closes[-1]

        distance = abs(last - ema)

        # -------------------------

        if (

            trend["trend"] == "BULLISH"

            and

            last <= ema

            and

            distance < 0.0005

        ):

            return {

                "strategy": "PULLBACK",

                "signal": "BUY",

                "confidence": 88,

                "reason": [

                    "Bullish Trend",

                    "Price pulled back to EMA20",

                ],

            }

        # -------------------------

        if (

            trend["trend"] == "BEARISH"

            and

            last >= ema

            and

            distance < 0.0005

        ):

            return {

                "strategy": "PULLBACK",

                "signal": "SELL",

                "confidence": 88,

                "reason": [

                    "Bearish Trend",

                    "Price pulled back to EMA20",

                ],

            }

        return {

            "strategy": "PULLBACK",

            "signal": "WAIT",

            "confidence": 0,

            "reason": "No pullback",

        }