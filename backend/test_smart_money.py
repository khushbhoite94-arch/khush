from app.indicators.smart_money import SmartMoney

candles = [

    {

        "open":1.1000,

        "high":1.1010,

        "low":1.0990,

        "close":1.1008,

    },

    {

        "open":1.1008,

        "high":1.1020,

        "low":1.1000,

        "close":1.1018,

    },

    {

        "open":1.1018,

        "high":1.1035,

        "low":1.1012,

        "close":1.1028,

    },

]

smc = SmartMoney()

print(smc.calculate(candles))