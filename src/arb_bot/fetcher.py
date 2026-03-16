"""Market price fetchers — one async function per exchange.

TODO (US-001): Implement real API calls.
These stubs return sample data so the scanner can be developed in parallel.
"""

from datetime import datetime, timezone
from typing import Any


async def fetch_polymarket(api_key: str) -> list[dict[str, Any]]:
    """Fetch current contract prices from Polymarket."""
    # TODO: Replace with real aiohttp call to Polymarket API
    return [
        {
            "market": "polymarket",
            "contract": "BTC > 100k by July",
            "yes_price": 0.6234,
            "no_price": 0.3766,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        },
    ]


async def fetch_kalshi(api_key: str) -> list[dict[str, Any]]:
    """Fetch current contract prices from Kalshi."""
    # TODO: Replace with real aiohttp call to Kalshi API
    return [
        {
            "market": "kalshi",
            "contract": "BTC > 100k by July",
            "yes_price": 0.6089,
            "no_price": 0.3911,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        },
    ]
