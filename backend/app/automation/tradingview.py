"""
AEGIS AI
TradingView Controller
"""

from playwright.sync_api import Page, TimeoutError

from app.core import log


class TradingViewController:

    CHART_URL = "https://www.tradingview.com/chart/"

    def __init__(self, page: Page):
        self.page = page

    # -----------------------------------------------------
    # Navigation
    # -----------------------------------------------------

    def open(self):

        log.info("Opening TradingView...")

        self.page.goto(
            self.CHART_URL,
            wait_until="networkidle",
            timeout=60000,
        )

        self.page.wait_for_timeout(3000)

        log.success("TradingView loaded.")

    # -----------------------------------------------------
    # Login Detection
    # -----------------------------------------------------

    def is_logged_in(self) -> bool:

        # Method 1
        try:
            if self.page.get_by_text("Sign in").count() > 0:
                return False
        except Exception:
            pass

        # Method 2
        try:
            if self.page.get_by_role(
                "button",
                name="Open user menu",
            ).count() > 0:
                return True
        except Exception:
            pass

        # Method 3
        try:
            state = self.page.evaluate(
                """
() => {
    if (!window.__INITIAL_STATE__)
        return null;

    const auth = window.__INITIAL_STATE__.auth;

    if (!auth)
        return null;

    return {
        authenticated: auth.is_authenticated,
        username: auth.user ? auth.user.username : null
    };
}
"""
            )

            if state is not None:
                return bool(state.get("authenticated"))

        except Exception:
            pass

        return False

    # -----------------------------------------------------
    # Symbol
    # -----------------------------------------------------

    def change_symbol(self, symbol: str):

        log.info(f"Changing symbol to {symbol}")

        self.page.keyboard.press("/")

        self.page.wait_for_timeout(700)

        textbox = self.page.get_by_role("textbox").first

        textbox.fill(symbol)

        self.page.wait_for_timeout(500)

        self.page.keyboard.press("Enter")

        self.page.wait_for_timeout(2500)

        log.success(f"Symbol changed to {symbol}")

    # -----------------------------------------------------
    # Timeframe
    # -----------------------------------------------------

    def change_timeframe(self, timeframe: str):

        log.info(f"Changing timeframe to {timeframe}")

        self.page.keyboard.press(",")

        self.page.wait_for_timeout(500)

        self.page.keyboard.type(timeframe)

        self.page.wait_for_timeout(500)

        self.page.keyboard.press("Enter")

        self.page.wait_for_timeout(2000)

        log.success(f"Timeframe changed to {timeframe}")

    # -----------------------------------------------------
    # Screenshot
    # -----------------------------------------------------

    def screenshot(self, path: str):

        self.page.screenshot(
            path=path,
            full_page=False,
        )

        log.success(f"Screenshot saved to {path}")

    # -----------------------------------------------------
    # Current URL
    # -----------------------------------------------------

    def current_url(self) -> str:

        return self.page.url

    # -----------------------------------------------------
    # Current Title
    # -----------------------------------------------------

    def current_title(self) -> str:

        return self.page.title()

    # -----------------------------------------------------
    # Refresh
    # -----------------------------------------------------

    def refresh(self):

        log.info("Refreshing page...")

        self.page.reload(
            wait_until="networkidle"
        )

        self.page.wait_for_timeout(3000)

        log.success("Page refreshed.")

    # -----------------------------------------------------
    # Wait
    # -----------------------------------------------------

    def wait(self, milliseconds: int):

        self.page.wait_for_timeout(milliseconds)