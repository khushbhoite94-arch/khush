"""
AEGIS AI v2
Professional Candle Builder

Converts live ticks into OHLC candles.

Features
--------
✓ Supports 1m, 3m, 5m, 15m, 30m, 1h...
✓ Auto closes candles
✓ Emits completed candles
✓ Thread-safe
✓ Easy to extend
"""

from __future__ import annotations

from datetime import datetime, timedelta
from threading import Lock


TIMEFRAME_SECONDS = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "4h": 14400,
    "1d": 86400,
}


class CandleBuilder:

    def __init__(self, timeframe="1m"):

        if timeframe not in TIMEFRAME_SECONDS:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        self.timeframe = timeframe
        self.duration = TIMEFRAME_SECONDS[timeframe]

        self.lock = Lock()

        self.current = None

        self.closed = []

    # -----------------------------------------------------

    def _floor_time(self, dt):

        ts = int(dt.timestamp())

        ts -= ts % self.duration

        return datetime.fromtimestamp(ts)

    # -----------------------------------------------------

    def _new_candle(self, dt, price):

        start = self._floor_time(dt)

        return {

            "time": start,

            "open": price,

            "high": price,

            "low": price,

            "close": price,

            "volume": 0,

        }

    # -----------------------------------------------------

    def update(self, price, volume=0, timestamp=None):

        if timestamp is None:

            timestamp = datetime.utcnow()

        with self.lock:

            if self.current is None:

                self.current = self._new_candle(timestamp, price)

                return None

            start = self.current["time"]

            if timestamp >= start + timedelta(seconds=self.duration):

                finished = self.current

                self.closed.append(finished)

                self.current = self._new_candle(timestamp, price)

                return finished

            self.current["close"] = price

            if price > self.current["high"]:

                self.current["high"] = price

            if price < self.current["low"]:

                self.current["low"] = price

            self.current["volume"] += volume

            return None

    # -----------------------------------------------------

    def current_candle(self):

        return self.current

    # -----------------------------------------------------

    def get_closed(self):

        return self.closed

    # -----------------------------------------------------

    def clear(self):

        self.current = None

        self.closed.clear()

    # -----------------------------------------------------

    def total_closed(self):

        return len(self.closed)