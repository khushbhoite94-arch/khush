"""
AEGIS AI
Configuration Manager
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        extra="ignore",
        case_sensitive=False,
    )

    # -------------------------------------------------
    # Application
    # -------------------------------------------------

    APP_NAME: str = "AEGIS AI"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    HOST: str = "127.0.0.1"

    PORT: int = 8000

    # -------------------------------------------------
    # MongoDB
    # -------------------------------------------------

    MONGODB_URI: str = Field(
        default="mongodb://localhost:27017"
    )

    DATABASE_NAME: str = "aegis_ai"

    # -------------------------------------------------
    # Browser
    # -------------------------------------------------

    HEADLESS: bool = False

    BROWSER_PROFILE: str = "browser/profile"

    BROWSER_STATE: str = "browser/state"

    SCREENSHOT_PATH: str = "screenshots"

    DOWNLOAD_PATH: str = "browser/downloads"

    # -------------------------------------------------
    # Trading
    # -------------------------------------------------

    DEFAULT_PAIR: str = "EURUSD"

    DEFAULT_TIMEFRAME: str = "M5"

    DEFAULT_STYLE: str = "INTRADAY"

    DEFAULT_SESSION: str = "LONDON"

    AI_CONFIDENCE: int = 90

    RISK_PER_TRADE: float = 1.0

    # -------------------------------------------------
    # Paths
    # -------------------------------------------------

    LOG_DIR: Path = ROOT_DIR / "logs"

    DATA_DIR: Path = ROOT_DIR / "data"

    PROFILE_DIR: Path = ROOT_DIR / "browser/profile"

    STATE_DIR: Path = ROOT_DIR / "browser/state"

    SCREENSHOT_DIR: Path = ROOT_DIR / "screenshots"

    DOWNLOAD_DIR: Path = ROOT_DIR / "browser/downloads"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()