"""
AEGIS AI v2
Momentum Analyzer

Measures market momentum using
price change, RSI and MACD.
"""

from __future__ import annotations

from app.indicators.rsi import RSI
from app.indicators.macd import MACD


class Momentum:

    def __init__(

        self,

        period=14,

    ):

        self.period = period

        self.rsi = RSI(period)

        self.macd = MACD()

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

        if len(prices) < 35:

            return {

                "momentum": None,

                "score": 0,

                "rsi": None,

                "macd": None,

            }

        rsi = self.rsi.calculate(prices)

        macd = self.macd.calculate(prices)

        score = 50

        if rsi is not None:

            if rsi > 70:
                score += 25

            elif rsi > 60:
                score += 15

            elif rsi < 30:
                score -= 25

            elif rsi < 40:
                score -= 15

        histogram = macd["histogram"]

        if histogram is not None:

            if histogram > 0:
                score += 20

            elif histogram < 0:
                score -= 20

        score = max(0, min(score, 100))

        if score >= 80:

            momentum = "VERY_STRONG_BULLISH"

        elif score >= 60:

            momentum = "BULLISH"

        elif score <= 20:

            momentum = "VERY_STRONG_BEARISH"

        elif score <= 40:

            momentum = "BEARISH"

        else:

            momentum = "NEUTRAL"

        return {

            "momentum": momentum,

            "score": score,

            "rsi": rsi,

            "macd": macd,

        }

    # --------------------------------------------------

    def bullish(

        self,

        prices,

    ):

        return self.calculate(prices)["score"] > 60

    # --------------------------------------------------

    def bearish(

        self,

        prices,

    ):

        return self.calculate(prices)["score"] < 40