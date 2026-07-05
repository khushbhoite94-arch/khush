from app.automation.browser import BrowserManager
from app.core.bot import TradingBot

browser = BrowserManager()

browser.connect()

browser.open("https://trading-terminal.tradingview-widget.com/")

input("Load TradingView then press ENTER...")

bot = TradingBot(browser.page)

bot.run()