"""
AEGIS AI v2
Volatility Indicator

Uses ATR to classify
market volatility.
"""

from __future__ import annotations

from app.indicators.atr import ATR


class Volatility:

    def __init__(

        self,

        period=14,

    ):

        self.period = period

        self.atr = ATR(period)

    # --------------------------------------------------

    def calculate(

        self,

        candles,

    ):

        atr = self.atr.calculate(candles)

        if atr is None:

            return {

                "atr": None,

                "state": None,

            }

        if atr < 0.0005:

            state = "VERY_LOW"

        elif atr < 0.0010:

            state = "LOW"

        elif atr < 0.0020:

            state = "NORMAL"

        elif atr < 0.0040:

            state = "HIGH"

        else:

            state = "EXTREME"

        return {

            "atr": atr,

            "state": state,

        }

    # --------------------------------------------------

    def tradable(

        self,

        candles,

    ):

        state = self.calculate(candles)["state"]

        return state in (

            "NORMAL",

            "HIGH",

        )

    # --------------------------------------------------

    def dangerous(

        self,

        candles,

    ):

        return self.calculate(candles)["state"] == "EXTREME"