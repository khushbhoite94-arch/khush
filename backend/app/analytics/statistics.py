"""
AEGIS AI v2
Statistics Engine
"""

from __future__ import annotations

import math
from statistics import mean, median


class Statistics:

    # =====================================================
    # RETURNS
    # =====================================================

    def returns(self, candles):

        if len(candles) < 2:

            return []

        result = []

        for i in range(1, len(candles)):

            previous = candles[i - 1]["close"]

            current = candles[i]["close"]

            if previous == 0:

                continue

            result.append(

                (current - previous) / previous

            )

        return result

    # =====================================================
    # MEAN
    # =====================================================

    def mean(self, values):

        if not values:

            return 0.0

        return mean(values)

    # =====================================================
    # MEDIAN
    # =====================================================

    def median(self, values):

        if not values:

            return 0.0

        return median(values)

    # =====================================================
    # VARIANCE
    # =====================================================

    def variance(self, values):

        if len(values) < 2:

            return 0.0

        avg = self.mean(values)

        return sum(

            (x - avg) ** 2

            for x in values

        ) / (len(values) - 1)

    # =====================================================
    # STD DEV
    # =====================================================

    def std(self, values):

        return math.sqrt(

            self.variance(values)

        )

    # =====================================================
    # VOLATILITY
    # =====================================================

    def volatility(self, candles):

        returns = self.returns(candles)

        return self.std(returns)

    # =====================================================
    # ROLLING VOLATILITY
    # =====================================================

    def rolling_volatility(

        self,

        candles,

        window=20,

    ):

        result = []

        if len(candles) < window:

            return result

        for i in range(

            window,

            len(candles) + 1,

        ):

            part = candles[

                i - window:i

            ]

            result.append(

                self.volatility(part)

            )

        return result

    # =====================================================
    # Z SCORE
    # =====================================================

    def z_score(

        self,

        value,

        values,

    ):

        std = self.std(values)

        if std == 0:

            return 0

        return (

            value - self.mean(values)

        ) / std

    # =====================================================
    # OUTLIERS
    # =====================================================

    def outliers(

        self,

        values,

        threshold=2,

    ):

        result = []

        for value in values:

            if abs(

                self.z_score(

                    value,

                    values,

                )

            ) >= threshold:

                result.append(value)

        return result

    # =====================================================
    # CORRELATION
    # =====================================================

    def correlation(

        self,

        x,

        y,

    ):

        if len(x) != len(y):

            return 0

        if len(x) < 2:

            return 0

        mx = self.mean(x)

        my = self.mean(y)

        numerator = sum(

            (a - mx) * (b - my)

            for a, b in zip(x, y)

        )

        denominator = math.sqrt(

            sum(

                (a - mx) ** 2

                for a in x

            )

            *

            sum(

                (b - my) ** 2

                for b in y

            )

        )

        if denominator == 0:

            return 0

        return numerator / denominator

    # =====================================================
    # EXPECTANCY
    # =====================================================

    def expectancy(

        self,

        trades,

    ):

        if not trades:

            return 0

        wins = [

            t

            for t in trades

            if t > 0

        ]

        losses = [

            abs(t)

            for t in trades

            if t < 0

        ]

        if not wins:

            return -self.mean(losses)

        if not losses:

            return self.mean(wins)

        win_rate = len(wins) / len(trades)

        loss_rate = len(losses) / len(trades)

        return (

            win_rate * self.mean(wins)

        ) - (

            loss_rate * self.mean(losses)

        )

    # =====================================================
    # SHARPE
    # =====================================================

    def sharpe(

        self,

        candles,

        risk_free=0,

    ):

        returns = self.returns(candles)

        if not returns:

            return 0

        std = self.std(returns)

        if std == 0:

            return 0

        return (

            self.mean(returns) - risk_free

        ) / std

    # =====================================================
    # MAX DRAWDOWN
    # =====================================================

    def max_drawdown(

        self,

        candles,

    ):

        closes = [

            c["close"]

            for c in candles

        ]

        peak = closes[0]

        drawdown = 0

        for close in closes:

            peak = max(

                peak,

                close,

            )

            dd = (

                peak - close

            ) / peak

            drawdown = max(

                drawdown,

                dd,

            )

        return drawdown

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        candles,

    ):

        returns = self.returns(candles)

        return {

            "mean": self.mean(returns),

            "median": self.median(returns),

            "variance": self.variance(returns),

            "std": self.std(returns),

            "volatility": self.volatility(candles),

            "sharpe": self.sharpe(candles),

            "max_drawdown": self.max_drawdown(candles),

            "outliers": self.outliers(returns),

        }