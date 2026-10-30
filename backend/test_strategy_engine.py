from app.strategy.startegy_engine import StrategyEngine

closes = []
candles = []

price = 1.1000

for _ in range(150):

    price += 0.00025

    closes.append(price)

    candles.append(
        {
            "open": price - 0.0001,
            "high": price + 0.0002,
            "low": price - 0.0002,
            "close": price,
        }
    )

engine = StrategyEngine()

result = engine.calculate(closes, candles)

print(result)