"""
AEGIS AI v2
Indicator Engine

Single entry point for all indicators.
"""

from __future__ import annotations

from app.indicators.ema import EMA
from app.indicators.rsi import RSI
from app.indicators.atr import ATR
from app.indicators.macd import MACD
from app.indicators.trend import Trend
from app.indicators.momentum import Momentum
from app.indicators.volume import Volume
from app.indicators.volatility import Volatility
from app.indicators.candlestick import Candlestick
from app.indicators.smart_money import SmartMoney


class IndicatorEngine:

    def __init__(self):

        self.ema20 = EMA(20)

        self.ema50 = EMA(50)

        self.rsi = RSI()

        self.atr = ATR()

        self.macd = MACD()

        self.trend = Trend()

        self.momentum = Momentum()

        self.volume = Volume()

        self.volatility = Volatility()

        self.candlestick = Candlestick()

        self.smart_money = SmartMoney()

    # ----------------------------------------------------

    def calculate(

        self,

        closes,

        candles,

        volumes=None,

    ):

        if volumes is None:

            volumes = []

        result = {

            "ema20": self.ema20.calculate(closes),

            "ema50": self.ema50.calculate(closes),

            "rsi": self.rsi.calculate(closes),

            "atr": self.atr.calculate(candles),

            "macd": self.macd.calculate(closes),

            "trend": self.trend.calculate(closes),

            "momentum": self.momentum.calculate(closes),

            "volume": self.volume.calculate(volumes),

            "volatility": self.volatility.calculate(candles),

            "candlestick": self.candlestick.detect(candles),

            "smart_money": self.smart_money.calculate(candles),

        }

        return result