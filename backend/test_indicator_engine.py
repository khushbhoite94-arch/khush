from app.indicators.indicator_engine import IndicatorEngine

candles = []

price = 1.1000

for i in range(100):

    candle = {

        "open": price,

        "high": price + 0.0012,

        "low": price - 0.0008,

        "close": price + 0.0006,

    }

    candles.append(candle)

    price += 0.0003

closes = [

    c["close"]

    for c in candles

]

volumes = [

    100 + i

    for i in range(100)

]

engine = IndicatorEngine()

result = engine.calculate(

    closes,

    candles,

    volumes,

)

for key, value in result.items():

    print(key)

    print(value)

    print("-" * 40)