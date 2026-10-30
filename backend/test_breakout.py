from app.strategy.breakout import Breakout

candles = []

price = 1.1000

for i in range(30):

    candles.append({

        "open": price,

        "high": price + 0.0010,

        "low": price - 0.0010,

        "close": price,

    })

    price += 0.0002

candles[-1]["close"] = candles[-2]["high"] + 0.002

strategy = Breakout()

print(

    strategy.signal(

        candles

    )

)