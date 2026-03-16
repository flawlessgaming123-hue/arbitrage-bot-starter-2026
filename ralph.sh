#!/bin/bash
# Ralph Loop — autonomous Claude Code iterations
# Based on https://github.com/snarktank/ralph
#
# Each iteration spawns a fresh Claude instance with clean context.
# Memory persists through git history + prd.json + CLAUDE.md.
# Loop terminates when all prd.json stories have passes=true.

set -euo pipefail

MAX_ITERATIONS=${1:-10}
ITERATION=0
TOTAL_COST=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COST_LOG="$SCRIPT_DIR/logs/cost.csv"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${GREEN}Starting Ralph Loop (March 2026 meta)${NC}"
echo "  Max iterations: $MAX_ITERATIONS"
echo "  PRD: prd.json"
echo "  Skills: .claude/skills/"
echo "  Hooks: .claude/settings.json"
echo ""

# Check prerequisites
if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code${NC}"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq not found. Install with your package manager.${NC}"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/prd.json" ]; then
    echo -e "${RED}Error: prd.json not found in $SCRIPT_DIR${NC}"
    exit 1
fi

cd "$SCRIPT_DIR"
mkdir -p logs reports data

# Initialize cost log
if [ ! -f "$COST_LOG" ]; then
    echo "iteration,story,input_tokens,output_tokens,estimated_cost_usd,timestamp" > "$COST_LOG"
fi

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))

    # Check how many stories remain
    REMAINING=$(jq '[.stories[] | select(.passes == false)] | length' prd.json)

    if [ "$REMAINING" -eq 0 ]; then
        echo -e "${GREEN}All stories complete! Bot ready for paper trading.${NC}"
        echo -e "${CYAN}Total estimated cost: \$${TOTAL_COST}${NC}"
        exit 0
    fi

    # Get next incomplete story
    NEXT_STORY=$(jq -r '[.stories[] | select(.passes == false)][0].id' prd.json)
    NEXT_TITLE=$(jq -r '[.stories[] | select(.passes == false)][0].title' prd.json)

    echo -e "${YELLOW}--- Iteration $ITERATION/$MAX_ITERATIONS ---${NC}"
    echo "  Remaining stories: $REMAINING"
    echo "  Working on: $NEXT_STORY — $NEXT_TITLE"
    echo "  Running cost: \$${TOTAL_COST}"
    echo ""

    # Build the prompt for this iteration
    PROMPT="You are working on the arbitrage bot project. Read CLAUDE.md for project rules.

Current task: Implement story $NEXT_STORY — '$NEXT_TITLE'

Steps:
1. Read prd.json to understand the full story description
2. Check git log to see what previous iterations have built
3. Look at the existing code in src/arb_bot/ — build on what's there
4. Implement the story (write code, tests, configs as needed)
5. Run tests to verify: pytest tests/ -v
6. If tests pass, update prd.json: set this story's status to 'done' and passes to true
7. Commit your work: git add -A && git commit -m 'feat($NEXT_STORY): $NEXT_TITLE'

If you get stuck, document what's blocking in a comment in prd.json and move on."

    ITER_START=$(date +%s)

    # Run Claude Code in headless mode with JSON output for cost tracking
    # --dangerously-skip-permissions enables full autonomy (use ralph-docker.sh for sandboxing!)
    OUTPUT=$(echo "$PROMPT" | claude --dangerously-skip-permissions \
        --print \
        --max-turns 25 \
        --output-format json \
        2>&1) || true

    # Save full output
    echo "$OUTPUT" > "logs/iteration-${ITERATION}.json"

    # Extract cost data from JSON output
    INPUT_TOKENS=$(echo "$OUTPUT" | jq -r '.usage.input_tokens // 0' 2>/dev/null || echo "0")
    OUTPUT_TOKENS=$(echo "$OUTPUT" | jq -r '.usage.output_tokens // 0' 2>/dev/null || echo "0")

    # Estimate cost (Sonnet 4.6 pricing: $3/M input, $15/M output — adjust for your model)
    ITER_COST=$(echo "scale=4; ($INPUT_TOKENS * 0.000003) + ($OUTPUT_TOKENS * 0.000015)" | bc 2>/dev/null || echo "0")
    TOTAL_COST=$(echo "scale=4; $TOTAL_COST + $ITER_COST" | bc 2>/dev/null || echo "$TOTAL_COST")

    # Log cost
    echo "$ITERATION,$NEXT_STORY,$INPUT_TOKENS,$OUTPUT_TOKENS,$ITER_COST,$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$COST_LOG"

    ITER_ELAPSED=$(( $(date +%s) - ITER_START ))

    echo ""
    echo -e "Iteration $ITERATION complete (${ITER_ELAPSED}s, ~\$${ITER_COST})"
    echo ""

    # Brief pause between iterations
    sleep 5
done

# Final check
REMAINING=$(jq '[.stories[] | select(.passes == false)] | length' prd.json)
if [ "$REMAINING" -eq 0 ]; then
    echo -e "${GREEN}All stories complete after $ITERATION iterations!${NC}"
else
    echo -e "${RED}Hit max iterations ($MAX_ITERATIONS). $REMAINING stories remaining.${NC}"
    echo "Run ./ralph.sh again to continue, or increase max: ./ralph.sh 20"
fi

echo -e "${CYAN}Total estimated cost: \$${TOTAL_COST}${NC}"
echo -e "${CYAN}Cost log: $COST_LOG${NC}"
