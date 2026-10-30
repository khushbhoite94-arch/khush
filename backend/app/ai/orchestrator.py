"""
AEGIS AI v3
AI Orchestrator
"""

from app.ai.ai_engine import AIEngine


class AIOrchestrator:

    def __init__(

        self,

        balance=10000,

    ):

        self.engine = AIEngine(

            account_balance=balance,

        )

    # -----------------------------------------------------

    def process(

        self,

        candles,

    ):

        return self.engine.process(

            candles,

        )

    # -----------------------------------------------------

    def predict(

        self,

        candles,

    ):

        return self.engine.predict(

            candles,

        )

    # -----------------------------------------------------

    def paper_trade(

        self,

        candles,

    ):

        return self.engine.paper_trade(

            candles,

        )

    # -----------------------------------------------------

    def live_trade(

        self,

        candles,

        executor,

    ):

        return self.engine.live_trade(

            candles,

            executor,

        )

    # -----------------------------------------------------

    def summary(

        self,

    ):

        return self.engine.summary()

    # -----------------------------------------------------

    def reset(

        self,

    ):

        self.engine.reset()