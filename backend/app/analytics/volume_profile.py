"""
AEGIS AI v2
Volume Profile
"""

from __future__ import annotations

from collections import defaultdict


class VolumeProfile:

    def __init__(

        self,

        bins=50,

        value_area=0.70,

    ):

        self.bins = bins

        self.value_area = value_area

    # =====================================================
    # BUILD PROFILE
    # =====================================================

    def build(

        self,

        candles,

    ):

        if not candles:

            return {}

        high = max(

            c["high"]

            for c in candles

        )

        low = min(

            c["low"]

            for c in candles

        )

        step = (high - low) / self.bins

        if step == 0:

            step = 0.00001

        profile = defaultdict(float)

        for candle in candles:

            price = candle["close"]

            volume = candle.get(

                "volume",

                1,

            )

            bucket = round(

                ((price - low) // step) * step + low,

                6,

            )

            profile[bucket] += volume

        return dict(profile)

    # =====================================================
    # POINT OF CONTROL
    # =====================================================

    def poc(

        self,

        profile,

    ):

        if not profile:

            return None

        return max(

            profile,

            key=profile.get,

        )

    # =====================================================
    # SORT PROFILE
    # =====================================================

    def sorted_profile(

        self,

        profile,

    ):

        return sorted(

            profile.items(),

            key=lambda x: x[1],

            reverse=True,

        )

    # =====================================================
    # VALUE AREA
    # =====================================================

    def value_area_levels(

        self,

        profile,

    ):

        if not profile:

            return None, None

        total = sum(

            profile.values()

        )

        target = total * self.value_area

        running = 0

        selected = []

        for price, volume in self.sorted_profile(profile):

            running += volume

            selected.append(price)

            if running >= target:

                break

        return (

            min(selected),

            max(selected),

        )

    # =====================================================
    # HIGH VOLUME NODES
    # =====================================================

    def hvn(

        self,

        profile,

        limit=5,

    ):

        return [

            p

            for p, _ in self.sorted_profile(profile)[:limit]

        ]

    # =====================================================
    # LOW VOLUME NODES
    # =====================================================

    def lvn(

        self,

        profile,

        limit=5,

    ):

        return [

            p

            for p, _ in sorted(

                profile.items(),

                key=lambda x: x[1],

            )[:limit]

        ]

    # =====================================================
    # NEAREST HVN
    # =====================================================

    def nearest_hvn(

        self,

        candles,

    ):

        profile = self.build(candles)

        nodes = self.hvn(profile)

        if not nodes:

            return None

        close = candles[-1]["close"]

        return min(

            nodes,

            key=lambda x: abs(x - close),

        )

    # =====================================================
    # NEAREST LVN
    # =====================================================

    def nearest_lvn(

        self,

        candles,

    ):

        profile = self.build(candles)

        nodes = self.lvn(profile)

        if not nodes:

            return None

        close = candles[-1]["close"]

        return min(

            nodes,

            key=lambda x: abs(x - close),

        )

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        profile = self.build(candles)

        vah, val = self.value_area_levels(profile)

        return {

            "profile": profile,

            "poc": self.poc(profile),

            "vah": vah,

            "val": val,

            "hvn": self.hvn(profile),

            "lvn": self.lvn(profile),

            "nearest_hvn": self.nearest_hvn(candles),

            "nearest_lvn": self.nearest_lvn(candles),

        }