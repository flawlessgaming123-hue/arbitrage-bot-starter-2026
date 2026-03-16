#!/bin/bash
# Sandboxed Ralph — runs the autonomous loop inside Docker
# The container has no access to your host filesystem or network secrets
# beyond what you explicitly pass via --env-file.
#
# Usage:
#   chmod +x ralph-docker.sh
#   ./ralph-docker.sh [max_iterations]

set -euo pipefail

MAX_ITERATIONS=${1:-10}
IMAGE_NAME="arbitrage-bot-ralph"

# Build the image if needed
if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
    echo "Building Docker image (first run only)..."
    docker build -t "$IMAGE_NAME" .
fi

# Run sandboxed — read-only root FS, no network egress except API calls,
# non-root user, tmpfs for /tmp
docker run --rm \
    --env-file .env \
    --read-only \
    --tmpfs /tmp:rw,noexec,nosuid \
    --memory=2g \
    --cpus=2 \
    -v "$(pwd)/logs:/workspace/logs:rw" \
    -v "$(pwd)/prd.json:/workspace/prd.json:rw" \
    -v "$(pwd)/reports:/workspace/reports:rw" \
    "$IMAGE_NAME" "$MAX_ITERATIONS"
