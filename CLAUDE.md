# Arbitrage Bot — Project Rules

These rules are loaded into every Claude Code session automatically.
Ralph iterations, skills, and agent teams all inherit them.

## Architecture

- Target markets: Polymarket, Kalshi, PredictIt
- All prices stored as USD with 4 decimal precision (e.g. 0.5234)
- Every trade proposal must pass through the `/risk-manager` skill before execution
- Data flows: Market API -> Postgres -> Scanner -> Risk Gate -> Execution

## Workflow

When working on prd.json stories, follow this order:

1. Read prd.json and pick the first story where `passes` is `false`
2. Implement the story (code, tests, docs as needed)
3. Run tests — the story only passes if tests pass
4. Update prd.json: set `status` to `"done"` and `passes` to `true`
5. Commit with message format: `feat(US-XXX): short description`
6. Move to the next story

## Skills Available

- `/arbitrage-scanner` — pulls prices, calculates spreads, ranks opportunities
- `/risk-manager` — validates trade size, enforces portfolio caps, blocks violations

Claude will auto-invoke these when relevant based on their descriptions.
You can also invoke them explicitly with the slash command.

## MCP Tools

- `telegram` — send notifications (use for alerts on >1% edges)
- `postgres-prices` — read/write market price data

## Hard Rules (never violate)

- NEVER commit `.env`, API keys, or secrets — the PreToolUse hook will block this
- NEVER use real money without explicit human approval in the chat
- NEVER skip the risk-manager skill before any trade logic
- NEVER exceed 2% portfolio risk on any single position
- Always run tests before marking a story as done
- Keep each commit focused on one story

## Code Standards

- Python 3.11+, type hints on all public functions
- Tests in `tests/` using pytest
- Format with black, lint with ruff
- Async where possible (aiohttp for market APIs)
