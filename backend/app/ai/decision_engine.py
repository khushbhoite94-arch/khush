"""
AEGIS AI
Decision Engine
"""


class DecisionEngine:

    def decide(
        self,
        strategy_signal,
        rsi,
        macd,
    ):

        # --------------------------------------------------
        # Not enough MACD history yet
        # --------------------------------------------------

        if macd is None:
            return {
                "action": "WAIT",
                "confidence": 0,
                "reason": "MACD unavailable",
            }

        if macd.get("signal") is None:
            return {
                "action": "WAIT",
                "confidence": 0,
                "reason": "Waiting for MACD signal line",
            }

        # --------------------------------------------------
        # BUY
        # --------------------------------------------------

        if strategy_signal == "BUY":

            if rsi < 70 and macd["macd"] > macd["signal"]:

                return {
                    "action": "BUY",
                    "confidence": 90,
                }

        # --------------------------------------------------
        # SELL
        # --------------------------------------------------

        if strategy_signal == "SELL":

            if rsi > 30 and macd["macd"] < macd["signal"]:

                return {
                    "action": "SELL",
                    "confidence": 90,
                }

        # --------------------------------------------------

        return {
            "action": "WAIT",
            "confidence": 25,
            "reason": "Conditions not met",
        }