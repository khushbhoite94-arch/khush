from app.strategy.range import RangeStrategy

candles = []

for i in range(30):

    candles.append({

        "open": 1.1000,

        "high": 1.1010,

        "low": 1.0990,

        "close": 1.0991,

    })

strategy = RangeStrategy()

print(

    strategy.signal(

        candles

    )

)