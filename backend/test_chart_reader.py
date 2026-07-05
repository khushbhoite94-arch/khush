from app.automation.browser import BrowserManager
from app.automation.chart_reader import ChartReader

browser = BrowserManager()

browser.connect()

reader = ChartReader(browser.page)

print("=" * 50)

print("Symbol     :", reader.symbol())
print("Timeframe  :", reader.timeframe())
print("OHLC       :", reader.ohlc())
print("Bid        :", reader.bid())
print("Ask        :", reader.ask())

print("=" * 50)

input("Press ENTER...")

browser.stop()