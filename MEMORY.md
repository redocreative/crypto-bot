# Mission Control Memory

## Trading Automation Project (Crypto)

### Infrastructure (Ready)
- **Trader agent:** Configured (Haiku + Gemini fallback)
- **Risk-Manager agent:** Configured (Haiku only)
- **Data-Fetcher agent:** Configured (Gemini)
- **Monitor agent:** Configured (Gemini)

### Plan Overview
**Objective:** Automated crypto trading bot with risk management, signals, and reporting

**Data Sources Strategy:**
| Source | Data | Cost | Status |
|--------|------|------|--------|
| Alpaca | Prices, trades (live) | Free paper; $99/mo live | TBD |
| Binance/KuCoin | Futures, funding, vol | Free (rate-limited) | TBD |
| CoinGecko | Prices, on-chain | Free | TBD |
| Glassnode | On-chain metrics, whale alerts | Free + $29/mo pro | TBD |
| LunarCrush | Social sentiment (Galaxy Score) | Free API (limited) | TBD |
| Alpha Vantage | News sentiment | Free (500/day) | TBD |

**Signals:**
- Fear/Greed index
- Sentiment (social + news)
- On-chain metrics

**Reporting:**
- Daily logs: Capital, P&L, trades, Sharpe, positions
- P&L tracking via SQLite + canvas charts
- Alerts: >5% drawdown, API errors, new highs/lows (Telegram)

**Next Step:** Spawn RiskManager first (safest). Test full stack on paper 1mo.

---

## xAI API Setup (Completed Mar 9)
- API key: Set in LaunchAgent plist (XAI_API_KEY env var)
- Models working: grok-4-1-fast-reasoning ✅, grok-3 ✅
- Both tested and responding correctly

## Agent Configuration (Mar 9 Updated)
- **main:** Claude Haiku (default)
- **trader:** Claude Haiku + Gemini fallback
- **risk-manager:** Claude Haiku only
- **data-fetcher:** Gemini
- **monitor:** Gemini
- **evaluator:** Grok 4.1 (NEW) + Claude Haiku fallback ✅

## Current Status
- Gateway: Stable, all models available (including Grok)
- Grok API: Ready to use (primary model for evaluator agent now)
- Step 1 (Data Sources): ✅ Validated - Alpaca + Binance + CoinGecko MVP stack approved
- Step 2 (Trading Signals): ✅ Validated - 5-signal ensemble strategy designed
- Next: Step 3 - Risk Management & Position Sizing
