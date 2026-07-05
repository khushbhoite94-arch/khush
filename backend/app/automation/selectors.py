"""
AEGIS AI
TradingView Selectors

All TradingView locators live here.
Never use selectors directly anywhere else.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TradingViewSelectors:

    # -------------------------
    # Navigation
    # -------------------------

    CHART_URL = "https://www.tradingview.com/chart/"

    # -------------------------
    # Search
    # -------------------------

    SYMBOL_SEARCH_BUTTON = '[data-name="legend-source-title"]'

    SYMBOL_SEARCH_INPUT = 'input[type="text"]'

    # -------------------------
    # Toolbar
    # -------------------------

    TIMEFRAME_BUTTON = '[data-name="header-intervals-button"]'

    # -------------------------
    # Trading Panel
    # -------------------------

    TRADING_PANEL = '[data-name="backtesting"]'

    BUY_BUTTON = 'text=Buy'

    SELL_BUTTON = 'text=Sell'

    # -------------------------
    # Positions
    # -------------------------

    POSITION_TAB = 'text=Positions'

    ORDERS_TAB = 'text=Orders'

    # -------------------------
    # Authentication
    # -------------------------

    PROFILE_BUTTON = '[aria-label="Open user menu"]'

    SIGN_IN_BUTTON = 'text=Sign in'

    # -------------------------
    # Common
    # -------------------------

    LOADING = '.loading-indicator'

    DIALOG = '[role="dialog"]'


selectors = TradingViewSelectors()