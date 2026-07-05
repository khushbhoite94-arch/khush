"""
AEGIS AI
Main Trading Bot
"""

import time

from app.market.market_stream import MarketStream
from app.market.history import MarketHistory
from app.core.trading_engine import TradingEngine
from app.execution.paper_executor import PaperExecutor
from app.risk.risk_manager import RiskManager


class TradingBot:

    def __init__(self, page):

        self.stream = MarketStream(page)

        self.history = MarketHistory()

        self.engine = TradingEngine()

        self.paper = PaperExecutor()

        self.risk = RiskManager()

    # --------------------------------------------------

    def run(self):

        while True:

            tick = self.stream.read()

            self.history.add(tick)

            closes = self.history.closes()

            if len(closes) < 35:

                print(f"Collecting candles... {len(closes)}/35")

                time.sleep(1)

                continue

            result = self.engine.process(closes)

            print()

            print("=" * 70)

            print(result)

            decision = result["decision"]["action"]

            if decision == "BUY":

                lot = self.risk.calculate_lot(

                    balance=self.paper.balance,

                    stop_loss_points=100,

                    pip_value=10,

                )

                trade = self.paper.buy(

                    symbol=tick["symbol"],

                    lot=lot,

                    entry=tick["ohlc"]["close"],

                    sl=tick["ohlc"]["close"] - 100,

                    tp=tick["ohlc"]["close"] + 200,

                )

                print()

                print("BUY EXECUTED")

                print(trade)

            elif decision == "SELL":

                lot = self.risk.calculate_lot(

                    balance=self.paper.balance,

                    stop_loss_points=100,

                    pip_value=10,

                )

                trade = self.paper.sell(

                    symbol=tick["symbol"],

                    lot=lot,

                    entry=tick["ohlc"]["close"],

                    sl=tick["ohlc"]["close"] + 100,

                    tp=tick["ohlc"]["close"] - 200,

                )

                print()

                print("SELL EXECUTED")

                print(trade)

            time.sleep(1)