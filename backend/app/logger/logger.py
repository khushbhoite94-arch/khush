"""
AEGIS AI v2
Professional Logger

Features
--------
✔ Colored Console Logs
✔ File Logging
✔ Trade Logging
✔ AI Logging
✔ Performance Timer
✔ Exception Logger
✔ Singleton
"""

from __future__ import annotations

import logging
import traceback
import time

from pathlib import Path
from logging.handlers import RotatingFileHandler

from app.config import settings


# ============================================================
# COLORS
# ============================================================

RESET = "\033[0m"

RED = "\033[91m"

GREEN = "\033[92m"

YELLOW = "\033[93m"

BLUE = "\033[94m"

CYAN = "\033[96m"


# ============================================================
# LOGGER
# ============================================================


class Logger:

    _instance = None

    # --------------------------------------------------------

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._setup()

        return cls._instance

    # --------------------------------------------------------

    def _setup(self):

        self.logger = logging.getLogger("AEGIS")

        self.logger.setLevel(logging.INFO)

        self.logger.handlers.clear()

        formatter = logging.Formatter(

            "[%(asctime)s] %(levelname)s | %(message)s",

            "%H:%M:%S",

        )

        if settings.logging.console:

            console = logging.StreamHandler()

            console.setFormatter(formatter)

            self.logger.addHandler(console)

        if settings.logging.file:

            log_folder = Path(settings.logging.folder)

            log_folder.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(

                log_folder / "aegis.log",

                maxBytes=5 * 1024 * 1024,

                backupCount=10,

            )

            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    # --------------------------------------------------------

    def info(self, message):

        print(f"{BLUE}[INFO]{RESET} {message}")

        self.logger.info(message)

    # --------------------------------------------------------

    def success(self, message):

        print(f"{GREEN}[SUCCESS]{RESET} {message}")

        self.logger.info(message)

    # --------------------------------------------------------

    def warning(self, message):

        print(f"{YELLOW}[WARNING]{RESET} {message}")

        self.logger.warning(message)

    # --------------------------------------------------------

    def error(self, message):

        print(f"{RED}[ERROR]{RESET} {message}")

        self.logger.error(message)

    # --------------------------------------------------------

    def exception(self, e):

        print(f"{RED}EXCEPTION{RESET}")

        traceback.print_exc()

        self.logger.exception(e)

    # --------------------------------------------------------

    def trade(

        self,

        action,

        symbol,

        entry,

        sl,

        tp,

    ):

        line = "=" * 70

        print()

        print(line)

        print(f"{CYAN}TRADE EXECUTED{RESET}")

        print()

        print("Action :", action)

        print("Symbol :", symbol)

        print("Entry  :", entry)

        print("SL     :", sl)

        print("TP     :", tp)

        print(line)

        print()

        self.logger.info(

            f"TRADE {action} {symbol} Entry={entry} SL={sl} TP={tp}"

        )

    # --------------------------------------------------------

    def ai(

        self,

        result: dict,

    ):

        line = "=" * 70

        print()

        print(line)

        print(f"{CYAN}AI DECISION{RESET}")

        print()

        for k, v in result.items():

            print(f"{k:<15}: {v}")

        print()

        print(line)

        print()

    # --------------------------------------------------------

    def timer(self):

        return Timer()

    # --------------------------------------------------------

    def separator(self):

        print("=" * 70)


# ============================================================
# TIMER
# ============================================================


class Timer:

    def __init__(self):

        self.start = time.perf_counter()

    def stop(self, name="Task"):

        elapsed = time.perf_counter() - self.start

        print(f"{GREEN}{name}{RESET} finished in {elapsed:.4f}s")


# ============================================================
# GLOBAL LOGGER
# ============================================================

logger = Logger()