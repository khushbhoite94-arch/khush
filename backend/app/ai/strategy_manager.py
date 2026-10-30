"""
AEGIS AI v3
Dynamic Strategy Manager
"""

from __future__ import annotations

from enum import Enum


class Strategy(Enum):

    SCALPING = "SCALPING"

    TREND = "TREND"

    BREAKOUT = "BREAKOUT"

    MEAN_REVERSION = "MEAN_REVERSION"

    SMART_MONEY = "SMART_MONEY"

    RANGE = "RANGE"

    WAIT = "WAIT"


class StrategyManager:

    def __init__(self):

        self.current_strategy = Strategy.WAIT

    # =====================================================
    # TREND
    # =====================================================

    def trend_strategy(

        self,

        report,

    ):

        market = report.get(

            "market",

            {},

        )

        confidence = report.get(

            "confidence",

            0,

        )

        trend = market.get(

            "trend",

            "WAIT",

        )

        if trend in (

            "UPTREND",

            "DOWNTREND",

        ) and confidence >= 75:

            return Strategy.TREND

        return None

    # =====================================================
    # BREAKOUT
    # =====================================================

    def breakout_strategy(

        self,

        report,

    ):

        flow = report.get(

            "order_flow",

            {},

        )

        liquidity = report.get(

            "liquidity",

            {},

        )

        if (

            flow.get(

                "volume_spike",

                False,

            )

            and liquidity.get(

                "signal",

                "NEUTRAL",

            )

            != "NEUTRAL"

        ):

            return Strategy.BREAKOUT

        return None

    # =====================================================
    # RANGE
    # =====================================================

    def range_strategy(

        self,

        report,

    ):

        market = report.get(

            "market",

            {},

        )

        if market.get(

            "trend",

        ) == "RANGE":

            return Strategy.RANGE

        return None

    # =====================================================
    # SMART MONEY
    # =====================================================

    def smart_money_strategy(

        self,

        report,

    ):

        ob = report.get(

            "order_blocks",

            {},

        )

        fvg = report.get(

            "fair_value_gap",

            {},

        )

        liquidity = report.get(

            "liquidity",

            {},

        )

        signal = ob.get(

            "signal",

            "NEUTRAL",

        )

        if (

            signal != "NEUTRAL"

            and signal == fvg.get(

                "signal",

            )

            and signal == liquidity.get(

                "signal",

            )

        ):

            return Strategy.SMART_MONEY

        return None

    # =====================================================
    # MEAN REVERSION
    # =====================================================

    def mean_reversion(

        self,

        report,

    ):

        vp = report.get(

            "volume_profile",

            {},

        )

        if vp.get(

            "nearest_lvn",

        ) is not None:

            return Strategy.MEAN_REVERSION

        return None

    # =====================================================
    # SCALPING
    # =====================================================

    def scalping(

        self,

        report,

    ):

        flow = report.get(

            "order_flow",

            {},

        )

        imbalance = abs(

            flow.get(

                "imbalance",

                0,

            )

        )

        if imbalance > 0.40:

            return Strategy.SCALPING

        return None

    # =====================================================
    # SELECT STRATEGY
    # =====================================================

    def choose(

        self,

        report,

    ):

        strategies = (

            self.smart_money_strategy,

            self.breakout_strategy,

            self.trend_strategy,

            self.scalping,

            self.mean_reversion,

            self.range_strategy,

        )

        for strategy in strategies:

            result = strategy(

                report,

            )

            if result is not None:

                self.current_strategy = result

                return result

        self.current_strategy = Strategy.WAIT

        return Strategy.WAIT

    # =====================================================
    # PARAMETERS
    # =====================================================

    def parameters(

        self,

        strategy,

    ):

        configs = {

            Strategy.SCALPING: {

                "rr": 1.5,

                "risk": 0.005,

            },

            Strategy.TREND: {

                "rr": 3.0,

                "risk": 0.01,

            },

            Strategy.BREAKOUT: {

                "rr": 2.5,

                "risk": 0.01,

            },

            Strategy.SMART_MONEY: {

                "rr": 4.0,

                "risk": 0.01,

            },

            Strategy.MEAN_REVERSION: {

                "rr": 2.0,

                "risk": 0.0075,

            },

            Strategy.RANGE: {

                "rr": 1.8,

                "risk": 0.005,

            },

            Strategy.WAIT: {

                "rr": 0,

                "risk": 0,

            },

        }

        return configs.get(

            strategy,

            configs[

                Strategy.WAIT

            ],

        )

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        report,

    ):

        strategy = self.choose(

            report,

        )

        return {

            "strategy": strategy.value,

            "parameters": self.parameters(

                strategy,

            ),

        }

    # =====================================================
    # RESET
    # =====================================================

    def reset(

        self,

    ):

        self.current_strategy = Strategy.WAIT

    # =====================================================
    # CURRENT
    # =====================================================

    def current(

        self,

    ):

        return self.current_strategy.value

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(

        self,

    ):

        return {

            "current_strategy": self.current(),

        }