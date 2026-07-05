"""
AEGIS AI
History Loader
"""

import re


class HistoryLoader:

    def __init__(self, page):

        self.page = page

    # ----------------------------------------------------

    def load(self, candles=500):

        frame = None

        for f in self.page.frames:

            if f.url.startswith("blob:"):
                frame = f
                break

        if frame is None:
            return []

        text = frame.locator("body").inner_text(timeout=5000)

        prices = []

        matches = re.findall(r"\bC\s*([0-9,]+(?:\.\d+)?)", text)

        for m in matches:

            try:

                prices.append(float(m.replace(",", "")))

            except:

                pass

        history = []

        for p in prices[-candles:]:

            history.append(
                {
                    "open": p,
                    "high": p,
                    "low": p,
                    "close": p,
                }
            )

        return history