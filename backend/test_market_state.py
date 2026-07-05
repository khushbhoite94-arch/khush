from datetime import datetime

from app.market.candles import Candle
from app.market.ticks import Tick
from app.market.market_state import MarketState


market = MarketState()

market.add_tick(

    Tick(

        symbol="EURUSD",

        bid=1.1701,

        ask=1.1703,

        timestamp=datetime.now(),

    )

)

market.add_candle(

    Candle(

        symbol="EURUSD",

        timeframe="M5",

        timestamp=datetime.now(),

        open=1.1700,

        high=1.1710,

        low=1.1695,

        close=1.1708,

        volume=1200,

    )

)

print()

print("Latest Tick")

print(market.latest_tick())

print()

print("Latest Candle")

print(market.latest_candle())

print()

print("Tick Count")

print(market.tick_count())

print()

print("Candle Count")

print(market.candle_count())