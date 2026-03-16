# Arbitrage Bot Starter 2026

The real autonomous AI coding stack — not vibes, everything actually runs.

Built on the pattern Boris Cherny (creator of Claude Code) showed in his viral Jan 2026 thread:
multiple parallel Claude instances, each with fresh context, persisting memory through git.
This repo packages that into a single `./ralph.sh` that loops until your PRD is complete.

## The Stack

| Layer | What | Why |
|-------|------|-----|
| **Ralph** | Autonomous bash loop | Fresh context each iteration, memory via git + prd.json |
| **Claude Code CLI** | `claude -p --print` headless mode | Non-interactive execution with tool permissions |
| **Skills** | `.claude/skills/*/SKILL.md` | Reusable, auto-triggered agent instructions |
| **Hooks** | `.claude/settings.json` hooks | Safety gates — block sensitive files, auto-format, validate |
| **MCP** | `.mcp.json` server config | External tools (Telegram alerts, Postgres prices) |
| **Agent Teams** | Experimental multi-agent | Parallel agents with independent context windows |
| **LangGraph** | Production upgrade path | When you outgrow bash loops and need real state machines |

## Quick Start

```bash
# 1. Clone and setup
git clone <your-repo-url> && cd arbitrage-bot-starter-2026
cp .env.example .env   # fill in your API keys
pip install -r requirements.txt
pip install -e .        # install src/arb_bot as editable package

# 2. Run the autonomous loop
chmod +x ralph.sh
./ralph.sh              # loops until all PRD stories pass

# 2b. (Safer) Run sandboxed in Docker
chmod +x ralph-docker.sh
./ralph-docker.sh       # same loop, but in a locked-down container

# 3. Production upgrade (when ready)
python langgraph_starter.py
```

## Security: Why Docker Matters

`ralph.sh` uses `--dangerously-skip-permissions` which gives Claude **unrestricted shell access**.
That's fine for rapid prototyping on a throwaway machine — dangerous on your main dev box.

`ralph-docker.sh` wraps the same loop in a container with:
- **Read-only root filesystem** (can't modify system files)
- **Non-root user** (no privilege escalation)
- **Memory cap** (2GB — prevents runaway processes)
- Only `logs/`, `prd.json`, and `reports/` are writable from host

## How Ralph Actually Works

Each iteration:
1. Spawns a **fresh** Claude Code instance (`claude -p --print`)
2. Claude reads CLAUDE.md rules, discovers skills, connects MCP tools
3. Picks the next incomplete story from `prd.json`
4. Implements, tests, commits
5. Loop checks `jq '[.stories[] | select(.passes == false)] | length' prd.json`
6. If 0 remaining — done. Otherwise, next iteration with clean context.

Memory survives across iterations through **git history** (not fragile context windows).

## How Skills Work

Skills live at `.claude/skills/<name>/SKILL.md` with YAML frontmatter.
Claude reads all skill descriptions at session start (~100 tokens each).
When your conversation matches a skill's `description`, Claude auto-invokes it.

You can also invoke manually: `/arbitrage-scanner` or `/risk-manager`.

## How Hooks Work

Hooks are configured in `.claude/settings.json` (not shell scripts in a hooks dir).
They fire on events like `PreToolUse`, `PostToolUse`, `Stop`, etc.
Exit code 2 = block the action. Exit code 0 = proceed.

This repo ships with:
- **PreToolUse** hook on Bash: checks `git diff --cached --name-only` and blocks if staged files match `.env|.key|.secret|.pem|credentials`
- **PostToolUse** hook on Edit/Write: auto-runs `ruff check --fix` on any modified `.py` file

## Agent Teams (Experimental)

Requires Opus 4.6 + `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=true`.
One session is team lead, teammates get independent context windows.
Communication happens via JSON inbox files on disk.

## File Structure

```
arbitrage-bot-starter-2026/
├── README.md                              # You're here
├── CLAUDE.md                              # Rules Claude always follows
├── prd.json                               # Stories — Ralph loops until all pass
├── pyproject.toml                         # Python project config + pytest/ruff settings
├── .claude/
│   ├── settings.json                      # Hooks config (real format)
│   └── skills/
│       ├── arbitrage-scanner/SKILL.md     # Auto-triggered scanner
│       └── risk-manager/SKILL.md          # Auto-triggered risk gate
├── src/arb_bot/                           # Source scaffolding (Claude builds on these stubs)
│   ├── __init__.py
│   ├── config.py                          # Env-based configuration loader
│   ├── fetcher.py                         # Async market price fetchers (TODO stubs)
│   ├── scanner.py                         # Spread calculation + opportunity ranking
│   └── risk.py                            # Portfolio risk validation
├── tests/
│   ├── conftest.py                        # Shared fixtures
│   ├── test_scanner.py                    # Scanner unit tests
│   └── test_risk.py                       # Risk manager unit tests
├── .mcp.json                              # MCP server config
├── .env.example                           # API keys template
├── .gitignore                             # Keeps secrets out of git
├── ralph.sh                               # The autonomous loop (with cost tracking)
├── ralph-docker.sh                        # Sandboxed Docker wrapper
├── Dockerfile                             # Container definition for sandboxed runs
├── langgraph_starter.py                   # Production LangGraph agent (upgrade path)
└── requirements.txt                       # Python dependencies
```

## What This Is NOT

- Not a finished arbitrage bot (it's a **starter** that builds one autonomously)
- Not financial advice — paper trade only until you know what you're doing
- Not a toy — the Ralph loop + skills + hooks pattern is production-grade

## References

- [Ralph repo](https://github.com/snarktank/ralph) — the autonomous loop
- [Claude Code Skills docs](https://code.claude.com/docs/en/skills)
- [Claude Code Hooks docs](https://code.claude.com/docs/en/hooks)
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Agent Teams docs](https://code.claude.com/docs/en/agent-teams)
- [LangGraph + Anthropic](https://docs.langchain.com/oss/python/integrations/chat/anthropic)
