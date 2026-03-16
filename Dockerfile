FROM node:22-slim

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    git jq curl bash \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @anthropic-ai/claude-code

RUN useradd -m -s /bin/bash botuser

WORKDIR /workspace
COPY . .
RUN mkdir -p logs reports data \
    && chown -R botuser:botuser /workspace

RUN python3 -m venv /workspace/.venv \
    && /workspace/.venv/bin/pip install --no-cache-dir -r requirements.txt

USER botuser
ENV PATH="/workspace/.venv/bin:$PATH"

# Ralph needs a git repo for commits
RUN git config --global user.email "ralph@bot" \
    && git config --global user.name "Ralph Bot" \
    && git init && git add -A && git commit -m "init: container baseline"

ENTRYPOINT ["bash", "ralph.sh"]
