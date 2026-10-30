"""
AEGIS AI v2
Liquidity Engine
Institutional Smart Money Concepts
"""

from __future__ import annotations


class Liquidity:

    def __init__(

        self,

        tolerance=0.0005,

    ):

        self.tolerance = tolerance

    # =====================================================
    # EQUAL HIGHS
    # =====================================================

    def equal_highs(

        self,

        candles,

    ):

        result = []

        for i in range(1, len(candles)):

            h1 = candles[i - 1]["high"]

            h2 = candles[i]["high"]

            if abs(h1 - h2) <= h1 * self.tolerance:

                result.append(

                    {

                        "index": i,

                        "price": round(

                            (h1 + h2) / 2,

                            6,

                        ),

                    }

                )

        return result

    # =====================================================
    # EQUAL LOWS
    # =====================================================

    def equal_lows(

        self,

        candles,

    ):

        result = []

        for i in range(1, len(candles)):

            l1 = candles[i - 1]["low"]

            l2 = candles[i]["low"]

            if abs(l1 - l2) <= l1 * self.tolerance:

                result.append(

                    {

                        "index": i,

                        "price": round(

                            (l1 + l2) / 2,

                            6,

                        ),

                    }

                )

        return result

    # =====================================================
    # BUY SIDE LIQUIDITY
    # =====================================================

    def buy_side(

        self,

        candles,

    ):

        highs = self.equal_highs(candles)

        if highs:

            return highs[-1]

        return None

    # =====================================================
    # SELL SIDE LIQUIDITY
    # =====================================================

    def sell_side(

        self,

        candles,

    ):

        lows = self.equal_lows(candles)

        if lows:

            return lows[-1]

        return None

    # =====================================================
    # BUY SIDE SWEEP
    # =====================================================

    def buy_sweep(

        self,

        candles,

    ):

        if len(candles) < 2:

            return False

        level = self.buy_side(candles[:-1])

        if level is None:

            return False

        last = candles[-1]

        return (

            last["high"] > level["price"]

            and

            last["close"] < level["price"]

        )

    # =====================================================
    # SELL SIDE SWEEP
    # =====================================================

    def sell_sweep(

        self,

        candles,

    ):

        if len(candles) < 2:

            return False

        level = self.sell_side(candles[:-1])

        if level is None:

            return False

        last = candles[-1]

        return (

            last["low"] < level["price"]

            and

            last["close"] > level["price"]

        )

    # =====================================================
    # LIQUIDITY VOID
    # =====================================================

    def liquidity_void(

        self,

        candles,

    ):

        if len(candles) < 2:

            return None

        previous = candles[-2]

        current = candles[-1]

        gap = abs(

            current["open"]

            - previous["close"]

        )

        atr = (

            previous["high"]

            - previous["low"]

        )

        if atr == 0:

            return None

        if gap > atr * 1.5:

            return {

                "gap": gap,

                "direction":

                    "UP"

                    if current["open"] >

                    previous["close"]

                    else "DOWN",

            }

        return None

    # =====================================================
    # INDUCEMENT
    # =====================================================

    def inducement(

        self,

        candles,

    ):

        if len(candles) < 5:

            return None

        closes = [

            c["close"]

            for c in candles[-5:]

        ]

        if closes[-1] > max(closes[:-1]):

            return "BULLISH"

        if closes[-1] < min(closes[:-1]):

            return "BEARISH"

        return None

    # =====================================================
    # LIQUIDITY ZONES
    # =====================================================

    def zones(

        self,

        candles,

    ):

        return {

            "buy_side":

                self.buy_side(candles),

            "sell_side":

                self.sell_side(candles),

            "buy_sweep":

                self.buy_sweep(candles),

            "sell_sweep":

                self.sell_sweep(candles),

            "void":

                self.liquidity_void(candles),

            "inducement":

                self.inducement(candles),

        }

    # =====================================================
    # SIGNAL
    # =====================================================

    def signal(

        self,

        candles,

    ):

        if self.buy_sweep(candles):

            return "SELL"

        if self.sell_sweep(candles):

            return "BUY"

        return "NEUTRAL"

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        return {

            "equal_highs":

                self.equal_highs(candles),

            "equal_lows":

                self.equal_lows(candles),

            "zones":

                self.zones(candles),

            "signal":

                self.signal(candles),

        }