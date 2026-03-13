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
    
    for symbol in ['BTC/USD', 'ETH/USD']:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)  # 1h for better signals
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        df['ema9'] = ta.ema(df['close'], length=9)
        df['ema21'] = ta.ema(df['close'], length=21)
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        crossover = df['ema9'].iloc[-1] > df['ema21'].iloc[-1] and df['ema9'].iloc[-2] <= df['ema21'].iloc[-2]
        rsi_condition = df['rsi'].iloc[-1] < 40
        volume_spike = df['volume'].iloc[-1] > df['volume'].rolling(20).mean().iloc[-1]
        
        if crossover and rsi_condition and volume_spike:
            price = df['close'].iloc[-1]
            balance = float(exchange.fetch_balance()['total']['USD'])
            size = 0.01 * balance / price
            stop = price - 2 * df['atr'].iloc[-1]
            
            order = exchange.create_order(symbol, 'market', 'buy', size)
            
            log_trade("BUY EXECUTED", symbol, "EMA crossover + RSI<40 + Volume", f"Price: ${price:.2f}")
            asyncio.run(send_telegram(f"🚀 PAPER BUY EXECUTED\n{symbol} @ ${price:.2f}\nReason: Tuned strategy\nSize: {size:.6f}"))
        else:
            logger.info(f"No confluence on {symbol} — skipping")
    
    logger.info("=== Cycle complete ===\n")

if __name__ == "__main__":
    while True:
        run_trader_cycle()
        time.sleep(900)