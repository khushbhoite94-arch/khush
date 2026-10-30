"""
AEGIS AI v2
Master Smart Money Engine
"""

from __future__ import annotations

from app.analytics.market_structure import MarketStructure
from app.analytics.support_resistence import SupportResistance
from app.analytics.volume_profile import VolumeProfile
from app.analytics.order_flow import OrderFlow
from app.analytics.liquidity import Liquidity
from app.analytics.order_blocks import OrderBlocks
from app.analytics.fair_value_gap import FairValueGap
from app.analytics.pattern_engine import PatternEngine


class SmartMoneyEngine:

    def __init__(self):

        self.market = MarketStructure()

        self.sr = SupportResistance()

        self.volume = VolumeProfile()

        self.orderflow = OrderFlow()

        self.liquidity = Liquidity()

        self.orderblocks = OrderBlocks()

        self.fvg = FairValueGap()

        self.patterns = PatternEngine()

    # =====================================================
    # MARKET STRUCTURE
    # =====================================================

    def market_structure(

        self,

        candles,

    ):

        return self.market.analyze(

            candles

        )

    # =====================================================
    # SUPPORT / RESISTANCE
    # =====================================================

    def support_resistance(

        self,

        candles,

    ):

        return self.sr.analyze(

            candles

        )

    # =====================================================
    # ORDER FLOW
    # =====================================================

    def order_flow(

        self,

        candles,

    ):

        return self.orderflow.analyze(

            candles

        )

    # =====================================================
    # LIQUIDITY
    # =====================================================

    def liquidity_analysis(

        self,

        candles,

    ):

        return self.liquidity.analyze(

            candles

        )

    # =====================================================
    # ORDER BLOCKS
    # =====================================================

    def order_block_analysis(

        self,

        candles,

    ):

        return self.orderblocks.analyze(

            candles

        )

    # =====================================================
    # FAIR VALUE GAP
    # =====================================================

    def fvg_analysis(

        self,

        candles,

    ):

        return self.fvg.analyze(

            candles

        )

    # =====================================================
    # VOLUME PROFILE
    # =====================================================

    def volume_profile(

        self,

        candles,

    ):

        return self.volume.analyze(

            candles

        )

    # =====================================================
    # PATTERNS
    # =====================================================

    def pattern_analysis(

        self,

        candles,

    ):

        return self.patterns.analyze(

            candles

        )

    # =====================================================
    # CONFIDENCE SCORE
    # =====================================================

    def confidence(

        self,

        report,

    ):

        score = 0

        market = report["market"]

        liquidity = report["liquidity"]

        blocks = report["order_blocks"]

        fvg = report["fair_value_gap"]

        patterns = report["patterns"]

        flow = report["order_flow"]

        if market["trend"] == "UPTREND":

            score += 10

        elif market["trend"] == "DOWNTREND":

            score += 10

        if market["bos"] is not None:

            score += 15

        if market["choch"] is not None:

            score += 15

        if liquidity["signal"] != "NEUTRAL":

            score += 10

        if blocks["signal"] != "NEUTRAL":

            score += 15

        if fvg["signal"] != "NEUTRAL":

            score += 10

        score += min(

            patterns["confidence"],

            20,

        )

        if abs(

            flow["imbalance"]

        ) > 0.25:

            score += 5

        return min(

            score,

            100,

        )

    # =====================================================
    # TRADE DIRECTION
    # =====================================================

    def direction(

        self,

        report,

    ):

        buy = 0

        sell = 0

        modules = [

            report["liquidity"]["signal"],

            report["order_blocks"]["signal"],

            report["fair_value_gap"]["signal"],

            report["order_flow"]["signal"]["direction"],

        ]

        for signal in modules:

            if signal == "BUY":

                buy += 1

            elif signal == "SELL":

                sell += 1

        if buy > sell:

            return "BUY"

        if sell > buy:

            return "SELL"

        return "WAIT"

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        report = {

            "market": self.market_structure(

                candles

            ),

            "support_resistance": self.support_resistance(

                candles

            ),

            "volume_profile": self.volume_profile(

                candles

            ),

            "order_flow": self.order_flow(

                candles

            ),

            "liquidity": self.liquidity_analysis(

                candles

            ),

            "order_blocks": self.order_block_analysis(

                candles

            ),

            "fair_value_gap": self.fvg_analysis(

                candles

            ),

            "patterns": self.pattern_analysis(

                candles

            ),

        }

        report["direction"] = self.direction(

            report

        )

        report["confidence"] = self.confidence(

            report

        )

        return report

    # =====================================================
    # READY TO TRADE
    # =====================================================

    def tradable(

        self,

        candles,

        minimum=70,

    ):

        report = self.analyze(

            candles

        )

        return (

            report["confidence"] >= minimum,

            report,

        )