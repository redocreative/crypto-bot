import ccxt
import pandas as pd
import pandas_ta as ta
import os
from dotenv import load_dotenv
import time
from logging_config import logger, log_trade
import telegram
import asyncio

load_dotenv()

exchange = ccxt.alpaca({
    'apiKey': os.getenv('ALPACA_API_KEY'),
    'secret': os.getenv('ALPACA_SECRET_KEY'),
    'enableRateLimit': True
})
exchange.set_sandbox_mode(True)

bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
chat_id = os.getenv('TELEGRAM_CHAT_ID')

async def send_telegram(text):
    await bot.send_message(chat_id=chat_id, text=text)

def run_trader_cycle():
    logger.info("=== 15-min paper trading cycle started ===")
    
    for symbol in ['BTC/USD', 'ETH/USD', 'SOL/USD']:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=200)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        df['ema9'] = ta.ema(df['close'], length=9)
        df['ema21'] = ta.ema(df['close'], length=21)
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        df = df.dropna()
        if len(df) < 30:
            logger.info(f"Insufficient data on {symbol} — skipping")
            continue
        
        uptrend = df['ema9'].iloc[-1] > df['ema21'].iloc[-1]
        rsi_condition = df['rsi'].iloc[-1] < 48
        
        if uptrend and rsi_condition:
            price = df['close'].iloc[-1]
            balance = float(exchange.fetch_balance()['total']['USD'])
            size = 0.01 * balance / price
            stop = price - 2 * df['atr'].iloc[-1]
            
            order = exchange.create_order(symbol, 'market', 'buy', size)
            
            log_trade("BUY EXECUTED", symbol, "Uptrend + RSI<48 dip", f"Price: ${price:.2f} | RSI: {df['rsi'].iloc[-1]:.1f}")
            asyncio.run(send_telegram(f"🚀 PAPER BUY EXECUTED\n{symbol} @ ${price:.2f}\nReason: Uptrend dip\nSize: {size:.6f}"))
            logger.info(f"✅ SIGNAL on {symbol} — Order ID: {order['id']}")
        else:
            logger.info(f"No signal on {symbol} | RSI: {df['rsi'].iloc[-1]:.1f} | Uptrend: {uptrend}")
    
    logger.info("=== Cycle complete ===\n")

if __name__ == "__main__":
    while True:
        run_trader_cycle()
        time.sleep(900)