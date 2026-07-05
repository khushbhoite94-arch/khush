"""
AEGIS AI
Tick Model
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Tick:

    symbol: str

    bid: float

    ask: float

    timestamp: datetime

    @property
    def spread(self):

        return round(self.ask - self.bid, 5)

    @property
    def mid_price(self):

        return round((self.bid + self.ask) / 2, 5)

    def to_dict(self):

        return {

            "symbol": self.symbol,

            "bid": self.bid,

            "ask": self.ask,

            "spread": self.spread,

            "mid_price": self.mid_price,

            "timestamp": self.timestamp.isoformat(),

        }