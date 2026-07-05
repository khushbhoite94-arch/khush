from app.automation.browser import BrowserManager
from app.core.live_engine import LiveEngine

browser = BrowserManager()

browser.connect()

browser.open("https://trading-terminal.tradingview-widget.com/")

input("Load your chart then press ENTER...")

engine = LiveEngine(browser.page)

engine.run()