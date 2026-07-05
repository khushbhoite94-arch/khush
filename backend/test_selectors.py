from traceback import print_exc

from app.automation.browser import BrowserManager
from app.automation.actions import BrowserActions
from app.automation.selectors import selectors

browser = BrowserManager()

try:
    browser.start()

    browser.open_tradingview()

    actions = BrowserActions(browser.page)

    print("=" * 50)

    print(
        "Sign In Button Exists:",
        actions.exists(selectors.SIGN_IN_BUTTON),
    )

    print(
        "Profile Button Exists:",
        actions.exists(selectors.PROFILE_BUTTON),
    )

    print("=" * 50)

    input("Press ENTER to close...")

except Exception:
    print_exc()

finally:
    browser.stop()