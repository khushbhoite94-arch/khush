from app.automation.browser import BrowserManager
from app.market.market_stream import MarketStream
from app.market.history import MarketHistory

browser = BrowserManager()

browser.connect()

stream = MarketStream(browser.page)

history = MarketHistory()

for i, tick in enumerate(stream.stream()):

    history.add(tick)

    print("=" * 50)

    print("Ticks Stored :", len(history))

    print("Latest Tick")

    print(history.last())

    if i == 9:
        break

browser.stop()