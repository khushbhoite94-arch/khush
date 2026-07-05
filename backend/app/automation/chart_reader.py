"""
AEGIS AI
TradingView Chart Reader
"""

import re


class ChartReader:

    def __init__(self, page):

        self.page = page

    # ---------------------------------------------------------

    def _frame(self):

        for frame in self.page.frames:

            if frame.url.startswith("blob:"):
                return frame

        return None

    # ---------------------------------------------------------

    def text(self):

        frame = self._frame()

        if frame is None:
            return ""

        try:

            return frame.locator("body").inner_text(timeout=3000)

        except Exception:

            return ""

    # ---------------------------------------------------------

    def _number(self, label):

        txt = self.text()

        if not txt:
            return None

        pattern = rf"{label}\s*([0-9,]+(?:\.\d+)?)"

        m = re.search(pattern, txt)

        if not m:
            return None

        try:
            return float(m.group(1).replace(",", ""))
        except Exception:
            return None

    # ---------------------------------------------------------

    def symbol(self):

        txt = self.text()

        m = re.search(r"\b([A-Z]{3,10}(?:USD|USDT|EUR|JPY|GBP|BTC|ETH)?)\b", txt)

        if m:
            return m.group(1)

        return "UNKNOWN"

    # ---------------------------------------------------------

    def timeframe(self):

        txt = self.text()

        m = re.search(r"\b(1s|5s|15s|30s|1m|3m|5m|15m|30m|45m|1h|2h|4h|1D|1W|1M)\b", txt)

        if m:
            return m.group(1)

        return None

    # ---------------------------------------------------------

    def ohlc(self):

        return {

            "open": self._number("O"),

            "high": self._number("H"),

            "low": self._number("L"),

            "close": self._number("C"),

        }

    # ---------------------------------------------------------

    def bid(self):

        txt = self.text()

        m = re.search(
            r"SELL\s*([0-9,]+(?:\.\d+)?)",
            txt,
            re.IGNORECASE,
        )

        if m:

            return float(m.group(1).replace(",", ""))

        return None

    # ---------------------------------------------------------

    def ask(self):

        txt = self.text()

        m = re.search(
            r"BUY\s*([0-9,]+(?:\.\d+)?)",
            txt,
            re.IGNORECASE,
        )

        if m:

            return float(m.group(1).replace(",", ""))

        return None