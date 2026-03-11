# Trading Automation Strategy (Validated by Grok 4.1)

**Last Updated:** 2026-03-09  
**Evaluated By:** Grok 4.1 Fast Reasoning (xAI API)  
**Total XAI Tokens Used:** 3,745 tokens ($0.1729 cost)

---

## EXECUTIVE SUMMARY

Automated crypto trading bot using Alpaca + Binance + CoinGecko data pipeline. MVP architecture validated via comprehensive Grok evaluation.

**Success Rate (Free Tier):**
- MVP (backtesting, 5-10 symbols): **70-80%**
- Moderate scale (100+ symbols): **40-50% → 65% with hardening**
- Live trading: **10-20% → 30-70% with hardening + paid tiers**

---

## STEP 1: DATA SOURCES (VALIDATED ✅)

### Primary APIs
1. **Binance** (Futures, funding rates)
   - Cost: Free tier (2,400 req/min)
   - Reliability: 98.5-99.5% uptime
   - Risk: Occasional 2-6hr outages
   - Mitigation: Bybit fallback

2. **Alpaca** (Spot prices, paper trading execution)
   - Cost: Free paper tier, $99/mo live
   - Reliability: 99.99% uptime
   - Risk: Limited crypto pairs, no futures
   - Gotcha: Websocket auto-disconnect after 5min (needs ping)

3. **CoinGecko** (Fallback prices, on-chain basics)
   - Cost: Free tier (30-50 calls/min), $129/mo Pro
   - Reliability: 99.99% (aggregated)
   - Risk: 1-30s lag, no real-time
   - Use: Reference only, not primary

### Hardening Actions (Critical)
- [ ] Implement Bybit fallback for Binance downtime
- [ ] Add exponential backoff for rate limit handling
- [ ] Local 1-hour OHLCV cache to reduce API calls
- [ ] Circuit breaker: pause if data lag >5 seconds
- [ ] Cross-validate prices (Alpaca vs Binance)
- [ ] Weekly failover testing via toxiproxy
- [ ] Monitoring + alerting (log all API errors)

**Implementation Time:** ~22 hours (free, no cost)

---

## STEP 2: TRADING SIGNALS (DESIGNED, PENDING GROK VALIDATION)

### Signal Ensemble (5 signals + 1 regime filter)
1. **Funding Rates** (35% weight) - Binance futures funding (high = contrarian BUY)
2. **On-Chain Flows** (25% weight) - Exchange inflows/outflows + MVRV
3. **Technical TA** (20% weight) - Multi-timeframe RSI + MACD
4. **Fear/Greed Index** (15% weight) - Macro sentiment filter
5. **BTC Dominance** (5% weight) - Regime filter (risk-on vs risk-off)

### Entry Logic
```
IF (Funding Rate is HIGH) AND
   (Exchange Outflow OR MVRV <1.2) AND
   (TA: RSI oversold on 2+ timeframes) AND
   (Fear/Greed <65) AND
   (BTC dominance stable)
THEN: Enter long at 15m RSI cross above 30
SIZE: 2% of account
```

### Exit Logic
- TP1: +3-4% (exit 50%, move stop to BE)
- TP2: +6-8% (exit 30%, trail stop)
- TP3: +10-15% (exit 20%, trailing stop)
- SL: -2% hard stop

### Risk Filters (Skip trading if)
- BTC volatility >4%
- Bid-ask spread >0.5%
- Volume <10x typical
- Fear/Greed swinging >10 points/hour
- Time: 22:00-06:00 UTC (low volume)

**Expected Performance:**
- Win Rate: >45% (with 1:2+ risk/reward)
- Sharpe: >0.5
- Max Drawdown: <15%
- False Positive Rate: <20%

---

## STEP 3: RISK MANAGEMENT (PENDING)

TBD - Awaiting Grok evaluation

---

## IMPLEMENTATION ROADMAP

### Phase 1: Validation (Weeks 1-4)
- [ ] Harden Step 1 (22 hours)
- [ ] Implement Step 2 signals (40 hours)
- [ ] Offline backtest on 3-6 months data
- [ ] Paper trade on Alpaca (2 weeks)

### Phase 2: Proof of Concept (Weeks 5-8)
- [ ] Live paper trading (1 month minimum)
- [ ] Collect 100+ trades for statistical validation
- [ ] Verify Sharpe >0.5, Win Rate >45%
- [ ] Document all failures/edge cases

### Phase 3: Live Trading (Week 9+)
- [ ] $100 initial capital (test trades)
- [ ] Scale slowly (double every 2 weeks if profitable)
- [ ] Monitor Sharpe ratio continuously
- [ ] Kill-switch if drawdown >20%

---

## COST TRAJECTORY

| Phase | Cost | Justification |
|-------|------|-----------------|
| **MVP** | $0/mo | Binance + Alpaca free, CoinGecko free |
| **Validation** | $129/mo | Add CoinGecko Pro (unlock 500 calls/min) |
| **Production** | $228/mo | Alpaca live $99 + CoinGecko Pro $129 |
| **10x Scale** | $1,500+/mo | +Binance VIP1 + CoinGecko Enterprise + AWS infra |

---

## TOP RISKS & MITIGATIONS

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Binance outages (2-6hr) | **CRITICAL** | Bybit fallback API; cache 1hr data |
| Rate limit cascades | **HIGH** | Exponential backoff; upgrade to Pro early |
| Data inconsistency | **MEDIUM** | Cross-validate; use Binance as primary |
| Regulatory (Binance US blocks) | **MEDIUM** | Monitor SEC/CFTC; pivot to Kraken if needed |
| Backtesting overfitting | **HIGH** | Out-of-sample validation; paper trade 1mo first |

---

## RED FLAGS (Deal-Breakers)

❌ Don't go live without:
- Bybit fallback integrated + tested
- Circuit breaker (pause on stale data)
- Cache layer (survive 60s API downtime)
- 1-month paper trading validation
- Drawdown limits + kill-switch logic

❌ Don't scale without:
- CoinGecko Pro ($129/mo minimum)
- Institutional-grade data (Kaiko/Amberdata for production)
- Dedicated DevOps/monitoring

---

## NEXT STEPS

1. Harden Step 1 (implement fallback + cache + circuit breaker)
2. Get Grok evaluation of Step 2 (signals validation)
3. Get Grok evaluation of Step 3 (risk management & position sizing)
4. Build integrated MVP and backtest
5. Paper trade 1 month before going live

---

## GROK EVALUATION METADATA

**Step 1 Deep Dive Evaluation:**
- Request tokens: 402
- Completion tokens: 2,622
- Reasoning tokens: 721
- Total tokens: 3,745
- Cost: $0.1729 USD
- Model: grok-4-1-fast-reasoning
- Reasoning: Extended (721 tokens used for analysis)
