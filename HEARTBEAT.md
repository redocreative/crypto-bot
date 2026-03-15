# 💓 HEARTBEAT.md - Mission Control Trading Loop (15-Minute Cycles)

**Schedule:** Every 15 minutes (per SOUL.md)  
**Active Hours:** 8:00 AM - 10:00 PM (America/Phoenix)  
**Active Model:** Grok 4.1 for Trader, Gemini Flash for system checks  
**Response:** Spawn trader cycle + check system health

---

## On Every Heartbeat (Every 15 Minutes)

1. **SPAWN TRADER CYCLE** → Full market analysis, sentiment, entry decision, Telegram summary
2. **System health check** → Gateway running? No critical errors?
3. **If all clear** → Confirm cycle spawned, await completion

---

## Rules

- Never skip a cycle during active hours (8 AM - 10 PM MST)
- Trader uses Grok 4.1 primary (fast sentiment + strategy logic)
- Every decision must log to `logs/trading_YYYY-MM-DD.log`
- Send Telegram summary after each cycle completion
- Paper mode only until Spencer says "go live"

---

## Outside Active Hours (10 PM - 8 AM)

Respond HEARTBEAT_OK and stay quiet. No trading cycles.
