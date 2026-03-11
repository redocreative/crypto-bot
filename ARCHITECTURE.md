# 🏗️ ARCHITECTURE.md - Crypto Trading Bot System Design

**Version:** 2.0 (Phase 1: Core Infrastructure)  
**Date:** 2026-03-08  
**Status:** Active

## System Overview

Mission Control now coordinates a **specialized agent team** instead of a single trader. Each agent owns one domain and reports back.

```
┌─────────────────────────────────────────────────────┐
│         MISSION CONTROL (main agent)                │
│   Coordinator, delegates, receives reports          │
└──────┬─────────────────────────────┬────────────────┘
       │                             │
    ┌──▼──────────────┐      ┌──────▼──────────────┐
    │  DataFetcher    │      │      Trader         │
    │  (Gemini Flash) │      │   (Claude Haiku)    │
    │                 │      │                     │
    │ Fetches: prices,│      │ Proposes trades,    │
    │ volumes, data   │      │ manages positions   │
    │ Updates every   │      │ Reads: market data, │
    │ 5 minutes       │      │ STRATEGY.md         │
    └────────┬────────┘      └──────────┬──────────┘
             │                         │
       ┌─────▼────────────────────────▼────────┐
       │      RiskManager                       │
       │    (Claude Haiku)                      │
       │                                        │
       │ Approves/rejects trades                │
       │ Enforces position limits, stops        │
       │ Calculates position sizes              │
       │ Pauses trading if limits breached      │
       └─────────────────────────┬──────────────┘
                                 │
                        ┌────────▼─────────┐
                        │  Monitor          │
                        │ (Gemini Flash)    │
                        │                   │
                        │ 24/7 health check │
                        │ Alerts on errors  │
                        │ Daily P&L report  │
                        │ Sends to Telegram │
                        └───────────────────┘
```

## Agent Responsibilities

### main (Mission Control)
- **Role:** Coordinator and delegation hub
- **Model:** Claude Haiku 4.5
- **Responsibilities:**
  - Receives user commands ("start trading", "pause", etc.)
  - Spawns other agents as needed
  - Receives status reports from specialists
  - Makes high-level decisions

### trader
- **Role:** Trade execution engine
- **Model:** Claude Haiku 4.5
- **Responsibilities:**
  - Reads market data from DataFetcher
  - Reads STRATEGY.md for trading rules
  - Proposes trades to RiskManager
  - Executes approved trades via Alpaca API
  - Manages open positions
  - Logs all activity to TRADE_LOG.md
- **Files:**
  - Reads: MARKET_DATA.md (from data-fetcher), STRATEGY.md, EXCHANGE_CONFIG.md
  - Writes: TRADE_STATE.md, TRADE_LOG.md

### data-fetcher
- **Role:** Real-time market data provider
- **Model:** Gemini Flash (cheap, always-on)
- **Responsibilities:**
  - Fetches live BTC/ETH prices from Alpaca every 5 minutes
  - Calculates indicators (24h MA, ATR, volume ratio)
  - Validates data quality (sanity checks)
  - Writes clean data to MARKET_DATA.md
  - Logs API errors and warnings
  - Provides fallback cached data if API fails
- **Files:**
  - Reads: ../trader/workspace/EXCHANGE_CONFIG.md
  - Writes: MARKET_DATA.md, DATA_QUALITY_LOG.md, MARKET_DATA_CACHE.json
- **Schedule:** Every 5 minutes, 24/7

### risk-manager
- **Role:** Safeguard enforcement and position sizing
- **Model:** Claude Haiku 4.5 (fast for real-time decisions)
- **Responsibilities:**
  - Receives trade proposals from Trader
  - Reads current positions from TRADE_STATE.md
  - Calculates risk and position size based on 2% rule
  - Checks against RISK_CONFIG.md limits
  - Approves (with final size) or rejects (with reasoning)
  - Enforces drawdown stops (pause at -5% daily, -10% weekly, -20% overall)
  - Logs all decisions to RISK_LOG.md
- **Files:**
  - Reads: ../trader/workspace/TRADE_STATE.md, ../trader/workspace/STRATEGY.md, RISK_CONFIG.md
  - Writes: RISK_LOG.md
- **Schedule:** On-demand (called by Trader for each proposal)

### monitor
- **Role:** 24/7 system oversight and reporting
- **Model:** Gemini Flash (cheap, always-on)
- **Responsibilities:**
  - Reads all system state files every 5 minutes
  - Checks data freshness, API health, P&L limits
  - Detects anomalies (extreme moves, stale data, API errors)
  - Alerts immediately if thresholds breached (via Telegram)
  - Generates daily P&L summary at 9 PM with charts
  - Exports logs and performance metrics
- **Files:**
  - Reads: MARKET_DATA.md, TRADE_STATE.md, TRADE_LOG.md, RISK_LOG.md, DATA_QUALITY_LOG.md
  - Writes: MONITOR_LOG.md, MONITOR_ALERT_HISTORY.md, DAILY_SUMMARY.md
- **Schedule:** Every 5 minutes 24/7, plus 9 PM daily export

## Data Flow

### Trade Execution Flow
```
1. Trader reads MARKET_DATA.md (from DataFetcher)
   ↓
2. Trader applies STRATEGY.md rules
   ↓
3. Trader proposes: "Enter BTC long 2 contracts at $42,300, SL $41,000"
   ↓
4. RiskManager receives proposal
   ↓
5. RiskManager calculates position size, checks RISK_CONFIG.md limits
   ↓
6. RiskManager responds:
   - APPROVED: "Enter 1.85 contracts (risk = 2% capital)"
   - REJECTED: "Exceeds BTC limit, max 1.2 contracts"
   ↓
7. Trader executes approved trade or holds on rejection
   ↓
8. Trader updates TRADE_STATE.md (positions, capital)
   ↓
9. Trader logs to TRADE_LOG.md
   ↓
10. Monitor reads updates, checks P&L, sends alerts if needed
```

### Monitoring Flow
```
Every 5 minutes:
1. Monitor reads MARKET_DATA.md (check freshness, price sanity)
2. Monitor reads TRADE_STATE.md (check P&L vs limits)
3. Monitor reads TRADE_LOG.md (check for errors)
4. Monitor reads RISK_LOG.md (check for pauses)
5. Monitor checks MONITOR_CONFIG.md thresholds
6. If anything breached → send Telegram alert
7. If all OK → silent log entry
8. At 9 PM → compile daily summary, export to Telegram
```

## File Structure

```
agents/
├── main/                          # Mission Control
│   └── workspace/
│       ├── SOUL.md
│       ├── AGENTS.md
│       ├── USER.md
│       └── MEMORY.md
│
├── trader/                        # Trader agent
│   └── workspace/
│       ├── SOUL.md
│       ├── STRATEGY.md (Conservative Trend Follower)
│       ├── EXCHANGE_CONFIG.md (Alpaca setup)
│       ├── API_KEYS.md
│       ├── TRADE_STATE.md (positions, capital, P&L)
│       ├── TRADE_LOG.md (execution log)
│       └── AGENTS.md
│
├── data-fetcher/                  # Data Fetcher agent
│   └── workspace/
│       ├── SOUL.md
│       ├── MARKET_DATA.md (live prices, updated every 5 min)
│       ├── DATA_QUALITY_LOG.md
│       ├── MARKET_DATA_CACHE.json (fallback)
│       └── AGENTS.md
│
├── risk-manager/                  # Risk Manager agent
│   └── workspace/
│       ├── SOUL.md
│       ├── RISK_CONFIG.md (safeguard thresholds)
│       ├── RISK_LOG.md (approvals/rejections)
│       └── AGENTS.md
│
└── monitor/                       # Monitor agent
    └── workspace/
        ├── SOUL.md
        ├── MONITOR_CONFIG.md (alert thresholds)
        ├── MONITOR_LOG.md (health checks)
        ├── MONITOR_ALERT_HISTORY.md
        ├── DAILY_SUMMARY.md (9 PM export)
        └── AGENTS.md
```

## Communication Patterns

### Synchronous (Real-time)
- **Trader → RiskManager:** "Approve this trade?" (waits for response)
- **RiskManager → Trader:** "APPROVED: 1.85 contracts" or "REJECTED: reason"

### Asynchronous (Polling)
- **Monitor → All:** Reads state files every 5 minutes (no waiting)
- **DataFetcher → Market:** Fetches prices every 5 minutes (scheduled)

### Alerts (Push)
- **Monitor → Telegram:** Immediate alerts on thresholds breached
- **Monitor → Telegram:** 9 PM daily summary with charts

## API Efficiency

### DataFetcher
- **Batch calls:** Fetch all symbols (BTC+ETH) in one API call
- **Polling frequency:** 5 minutes (12 calls/hour vs 288 for 5min bars)
- **Caching:** Store MARKET_DATA_CACHE.json for fallback
- **Websockets:** If Alpaca supports it, use streams instead of polling
- **Target:** <20 API calls/hour (well under Alpaca free tier limits)

### Trader
- **On-demand data:** Only read MARKET_DATA.md when analyzing
- **Batch orders:** Group multiple orders if API supports
- **Throttling:** Respect rate limits, don't hammer API
- **Caching:** Store indicator values in memory between calls

### RiskManager
- **File reads:** Read TRADE_STATE.md (local, no API)
- **Calculations:** All math is local (no external API needed)
- **Decision time:** <1 second per trade

### Monitor
- **File reads:** All monitoring is local file reading (no API)
- **Caching:** Keep state in memory, update every 5min
- **Alerts:** Only send alerts on state changes (not every check)

## Safeguards (Critical)

### Position Limits
- Max 10% per asset (BTC/ETH)
- Max 30% total portfolio
- Max leverage 3x

### Loss Limits
- Daily: 5% ($5,000) → pause 24h
- Weekly: 10% ($10,000) → pause 48h
- Overall: 20% ($20,000) → liquidate + pause 72h

### Trade Safeguards
- 2% risk per trade (RiskManager enforces)
- Stop loss 3% below entry (STRATEGY.md rule)
- 1 hour cooldown post-exit
- 24h blacklist after stop-loss

### Monitoring
- 24/7 health checks (every 5 min)
- Immediate alerts on API/data failures
- Daily P&L reports at 9 PM

## Scaling (Future)

This architecture is designed to scale:

**Phase 2 candidates:**
- **Backtester** agent - run historical simulations
- **SentimentAnalyzer** agent - add social/news signals
- **Arbitrage agent** - find cross-exchange spreads
- **Portfolio agent** - optimize asset allocation

Each new agent slots into the system without breaking existing ones.

## Cost Estimate

**Monthly API costs:**
- Alpaca: Free (paper)
- DataFetcher: Free (Gemini Flash on free tier)
- Monitor: Free (Gemini Flash on free tier)
- RiskManager: <$0.01 (Haiku decisions, local file reads)
- Trader: Free (Haiku, Alpaca API is free)

**Total:** $0-2/month (within free tier limits)

## Next Steps

1. ✅ Create agents (done)
2. ✅ Define responsibilities (done)
3. ⏭️ Test DataFetcher (spawn and run 5 min)
4. ⏭️ Test RiskManager (send trade proposals)
5. ⏭️ Test Trader + RiskManager integration
6. ⏭️ Test Monitor (run 24/7 check)
7. ⏭️ Run full system paper trading
8. ⏭️ Collect 1 month data
9. ⏭️ Go live (1% capital)

---

**Architecture designed by:** Grok 4.1 (Evaluator)  
**Implemented:** 2026-03-08  
**Status:** Core agents created, ready for testing
