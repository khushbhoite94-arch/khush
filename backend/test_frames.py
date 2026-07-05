from app.automation.browser import BrowserManager

browser = BrowserManager()
browser.connect()

print("=" * 80)

for i, frame in enumerate(browser.page.frames):
    print(f"FRAME {i}")
    print("URL:", frame.url)
    print()

print("=" * 80)

input("Press ENTER...")

browser.stop()