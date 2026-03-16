---
name: arbitrage-scanner
description: Scan prediction markets for arbitrage opportunities. Use when the user mentions scanning, spreads, arbitrage, opportunities, or price differences across markets.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Arbitrage Scanner

You are scanning for arbitrage opportunities across prediction markets.

## Steps

1. **Fetch current prices** from all configured markets using the `postgres-prices` MCP tool.
   If MCP is unavailable, read from any cached price files in `data/`.

2. **Match equivalent contracts** across Polymarket, Kalshi, and PredictIt.
   Match by event slug/title similarity (normalize whitespace, case-insensitive).

3. **Calculate net spread** for each matched pair:
   ```
   spread = abs(market_a_price - market_b_price) - estimated_fees
   ```
   Use 2% combined fee estimate unless configured otherwise.

4. **Filter** to spreads > 0.5% (configurable via `MIN_SPREAD_PCT` env var).

5. **Rank** by net profit potential (spread * estimated available liquidity).

6. **Output report** to `reports/scan-$(date +%Y%m%d-%H%M%S).md` with:
   - Timestamp
   - Number of markets scanned
   - Each opportunity: markets, contract, prices, spread %, estimated profit
   - Summary statistics

7. **Notify** via Telegram MCP if any opportunity exceeds 1% edge.

## Important

- All prices must be in USD with 4 decimal precision
- Never execute trades — this skill only scans and reports
- Always invoke `/risk-manager` before any downstream trade logic
