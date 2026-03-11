#!/usr/bin/env python3
"""Direct Grok API test - shows real token usage"""
import requests
import json
import os

XAI_API_KEY = os.environ.get("XAI_API_KEY")
if not XAI_API_KEY:
    print("ERROR: XAI_API_KEY not set")
    exit(1)

prompt = """
Evaluate these 3 crypto APIs for trading:
1. Binance Futures
2. OKX Futures
3. Kraken Futures

Which is best for real-time data? Explain in 2-3 sentences.
"""

response = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {XAI_API_KEY}"
    },
    json={
        "model": "grok-4-1-fast-reasoning",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }
)

data = response.json()

print("=== GROK 4.1 RESPONSE ===\n")
print("ANSWER:")
print(data["choices"][0]["message"]["content"])
print("\n=== TOKEN USAGE ===")
print(f"Prompt tokens: {data['usage']['prompt_tokens']}")
print(f"Completion tokens: {data['usage']['completion_tokens']}")
print(f"Reasoning tokens: {data['usage']['completion_tokens_details']['reasoning_tokens']}")
print(f"Total tokens: {data['usage']['total_tokens']}")
print(f"\nCost (USD ticks): {data['usage']['cost_in_usd_ticks']}")
print(f"Cost (USD): ${data['usage']['cost_in_usd_ticks'] / 1e7:.6f}")
