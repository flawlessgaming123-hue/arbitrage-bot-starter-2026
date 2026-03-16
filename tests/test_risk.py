"""Tests for the risk manager."""

from arb_bot.risk import check_risk


def test_risk_within_limit():
    result = check_risk(trade_size_usd=150.0, portfolio_value=10000.0)
    assert result.approved is True
    assert result.pct_of_portfolio == 1.5


def test_risk_at_exact_limit():
    result = check_risk(trade_size_usd=200.0, portfolio_value=10000.0)
    assert result.approved is True
    assert result.pct_of_portfolio == 2.0


def test_risk_exceeds_limit():
    result = check_risk(trade_size_usd=300.0, portfolio_value=10000.0)
    assert result.approved is False
    assert result.pct_of_portfolio == 3.0
    assert "Exceeds" in result.reason


def test_risk_custom_limit():
    result = check_risk(trade_size_usd=500.0, portfolio_value=10000.0, max_position_pct=5.0)
    assert result.approved is True
    assert result.pct_of_portfolio == 5.0
