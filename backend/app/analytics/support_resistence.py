"""
AEGIS AI v2
Support & Resistance Engine
"""

from __future__ import annotations

from statistics import mean


class SupportResistance:

    def __init__(

        self,

        lookback=3,

        merge_distance=0.002,

    ):

        self.lookback = lookback

        self.merge_distance = merge_distance

    # =====================================================
    # SWING HIGHS
    # =====================================================

    def swing_highs(

        self,

        candles,

    ):

        levels = []

        n = len(candles)

        if n < self.lookback * 2 + 1:

            return levels

        for i in range(

            self.lookback,

            n - self.lookback,

        ):

            current = candles[i]["high"]

            left = max(

                c["high"]

                for c in candles[

                    i - self.lookback:i

                ]

            )

            right = max(

                c["high"]

                for c in candles[

                    i + 1:i + self.lookback + 1

                ]

            )

            if current >= left and current >= right:

                levels.append(current)

        return levels

    # =====================================================
    # SWING LOWS
    # =====================================================

    def swing_lows(

        self,

        candles,

    ):

        levels = []

        n = len(candles)

        if n < self.lookback * 2 + 1:

            return levels

        for i in range(

            self.lookback,

            n - self.lookback,

        ):

            current = candles[i]["low"]

            left = min(

                c["low"]

                for c in candles[

                    i - self.lookback:i

                ]

            )

            right = min(

                c["low"]

                for c in candles[

                    i + 1:i + self.lookback + 1

                ]

            )

            if current <= left and current <= right:

                levels.append(current)

        return levels

    # =====================================================
    # MERGE LEVELS
    # =====================================================

    def merge(

        self,

        levels,

    ):

        if not levels:

            return []

        levels = sorted(levels)

        merged = [[levels[0]]]

        for value in levels[1:]:

            previous = mean(

                merged[-1]

            )

            if abs(value - previous) <= (

                previous * self.merge_distance

            ):

                merged[-1].append(value)

            else:

                merged.append([value])

        return [

            round(mean(group), 6)

            for group in merged

        ]

    # =====================================================
    # SUPPORT
    # =====================================================

    def supports(

        self,

        candles,

    ):

        return self.merge(

            self.swing_lows(candles)

        )

    # =====================================================
    # RESISTANCE
    # =====================================================

    def resistances(

        self,

        candles,

    ):

        return self.merge(

            self.swing_highs(candles)

        )

    # =====================================================
    # NEAREST SUPPORT
    # =====================================================

    def nearest_support(

        self,

        candles,

    ):

        close = candles[-1]["close"]

        supports = [

            s

            for s in self.supports(candles)

            if s <= close

        ]

        if not supports:

            return None

        return max(supports)

    # =====================================================
    # NEAREST RESISTANCE
    # =====================================================

    def nearest_resistance(

        self,

        candles,

    ):

        close = candles[-1]["close"]

        resistances = [

            r

            for r in self.resistances(candles)

            if r >= close

        ]

        if not resistances:

            return None

        return min(resistances)

    # =====================================================
    # LEVEL STRENGTH
    # =====================================================

    def strength(

        self,

        candles,

        level,

        tolerance=0.001,

    ):

        touches = 0

        for candle in candles:

            if abs(

                candle["high"] - level

            ) <= level * tolerance:

                touches += 1

                continue

            if abs(

                candle["low"] - level

            ) <= level * tolerance:

                touches += 1

        return touches

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        support = self.nearest_support(candles)

        resistance = self.nearest_resistance(candles)

        return {

            "supports": self.supports(candles),

            "resistances": self.resistances(candles),

            "nearest_support": support,

            "nearest_resistance": resistance,

            "support_strength": self.strength(

                candles,

                support,

            ) if support else 0,

            "resistance_strength": self.strength(

                candles,

                resistance,

            ) if resistance else 0,

        }