"""
AEGIS AI v2
Strategy Engine

Collects all strategy signals
and returns the strongest one.
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

    # ----------------------------------------------------

    def calculate(

    self,

    closes,

    candles,

):
        signals = []

        for strategy in self.strategies:

            try:
                
             if isinstance(strategy, (EMACrossover, Pullback)):

                result = strategy.signal(closes)

             else:

                result = strategy.signal(candles)

                if result["signal"] != "WAIT":

                    signals.append(result)

            except Exception:

                continue

        if not signals:

            return {

                "signal": "WAIT",

                "confidence": 0,

                "strategy": None,

                "reason": "No strategy generated a signal",

            }

        best = max(

            signals,

            key=lambda x: x["confidence"],

        )

        return best