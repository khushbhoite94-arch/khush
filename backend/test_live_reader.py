from app.automation.browser import BrowserManager
from app.automation.live_reader import LiveReader

browser = BrowserManager()

browser.connect()

reader = LiveReader(browser.page)

print()

print("=" * 80)

print("URL")
print(browser.current_url())

print()

print("TITLE")
print(browser.title())

print()

print(reader.dump())

print("=" * 80)

input("\nPress ENTER...")

browser.stop()