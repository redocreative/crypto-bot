# Trading Strategy v2.0 — Momentum + LLM Sentiment (Bybit Spot)

**Last Updated:** 2026-03-13  
**Goal:** 55%+ win rate with <10% max drawdown

## Signals (Confluence Required)
1. **Technical (60% weight)** — Multi-TF EMA crossover + RSI
2. **LLM Sentiment (30% weight)** — Browser scan of X/Reddit (bullish score >70)
3. **Regime (10% weight)** — BTC dominance <55% + Fear & Greed <65

## Entry
- Long only when all 3 align + volume spike
- Size: 1% of portfolio
- Stop: 2× ATR below entry
- TP1: +4% (50%), TP2: +8% (trailing)

## Risk Rules (Non-Negotiable)
- Max 1% risk per trade
- Max 5 open positions
- Pause if daily loss >3% or weekly >8%
- No trading 22:00-06:00 UTC
- Paper mode until 100 trades validated

## Execution Flow
Trader agent → RiskManager approval → Bybit order

Backtest first, then paper 2 weeks, then $100 live.