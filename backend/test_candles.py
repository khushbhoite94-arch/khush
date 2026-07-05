from datetime import datetime

from app.market.candles import Candle


candle = Candle(

    symbol="EURUSD",

    timeframe="M5",

    timestamp=datetime.now(),

    open=1.1700,

    high=1.1725,

    low=1.1690,

    close=1.1718,

    volume=1520,

)

print()

print(candle.to_dict())

print()

print("Bullish :", candle.bullish)

print("Bearish :", candle.bearish)

print("Body :", candle.body)

print("Upper Wick :", candle.upper_wick)

print("Lower Wick :", candle.lower_wick)

print("Range :", candle.range)