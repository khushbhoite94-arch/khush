from app.automation.browser import BrowserManager
from app.market.market_stream import MarketStream

browser = BrowserManager()
browser.connect()

stream = MarketStream(browser.page)

for tick in stream.stream():

    print(tick)