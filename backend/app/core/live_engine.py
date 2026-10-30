"""
AEGIS AI v2
Live Engine

PART 1 / 6
"""

from __future__ import annotations

import time
from collections import deque

from app.logger.logger import logger

from app.market.market_stream import MarketStream
from app.market.candle_builder import CandleBuilder

from app.market.history_api import HistoryAPI

from app.intelligence.history_server import HistoryServer
from app.intelligence.memory import Memory

from app.core.trading_engine import TradingEngine
from app.core.state import state

from app.config import settings


class LiveEngine:

    # =======================================================
    # INIT
    # =======================================================

    def __init__(

        self,

        page,

    ):

        logger.info("Initializing Live Engine...")

        self.page = page

        self.stream = MarketStream(page)

        self.builder = CandleBuilder(

            settings.market.timeframe

        )

        self.history = HistoryServer()

        self.memory = Memory()

        self.engine = TradingEngine()

        self.running = False

        self.candles = deque(

            maxlen=10000

        )

        self.history_api = HistoryAPI()

        logger.success(

            "Live Engine Initialized"

        )

    # =======================================================
    # LOAD HISTORY
    # =======================================================

    def load_history(self):

        logger.info(

            "Downloading history..."

        )

        candles = self.history_api.load(

            symbol=settings.market.symbol,

            timeframe=settings.market.timeframe,

            limit=settings.market.history,

        )

        if candles is None:

            candles = []

        self.history.load(

            candles

        )

        self.candles.extend(

            candles

        )

        state.set_history(

            candles

        )

        logger.success(

            f"Loaded {len(candles)} candles."

        )

    # =======================================================
    # START
    # =======================================================

    def start(self):

        if self.running:

            return

        self.running = True

        logger.separator()

        logger.success(

            "AEGIS Live Engine Started"

        )

        logger.separator()

        self.load_history()

    # =======================================================
    # STOP
    # =======================================================

    def stop(self):

        self.running = False

        self.stream.stop()

        logger.warning(

            "Live Engine Stopped"

        )
            # =======================================================
    # MAIN LOOP
    # =======================================================

    def run(self):

        self.start()

        logger.info("Waiting for live ticks...")

        for tick in self.stream.stream():

            if not self.running:

                break

            if tick is None:

                continue

            price = tick["ohlc"]["close"]

            logger.info(f"LIVE {tick['symbol']} | {price}")

            candle = self.builder.update(

                price=price,

                volume=tick.get("volume", 0),

                timestamp=tick.get("time"),

            )

            if candle is None:

                continue

            self.on_candle_closed(candle)

        self.stop()

    # =======================================================
    # NEW CANDLE
    # =======================================================

    def on_candle_closed(

        self,

        candle,

    ):

        self.candles.append(candle)

        self.history.append(candle)

        state.append_candle(candle)

        logger.separator()

        logger.success("NEW CANDLE CLOSED")

        print(candle)

        print()

        logger.info(

            f"TOTAL CANDLES : {len(self.candles)}"

        )

        result = self.engine.process(

            list(self.candles)

        )

        state.last_ai = result

        logger.ai(result)

        self.memory.remember(

            {

                "time": candle["time"],

                "close": candle["close"],

                "decision": result,

            }

        )

        self.after_decision(

            result,

            candle,

        )
            # =======================================================
    # AFTER AI DECISION
    # =======================================================

    def after_decision(

        self,

        result,

        candle,

    ):

        if result is None:

            return

        action = result.get(

            "action",

            "WAIT",

        )

        if action == "WAIT":

            return

        confidence = result.get(

            "confidence",

            0,

        )

        minimum = settings.ai.minimum_confidence

        if confidence < minimum:

            logger.warning(

                f"Confidence {confidence}% < {minimum}%"

            )

            return

        if state.position is not None:

            logger.info(

                "Position already open."

            )

            return

        if action == "BUY":

            self.execute_buy(candle)

            return

        if action == "SELL":

            self.execute_sell(candle)

            return

    # =======================================================
    # BUY
    # =======================================================

    def execute_buy(

        self,

        candle,

    ):

        price = candle["close"]

        atr = self.engine.atr.calculate(

            list(self.candles)

        )

        if atr is None:

            atr = 1

        stop_loss = price - (atr * 2)

        take_profit = price + (atr * 4)

        state.position = {

            "side": "BUY",

            "entry": price,

            "sl": stop_loss,

            "tp": take_profit,

        }

        logger.trade(

            "BUY",

            settings.market.symbol,

            price,

            stop_loss,

            take_profit,

        )

    # =======================================================
    # SELL
    # =======================================================

    def execute_sell(

        self,

        candle,

    ):

        price = candle["close"]

        atr = self.engine.atr.calculate(

            list(self.candles)

        )

        if atr is None:

            atr = 1

        stop_loss = price + (atr * 2)

        take_profit = price - (atr * 4)

        state.position = {

            "side": "SELL",

            "entry": price,

            "sl": stop_loss,

            "tp": take_profit,

        }

        logger.trade(

            "SELL",

            settings.market.symbol,

            price,

            stop_loss,

            take_profit,

        )
            # =======================================================
    # POSITION MONITOR
    # =======================================================

    def update_position(self, price):

        position = state.position

        if position is None:

            return

        side = position["side"]

        entry = position["entry"]

        sl = position["sl"]

        tp = position["tp"]

        if side == "BUY":

            pnl = price - entry

        else:

            pnl = entry - price

        state.unrealized_pnl = round(pnl, 6)

        if side == "BUY":

            if price <= sl:

                logger.warning("BUY Stop Loss Hit")

                self.close_position(price, "STOP LOSS")

                return

            if price >= tp:

                logger.success("BUY Take Profit Hit")

                self.close_position(price, "TAKE PROFIT")

                return

        if side == "SELL":

            if price >= sl:

                logger.warning("SELL Stop Loss Hit")

                self.close_position(price, "STOP LOSS")

                return

            if price <= tp:

                logger.success("SELL Take Profit Hit")

                self.close_position(price, "TAKE PROFIT")

                return

    # =======================================================
    # CLOSE POSITION
    # =======================================================

    def close_position(

        self,

        exit_price,

        reason,

    ):

        position = state.position

        if position is None:

            return

        entry = position["entry"]

        side = position["side"]

        if side == "BUY":

            pnl = exit_price - entry

        else:

            pnl = entry - exit_price

        state.balance += pnl

        state.realized_pnl += pnl

        state.unrealized_pnl = 0

        logger.separator()

        logger.success("POSITION CLOSED")

        print()

        print("Reason :", reason)

        print("Side   :", side)

        print("Entry  :", round(entry, 6))

        print("Exit   :", round(exit_price, 6))

        print("PnL    :", round(pnl, 6))

        print("Balance:", round(state.balance, 2))

        print()

        logger.separator()

        self.memory.remember(

            {

                "side": side,

                "entry": entry,

                "exit": exit_price,

                "pnl": pnl,

                "reason": reason,

            }

        )

        state.position = None
            # =======================================================
    # DASHBOARD
    # =======================================================

    def print_status(self):

        logger.separator()

        print("AEGIS LIVE STATUS")

        logger.separator()

        print(f"Symbol            : {settings.market.symbol}")
        print(f"Timeframe         : {settings.market.timeframe}")
        print(f"Candles           : {len(self.candles)}")
        print(f"Balance           : {round(state.balance,2)}")
        print(f"Equity            : {round(state.equity,2)}")
        print(f"Realized PnL      : {round(state.realized_pnl,2)}")
        print(f"Unrealized PnL    : {round(state.unrealized_pnl,2)}")

        if state.position is None:

            print("Position          : NONE")

        else:

            print("Position          :", state.position["side"])
            print("Entry             :", round(state.position["entry"],6))
            print("Stop Loss         :", round(state.position["sl"],6))
            print("Take Profit       :", round(state.position["tp"],6))

        print()

        stats = self.memory.statistics()

        print("Memory")

        for k, v in stats.items():

            print(f"{k:<18}: {v}")

        print()

        logger.separator()

    # =======================================================
    # HEARTBEAT
    # =======================================================

    def heartbeat(self):

        logger.info(

            "Engine Running..."

        )

        logger.info(

            f"Candles : {len(self.candles)}"

        )

        logger.info(

            f"Balance : {round(state.balance,2)}"

        )

        if state.position:

            logger.info(

                f"Open Position : {state.position['side']}"

            )

        else:

            logger.info(

                "Open Position : NONE"

            )

    # =======================================================
    # RESET
    # =======================================================

    def reset(self):

        logger.warning(

            "Resetting Live Engine..."

        )

        self.candles.clear()

        self.memory.clear()

        self.builder.clear()

        self.history.history.clear()

        state.position = None

        state.realized_pnl = 0

        state.unrealized_pnl = 0

        logger.success(

            "Reset Complete"

        )

    # =======================================================
    # SHUTDOWN
    # =======================================================

    def shutdown(self):

        logger.separator()

        logger.warning(

            "Stopping AEGIS..."

        )

        self.stop()

        self.print_status()

        logger.success(

            "Shutdown Complete"

        )

        logger.separator()