import ccxt
import pandas as pd
import pandas_ta as ta
import os
from dotenv import load_dotenv
import time
from logging_config import logger, log_trade
import telegram

load_dotenv()

exchange = ccxt.alpaca({
    'apiKey': os.getenv('ALPACA_API_KEY'),
    'secret': os.getenv('ALPACA_SECRET_KEY'),
    'enableRateLimit': True
})
exchange.set_sandbox_mode(True)

bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
chat_id = os.getenv('TELEGRAM_CHAT_ID')

def run_trader_cycle():
    logger.info("=== 15-min paper trading cycle started ===")
    
    bars = exchange.fetch_ohlcv('BTC/USD', timeframe='15m', limit=100)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    df['ema9'] = ta.ema(df['close'], length=9)
    df['ema21'] = ta.ema(df['close'], length=21)
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    
    crossover = df['ema9'].iloc[-1] > df['ema21'].iloc[-1] and df['ema9'].iloc[-2] <= df['ema21'].iloc[-2]
    rsi_oversold = df['rsi'].iloc[-1] < 35
    
    if crossover and rsi_oversold:
        price = df['close'].iloc[-1]
        size = 0.01 * float(exchange.fetch_balance()['total']['USD']) / price
        stop = price - 2 * df['atr'].iloc[-1]
        
        log_trade("BUY SIGNAL", "BTC/USD", "EMA crossover + RSI", f"Price: ${price:.2f}")
        bot.send_message(chat_id=chat_id, text=f"🚀 PAPER BUY SIGNAL\nBTC/USD @ ${price:.2f}\nReason: Technical confluence\nStop: ${stop:.2f}")
    else:
        logger.info("No full confluence — no trade")
    
    logger.info("=== Cycle complete ===\n")

if __name__ == "__main__":
    while True:
        run_trader_cycle()
        time.sleep(900)  # 15 minutes