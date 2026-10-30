"""
AEGIS AI v2
EMA Crossover Strategy
"""

from __future__ import annotations

from app.indicators.ema import EMA
from app.indicators.rsi import RSI
from app.indicators.macd import MACD
from app.indicators.trend import Trend


class EMACrossover:

    def __init__(self):

        self.fast = EMA(9)
        self.slow = EMA(21)

        self.rsi = RSI()
        self.macd = MACD()
        self.trend = Trend()

    # ----------------------------------------------------

    def signal(self, closes):

        closes = [

            float(x)

            for x in closes

            if x is not None

        ]

        if len(closes) < 40:

            return {

                "signal": "WAIT",

                "confidence": 0,

                "reason": "Not enough candles",

            }

        fast_now = self.fast.calculate(closes)

        slow_now = self.slow.calculate(closes)

        fast_prev = self.fast.calculate(closes[:-1])

        slow_prev = self.slow.calculate(closes[:-1])

        rsi = self.rsi.calculate(closes)

        macd = self.macd.calculate(closes)

        trend = self.trend.calculate(closes)

        # ------------------------------------------

        bullish_cross = (

            fast_prev <= slow_prev

            and

            fast_now > slow_now

        )

        bearish_cross = (

            fast_prev >= slow_prev

            and

            fast_now < slow_now

        )

        # ------------------------------------------

        if (

            bullish_cross

            and

            trend["trend"] == "BULLISH"

            and

            rsi > 50

            and

            macd["histogram"] > 0

        ):

            return {

                "signal": "BUY",

                "confidence": 85,

                "reason": [

                    "EMA Bullish Crossover",

                    "Trend Bullish",

                    "RSI > 50",

                    "MACD Bullish",

                ],

            }

        # ------------------------------------------

        if (

            bearish_cross

            and

            trend["trend"] == "BEARISH"

            and

            rsi < 50

            and

            macd["histogram"] < 0

        ):

            return {

                "signal": "SELL",

                "confidence": 85,

                "reason": [

                    "EMA Bearish Crossover",

                    "Trend Bearish",

                    "RSI < 50",

                    "MACD Bearish",

                ],

            }

        return {

            "signal": "WAIT",

            "confidence": 0,

            "reason": "No valid crossover",

        }