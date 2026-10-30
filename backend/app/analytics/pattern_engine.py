"""
AEGIS AI v2
Pattern Recognition Engine
"""

from __future__ import annotations


class PatternEngine:

    def __init__(self):

        self.patterns = []

    # =====================================================
    # BODY
    # =====================================================

    def body(self, candle):

        return abs(

            candle["close"] - candle["open"]

        )

    # =====================================================
    # UPPER WICK
    # =====================================================

    def upper_wick(self, candle):

        return candle["high"] - max(

            candle["open"],

            candle["close"],

        )

    # =====================================================
    # LOWER WICK
    # =====================================================

    def lower_wick(self, candle):

        return min(

            candle["open"],

            candle["close"],

        ) - candle["low"]

    # =====================================================
    # DOJI
    # =====================================================

    def doji(self, candle):

        return self.body(candle) <= (

            candle["high"] - candle["low"]

        ) * 0.1

    # =====================================================
    # HAMMER
    # =====================================================

    def hammer(self, candle):

        return (

            self.lower_wick(candle)

            > self.body(candle) * 2

            and

            self.upper_wick(candle)

            < self.body(candle)

        )

    # =====================================================
    # SHOOTING STAR
    # =====================================================

    def shooting_star(self, candle):

        return (

            self.upper_wick(candle)

            > self.body(candle) * 2

            and

            self.lower_wick(candle)

            < self.body(candle)

        )

    # =====================================================
    # BULLISH ENGULFING
    # =====================================================

    def bullish_engulfing(

        self,

        previous,

        current,

    ):

        return (

            previous["close"]

            < previous["open"]

            and

            current["close"]

            > current["open"]

            and

            current["close"]

            > previous["open"]

            and

            current["open"]

            < previous["close"]

        )

    # =====================================================
    # BEARISH ENGULFING
    # =====================================================

    def bearish_engulfing(

        self,

        previous,

        current,

    ):

        return (

            previous["close"]

            > previous["open"]

            and

            current["close"]

            < current["open"]

            and

            current["open"]

            > previous["close"]

            and

            current["close"]

            < previous["open"]

        )

    # =====================================================
    # INSIDE BAR
    # =====================================================

    def inside_bar(

        self,

        previous,

        current,

    ):

        return (

            current["high"]

            <= previous["high"]

            and

            current["low"]

            >= previous["low"]

        )

    # =====================================================
    # OUTSIDE BAR
    # =====================================================

    def outside_bar(

        self,

        previous,

        current,

    ):

        return (

            current["high"]

            >= previous["high"]

            and

            current["low"]

            <= previous["low"]

        )

    # =====================================================
    # DETECT
    # =====================================================

    def detect(

        self,

        candles,

    ):

        if len(candles) < 2:

            return []

        current = candles[-1]

        previous = candles[-2]

        found = []

        if self.doji(current):

            found.append("DOJI")

        if self.hammer(current):

            found.append("HAMMER")

        if self.shooting_star(current):

            found.append("SHOOTING_STAR")

        if self.bullish_engulfing(previous, current):

            found.append("BULLISH_ENGULFING")

        if self.bearish_engulfing(previous, current):

            found.append("BEARISH_ENGULFING")

        if self.inside_bar(previous, current):

            found.append("INSIDE_BAR")

        if self.outside_bar(previous, current):

            found.append("OUTSIDE_BAR")

        return found

    # =====================================================
    # SCORE
    # =====================================================

    def confidence(

        self,

        patterns,

    ):

        score = 0

        weights = {

            "HAMMER": 20,

            "SHOOTING_STAR": 20,

            "DOJI": 10,

            "BULLISH_ENGULFING": 30,

            "BEARISH_ENGULFING": 30,

            "INSIDE_BAR": 10,

            "OUTSIDE_BAR": 15,

        }

        for pattern in patterns:

            score += weights.get(

                pattern,

                5,

            )

        return min(

            score,

            100,

        )

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        patterns = self.detect(candles)

        return {

            "patterns": patterns,

            "confidence": self.confidence(patterns),

            "count": len(patterns),

        }