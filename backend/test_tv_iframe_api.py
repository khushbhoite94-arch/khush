from app.automation.browser import BrowserManager
import json

browser = BrowserManager()
browser.connect()

# Find the TradingView blob frame
frame = None

for f in browser.page.frames:
    if f.url.startswith("blob:"):
        frame = f
        break

result = frame.evaluate("""
() => {

    const out = {};

    out.windowKeys = Object.keys(window).filter(k =>
        k.toLowerCase().includes("tv") ||
        k.toLowerCase().includes("chart") ||
        k.toLowerCase().includes("widget") ||
        k.toLowerCase().includes("data")
    );

    if (typeof TradingView !== "undefined") {

        out.tradingViewKeys = Object.keys(TradingView);

    }

    return out;

}
""")

print(json.dumps(result, indent=4))

input("Press ENTER...")

browser.stop()