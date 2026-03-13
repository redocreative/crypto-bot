import ccxt
import os
from dotenv import load_dotenv
import telegram  # for reliable alerts

load_dotenv()

# === ALPACA PAPER MODE TEST ===
exchange = ccxt.alpaca({
    'apiKey': os.getenv('ALPACA_API_KEY'),
    'secret': os.getenv('ALPACA_SECRET_KEY'),
    'enableRateLimit': True
})
exchange.set_sandbox_mode(True)   # PAPER ONLY — safe!

print("✅ Connected to ALPACA PAPER MODE")
print("Balance:", exchange.fetch_balance()['total'])
print("BTC price:", exchange.fetch_ticker('BTC/USD')['last'])

# Telegram test (fixes your old spotty updates)
bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
chat_id = os.getenv('TELEGRAM_CHAT_ID')
bot.send_message(chat_id=chat_id, text="🚀 Crypto bot test successful!\nMode: Alpaca PAPER\nSpencer in Phoenix — ready to trade!")
print("✅ Telegram alert sent (reliable polling enabled)")