"""
Browser helper functions.
"""

from playwright.sync_api import Page

from app.core import log


class BrowserActions:

    def __init__(self, page: Page):

        self.page = page

    def click(self, selector: str):

        log.info(f"Clicking {selector}")

        self.page.locator(selector).click(timeout=10000)

    def fill(self, selector: str, value: str):

        log.info(f"Typing into {selector}")

        self.page.locator(selector).fill(value)

    def press(self, key: str):

        self.page.keyboard.press(key)

    def wait(self, milliseconds: int):

        self.page.wait_for_timeout(milliseconds)

    def exists(self, selector: str):

        return self.page.locator(selector).count() > 0