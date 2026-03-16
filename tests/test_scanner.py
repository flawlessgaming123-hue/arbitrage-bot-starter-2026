"""Tests for the arbitrage scanner."""

from arb_bot.scanner import calculate_spread


def test_calculate_spread_profitable():
    """A spread of 0.0145 minus 0.02 fees is negative — not profitable."""
    opp = calculate_spread(
        contract="BTC > 100k by July",
        market_a="polymarket",
        price_a=0.6234,
        market_b="kalshi",
        price_b=0.6089,
        fee_pct=0.02,
    )
    assert opp.gross_spread == 0.0145
    assert opp.net_spread == round(0.0145 - 0.02, 4)
    assert opp.profitable is False


def test_calculate_spread_with_large_gap():
    """A spread large enough to overcome fees should be flagged profitable."""
    opp = calculate_spread(
        contract="Test Contract",
        market_a="polymarket",
        price_a=0.70,
        market_b="kalshi",
        price_b=0.65,
        fee_pct=0.02,
    )
    assert opp.gross_spread == 0.05
    assert opp.net_spread == 0.03
    assert opp.profitable is True
