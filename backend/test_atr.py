"""
AEGIS AI
ATR Indicator
"""


class ATR:

    def __init__(self, period=14):

        self.period = period

    def calculate(self, highs, lows, closes):

        if len(highs) < self.period + 1:
            return None

        tr = []

        for i in range(1, len(highs)):

            hl = highs[i] - lows[i]
            hc = abs(highs[i] - closes[i - 1])
            lc = abs(lows[i] - closes[i - 1])

            tr.append(max(hl, hc, lc))

        atr = sum(tr[:self.period]) / self.period

        for value in tr[self.period:]:

            atr = ((atr * (self.period - 1)) + value) / self.period

        return round(atr, 5)