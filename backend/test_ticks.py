from datetime import datetime

from app.market.ticks import Tick


tick = Tick(

    symbol="EURUSD",

    bid=1.17020,

    ask=1.17035,

    timestamp=datetime.now(),

)

print()

print(tick.to_dict())

print()

print("Spread :", tick.spread)

print("Mid Price :", tick.mid_price)