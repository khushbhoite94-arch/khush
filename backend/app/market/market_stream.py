"""
AEGIS AI
Market Stream
"""

import time
from app.automation.chart_reader import ChartReader


class MarketStream:

    def __init__(self, page):

        self.reader = ChartReader(page)

    def read(self):

        return {
            "symbol": self.reader.symbol(),
            "timeframe": self.reader.timeframe(),
            "ohlc": self.reader.ohlc(),
            "bid": self.reader.bid(),
            "ask": self.reader.ask(),
        }

    def stream(self, interval=1):

        while True:

            yield self.read()

            time.sleep(interval)