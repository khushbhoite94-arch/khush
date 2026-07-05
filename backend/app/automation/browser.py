"""
AEGIS AI
Browser Manager (CDP)
"""

from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

        self.debugger_port = 9222

    # --------------------------------------------------

    def connect(self):

        print("[AEGIS] Connecting to Chrome CDP...")

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.connect_over_cdp(
            f"http://127.0.0.1:{self.debugger_port}"
        )

        if not self.browser.contexts:
            raise RuntimeError("No browser contexts found.")

        self.context = self.browser.contexts[0]

        # --------------------------------------------------
        # Find TradingView tab automatically
        # --------------------------------------------------

        self.page = None

        for page in self.context.pages:

            url = page.url.lower()

            if (
                "tradingview" in url
                or "trading-terminal" in url
                or "widget" in url
            ):

                self.page = page
                break

        if self.page is None:

            print("[AEGIS] TradingView tab not found.")

            print("[AEGIS] Using first browser tab.")

            self.page = self.context.pages[0]

        print()

        print("[AEGIS] Connected Successfully")

        print("URL :", self.page.url)

        print("TITLE :", self.page.title())

        print()

    # --------------------------------------------------

    def open(self, url):

        self.page.goto(
            url,
            wait_until="networkidle",
            timeout=60000,
        )

    # --------------------------------------------------

    def current_url(self):

        return self.page.url

    # --------------------------------------------------

    def title(self):

        return self.page.title()

    # --------------------------------------------------

    def screenshot(self, path="chart.png"):

        self.page.screenshot(
            path=path,
            full_page=True,
        )

    # --------------------------------------------------

    def stop(self):

        print()

        print("[AEGIS] Disconnecting...")

        if self.playwright:

            self.playwright.stop()

        print("[AEGIS] Done.")