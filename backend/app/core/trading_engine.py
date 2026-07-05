"""
AEGIS AI
Trading Engine
"""

from app.strategy.ema_crossover import EMACrossover
from app.indicators.rsi import RSI
from app.indicators.macd import MACD
from app.ai.decision_engine import DecisionEngine


class TradingEngine:

    def __init__(self):

        self.strategy = EMACrossover()
        self.rsi = RSI()
        self.macd = MACD()
        self.ai = DecisionEngine()

    def process(self, closes):

        # Remove invalid values
        closes = [c for c in closes if c is not None]

        if len(closes) < 35:

            return {
                "action": "WAIT",
                "reason": f"Need more candles ({len(closes)}/35)"
            }

        signal = self.strategy.signal(closes)

        rsi_value = self.rsi.calculate(closes)

        macd_value = self.macd.calculate(closes)

        if rsi_value is None or macd_value is None:

            return {
                "action": "WAIT",
                "reason": "Indicators not ready"
            }

        decision = self.ai.decide(
            signal,
            rsi_value,
            macd_value,
        )

        return {
            "signal": signal,
            "rsi": rsi_value,
            "macd": macd_value,
            "decision": decision,
        }