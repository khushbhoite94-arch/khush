"""
AEGIS AI v3
Decision Object
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Decision:

    action: str = "WAIT"

    confidence: float = 0.0

    strategy: str = "WAIT"

    entry: Optional[float] = None

    stop_loss: Optional[float] = None

    take_profit: Optional[float] = None

    risk_reward: Optional[float] = None

    reason: str = ""

    def trade(self):

        if self.action == "WAIT":

            return None

        return {

            "direction": self.action,

            "entry": self.entry,

            "stop_loss": self.stop_loss,

            "take_profit": self.take_profit,

            "risk_reward": self.risk_reward,

        }

    def summary(self):

        return {

            "action": self.action,

            "confidence": self.confidence,

            "strategy": self.strategy,

            "reason": self.reason,

        }