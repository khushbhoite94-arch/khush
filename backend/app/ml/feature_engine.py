"""
AEGIS AI v2
Feature Engine

Converts candles into ML-ready features.
"""

from __future__ import annotations

import statistics


class FeatureEngine:

    def __init__(self):

        self.window = 20

    # --------------------------------------------------

    def build(self, candles):

        if len(candles) < self.window:

            return None

        closes = [c["close"] for c in candles[-self.window:]]

        highs = [c["high"] for c in candles[-self.window:]]

        lows = [c["low"] for c in candles[-self.window:]]

        opens = [c["open"] for c in candles[-self.window:]]

        return {

            "close": closes[-1],

            "mean": statistics.mean(closes),

            "median": statistics.median(closes),

            "stdev": statistics.stdev(closes),

            "high": max(highs),

            "low": min(lows),

            "range": max(highs) - min(lows),

            "momentum": closes[-1] - closes[0],

            "body": closes[-1] - opens[-1],

            "upper_wick": highs[-1] - max(opens[-1], closes[-1]),

            "lower_wick": min(opens[-1], closes[-1]) - lows[-1],

        }

    # --------------------------------------------------

    def normalize(self, features):

        if features is None:

            return None

        normalized = {}

        maximum = max(

            abs(v)

            for v in features.values()

            if isinstance(v, (int, float))

        )

        if maximum == 0:

            maximum = 1

        for k, v in features.items():

            if isinstance(v, (int, float)):

                normalized[k] = round(v / maximum, 6)

            else:

                normalized[k] = v

        return normalized