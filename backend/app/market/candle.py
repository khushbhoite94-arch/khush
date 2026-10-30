"""
AEGIS AI
Candle Model
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Candle:

    symbol: str

    timeframe: str

    timestamp: datetime

    open: float

    high: float

    low: float

    close: float

    volume: float = 0.0

    @property
    def body(self):

        return abs(self.close - self.open)

    @property
    def bullish(self):

        return self.close > self.open

    @property
    def bearish(self):

        return self.close < self.open

    @property
    def range(self):

        return self.high - self.low

    def to_dict(self):

        return {

            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "timestamp": self.timestamp.isoformat(),

            "open": self.open,

            "high": self.high,

            "low": self.low,

            "close": self.close,

            "volume": self.volume,

        }