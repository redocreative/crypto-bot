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
exchange.set_sandbox_mode(True)

def backtest_strategy(days=30, rsi_threshold=40, timeframe='1h'):
    print(f"=== Backtest: Last {days} days | RSI < {rsi_threshold} | {timeframe} timeframe ===")
    since = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    
    for symbol in ['BTC/USD', 'ETH/USD']:
        bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=2000)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        df['ema9'] = ta.ema(df['close'], length=9)
        df['ema21'] = ta.ema(df['close'], length=21)
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        # Tuned rules (more signals but still safe)
        crossover = (df['ema9'] > df['ema21']) & (df['ema9'].shift(1) <= df['ema21'].shift(1))
        volume_spike = df['volume'] > df['volume'].rolling(20).mean()
        
        df['signal'] = crossover & (df['rsi'] < rsi_threshold) & volume_spike
        
        signals = df[df['signal']].copy()
        print(f"\n{symbol} — Signals found: {len(signals)}")
        
        if len(signals) > 0:
            print(signals[['timestamp', 'close', 'rsi', 'volume']].tail(10).to_string())
        else:
            print("Still no signals — we can loosen more.")

if __name__ == "__main__":
    backtest_strategy(days=30, rsi_threshold=40, timeframe='1h')  # ← easy to change