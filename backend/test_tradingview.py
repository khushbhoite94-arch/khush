from app.automation.browser import BrowserManager
from app.automation.tradingview import TradingViewController

browser = BrowserManager()

try:

    browser.start()

    tv = TradingViewController(browser.page)

    tv.open()

    print()

    print("Logged In :", tv.is_logged_in())

    print()

    input("Press ENTER to close...")

finally:

    browser.stop()