import ccxt
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

exchange = ccxt.alpaca({
    'apiKey': os.getenv('ALPACA_API_KEY'),
    'secret': os.getenv('ALPACA_SECRET_KEY'),
    'enableRateLimit': True
})
exchange.set_sandbox_mode(True)  # still paper-safe

def backtest_strategy(days=30):
    print("=== Starting Backtest (last", days, "days) ===")
    since = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    
    for symbol in ['BTC/USD', 'ETH/USD']:
        bars = exchange.fetch_ohlcv(symbol, timeframe='15m', since=since, limit=2000)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        df['ema9'] = ta.ema(df['close'], length=9)
        df['ema21'] = ta.ema(df['close'], length=21)
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        df['signal'] = (df['ema9'] > df['ema21']) & (df['ema9'].shift(1) <= df['ema21'].shift(1)) & (df['rsi'] < 35)
        
        signals = df[df['signal']].copy()
        print(f"\n{symbol} — Signals found: {len(signals)}")
        
        if len(signals) > 0:
            print(signals[['timestamp', 'close', 'rsi']].to_string())
        else:
            print("No signals in the period — same strict rules as live bot.")

if __name__ == "__main__":
    backtest_strategy(days=30)  # change to 60 or 90 if you want longer test