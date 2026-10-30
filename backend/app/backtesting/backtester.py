"""
AEGIS AI v2
Backtesting Engine
"""

from __future__ import annotations

from app.backtesting.performance import Performance


class Backtester:

    def __init__(

        self,

        engine,

    ):

        self.engine = engine

        self.performance = Performance()

    # --------------------------------------------------

    def run(

        self,

        candles,

    ):

        closes = []

        print()

        print("=" * 70)

        print("AEGIS BACKTEST")

        print("=" * 70)

        print()

        for candle in candles:

            closes.append(

                candle["close"]

            )

            result = self.engine.process(

                closes

            )

            if result is None:

                continue

            if result["action"] == "WAIT":

                continue

            trade = {

                "action": result["action"],

                "price": candle["close"],

                "pnl": 0,

            }

            next_close = candle["close"]

            if len(closes) >= 2:

                previous = closes[-2]

                if result["action"] == "BUY":

                    trade["pnl"] = next_close - previous

                else:

                    trade["pnl"] = previous - next_close

            self.performance.add_trade(

                trade

            )

        print()

        print("=" * 70)

        print("BACKTEST COMPLETE")

        print("=" * 70)

        print()

        report = self.performance.report()

        for k, v in report.items():

            print(f"{k:<20}{v}")

        print()

        return report