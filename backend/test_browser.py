from app.automation.browser import BrowserManager

browser = BrowserManager()

browser.connect()

page = browser.page

page.goto(
    "https://trading-terminal.tradingview-widget.com/",
    wait_until="domcontentloaded",
    timeout=60000,
)

print("\nCurrent URL:")
print(page.url)

input("\nPress ENTER to exit...")

browser.stop()
