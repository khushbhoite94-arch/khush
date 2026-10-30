"""
AEGIS AI
Liquidity Analysis
"""

from dataclasses import dataclass


@dataclass(slots=True)
class LiquidityZone:
    price: float
    zone_type: str      # "BUY_SIDE" or "SELL_SIDE"
    strength: int = 1


class LiquidityAnalyzer:

    def __init__(self):
        self.buy_side = []
        self.sell_side = []

    def add_buy_side(self, price):
        self.buy_side.append(
            LiquidityZone(
                price=price,
                zone_type="BUY_SIDE"
            )
        )

    def add_sell_side(self, price):
        self.sell_side.append(
            LiquidityZone(
                price=price,
                zone_type="SELL_SIDE"
            )
        )

    def nearest_buy(self, price):

        if not self.buy_side:
            return None

        return min(
            self.buy_side,
            key=lambda z: abs(z.price - price)
        )

    def nearest_sell(self, price):

        if not self.sell_side:
            return None

        return min(
            self.sell_side,
            key=lambda z: abs(z.price - price)
        )

    def clear(self):
        self.buy_side.clear()
        self.sell_side.clear()