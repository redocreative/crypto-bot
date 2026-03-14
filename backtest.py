import ccxt
import pandas as pd
import pandas_ta as ta
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

exchange = ccxt.alpaca({
    'apiKey': os.getenv('ALPACA_API_KEY'),
    'secret': os.getenv('ALPACA_SECRET_KEY'),
    'enableRateLimit': True
})
exchange.set_sandbox_mode(True)

def backtest_strategy(days=30, rsi_threshold=45):
    print(f"=== Backtest: Last {days} days | RSI < {rsi_threshold} | 1h timeframe ===")
    since = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    total_signals = 0
    
    for symbol in ['BTC/USD', 'ETH/USD', 'SOL/USD']:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', since=since, limit=2000)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        df['ema9'] = ta.ema(df['close'], length=9)
        df['ema21'] = ta.ema(df['close'], length=21)
        df['rsi'] = ta.rsi(df['close'], length=14)
        
        df = df.dropna()
        if len(df) < 30:
            print(f"{symbol}: Insufficient data")
            continue
        
        # New relaxed logic: uptrend + RSI dip
        uptrend = df['ema9'] > df['ema21']
        oversold = df['rsi'] < rsi_threshold
        df['signal'] = uptrend & oversold
        
        signals = df[df['signal']]
        print(f"\n{symbol} — Signals found: {len(signals)}")
        if len(signals) > 0:
            print(signals[['timestamp', 'close', 'rsi']].tail(6).to_string())
            total_signals += len(signals)
        else:
            print(f"No signals on {symbol} — last RSI: {df['rsi'].iloc[-1]:.1f} | EMA9>EMA21? {df['ema9'].iloc[-1] > df['ema21'].iloc[-1]}")
    
    print(f"\n=== Total signals across coins: {total_signals} ===")

if __name__ == "__main__":
    backtest_strategy(days=30, rsi_threshold=45)