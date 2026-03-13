# TOOLS.md - Crypto-Specific Local Notes & Skills (Alpaca Paper Mode)

## Exchange Config (Paper Only — Arizona Compliant)
- Use Alpaca paper trading (fully legal in AZ)
- CCXT setup (copy-paste ready):
  ```python
  import ccxt
  import os
  from dotenv import load_dotenv
  load_dotenv()

  exchange = ccxt.alpaca({
      'apiKey': os.getenv('ALPACA_API_KEY'),
      'secret': os.getenv('ALPACA_SECRET_KEY'),
      'enableRateLimit': True
  })
  exchange.set_sandbox_mode(True)  # ← CRITICAL: keeps everything in paper mode