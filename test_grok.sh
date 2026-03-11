#!/bin/bash

# Test if we can call Grok via OpenClaw
echo '{"messages": [{"role": "user", "content": "What is 2 + 2?"}], "model": "xai/grok-4-1-fast-reasoning"}' | \
  openclaw session eval --model xai/grok-4-1-fast-reasoning --json 2>/dev/null || echo "Failed to eval"
