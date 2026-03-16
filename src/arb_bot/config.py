"""Configuration loader — reads from environment variables with sensible defaults."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    # Market API keys
    polymarket_api_key: str = ""
    kalshi_api_key: str = ""
    predictit_api_key: str = ""

    # Risk parameters
    max_single_position_pct: float = 2.0
    max_total_exposure_pct: float = 20.0
    min_spread_pct: float = 0.5

    # Notification
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Database
    database_url: str = ""


def load_config() -> Config:
    """Load config from environment variables."""
    return Config(
        polymarket_api_key=os.getenv("POLYMARKET_API_KEY", ""),
        kalshi_api_key=os.getenv("KALSHI_API_KEY", ""),
        predictit_api_key=os.getenv("PREDICTIT_API_KEY", ""),
        max_single_position_pct=float(os.getenv("MAX_SINGLE_POSITION_PCT", "2.0")),
        max_total_exposure_pct=float(os.getenv("MAX_TOTAL_EXPOSURE_PCT", "20.0")),
        min_spread_pct=float(os.getenv("MIN_SPREAD_PCT", "0.5")),
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        database_url=os.getenv("DATABASE_URL", ""),
    )
