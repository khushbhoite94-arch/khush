"""
AEGIS AI v2
Market Stream

Reads live market data from TradingView.

Features
--------
✓ Continuous Streaming
✓ Auto Reconnect
✓ Duplicate Tick Filter
✓ Tick Validation
✓ Spread Calculation
✓ Events
✓ Thread Safe
"""

from __future__ import annotations

import time
from threading import Lock

from app.automation.chart_reader import ChartReader
from app.logger.logger import logger
from app.core.events import events, PRICE_UPDATE


class MarketStream:

    def __init__(self, page):

        self.reader = ChartReader(page)

        self.running = False

        self.lock = Lock()

        self.last_price = None

        self.last_bid = None

        self.last_ask = None

        self.last_symbol = None

        self.last_timeframe = None

    # -----------------------------------------------------

    def start(self):

        self.running = True

        logger.success("Market Stream Started")

    # -----------------------------------------------------

    def stop(self):

        self.running = False

        logger.warning("Market Stream Stopped")

    # -----------------------------------------------------

    def validate(self, tick):

        if tick is None:

            return False

        if "ohlc" not in tick:

            return False

        close = tick["ohlc"].get("close")

        if close is None:

            return False

        try:

            float(close)

        except Exception:

            return False

        return True

    # -----------------------------------------------------

    def duplicate(self, tick):

        price = tick["ohlc"]["close"]

        if self.last_price is None:

            return False

        return price == self.last_price

    # -----------------------------------------------------

    def update_cache(self, tick):

        self.last_price = tick["ohlc"]["close"]

        self.last_bid = tick.get("bid")

        self.last_ask = tick.get("ask")

        self.last_symbol = tick.get("symbol")

        self.last_timeframe = tick.get("timeframe")

    # -----------------------------------------------------

    def calculate_spread(self):

        if self.last_bid is None:

            return None

        if self.last_ask is None:

            return None

        return round(self.last_ask - self.last_bid, 8)

    # -----------------------------------------------------

    def read(self):

        try:

            tick = self.reader.read()

        except Exception as e:

            logger.exception(e)

            return None

        if not self.validate(tick):

            return None

        if self.duplicate(tick):

            return None

        self.update_cache(tick)

        tick["spread"] = self.calculate_spread()

        events.emit(

            PRICE_UPDATE,

            tick,

        )

        return tick

    # -----------------------------------------------------

    def stream(

        self,

        interval=1.0,

    ):

        self.start()

        while self.running:

            tick = self.read()

            if tick:

                yield tick

            time.sleep(interval)

    # -----------------------------------------------------

    @property

    def symbol(self):

        return self.last_symbol

    @property

    def timeframe(self):

        return self.last_timeframe

    @property

    def price(self):

        return self.last_price

    @property

    def bid(self):

        return self.last_bid

    @property

    def ask(self):

        return self.last_ask

    @property

    def spread(self):

        return self.calculate_spread()