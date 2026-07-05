from app.automation.browser import BrowserManager

browser = BrowserManager()
browser.connect()

frame = browser.page.frames[2]

print("=" * 80)
print("FRAME URL:")
print(frame.url)
print("=" * 80)

text = frame.locator("body").inner_text(timeout=10000)

print(text[:10000])

input("\nPress ENTER...")

browser.stop()