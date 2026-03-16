#!/bin/bash
# One-command setup for arbitrage-bot-starter-2026
# Run: bash setup-arbitrage-starter.sh
set -euo pipefail

echo "Setting up arbitrage-bot-starter-2026..."

# Create directories
mkdir -p arbitrage-bot-starter-2026/.claude/skills/arbitrage-scanner
mkdir -p arbitrage-bot-starter-2026/.claude/skills/risk-manager
mkdir -p arbitrage-bot-starter-2026/logs
mkdir -p arbitrage-bot-starter-2026/reports
mkdir -p arbitrage-bot-starter-2026/data
mkdir -p arbitrage-bot-starter-2026/tests

cd arbitrage-bot-starter-2026

# Gitkeep for empty dirs
touch logs/.gitkeep reports/.gitkeep data/.gitkeep tests/__init__.py

# Init git, add all, commit
git init
chmod +x ralph.sh
git add -A
git commit -m "init: arbitrage-bot-starter-2026 — Ralph + Skills + Hooks + MCP + LangGraph"

echo ""
echo "Setup complete. Next steps:"
echo "  cd arbitrage-bot-starter-2026"
echo "  cp .env.example .env         # fill in API keys"
echo "  pip install -r requirements.txt"
echo "  chmod +x ralph.sh"
echo "  ./ralph.sh                   # start autonomous loop"
echo ""
echo "To push public:"
echo "  gh repo create arbitrage-bot-starter-2026 --public --source . --push"
