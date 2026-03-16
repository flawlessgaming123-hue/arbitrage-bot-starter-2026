"""Risk manager — validates trades against portfolio limits.

TODO (US-003): Load portfolio state from data/portfolio.json.
"""

from dataclasses import dataclass


@dataclass
class RiskDecision:
    approved: bool
    trade_size_usd: float
    pct_of_portfolio: float
    reason: str


def check_risk(
    trade_size_usd: float,
    portfolio_value: float = 10000.0,
    max_position_pct: float = 2.0,
) -> RiskDecision:
    """Check if a proposed trade passes risk limits."""
    pct = (trade_size_usd / portfolio_value) * 100
    approved = pct <= max_position_pct
    return RiskDecision(
        approved=approved,
        trade_size_usd=trade_size_usd,
        pct_of_portfolio=round(pct, 2),
        reason="Within limit" if approved else f"Exceeds {max_position_pct}% limit ({pct:.1f}%)",
    )
