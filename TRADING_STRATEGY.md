# Trading Strategy v3.0 — Momentum + LLM Sentiment (Alpaca Paper Only)

**Last Updated:** 2026-03-13  
**Mode:** Paper trading (Alpaca sandbox) — NO real money

## Signals (Full Confluence Required)
1. Technical (60%) — 15m/1h/4h EMA 9/21 crossover + RSI(14) <35 or >65 + volume
2. LLM Sentiment (30%) — Grok scores X/Reddit/news (bullish >70)
3. Regime (10%) — BTC dominance + Fear & Greed (free)

## Entry / Risk Rules
- Long only on full confluence (BTC/USD, ETH/USD + 2 alts)
- Size: 1% of paper portfolio
- Stop: 2× ATR
- TP: +4% (50%) + trailing
- Max 5 positions
- Pause if daily paper loss >3%

## Execution
Trader runs every 15 min → logs everything → sends Telegram summary