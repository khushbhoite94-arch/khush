"""
AEGIS AI v2
Smart Money Concepts (SMC)

Detects:

• BOS
• CHOCH
• Equal Highs
• Equal Lows
• Liquidity Sweep
• Fair Value Gap (FVG)
"""

from __future__ import annotations


class SmartMoney:

    def __init__(self, tolerance=0.00010):

        self.tolerance = tolerance

    # --------------------------------------------------

    def bos(self, candles):

        if len(candles) < 3:
            return False

        return (

            candles[-1]["high"]

            >

            candles[-2]["high"]

        )

    # --------------------------------------------------

    def choch(self, candles):

        if len(candles) < 4:
            return False

        return (

            candles[-1]["low"]

            <

            candles[-2]["low"]

        )

    # --------------------------------------------------

    def equal_highs(self, candles):

        if len(candles) < 2:
            return False

        h1 = candles[-1]["high"]

        h2 = candles[-2]["high"]

        return abs(h1 - h2) <= self.tolerance

    # --------------------------------------------------

    def equal_lows(self, candles):

        if len(candles) < 2:
            return False

        l1 = candles[-1]["low"]

        l2 = candles[-2]["low"]

        return abs(l1 - l2) <= self.tolerance

    # --------------------------------------------------

    def bullish_fvg(self, candles):

        if len(candles) < 3:
            return False

        return (

            candles[-3]["high"]

            <

            candles[-1]["low"]

        )

    # --------------------------------------------------

    def bearish_fvg(self, candles):

        if len(candles) < 3:
            return False

        return (

            candles[-3]["low"]

            >

            candles[-1]["high"]

        )

    # --------------------------------------------------

    def liquidity_sweep(self, candles):

        if len(candles) < 3:
            return None

        if (

            candles[-1]["high"]

            >

            candles[-2]["high"]

            and

            candles[-1]["close"]

            <

            candles[-2]["high"]

        ):

            return "BUY_SIDE"

        if (

            candles[-1]["low"]

            <

            candles[-2]["low"]

            and

            candles[-1]["close"]

            >

            candles[-2]["low"]

        ):

            return "SELL_SIDE"

        return None

    # --------------------------------------------------

    def calculate(self, candles):

        return {

            "bos": self.bos(candles),

            "choch": self.choch(candles),

            "equal_highs": self.equal_highs(candles),

            "equal_lows": self.equal_lows(candles),

            "bullish_fvg": self.bullish_fvg(candles),

            "bearish_fvg": self.bearish_fvg(candles),

            "liquidity": self.liquidity_sweep(candles),

        }