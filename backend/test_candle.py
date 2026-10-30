import time

from app.market.candle_builder import CandleBuilder

builder = CandleBuilder()

prices = [100,101,102,99,103,104,105]

for p in prices:

    candle = builder.update(p)

    print("Tick:", p)

    if candle:
        print("Closed Candle:", candle)

    time.sleep(10)