from app.automation.browser import BrowserManager
import json

browser = BrowserManager()
browser.connect()

page = browser.page

result = page.evaluate("""
() => {

    const data = {};

    data.windowKeys = Object.keys(window);

    data.tvKeys = Object.keys(window).filter(
        k =>
            k.toLowerCase().includes("tv") ||
            k.toLowerCase().includes("chart") ||
            k.toLowerCase().includes("trading")
    );

    return data;

}
""")

print(json.dumps(result, indent=2))

input("Press ENTER...")

browser.stop()