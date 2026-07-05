from app.automation.browser import BrowserManager
from app.automation.dom_inspector import DOMInspector

browser = BrowserManager()

browser.connect()

browser.open_tradingview()

input("\nMake sure your TradingView chart is visible.\nPress ENTER...")

inspector = DOMInspector(browser.page)

inspector.inspect()

print("\nInspection Finished.")

input("\nPress ENTER to close...")

browser.stop()