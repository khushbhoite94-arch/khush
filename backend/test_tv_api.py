from app.automation.browser import BrowserManager
import json

browser = BrowserManager()
browser.connect()

page = browser.page

result = page.evaluate("""
() => {

    function inspect(obj, depth = 2, visited = new WeakSet()) {

        if (obj === null || typeof obj !== "object")
            return typeof obj;

        if (visited.has(obj))
            return "[Circular]";

        visited.add(obj);

        const out = {};

        for (const key of Object.keys(obj)) {

            try {

                const value = obj[key];

                if (typeof value === "function") {

                    out[key] = "function";

                } else if (typeof value === "object") {

                    if (depth > 0)
                        out[key] = inspect(value, depth - 1, visited);
                    else
                        out[key] = "object";

                } else {

                    out[key] = value;

                }

            } catch(e) {

                out[key] = "ERROR";

            }

        }

        return out;
    }

    return {

        TradingView : inspect(TradingView,1),

        tvWidget : inspect(tvWidget,3)

    };

}
""")

print(json.dumps(result, indent=2))

input("Press ENTER...")

browser.stop()