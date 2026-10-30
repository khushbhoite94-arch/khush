"""
AEGIS AI v2
Candlestick Pattern Recognition
"""

from __future__ import annotations


class Candlestick:

    # --------------------------------------------------

    def doji(self, candle):

        body = abs(candle["close"] - candle["open"])

        rng = candle["high"] - candle["low"]

        if rng == 0:

            return False

        return body <= rng * 0.10

    # --------------------------------------------------

    def hammer(self, candle):

        body = abs(candle["close"] - candle["open"])

        lower = min(candle["open"], candle["close"]) - candle["low"]

        upper = candle["high"] - max(candle["open"], candle["close"])

        return (

            lower > body * 2

            and

            upper < body

        )

    # --------------------------------------------------

    def shooting_star(self, candle):

        body = abs(candle["close"] - candle["open"])

        upper = candle["high"] - max(candle["open"], candle["close"])

        lower = min(candle["open"], candle["close"]) - candle["low"]

        return (

            upper > body * 2

            and

            lower < body

        )

    # --------------------------------------------------

    def bullish_engulfing(

        self,

        previous,

        current,

    ):

        return (

            previous["close"] < previous["open"]

            and

            current["close"] > current["open"]

            and

            current["open"] < previous["close"]

            and

            current["close"] > previous["open"]

        )

    # --------------------------------------------------

    def bearish_engulfing(

        self,

        previous,

        current,

    ):

        return (

            previous["close"] > previous["open"]

            and

            current["close"] < current["open"]

            and

            current["open"] > previous["close"]

            and

            current["close"] < previous["open"]

        )

    # --------------------------------------------------

    def marubozu(self, candle):

        body = abs(candle["close"] - candle["open"])

        rng = candle["high"] - candle["low"]

        if rng == 0:

            return False

        return body >= rng * 0.90

    # --------------------------------------------------

    def detect(

        self,

        candles,

    ):

        if len(candles) < 2:

            return None

        previous = candles[-2]

        current = candles[-1]

        if self.bullish_engulfing(previous, current):

            return "BULLISH_ENGULFING"

        if self.bearish_engulfing(previous, current):

            return "BEARISH_ENGULFING"

        if self.hammer(current):

            return "HAMMER"

        if self.shooting_star(current):

            return "SHOOTING_STAR"

        if self.doji(current):

            return "DOJI"

        if self.marubozu(current):

            return "MARUBOZU"

        return "NONE"