"""
AEGIS AI v2
Strategy Engine

Collects strategy signals and returns the strongest valid signal.
"""

from __future__ import annotations

from app.strategy.ema_crossover import EMACrossover
from app.strategy.breakout import Breakout
from app.strategy.pullback import Pullback
from app.strategy.range import RangeStrategy
from app.strategy.smart_money import SmartMoney


class StrategyEngine:
    def __init__(self):
        self.strategies = [
            EMACrossover(),
            Breakout(),
            Pullback(),
            RangeStrategy(),
            SmartMoney(),
        ]

    def calculate(self, closes, candles):
        signals = []

        for strategy in self.strategies:
            try:
                if isinstance(strategy, (EMACrossover, Pullback)):
                    result = strategy.signal(closes)
                else:
                    result = strategy.signal(candles)

                # Collect signals from every strategy, not only candle-based ones.
                if not isinstance(result, dict):
                    continue

                if result.get("signal") not in ("BUY", "SELL"):
                    continue

                confidence = result.get("confidence", 0)
                if not isinstance(confidence, (int, float)):
                    continue

                signals.append(result)

            except Exception:
                # A broken strategy must not prevent the remaining strategies
                # from evaluating. WAIT is returned if none can produce a signal.
                continue

        if not signals:
            return {
                "signal": "WAIT",
                "confidence": 0,
                "strategy": None,
                "reason": "No strategy generated a valid signal",
            }

        return max(signals, key=lambda item: item["confidence"])
}
