"""
AEGIS AI v2
Institutional Fair Value Gap Engine
"""

from __future__ import annotations


class FairValueGap:

    def __init__(

        self,

        min_gap=0.00001,

    ):

        self.min_gap = min_gap

    # =====================================================
    # BULLISH FVG
    # =====================================================

    def bullish(

        self,

        candles,

    ):

        gaps = []

        if len(candles) < 3:

            return gaps

        for i in range(2, len(candles)):

            first = candles[i - 2]

            third = candles[i]

            gap = third["low"] - first["high"]

            if gap >= self.min_gap:

                gaps.append(

                    {

                        "index": i,

                        "type": "BULLISH",

                        "top": third["low"],

                        "bottom": first["high"],

                        "size": gap,

                    }

                )

        return gaps

    # =====================================================
    # BEARISH FVG
    # =====================================================

    def bearish(

        self,

        candles,

    ):

        gaps = []

        if len(candles) < 3:

            return gaps

        for i in range(2, len(candles)):

            first = candles[i - 2]

            third = candles[i]

            gap = first["low"] - third["high"]

            if gap >= self.min_gap:

                gaps.append(

                    {

                        "index": i,

                        "type": "BEARISH",

                        "top": first["low"],

                        "bottom": third["high"],

                        "size": gap,

                    }

                )

        return gaps

    # =====================================================
    # ALL FVG
    # =====================================================

    def all(

        self,

        candles,

    ):

        return (

            self.bullish(candles)

            +

            self.bearish(candles)

        )

    # =====================================================
    # FILLED
    # =====================================================

    def filled(

        self,

        candles,

    ):

        filled = []

        for gap in self.all(candles):

            for candle in candles[gap["index"] + 1:]:

                if (

                    candle["low"] <= gap["top"]

                    and

                    candle["high"] >= gap["bottom"]

                ):

                    filled.append(

                        {

                            **gap,

                            "filled": True,

                        }

                    )

                    break

        return filled

    # =====================================================
    # OPEN GAPS
    # =====================================================

    def open(

        self,

        candles,

    ):

        filled = {

            g["index"]

            for g in self.filled(candles)

        }

        return [

            g

            for g in self.all(candles)

            if g["index"] not in filled

        ]

    # =====================================================
    # INVERSE FVG
    # =====================================================

    def inverse(

        self,

        candles,

    ):

        inverse = []

        for gap in self.filled(candles):

            inverse.append(

                {

                    **gap,

                    "inverse": True,

                }

            )

        return inverse

    # =====================================================
    # LARGEST GAP
    # =====================================================

    def largest(

        self,

        candles,

    ):

        gaps = self.open(candles)

        if not gaps:

            return None

        return max(

            gaps,

            key=lambda g: g["size"],

        )

    # =====================================================
    # NEAREST GAP
    # =====================================================

    def nearest(

        self,

        candles,

    ):

        gaps = self.open(candles)

        if not gaps:

            return None

        close = candles[-1]["close"]

        return min(

            gaps,

            key=lambda g:

            min(

                abs(close - g["top"]),

                abs(close - g["bottom"]),

            ),

        )

    # =====================================================
    # SIGNAL
    # =====================================================

    def signal(

        self,

        candles,

    ):

        gap = self.nearest(candles)

        if gap is None:

            return "NEUTRAL"

        if gap["type"] == "BULLISH":

            return "BUY"

        return "SELL"

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        return {

            "bullish":

                self.bullish(candles),

            "bearish":

                self.bearish(candles),

            "open":

                self.open(candles),

            "filled":

                self.filled(candles),

            "inverse":

                self.inverse(candles),

            "largest":

                self.largest(candles),

            "nearest":

                self.nearest(candles),

            "signal":

                self.signal(candles),

        }