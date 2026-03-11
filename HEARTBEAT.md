# 💓 HEARTBEAT.md - Mission Control Check-In

**Schedule:** Every 4 hours  
**Active Hours:** 8:00 AM - 10:00 PM (America/Phoenix)  
**Model:** Gemini Flash (cheapest)  
**Response:** HEARTBEAT_OK if all clear, otherwise report what needs attention

---

## Quick Scan Checklist

During each heartbeat, check these items in order:

### 1. Sub-Agent Status
- Any sub-agents still running or waiting for user input?
- Any sub-agent tasks completed that need relaying to Spencer?
- Check `subagents list` for active sessions

### 2. Scheduled Tasks
- Any cron jobs scheduled to run?
- Any pending trader-cycle status if trading is active?

### 3. System Health
- Gateway still running? (quick probe)
- Any critical errors in logs?

### 4. Pending Work
- Anything in memory that needs follow-up?
- Any user requests outstanding?

---

## Decision Tree

**If it's outside 8am-10pm:** Respond HEARTBEAT_OK and stay quiet  
**If all checks clear:** Respond HEARTBEAT_OK  
**If something needs attention:** Report it (don't use HEARTBEAT_OK, describe the issue)  
**If sub-agent task completed:** Relay the result to Spencer in plain language

---

## Notes

- Keep heartbeats lean. Use Gemini Flash only.
- Never escalate model tier for heartbeats.
- This is a quick pulse check, not a deep analysis.
- If unsure whether something matters, ask Spencer rather than guess.
