"""
AEGIS AI v2
Chart Reader

Part 1/8
"""

from __future__ import annotations

import json
import time

from app.logger.logger import logger


class ChartReader:

    def __init__(self, page):

        self.page = page

        self.last_candle = None

        self.symbol_name = None

        self.timeframe_name = None

    # =====================================================
    # PAGE
    # =====================================================

    def wait_ready(self):

        self.page.wait_for_load_state("networkidle")

        time.sleep(2)

    # =====================================================
    # JAVASCRIPT
    # =====================================================

    def js(self, script):

        return self.page.evaluate(script)

    # =====================================================
    # SYMBOL
    # =====================================================

    def symbol(self):

        if self.symbol_name:

            return self.symbol_name

        selectors = [

            "[data-name='legend-source-title']",

            ".chart-markup-table",

            ".js-chart-title",

        ]

        for selector in selectors:

            try:

                if self.page.locator(selector).count():

                    self.symbol_name = self.page.locator(

                        selector

                    ).inner_text()

                    return self.symbol_name

            except Exception:

                pass

        return None

    # =====================================================
    # TIMEFRAME
    # =====================================================

    def timeframe(self):

        if self.timeframe_name:

            return self.timeframe_name

        selectors = [

            "[data-name='interval-dialog-button']",

            ".interval-dialog-button",

        ]

        for selector in selectors:

            try:

                if self.page.locator(selector).count():

                    self.timeframe_name = self.page.locator(

                        selector

                    ).inner_text()

                    return self.timeframe_name

            except Exception:

                pass

        return None

    # =====================================================
    # PRICE
    # =====================================================

    def last_price(self):

        selectors = [

            "[data-field-key='last']",

            "[data-name='legend-series-last-value']",

            ".last-price",

        ]

        for selector in selectors:

            try:

                if self.page.locator(selector).count():

                    value = self.page.locator(

                        selector

                    ).inner_text()

                    value = value.replace(",", "")

                    value = value.replace("$", "")

                    return float(value)

            except Exception:

                pass

        return None
        # =====================================================
    # OHLC FROM DOM
    # =====================================================

    def ohlc(self):

        selectors = [

            "[data-name='legend-source-item']",

            ".pane-legend",

            ".legend-source-item",

        ]

        for selector in selectors:

            try:

                if not self.page.locator(selector).count():

                    continue

                text = self.page.locator(selector).inner_text()

                numbers = []

                for word in text.replace(",", " ").split():

                    try:

                        numbers.append(float(word))

                    except Exception:

                        pass

                if len(numbers) >= 4:

                    return {

                        "open": numbers[0],

                        "high": numbers[1],

                        "low": numbers[2],

                        "close": numbers[3],

                    }

            except Exception:

                pass

        return None

    # =====================================================
    # OHLC VIA JAVASCRIPT
    # =====================================================

    def js_ohlc(self):

        script = """

        () => {

            const text = document.body.innerText;

            return text;

        }

        """

        try:

            text = self.page.evaluate(script)

        except Exception:

            return None

        values = []

        for token in text.replace(",", " ").split():

            try:

                values.append(float(token))

            except Exception:

                pass

        if len(values) < 4:

            return None

        return {

            "open": values[0],

            "high": values[1],

            "low": values[2],

            "close": values[3],

        }

    # =====================================================
    # BEST OHLC
    # =====================================================

    def candle(self):

        data = self.ohlc()

        if data:

            return data

        return self.js_ohlc()

    # =====================================================
    # CANDLE CHANGED
    # =====================================================

    def candle_changed(self):

        candle = self.candle()

        if candle is None:

            return False

        if self.last_candle is None:

            self.last_candle = candle

            return False

        if candle["close"] != self.last_candle["close"]:

            self.last_candle = candle

            return True

        return False
        # =====================================================
    # LIVE CANDLE STREAM
    # =====================================================

    def stream(

        self,

        interval=0.25,

    ):

        while True:

            try:

                candle = self.candle()

                if candle:

                    yield candle

            except Exception:

                pass

            time.sleep(interval)

    # =====================================================
    # WAIT FOR NEW CANDLE
    # =====================================================

    def wait_new_candle(

        self,

        timeout=120,

    ):

        start = time.time()

        previous = self.candle()

        while time.time() - start < timeout:

            current = self.candle()

            if current is None:

                time.sleep(0.2)

                continue

            if previous is None:

                previous = current

                continue

            if current["close"] != previous["close"]:

                self.last_candle = current

                return current

            time.sleep(0.2)

        return None

    # =====================================================
    # TIMESTAMP
    # =====================================================

    def timestamp(self):

        script = """

        () => {

            return Date.now();

        }

        """

        try:

            return self.page.evaluate(script)

        except Exception:

            return int(time.time() * 1000)

    # =====================================================
    # COMPLETE CANDLE
    # =====================================================

    def current_candle(self):

        candle = self.candle()

        if candle is None:

            return None

        candle["symbol"] = self.symbol()

        candle["timeframe"] = self.timeframe()

        candle["timestamp"] = self.timestamp()

        return candle

    # =====================================================
    # HISTORY BUFFER
    # =====================================================

    def history(

        self,

        count=500,

    ):

        candles = []

        last_close = None

        attempts = 0

        while len(candles) < count and attempts < count * 20:

            attempts += 1

            candle = self.current_candle()

            if candle is None:

                time.sleep(0.1)

                continue

            if last_close != candle["close"]:

                candles.append(candle)

                last_close = candle["close"]

            time.sleep(0.05)

        return candles

    # =====================================================
    # BUFFER STATUS
    # =====================================================

    def buffer_status(

        self,

        candles,

    ):

        return {

            "symbol": self.symbol(),

            "timeframe": self.timeframe(),

            "candles": len(candles),

            "last_close": candles[-1]["close"] if candles else None,

        }
        # =====================================================
    # INDICATOR VALUE
    # =====================================================

    def indicator_value(

        self,

        name,

    ):

        selectors = [

            f"[data-name='{name}']",

            f"[aria-label*='{name}']",

            ".pane-legend",

            ".legend-source-item",

        ]

        for selector in selectors:

            try:

                locator = self.page.locator(selector)

                if locator.count() == 0:

                    continue

                text = locator.first.inner_text()

                tokens = text.replace(",", " ").split()

                values = []

                for token in tokens:

                    try:

                        values.append(float(token))

                    except Exception:

                        pass

                if values:

                    return values[-1]

            except Exception:

                pass

        return None

    # =====================================================
    # EMA
    # =====================================================

    def ema(

        self,

        period=20,

    ):

        return self.indicator_value(

            f"EMA {period}"

        )

    # =====================================================
    # RSI
    # =====================================================

    def rsi(self):

        return self.indicator_value(

            "RSI"

        )

    # =====================================================
    # ATR
    # =====================================================

    def atr(self):

        return self.indicator_value(

            "ATR"

        )

    # =====================================================
    # MACD
    # =====================================================

    def macd(self):

        value = self.indicator_value(

            "MACD"

        )

        if value is None:

            return None

        return {

            "macd": value,

        }

    # =====================================================
    # VOLUME
    # =====================================================

    def volume(self):

        return self.indicator_value(

            "Vol"

        )

    # =====================================================
    # INDICATOR SNAPSHOT
    # =====================================================

    def indicators(self):

        return {

            "ema9": self.ema(9),

            "ema20": self.ema(20),

            "ema50": self.ema(50),

            "rsi": self.rsi(),

            "atr": self.atr(),

            "macd": self.macd(),

            "volume": self.volume(),

        }

    # =====================================================
    # COMPLETE SNAPSHOT
    # =====================================================

    def snapshot(self):

        candle = self.current_candle()

        if candle is None:

            return None

        candle["indicators"] = self.indicators()

        return candle
        # =====================================================
    # JAVASCRIPT SNAPSHOT
    # =====================================================

    def js_snapshot(self):

        script = """
        () => {

            return {

                title: document.title,

                url: location.href,

                timestamp: Date.now(),

                body: document.body.innerText

            };

        }
        """

        try:

            return self.page.evaluate(script)

        except Exception:

            return None

    # =====================================================
    # VIEWPORT SIZE
    # =====================================================

    def viewport(self):

        script = """
        () => {

            return {

                width: window.innerWidth,

                height: window.innerHeight

            };

        }
        """

        try:

            return self.page.evaluate(script)

        except Exception:

            return None

    # =====================================================
    # CHART CANVAS
    # =====================================================

    def chart_canvas(self):

        selectors = [

            "canvas",

            ".chart-gui-wrapper canvas",

            ".chart-container canvas",

        ]

        for selector in selectors:

            try:

                locator = self.page.locator(selector)

                if locator.count():

                    return locator.first

            except Exception:

                pass

        return None

    # =====================================================
    # CHART EXISTS
    # =====================================================

    def chart_loaded(self):

        return self.chart_canvas() is not None

    # =====================================================
    # VISIBLE CANDLES
    # =====================================================

    def visible_candles(self):

        script = """

        () => {

            return document.querySelectorAll("canvas").length;

        }

        """

        try:

            return self.page.evaluate(script)

        except Exception:

            return 0

    # =====================================================
    # CROSSHAIR
    # =====================================================

    def move_crosshair(

        self,

        x,

        y,

    ):

        canvas = self.chart_canvas()

        if canvas is None:

            return

        box = canvas.bounding_box()

        if box is None:

            return

        self.page.mouse.move(

            box["x"] + x,

            box["y"] + y,

        )

    # =====================================================
    # SCAN CHART
    # =====================================================

    def scan_chart(

        self,

        samples=20,

    ):

        canvas = self.chart_canvas()

        if canvas is None:

            return []

        box = canvas.bounding_box()

        if box is None:

            return []

        width = int(box["width"])

        height = int(box["height"])

        result = []

        step = max(

            width // samples,

            1,

        )

        for x in range(10, width - 10, step):

            self.move_crosshair(

                x,

                height // 2,

            )

            self.page.wait_for_timeout(40)

            candle = self.current_candle()

            if candle:

                result.append(candle)

        return result

    # =====================================================
    # SNAPSHOT REPORT
    # =====================================================

    def report(self):

        return {

            "symbol": self.symbol(),

            "timeframe": self.timeframe(),

            "price": self.last_price(),

            "viewport": self.viewport(),

            "chart_loaded": self.chart_loaded(),

            "visible_canvases": self.visible_candles(),

            "snapshot": self.js_snapshot(),

        }
        # =====================================================
    # BUILD HISTORY FROM CHART
    # =====================================================

    def build_chart_history(

        self,

        samples=150,

    ):

        candles = []

        last = None

        scan = self.scan_chart(samples)

        for candle in scan:

            if candle is None:

                continue

            if last is None:

                candles.append(candle)

                last = candle["close"]

                continue

            if candle["close"] != last:

                candles.append(candle)

                last = candle["close"]

        return candles

    # =====================================================
    # HIGH
    # =====================================================

    def highest_high(

        self,

        candles,

    ):

        if not candles:

            return None

        return max(

            candle["high"]

            for candle in candles

        )

    # =====================================================
    # LOW
    # =====================================================

    def lowest_low(

        self,

        candles,

    ):

        if not candles:

            return None

        return min(

            candle["low"]

            for candle in candles

        )

    # =====================================================
    # TREND
    # =====================================================

    def trend(

        self,

        candles,

    ):

        if len(candles) < 10:

            return "UNKNOWN"

        first = candles[0]["close"]

        last = candles[-1]["close"]

        change = ((last - first) / first) * 100

        if change > 0.50:

            return "UPTREND"

        if change < -0.50:

            return "DOWNTREND"

        return "SIDEWAYS"

    # =====================================================
    # SUPPORT
    # =====================================================

    def support(

        self,

        candles,

    ):

        if not candles:

            return None

        lows = sorted(

            [

                candle["low"]

                for candle in candles

            ]

        )

        return lows[0]

    # =====================================================
    # RESISTANCE
    # =====================================================

    def resistance(

        self,

        candles,

    ):

        if not candles:

            return None

        highs = sorted(

            [

                candle["high"]

                for candle in candles

            ],

            reverse=True,

        )

        return highs[0]

    # =====================================================
    # RANGE
    # =====================================================

    def market_range(

        self,

        candles,

    ):

        high = self.highest_high(candles)

        low = self.lowest_low(candles)

        if high is None or low is None:

            return None

        return round(

            high - low,

            6,

        )

    # =====================================================
    # MARKET SUMMARY
    # =====================================================

    def summary(

        self,

        candles,

    ):

        return {

            "symbol": self.symbol(),

            "timeframe": self.timeframe(),

            "trend": self.trend(candles),

            "high": self.highest_high(candles),

            "low": self.lowest_low(candles),

            "support": self.support(candles),

            "resistance": self.resistance(candles),

            "range": self.market_range(candles),

        }
            # =====================================================
    # SWING HIGHS
    # =====================================================

    def swing_highs(

        self,

        candles,

        lookback=2,

    ):

        swings = []

        if len(candles) < (lookback * 2 + 1):

            return swings

        for i in range(lookback, len(candles) - lookback):

            current = candles[i]["high"]

            left = max(

                c["high"]

                for c in candles[i - lookback:i]

            )

            right = max(

                c["high"]

                for c in candles[i + 1:i + lookback + 1]

            )

            if current > left and current > right:

                swings.append(

                    {

                        "index": i,

                        "price": current,

                    }

                )

        return swings

    # =====================================================
    # SWING LOWS
    # =====================================================

    def swing_lows(

        self,

        candles,

        lookback=2,

    ):

        swings = []

        if len(candles) < (lookback * 2 + 1):

            return swings

        for i in range(lookback, len(candles) - lookback):

            current = candles[i]["low"]

            left = min(

                c["low"]

                for c in candles[i - lookback:i]

            )

            right = min(

                c["low"]

                for c in candles[i + 1:i + lookback + 1]

            )

            if current < left and current < right:

                swings.append(

                    {

                        "index": i,

                        "price": current,

                    }

                )

        return swings

    # =====================================================
    # BREAK OF STRUCTURE
    # =====================================================

    def bos(

        self,

        candles,

    ):

        highs = self.swing_highs(candles)

        lows = self.swing_lows(candles)

        if len(highs) < 2 or len(lows) < 2:

            return None

        if highs[-1]["price"] > highs[-2]["price"]:

            return "BULLISH"

        if lows[-1]["price"] < lows[-2]["price"]:

            return "BEARISH"

        return None

    # =====================================================
    # CHANGE OF CHARACTER
    # =====================================================

    def choch(

        self,

        candles,

    ):

        trend = self.trend(candles)

        bos = self.bos(candles)

        if trend == "UPTREND" and bos == "BEARISH":

            return "BEARISH CHOCH"

        if trend == "DOWNTREND" and bos == "BULLISH":

            return "BULLISH CHOCH"

        return None

    # =====================================================
    # LIQUIDITY SWEEP
    # =====================================================

    def liquidity_sweep(

        self,

        candles,

    ):

        if len(candles) < 3:

            return None

        last = candles[-1]

        previous = candles[-2]

        if last["high"] > previous["high"] and last["close"] < previous["high"]:

            return "BUY SIDE"

        if last["low"] < previous["low"] and last["close"] > previous["low"]:

            return "SELL SIDE"

        return None

    # =====================================================
    # FAIR VALUE GAP
    # =====================================================

    def fair_value_gap(

        self,

        candles,

    ):

        if len(candles) < 3:

            return None

        first = candles[-3]

        third = candles[-1]

        if third["low"] > first["high"]:

            return {

                "type": "BULLISH",

                "top": third["low"],

                "bottom": first["high"],

            }

        if third["high"] < first["low"]:

            return {

                "type": "BEARISH",

                "top": first["low"],

                "bottom": third["high"],

            }

        return None
            # =====================================================
    # SMART MONEY SUMMARY
    # =====================================================

    def smart_money_summary(

        self,

        candles,

    ):

        return {

            "trend": self.trend(candles),

            "bos": self.bos(candles),

            "choch": self.choch(candles),

            "liquidity": self.liquidity_sweep(candles),

            "fvg": self.fair_value_gap(candles),

            "support": self.support(candles),

            "resistance": self.resistance(candles),

        }

    # =====================================================
    # AI FEATURES
    # =====================================================

    def ai_features(

        self,

        candles,

    ):

        summary = self.smart_money_summary(candles)

        indicators = self.indicators()

        candle = candles[-1]

        return {

            "symbol": self.symbol(),

            "timeframe": self.timeframe(),

            "open": candle["open"],

            "high": candle["high"],

            "low": candle["low"],

            "close": candle["close"],

            "volume": indicators["volume"],

            "ema9": indicators["ema9"],

            "ema20": indicators["ema20"],

            "ema50": indicators["ema50"],

            "rsi": indicators["rsi"],

            "atr": indicators["atr"],

            "macd": indicators["macd"],

            "trend": summary["trend"],

            "bos": summary["bos"],

            "choch": summary["choch"],

            "liquidity": summary["liquidity"],

            "support": summary["support"],

            "resistance": summary["resistance"],

            "fvg": summary["fvg"],

        }

    # =====================================================
    # EXPORT JSON
    # =====================================================

    def export_json(

        self,

        candles,

        path,

    ):

        data = {

            "market": self.summary(candles),

            "smart_money": self.smart_money_summary(candles),

            "indicators": self.indicators(),

            "features": self.ai_features(candles),

        }

        with open(path, "w") as f:

            json.dump(

                data,

                f,

                indent=4,

            )

        return path

    # =====================================================
    # IMPORT JSON
    # =====================================================

    def import_json(

        self,

        path,

    ):

        with open(path) as f:

            return json.load(f)

    # =====================================================
    # COMPLETE REPORT
    # =====================================================

    def report(

        self,

        candles,

    ):

        return {

            "market": self.summary(candles),

            "smart_money": self.smart_money_summary(candles),

            "indicators": self.indicators(),

            "snapshot": self.snapshot(),

        }

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.last_candle = None

        self.symbol_name = None

        self.timeframe_name = None

    # =====================================================
    # STRING
    # =====================================================

    def __repr__(self):

        return (

            f"<ChartReader "

            f"symbol={self.symbol()} "

            f"timeframe={self.timeframe()}>"

        )