"""
AEGIS AI
RSI Indicator
"""


class RSI:

    def __init__(self, period=14):

        self.period = period

    def calculate(self, prices):

        if len(prices) < self.period + 1:
            return None

        gains = []
        losses = []

        for i in range(1, self.period + 1):

            change = prices[i] - prices[i - 1]

            if change >= 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains) / self.period
        avg_loss = sum(losses) / self.period

        for i in range(self.period + 1, len(prices)):

            change = prices[i] - prices[i - 1]

            gain = max(change, 0)
            loss = abs(min(change, 0))

            avg_gain = ((avg_gain * (self.period - 1)) + gain) / self.period
            avg_loss = ((avg_loss * (self.period - 1)) + loss) / self.period

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return round(rsi, 2)