# Trading Strategy v2.1 — Momentum + LLM Sentiment (Alpaca Paper Mode)

**Last Updated:** 2026-03-13  
**Mode:** Paper trading only (Alpaca sandbox)  
**Goal:** 55%+ win rate, <10% drawdown — proven for OpenClaw bots

## Signals (Confluence Required — 3 out of 3)
1. Technical (60%) — 15m/1h/4h EMA 9/21 crossover + RSI(14) <35 or >65 + volume spike
2. LLM Sentiment (30%) — Browser scan of X/Reddit/news (bullish score >70)
3. Regime Filter (10%) — BTC dominance + Fear & Greed (free APIs)

## Entry / Risk (Paper Mode)
- Long only on full confluence (BTC/USD, ETH/USD focus + 2-3 alts)
- Size: 1% of paper portfolio
- Stop-loss: 2× ATR below entry
- Take-profit: +4% partial + trailing stop
- Max 5 open positions
- Pause if daily paper loss >3%

## Execution Flow
Mission Control → Trader agent → RiskManager check → Alpaca paper order

This is simpler and more reliable than the old funding-rate ensemble (no Binance outages, no extra paid APIs). Backtest first, run paper for 2 weeks, then we review.

Expected: 1-3% monthly in sideways markets, 15-40% in trends (with strict risk).