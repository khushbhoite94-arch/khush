from traceback import print_exc

from app.automation.browser import BrowserManager

browser = BrowserManager()

try:
    browser.start()

    browser.open_tradingview()

    page = browser.page

    print("=" * 60)

    print("Waiting for TradingView...")

    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(5000)

    print("TITLE :", page.title())
    print("URL   :", page.url)

    print("=" * 60)

    input("Press ENTER to close...")

except Exception:
    print_exc()

finally:
    browser.stop()