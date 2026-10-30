"""
AEGIS AI v2
Institutional Order Flow Engine
"""

from __future__ import annotations

from collections import deque


class OrderFlow:

    def __init__(

        self,

        history=500,

    ):

        self.history = history

        self.delta_history = deque(

            maxlen=history

        )

    # =====================================================
    # BUY VOLUME
    # =====================================================

    def buy_volume(

        self,

        candles,

    ):

        volume = 0

        for candle in candles:

            if candle["close"] > candle["open"]:

                volume += candle.get(

                    "volume",

                    1,

                )

        return volume

    # =====================================================
    # SELL VOLUME
    # =====================================================

    def sell_volume(

        self,

        candles,

    ):

        volume = 0

        for candle in candles:

            if candle["close"] < candle["open"]:

                volume += candle.get(

                    "volume",

                    1,

                )

        return volume

    # =====================================================
    # DELTA
    # =====================================================

    def delta(

        self,

        candles,

    ):

        buy = self.buy_volume(candles)

        sell = self.sell_volume(candles)

        value = buy - sell

        self.delta_history.append(value)

        return value

    # =====================================================
    # CUMULATIVE DELTA
    # =====================================================

    def cumulative_delta(self):

        return sum(

            self.delta_history

        )

    # =====================================================
    # BUY PRESSURE
    # =====================================================

    def buy_pressure(

        self,

        candles,

    ):

        buy = self.buy_volume(candles)

        sell = self.sell_volume(candles)

        total = buy + sell

        if total == 0:

            return 0

        return round(

            buy / total,

            4,

        )

    # =====================================================
    # SELL PRESSURE
    # =====================================================

    def sell_pressure(

        self,

        candles,

    ):

        buy = self.buy_volume(candles)

        sell = self.sell_volume(candles)

        total = buy + sell

        if total == 0:

            return 0

        return round(

            sell / total,

            4,

        )

    # =====================================================
    # IMBALANCE
    # =====================================================

    def imbalance(

        self,

        candles,

    ):

        buy = self.buy_pressure(candles)

        sell = self.sell_pressure(candles)

        return round(

            buy - sell,

            4,

        )

    # =====================================================
    # ABSORPTION
    # =====================================================

    def absorption(

        self,

        candles,

    ):

        if len(candles) < 2:

            return None

        current = candles[-1]

        previous = candles[-2]

        volume = current.get(

            "volume",

            1,

        )

        spread = current["high"] - current["low"]

        if spread == 0:

            return None

        score = volume / spread

        if (

            current["close"] > previous["close"]

            and score > 1000

        ):

            return "BUY_ABSORPTION"

        if (

            current["close"] < previous["close"]

            and score > 1000

        ):

            return "SELL_ABSORPTION"

        return None

    # =====================================================
    # VOLUME SPIKE
    # =====================================================

    def volume_spike(

        self,

        candles,

        multiplier=2,

    ):

        if len(candles) < 20:

            return False

        volumes = [

            c.get(

                "volume",

                1,

            )

            for c in candles[:-1]

        ]

        average = sum(volumes) / len(volumes)

        latest = candles[-1].get(

            "volume",

            1,

        )

        return latest >= average * multiplier

    # =====================================================
    # ORDER FLOW SIGNAL
    # =====================================================

    def signal(

        self,

        candles,

    ):

        imbalance = self.imbalance(candles)

        absorption = self.absorption(candles)

        spike = self.volume_spike(candles)

        if imbalance > 0.20:

            direction = "BUY"

        elif imbalance < -0.20:

            direction = "SELL"

        else:

            direction = "NEUTRAL"

        return {

            "direction": direction,

            "imbalance": imbalance,

            "absorption": absorption,

            "volume_spike": spike,

        }

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        return {

            "buy_volume": self.buy_volume(candles),

            "sell_volume": self.sell_volume(candles),

            "delta": self.delta(candles),

            "cumulative_delta": self.cumulative_delta(),

            "buy_pressure": self.buy_pressure(candles),

            "sell_pressure": self.sell_pressure(candles),

            "imbalance": self.imbalance(candles),

            "absorption": self.absorption(candles),

            "volume_spike": self.volume_spike(candles),

            "signal": self.signal(candles),

        }