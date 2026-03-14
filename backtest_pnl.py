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

def backtest_pnl(days=30, rsi_threshold=48):
    print(f"=== Backtest + P&L: Last {days} days | RSI < {rsi_threshold} | 1h timeframe ===")
    since = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    total_signals = 0
    total_pnl = 0.0
    
    for symbol in ['BTC/USD', 'ETH/USD', 'SOL/USD']:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', since=since, limit=2000)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        df['ema9'] = ta.ema(df['close'], length=9)
        df['ema21'] = ta.ema(df['close'], length=21)
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        df = df.dropna()
        if len(df) < 30:
            continue
        
        # Uptrend + dip logic
        uptrend = df['ema9'] > df['ema21']
        df['signal'] = uptrend & (df['rsi'] < rsi_threshold)
        
        signals = df[df['signal']]
        print(f"\n{symbol} — Signals found: {len(signals)}")
        
        for idx in signals.index:
            total_signals += 1
            price = df.loc[idx, 'close']
            atr = df.loc[idx, 'atr']
            size = 0.01 * 100000 / price  # 1% of $100k paper portfolio
            
            # Simple P&L simulation
            tp_price = price * 1.04
            sl_price = price - 2 * atr
            hypothetical_pnl = size * 0.04   # +4% TP win
            total_pnl += hypothetical_pnl
            
            print(f"  Signal @ {df.loc[idx, 'timestamp']} | Price ${price:.2f} | RSI {df.loc[idx, 'rsi']:.1f}")
            print(f"    → Hypothetical win: +${hypothetical_pnl:.2f} portfolio (4% TP)")
    
    print(f"\n=== SUMMARY ===\nTotal signals: {total_signals}\nEstimated 30-day P&L (if all hit 4% TP): +${total_pnl:.2f} (+{total_pnl/1000:.1f}% on $100k)")

if __name__ == "__main__":
    backtest_pnl(days=30, rsi_threshold=48)