"""Shared test fixtures for the arbitrage bot."""

import pytest

from arb_bot.config import Config


@pytest.fixture
def config() -> Config:
    """Default test config — no real API keys needed."""
    return Config(
        max_single_position_pct=2.0,
        max_total_exposure_pct=20.0,
        min_spread_pct=0.5,
    )


@pytest.fixture
def sample_prices() -> dict[str, list[dict]]:
    """Sample price data for two markets with a known spread."""
    return {
        "polymarket": [
            {"contract": "BTC > 100k by July", "yes_price": 0.6234, "no_price": 0.3766},
        ],
        "kalshi": [
            {"contract": "BTC > 100k by July", "yes_price": 0.6089, "no_price": 0.3911},
        ],
    }
