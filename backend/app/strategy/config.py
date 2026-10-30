"""
AEGIS AI v2
Global Configuration

Single source of truth for the whole application.
Never hardcode configuration anywhere else.
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
import json
import os


# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

APP = ROOT / "app"

DATA = ROOT / "data"

MODELS = ROOT / "models"

CONFIG = ROOT / "config"

LOGS = ROOT / "logs"

CACHE = ROOT / "cache"

EXPORTS = ROOT / "exports"

BACKUPS = ROOT / "backups"

for folder in (
    DATA,
    MODELS,
    CONFIG,
    LOGS,
    CACHE,
    EXPORTS,
    BACKUPS,
):
    folder.mkdir(parents=True, exist_ok=True)


# ==========================================================
# MARKET
# ==========================================================


@dataclass(slots=True)
class MarketConfig:

    symbol: str = "BTCUSD"

    exchange: str = "BITSTAMP"

    timeframe: str = "1m"

    history: int = 500

    poll_interval: float = 1.0

    timezone: str = "UTC"


# ==========================================================
# INDICATORS
# ==========================================================


@dataclass(slots=True)
class IndicatorConfig:

    ema_fast: int = 9

    ema_slow: int = 21

    rsi_period: int = 14

    macd_fast: int = 12

    macd_slow: int = 26

    macd_signal: int = 9

    atr_period: int = 14


# ==========================================================
# RISK
# ==========================================================


@dataclass(slots=True)
class RiskConfig:

    account_size: float = 10000.0

    risk_percent: float = 1.0

    reward_ratio: float = 2.0

    max_positions: int = 1

    daily_loss_limit: float = 5.0

    max_drawdown: float = 20.0


# ==========================================================
# PAPER
# ==========================================================


@dataclass(slots=True)
class PaperConfig:

    balance: float = 100000.0

    commission: float = 0.0

    slippage: float = 0.0


# ==========================================================
# HISTORY
# ==========================================================


@dataclass(slots=True)
class HistoryConfig:

    provider: str = "stooq"

    cache: bool = True

    cache_days: int = 3650

    auto_download: bool = True


# ==========================================================
# AI
# ==========================================================


@dataclass(slots=True)
class AIConfig:

    minimum_confidence: int = 70

    minimum_candles: int = 35

    use_pattern_engine: bool = True

    use_history_server: bool = True

    use_memory: bool = True

    use_news: bool = False


# ==========================================================
# BROWSER
# ==========================================================


@dataclass(slots=True)
class BrowserConfig:

    debugger_port: int = 9222

    headless: bool = False

    timeout: int = 30000


# ==========================================================
# LOGGING
# ==========================================================


@dataclass(slots=True)
class LoggingConfig:

    debug: bool = True

    console: bool = True

    file: bool = True

    level: str = "INFO"

    folder: Path = LOGS


# ==========================================================
# MASTER CONFIG
# ==========================================================


class Settings:

    def __init__(self):

        self.market = MarketConfig()

        self.indicators = IndicatorConfig()

        self.risk = RiskConfig()

        self.paper = PaperConfig()

        self.history = HistoryConfig()

        self.ai = AIConfig()

        self.browser = BrowserConfig()

        self.logging = LoggingConfig()

    # ------------------------------------------------------

    def load_json(self, file: str):

        path = CONFIG / file

        if not path.exists():

            return

        with open(path) as f:

            data = json.load(f)

        for section, values in data.items():

            if hasattr(self, section):

                obj = getattr(self, section)

                for key, value in values.items():

                    if hasattr(obj, key):

                        setattr(obj, key, value)

    # ------------------------------------------------------

    def load_env(self):

        symbol = os.getenv("AEGIS_SYMBOL")

        if symbol:

            self.market.symbol = symbol

        tf = os.getenv("AEGIS_TIMEFRAME")

        if tf:

            self.market.timeframe = tf


settings = Settings()

settings.load_env()

try:

    settings.load_json("settings.json")

except Exception:

    pass