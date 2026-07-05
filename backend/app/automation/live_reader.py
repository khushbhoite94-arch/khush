"""
AEGIS AI
Live TradingView Reader
"""

import re


class LiveReader:

    def __init__(self, page):

        self.page = page

    # --------------------------------------------------

    def title(self):

        return self.page.title()

    # --------------------------------------------------

    def html(self):

        return self.page.content()

    # --------------------------------------------------

    def ohlc_text(self):

        html = self.html()

        html = re.sub(r"<[^>]+>", " ", html)

        html = re.sub(r"\s+", " ", html)

        return html

    # --------------------------------------------------

    def dump(self):

        text = self.ohlc_text()

        idx = text.find("O")

        if idx == -1:
            idx = text.find("Open")

        if idx == -1:
            return text[:500]

        return text[idx:idx + 500]