"""
AEGIS AI
Central Logging System
"""

from pathlib import Path
import sys

from loguru import logger

from app.core.config import settings


class LoggerManager:
    """
    Configures Loguru for the entire application.
    """

    def __init__(self):

        self.log_root = settings.LOG_DIR

        self._create_directories()

        logger.remove()

        # Console
        logger.add(
            sys.stdout,
            level="INFO",
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                   "<level>{message}</level>",
        )

        self._add_file_logger("system/system.log")
        self._add_file_logger("browser/browser.log")
        self._add_file_logger("trading/trading.log")
        self._add_file_logger("ai/ai.log")
        self._add_file_logger("database/database.log")
        self._add_file_logger("security/security.log")
        self._add_file_logger("errors/errors.log")

    def _create_directories(self):

        folders = [
            "system",
            "browser",
            "trading",
            "ai",
            "database",
            "security",
            "errors",
        ]

        for folder in folders:
            Path(self.log_root / folder).mkdir(
                parents=True,
                exist_ok=True,
            )

    def _add_file_logger(self, filename):

        logger.add(
            self.log_root / filename,
            rotation="25 MB",
            retention="30 days",
            compression="zip",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            level="DEBUG",
        )


LoggerManager()

log = logger
