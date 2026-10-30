from app.indicators.volatility import Volatility

candles = []

price = 1.1000

for i in range(50):

    candles.append(

        {

            "open": price,

            "high": price + 0.0015,

            "low": price - 0.0010,

            "close": price + 0.0008,

        }

    )

    price += 0.0003

v = Volatility()

print(v.calculate(candles))