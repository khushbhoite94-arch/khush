from app.market.history_api import HistoryAPI

api = HistoryAPI()

candles = api.load(

    symbol="AAPL",

    interval="1m",

    period="5d",

)

print()

print("Candles:", len(candles))

print()

print(candles[-3:])

print()