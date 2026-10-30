from app.indicators.candlestick import Candlestick

candles = [

    {

        "open": 1.1000,

        "high": 1.1010,

        "low": 1.0990,

        "close": 1.0992,

    },

    {

        "open": 1.0990,

        "high": 1.1025,

        "low": 1.0988,

        "close": 1.1022,

    }

]

c = Candlestick()

print(c.detect(candles))