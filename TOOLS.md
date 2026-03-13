# TOOLS.md - Crypto-Specific Local Notes & Skills

## Exchange Config
- Bybit testnet/paper: https://testnet.bybit.com (use for safe testing)
- API keys stored in .env (never hardcode)
- CCXT unified: `exchange = ccxt.bybit({'apiKey': os.getenv('BYBIT_API_KEY'), 'secret': os.getenv('BYBIT_API_SECRET')})`

## Available Skills (for OpenClaw code tool)
- Fetch OHLCV + indicators: Use pandas_ta for EMA, RSI, ATR
- Execute trade: `exchange.create_order(symbol, type, side, amount)`
- Sentiment scan: Browser tool → X/Reddit headlines
- Backtest: Simple script using historical CCXT data

## Quick Commands
- Test connection: `exchange.fetch_balance()`
- Get price: `exchange.fetch_ticker('BTC/USDT')`
- Risk calc: Position size = (account * 0.01) / (entry - stop)

Add anything else you learn here.