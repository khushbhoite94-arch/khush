"""
AEGIS AI v2
TradingView Automation

Part 1/6
"""
from __future__ import annotations

import time

from playwright.sync_api import TimeoutError


class TradingView:

    def __init__(self, page):

        self.page = page

        self.timeout = 10000

        self.buy_selector = None
        self.sell_selector = None
        self.order_panel_selector = None
        self.price_selector = None

    # =====================================================
    # PAGE
    # =====================================================

    def wait_until_ready(self):

        self.page.wait_for_load_state("networkidle")

        time.sleep(2)

    def title(self):

        return self.page.title()

    def url(self):

        return self.page.url

    # =====================================================
    # ELEMENT HELPERS
    # =====================================================

    def exists(

        self,

        selector,

    ):

        try:

            return self.page.locator(selector).count() > 0

        except Exception:

            return False

    def visible(

        self,

        selector,

    ):

        try:

            return self.page.locator(selector).is_visible()

        except Exception:

            return False

    def click(

        self,

        selector,

    ):

        self.page.locator(selector).click()

    def fill(

        self,

        selector,

        value,

    ):

        box = self.page.locator(selector)

        box.click()

        box.fill(str(value))

    def text(

        self,

        selector,

    ):

        return self.page.locator(selector).inner_text()

    # =====================================================
    # DISCOVER SELECTORS
    # =====================================================

    def detect_buy_button(self):

        candidates = [

            "button:has-text('Buy')",

            "button:has-text('BUY')",

            "[data-name='buy-button']",

            "[aria-label='Buy']",

        ]

        for selector in candidates:

            if self.exists(selector):

                self.buy_selector = selector

                return selector

        return None

    def detect_sell_button(self):

        candidates = [

            "button:has-text('Sell')",

            "button:has-text('SELL')",

            "[data-name='sell-button']",

            "[aria-label='Sell']",

        ]

        for selector in candidates:

            if self.exists(selector):

                self.sell_selector = selector

                return selector

        return None

    def detect_order_panel(self):

        candidates = [

            "[data-name='order-ticket']",

            ".order-ticket",

            ".tv-order-ticket",

            "[role='dialog']",

        ]

        for selector in candidates:

            if self.exists(selector):

                self.order_panel_selector = selector

                return selector

        return None
        # =====================================================
    # PRICE
    # =====================================================

    def detect_price_label(self):

        candidates = [

            "[data-name='legend-series-last-value']",

            "[data-field-key='last']",

            ".last-price",

            ".price-last",

        ]

        for selector in candidates:

            if self.exists(selector):

                self.price_selector = selector

                return selector

        return None

    def current_price(self):

        if self.price_selector is None:

            self.detect_price_label()

        if self.price_selector is None:

            return None

        try:

            value = self.text(

                self.price_selector

            )

            value = (

                value.replace(",", "")

                     .replace("$", "")
                     .strip()

            )

            return float(value)

        except Exception:

            return None

    # =====================================================
    # SYMBOL
    # =====================================================

    def symbol(self):

        candidates = [

            "[data-name='legend-source-title']",

            ".chart-symbol",

            ".symbol",

        ]

        for selector in candidates:

            if self.exists(selector):

                try:

                    return self.text(selector)

                except Exception:

                    pass

        return None

    # =====================================================
    # TIMEFRAME
    # =====================================================

    def timeframe(self):

        candidates = [

            "[data-name='interval-dialog-button']",

            ".interval-dialog-button",

            ".timeframe",

        ]

        for selector in candidates:

            if self.exists(selector):

                try:

                    return self.text(selector)

                except Exception:

                    pass

        return None

    # =====================================================
    # ACCOUNT
    # =====================================================

    def account_name(self):

        candidates = [

            "[data-name='account-manager-header']",

            ".account-name",

        ]

        for selector in candidates:

            if self.exists(selector):

                try:

                    return self.text(selector)

                except Exception:

                    pass

        return None

    def account_balance(self):

        candidates = [

            "[data-name='account-balance']",

            ".account-balance",

        ]

        for selector in candidates:

            if self.exists(selector):

                try:

                    txt = self.text(selector)

                    txt = (

                        txt.replace("$", "")
                           .replace(",", "")
                           .strip()

                    )

                    return float(txt)

                except Exception:

                    pass

        return None

    # =====================================================
    # STATUS
    # =====================================================

    def connected(self):

        return (

            self.detect_buy_button() is not None

            and

            self.detect_sell_button() is not None

        )

    def info(self):

        return {

            "title": self.title(),

            "url": self.url(),

            "symbol": self.symbol(),

            "timeframe": self.timeframe(),

            "price": self.current_price(),

            "account": self.account_name(),

            "balance": self.account_balance(),

        }
        # =====================================================
    # ORDER PANEL
    # =====================================================

    def open_order_panel(

        self,

        side,

    ):

        side = side.upper()

        if side == "BUY":

            if self.buy_selector is None:

                self.detect_buy_button()

            if self.buy_selector:

                self.click(self.buy_selector)

                self.page.wait_for_timeout(500)
                return True

        if side == "SELL":

            if self.sell_selector is None:

                self.detect_sell_button()

            if self.sell_selector:

                self.click(self.sell_selector)

                self.page.wait_for_timeout(500)
                return True

        return False

    # =====================================================
    # INPUT HELPERS
    # =====================================================

    def set_volume(

        self,

        volume,

    ):

        selectors = [

            "input[name='qty']",

            "input[name='quantity']",

            "input[type='number']",

            "[data-name='quantity-input'] input",

        ]

        for selector in selectors:

            if self.exists(selector):

                self.fill(selector, volume)

                return True

        return False

    def set_stop_loss(

        self,

        stop_loss,

    ):

        selectors = [

            "input[name='sl']",

            "input[name='stopLoss']",

            "[data-name='sl-input'] input",

        ]

        for selector in selectors:

            if self.exists(selector):

                self.fill(selector, stop_loss)

                return True

        return False

    def set_take_profit(

        self,

        take_profit,

    ):

        selectors = [

            "input[name='tp']",

            "input[name='takeProfit']",

            "[data-name='tp-input'] input",

        ]

        for selector in selectors:

            if self.exists(selector):

                self.fill(selector, take_profit)

                return True

        return False

    # =====================================================
    # PLACE ORDER
    # =====================================================

    def submit_order(self):

        selectors = [

            "button:has-text('Place Order')",

            "button:has-text('Buy')",

            "button:has-text('Sell')",

            "[data-name='submit-order']",

        ]

        for selector in selectors:

            if self.exists(selector):

                self.click(selector)

                self.page.wait_for_timeout(1000)

                return True

        return False

    # =====================================================
    # HIGH LEVEL
    # =====================================================

    def buy(

        self,

        volume,

        stop_loss,

        take_profit,

    ):

        if not self.open_order_panel("BUY"):

            return False

        self.set_volume(volume)

        self.set_stop_loss(stop_loss)

        self.set_take_profit(take_profit)

        return self.submit_order()

    def sell(

        self,

        volume,

        stop_loss,

        take_profit,

    ):

        if not self.open_order_panel("SELL"):

            return False

        self.set_volume(volume)

        self.set_stop_loss(stop_loss)

        self.set_take_profit(take_profit)

        return self.submit_order()
            # =====================================================
    # OPEN POSITION
    # =====================================================

    def has_open_position(self):

        selectors = [

            "[data-name='positions-tab']",

            ".positions-list",

            ".tv-position",

        ]

        for selector in selectors:

            if self.exists(selector):

                return True

        return False

    # =====================================================
    # POSITION INFO
    # =====================================================

    def current_position(self):

        if not self.has_open_position():

            return None

        position = {}

        fields = {

            "side": [

                "[data-name='position-side']",

                ".position-side",

            ],

            "entry": [

                "[data-name='position-entry']",

                ".position-entry",

            ],

            "profit": [

                "[data-name='position-profit']",

                ".position-profit",

            ],

            "volume": [

                "[data-name='position-volume']",

                ".position-volume",

            ],

        }

        for key, selectors in fields.items():

            value = None

            for selector in selectors:

                if self.exists(selector):

                    try:

                        value = self.text(selector)

                        break

                    except Exception:

                        pass

            position[key] = value

        return position

    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(self):

        selectors = [

            "button:has-text('Close Position')",

            "button:has-text('Close')",

            "[data-name='close-position']",

            "[aria-label='Close Position']",

        ]

        for selector in selectors:

            if self.exists(selector):

                self.click(selector)

                self.page.wait_for_timeout(1000)

                return True

        return False

    # =====================================================
    # CLOSE ALL
    # =====================================================

    def close_all_positions(self):

        while self.has_open_position():

            if not self.close_position():

                break

            self.page.wait_for_timeout(1500)

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        self.page.reload()

        self.page.wait_for_load_state("networkidle")

        time.sleep(2)

        self.detect_buy_button()

        self.detect_sell_button()

        self.detect_order_panel()

        self.detect_price_label()

    # =====================================================
    # RECOVERY
    # =====================================================

    def recover(self):

        try:

            self.refresh()

            return self.connected()

        except Exception:

            return False

    # =====================================================
    # KEEP ALIVE
    # =====================================================

    def keep_alive(self):

        try:

            self.page.mouse.move(500, 300)

            self.page.wait_for_timeout(100)

            self.page.mouse.move(700, 400)

        except Exception:

            pass
            # =====================================================
    # PENDING ORDERS
    # =====================================================

    def pending_orders(self):

        selectors = [

            "[data-name='orders-tab']",

            ".orders-list",

            ".pending-orders",

        ]

        for selector in selectors:

            if self.exists(selector):

                try:

                    return self.page.locator(
                        selector
                    ).count()

                except Exception:

                    return 0

        return 0

    # =====================================================
    # CANCEL ALL ORDERS
    # =====================================================

    def cancel_all_orders(self):

        selectors = [

            "button:has-text('Cancel All')",

            "[data-name='cancel-all-orders']",

            "[aria-label='Cancel All']",

        ]

        for selector in selectors:

            if self.exists(selector):

                self.click(selector)

                self.page.wait_for_timeout(1000)

                return True

        return False

    # =====================================================
    # SCREENSHOT
    # =====================================================

    def screenshot(

        self,

        path="tradingview.png",

    ):

        self.page.screenshot(

            path=path,

            full_page=True,

        )

        return path

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health(self):

        return {

            "connected": self.connected(),

            "buy_button": self.buy_selector is not None,

            "sell_button": self.sell_selector is not None,

            "order_panel": self.order_panel_selector is not None,

            "price_feed": self.current_price() is not None,

            "position": self.has_open_position(),

            "pending_orders": self.pending_orders(),

        }

    # =====================================================
    # ENSURE CONNECTION
    # =====================================================

    def ensure_connection(self):

        if self.connected():

            return True

        for _ in range(3):

            if self.recover():

                return True

            self.page.wait_for_timeout(2000)

        return False

    # =====================================================
    # WAIT FOR PRICE UPDATE
    # =====================================================

    def wait_for_price(

        self,

        timeout=30000,

    ):

        start = time.time()

        last = self.current_price()

        while time.time() - start < timeout / 1000:

            self.page.wait_for_timeout(250)

            new = self.current_price()

            if new is None:

                continue

            if last is None:

                last = new

                continue

            if new != last:

                return new

        return None

    # =====================================================
    # WAIT FOR POSITION
    # =====================================================

    def wait_for_position(

        self,

        timeout=10000,

    ):

        start = time.time()

        while time.time() - start < timeout / 1000:

            if self.has_open_position():

                return True

            self.page.wait_for_timeout(300)

        return False

    # =====================================================
    # WAIT FOR CLOSE
    # =====================================================

    def wait_until_closed(

        self,

        timeout=10000,

    ):

        start = time.time()

        while time.time() - start < timeout / 1000:

            if not self.has_open_position():

                return True

            self.page.wait_for_timeout(300)

        return False
        # =====================================================
    # REDISCOVER SELECTORS
    # =====================================================

    def rediscover(self):

        self.buy_selector = None
        self.sell_selector = None
        self.order_panel_selector = None
        self.price_selector = None

        self.detect_buy_button()
        self.detect_sell_button()
        self.detect_order_panel()
        self.detect_price_label()

        return self.connected()

    # =====================================================
    # DEBUG INFORMATION
    # =====================================================

    def debug(self):

        return {

            "title": self.title(),

            "url": self.url(),

            "connected": self.connected(),

            "buy_selector": self.buy_selector,

            "sell_selector": self.sell_selector,

            "order_panel": self.order_panel_selector,

            "price_selector": self.price_selector,

            "symbol": self.symbol(),

            "timeframe": self.timeframe(),

            "price": self.current_price(),

            "position": self.current_position(),

            "pending_orders": self.pending_orders(),

        }

    # =====================================================
    # PRINT DEBUG
    # =====================================================

    def print_debug(self):

        info = self.debug()

        print()

        print("=" * 60)

        print("TRADINGVIEW DEBUG")

        print("=" * 60)

        for key, value in info.items():

            print(f"{key:<20}: {value}")

        print("=" * 60)

        print()

    # =====================================================
    # VERIFY
    # =====================================================

    def verify(self):

        checks = [

            self.connected(),

            self.current_price() is not None,

            self.symbol() is not None,

            self.timeframe() is not None,

        ]

        return all(checks)

    # =====================================================
    # PING
    # =====================================================

    def ping(self):

        try:

            self.page.evaluate("() => document.title")

            return True

        except Exception:

            return False

    # =====================================================
    # SESSION STATUS
    # =====================================================

    def session(self):

        return {

            "alive": self.ping(),

            "verified": self.verify(),

            "connected": self.connected(),

            "account": self.account_name(),

            "balance": self.account_balance(),

            "symbol": self.symbol(),

            "timeframe": self.timeframe(),

        }

    # =====================================================
    # DISCONNECT
    # =====================================================

    def disconnect(self):

        try:

            self.page.close()

        except Exception:

            pass

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(self):

        self.buy_selector = None

        self.sell_selector = None

        self.order_panel_selector = None

        self.price_selector = None

    # =====================================================
    # RECONNECT
    # =====================================================

    def reconnect(self):

        self.cleanup()

        return self.recover()

    # =====================================================
    # STRING
    # =====================================================

    def __repr__(self):

        return (

            f"<TradingView "

            f"symbol={self.symbol()} "

            f"timeframe={self.timeframe()} "

            f"connected={self.connected()}>"

        )