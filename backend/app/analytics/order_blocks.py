"""
AEGIS AI v2
Order Block Engine
Institutional Smart Money Concepts
"""

from __future__ import annotations


class OrderBlocks:

    def __init__(

        self,

        impulse_multiplier=2.0,

    ):

        self.impulse_multiplier = impulse_multiplier

    # =====================================================
    # BODY
    # =====================================================

    def body(

        self,

        candle,

    ):

        return abs(

            candle["close"]

            - candle["open"]

        )

    # =====================================================
    # RANGE
    # =====================================================

    def candle_range(

        self,

        candle,

    ):

        return (

            candle["high"]

            - candle["low"]

        )

    # =====================================================
    # IMPULSE
    # =====================================================

    def impulse(

        self,

        candles,

        index,

    ):

        if index >= len(candles):

            return False

        candle = candles[index]

        body = self.body(candle)

        rng = self.candle_range(candle)

        if rng == 0:

            return False

        return (

            body / rng

        ) >= 0.70

    # =====================================================
    # BULLISH ORDER BLOCKS
    # =====================================================

    def bullish(

        self,

        candles,

    ):

        blocks = []

        for i in range(

            1,

            len(candles),

        ):

            previous = candles[i - 1]

            current = candles[i]

            if (

                previous["close"]

                < previous["open"]

                and

                current["close"]

                > current["open"]

                and

                self.impulse(candles, i)

            ):

                blocks.append(

                    {

                        "index": i - 1,

                        "high": previous["high"],

                        "low": previous["low"],

                        "type": "BULLISH",

                    }

                )

        return blocks

    # =====================================================
    # BEARISH ORDER BLOCKS
    # =====================================================

    def bearish(

        self,

        candles,

    ):

        blocks = []

        for i in range(

            1,

            len(candles),

        ):

            previous = candles[i - 1]

            current = candles[i]

            if (

                previous["close"]

                > previous["open"]

                and

                current["close"]

                < current["open"]

                and

                self.impulse(candles, i)

            ):

                blocks.append(

                    {

                        "index": i - 1,

                        "high": previous["high"],

                        "low": previous["low"],

                        "type": "BEARISH",

                    }

                )

        return blocks

    # =====================================================
    # BREAKER BLOCKS
    # =====================================================

    def breaker(

        self,

        candles,

    ):

        blocks = []

        for block in self.bullish(candles):

            if candles[-1]["close"] < block["low"]:

                blocks.append(

                    {

                        **block,

                        "breaker": True,

                    }

                )

        for block in self.bearish(candles):

            if candles[-1]["close"] > block["high"]:

                blocks.append(

                    {

                        **block,

                        "breaker": True,

                    }

                )

        return blocks

    # =====================================================
    # MITIGATION
    # =====================================================

    def mitigated(

        self,

        candles,

    ):

        mitigated = []

        for block in (

            self.bullish(candles)

            +

            self.bearish(candles)

        ):

            for candle in candles[

                block["index"] + 1:

            ]:

                if (

                    candle["low"]

                    <= block["high"]

                    and

                    candle["high"]

                    >= block["low"]

                ):

                    mitigated.append(block)

                    break

        return mitigated

    # =====================================================
    # ACTIVE BLOCKS
    # =====================================================

    def active(

        self,

        candles,

    ):

        mitigated = self.mitigated(candles)

        mitigated_index = {

            b["index"]

            for b in mitigated

        }

        active = []

        for block in (

            self.bullish(candles)

            +

            self.bearish(candles)

        ):

            if block["index"] not in mitigated_index:

                active.append(block)

        return active

    # =====================================================
    # NEAREST BLOCK
    # =====================================================

    def nearest(

        self,

        candles,

    ):

        close = candles[-1]["close"]

        active = self.active(candles)

        if not active:

            return None

        return min(

            active,

            key=lambda b:

            min(

                abs(close - b["high"]),

                abs(close - b["low"]),

            ),

        )

    # =====================================================
    # SIGNAL
    # =====================================================

    def signal(

        self,

        candles,

    ):

        block = self.nearest(candles)

        if block is None:

            return "NEUTRAL"

        if block["type"] == "BULLISH":

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

            "breaker":

                self.breaker(candles),

            "mitigated":

                self.mitigated(candles),

            "active":

                self.active(candles),

            "nearest":

                self.nearest(candles),

            "signal":

                self.signal(candles),

        }