from app.automation.browser import BrowserManager

browser = BrowserManager()
browser.connect()

frame = browser.page.frames[2]

text = frame.locator("body").inner_text(timeout=10000)

print(text)

input("Press ENTER...")

browser.stop()