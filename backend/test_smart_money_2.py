from app.strategy.smart_money import SmartMoney

candles = []

for i in range(20):

    candles.append({

        "open":1.1000,

        "high":1.1010,

        "low":1.0990,

        "close":1.1002,

    })

candles[-1] = {

    "open":1.1005,

    "high":1.1025,

    "low":1.1000,

    "close":1.1007,

}

strategy = SmartMoney()

print(strategy.signal(candles))