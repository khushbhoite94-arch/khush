"""
AEGIS AI v2
History Intelligence Server

Provides historical market intelligence.
"""

from __future__ import annotations

from pathlib import Path
import json


class HistoryServer:

    def __init__(self):

        self.history = []

    # ----------------------------------------------------

    def load(self, candles):

        self.history = candles

    # ----------------------------------------------------

    def append(self, candle):

        self.history.append(candle)

    # ----------------------------------------------------

    def last(self, n=100):

        if n <= 0:

            return []

        return self.history[-n:]

    # ----------------------------------------------------

    def average_close(self, n=100):

        candles = self.last(n)

        if not candles:

            return None

        closes = [

            c["close"]

            for c in candles

        ]

        return sum(closes) / len(closes)

    # ----------------------------------------------------

    def highest(self, n=100):

        candles = self.last(n)

        if not candles:

            return None

        return max(

            c["high"]

            for c in candles

        )

    # ----------------------------------------------------

    def lowest(self, n=100):

        candles = self.last(n)

        if not candles:

            return None

        return min(

            c["low"]

            for c in candles

        )

    # ----------------------------------------------------

    def trend(self, n=30):

        candles = self.last(n)

        if len(candles) < 2:

            return "UNKNOWN"

        first = candles[0]["close"]

        last = candles[-1]["close"]

        if last > first:

            return "UP"

        elif last < first:

            return "DOWN"

        return "SIDEWAYS"

    # ----------------------------------------------------

    def statistics(self):

        return {

            "candles": len(self.history),

            "trend": self.trend(),

            "average": self.average_close(),

            "highest": self.highest(),

            "lowest": self.lowest(),

        }

    # ----------------------------------------------------

    def save(self, path):

        with open(path, "w") as f:

            json.dump(

                self.history,

                f,

                default=str,

            )

    # ----------------------------------------------------

    def load_file(self, path):

        p = Path(path)

        if not p.exists():

            return

        with open(path) as f:

            self.history = json.load(f)