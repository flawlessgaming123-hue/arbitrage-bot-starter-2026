"""Arbitrage scanner — finds profitable spreads across markets.

TODO (US-002): Wire up to real fetcher output and add ranking logic.
"""

from dataclasses import dataclass


@dataclass
class Opportunity:
    contract: str
    market_a: str
    market_b: str
    price_a: float
    price_b: float
    gross_spread: float
    net_spread: float
    profitable: bool


def calculate_spread(
    contract: str,
    market_a: str,
    price_a: float,
    market_b: str,
    price_b: float,
    fee_pct: float = 0.02,
) -> Opportunity:
    """Calculate net arbitrage spread between two market prices."""
    gross = abs(price_a - price_b)
    net = gross - fee_pct
    return Opportunity(
        contract=contract,
        market_a=market_a,
        market_b=market_b,
        price_a=round(price_a, 4),
        price_b=round(price_b, 4),
        gross_spread=round(gross, 4),
        net_spread=round(net, 4),
        profitable=net > 0.005,
    )


def scan(prices_by_market: dict[str, list[dict]], min_spread: float = 0.005) -> list[Opportunity]:
    """Scan all markets for arbitrage opportunities above min_spread."""
    # TODO: Implement cross-market matching and ranking
    return []
