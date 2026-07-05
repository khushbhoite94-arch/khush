"""
AEGIS AI
Live Trading Engine
"""

from app.market.market_stream import MarketStream
from app.market.candle import CandleBuilder
from app.market.history import MarketHistory
from app.market.history_api import HistoryAPI
from app.core.trading_engine import TradingEngine


class LiveEngine:

    def __init__(self, page):

        self.page = page

        self.stream = MarketStream(page)

        self.builder = CandleBuilder()

        self.history = MarketHistory()

        self.api = HistoryAPI()

        self.engine = TradingEngine()

    # ----------------------------------------------------

    def preload(self, symbol="AAPL"):

        print("\n[AEGIS] Downloading history...")

        candles = self.api.load(

            symbol=symbol,

            interval="1m",

            period="5d",

        )

        for candle in candles:

            self.history.add(candle)

        print(f"[AEGIS] Loaded {self.history.count()} candles.")

    # ----------------------------------------------------

    def run(self):

        first_tick = next(self.stream.stream())

        symbol = first_tick["symbol"]

        self.preload(symbol)

        print("\n[AEGIS] Live Engine Started\n")

        while True:

            tick = self.stream.read()

            if tick is None:
                continue

            price = tick["ohlc"]["close"]

            if price is None:
                continue

            candle = self.builder.update(price)

            if candle is None:

                print(
                    f"\rLIVE {symbol} : {price}",
                    end="",
                    flush=True,
                )

                continue

            self.history.add(candle)

            closes = self.history.closes()

            result = self.engine.process(closes)

            print("\n")
            print("=" * 70)
            print("NEW CANDLE")
            print(candle)
            print("History :", self.history.count())
            print(result)
            print("=" * 70)