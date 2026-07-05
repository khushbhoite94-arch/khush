from app.automation.browser import BrowserManager

browser = BrowserManager()

try:
    browser.start()
    browser.open_tradingview()

    state = browser.page.evaluate("""
() => window.__INITIAL_STATE__
""")

    print(state)

    input("Press ENTER...")

finally:
    browser.stop()