"""
AEGIS AI v2
Market Structure Analyzer
"""

from __future__ import annotations


class MarketStructure:

    def __init__(self):

        self.lookback = 3

    # =====================================================
    # SWING HIGHS
    # =====================================================

    def swing_highs(

        self,

        candles,

    ):

        swings = []

        if len(candles) < self.lookback * 2 + 1:

            return swings

        for i in range(

            self.lookback,

            len(candles) - self.lookback,

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

            if current > left and current > right:

                swings.append(

                    {

                        "index": i,

                        "price": current,

                    }

                )

        return swings

    # =====================================================
    # SWING LOWS
    # =====================================================

    def swing_lows(

        self,

        candles,

    ):

        swings = []

        if len(candles) < self.lookback * 2 + 1:

            return swings

        for i in range(

            self.lookback,

            len(candles) - self.lookback,

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

            if current < left and current < right:

                swings.append(

                    {

                        "index": i,

                        "price": current,

                    }

                )

        return swings

    # =====================================================
    # MARKET TREND
    # =====================================================

    def trend(

        self,

        candles,

    ):

        highs = self.swing_highs(candles)

        lows = self.swing_lows(candles)

        if len(highs) < 2 or len(lows) < 2:

            return "UNKNOWN"

        hh = highs[-1]["price"] > highs[-2]["price"]

        hl = lows[-1]["price"] > lows[-2]["price"]

        lh = highs[-1]["price"] < highs[-2]["price"]

        ll = lows[-1]["price"] < lows[-2]["price"]

        if hh and hl:

            return "UPTREND"

        if lh and ll:

            return "DOWNTREND"

        return "RANGE"

    # =====================================================
    # BOS
    # =====================================================

    def bos(

        self,

        candles,

    ):

        highs = self.swing_highs(candles)

        lows = self.swing_lows(candles)

        if len(highs) < 2 or len(lows) < 2:

            return None

        if highs[-1]["price"] > highs[-2]["price"]:

            return "BULLISH"

        if lows[-1]["price"] < lows[-2]["price"]:

            return "BEARISH"

        return None

    # =====================================================
    # CHOCH
    # =====================================================

    def choch(

        self,

        candles,

    ):

        trend = self.trend(candles)

        bos = self.bos(candles)

        if trend == "UPTREND" and bos == "BEARISH":

            return "BEARISH"

        if trend == "DOWNTREND" and bos == "BULLISH":

            return "BULLISH"

        return None

    # =====================================================
    # PREMIUM ZONE
    # =====================================================

    def premium(

        self,

        candles,

    ):

        high = max(

            c["high"]

            for c in candles

        )

        low = min(

            c["low"]

            for c in candles

        )

        return low + ((high - low) * 0.75)

    # =====================================================
    # DISCOUNT ZONE
    # =====================================================

    def discount(

        self,

        candles,

    ):

        high = max(

            c["high"]

            for c in candles

        )

        low = min(

            c["low"]

            for c in candles

        )

        return low + ((high - low) * 0.25)

    # =====================================================
    # MARKET STATE
    # =====================================================

    def state(

        self,

        candles,

    ):

        trend = self.trend(candles)

        close = candles[-1]["close"]

        premium = self.premium(candles)

        discount = self.discount(candles)

        if close >= premium:

            zone = "PREMIUM"

        elif close <= discount:

            zone = "DISCOUNT"

        else:

            zone = "EQUILIBRIUM"

        return {

            "trend": trend,

            "bos": self.bos(candles),

            "choch": self.choch(candles),

            "zone": zone,

            "premium": premium,

            "discount": discount,

        }

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        return {

            "trend": self.trend(candles),

            "highs": self.swing_highs(candles),

            "lows": self.swing_lows(candles),

            "bos": self.bos(candles),

            "choch": self.choch(candles),

            "premium": self.premium(candles),

            "discount": self.discount(candles),

            "state": self.state(candles),

        }