"""
AEGIS AI V3
Central Trading Engine
"""

from app.ai.ai_engine import AIEngine


class TradingEngine:

    def __init__(self):

        self.ai = AIEngine()

    # ----------------------------------------------------

    def process(

        self,

        candles,

    ):

        """
        Main trading pipeline.

        Market
            ↓
        AI Engine
            ↓
        Trade Decision
        """

        if candles is None:

            return {

                "status": "ERROR",

                "reason": "No candle data.",

            }

        if len(candles) < 50:

            return {

                "status": "WAIT",

                "reason": f"Need 50 candles ({len(candles)}/50)",

            }

        return self.ai.process(

            candles,

        )

    # ----------------------------------------------------

    def health(

        self,

    ):

        return self.ai.health()

    # ----------------------------------------------------

    def reset(

        self,

    ):

        self.ai.reset()

    # ----------------------------------------------------

    def summary(

        self,

    ):

        return self.ai.summary()