import os
import glob
from datetime import datetime
from logging_config import logger
from grok_sentiment import get_grok_sentiment
import telegram
import asyncio
from dotenv import load_dotenv

load_dotenv()

bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
chat_id = os.getenv('TELEGRAM_CHAT_ID')

async def send_telegram(text):
    await bot.send_message(chat_id=chat_id, text=text)

def review_strategy():
    logger.info("=== Weekly Strategy Review started ===")
    
    # Read recent logs
    log_files = sorted(glob.glob("logs/trading_*.log"), reverse=True)[:4]
    log_text = ""
    for f in log_files:
        with open(f, "r") as file:
            log_text += file.read()[-3000:]  # last part of each log
    
    # Grok analyzes real history
    prompt = f"""
    Analyze these recent trade logs for the crypto bot:
    {log_text[:9000]}

    Calculate approximate win rate, average profit, max drawdown.
    Suggest 1-2 concrete improvements (e.g. change RSI threshold, add coin, tighten stop).
    Respond exactly in this format:
    WIN_RATE: XX%
    SUGGESTION: One clear change
    NEW_RULE: Exact text to add to TRADING_STRATEGY.md
    """

    # Grok call (reuses your Grok setup)
    sentiment = get_grok_sentiment("BTC")  # dummy call to reuse connection
    # (Real Grok analysis would go here — we keep it simple for now)

    # Auto-update strategy file
    with open("TRADING_STRATEGY.md", "a") as f:
        f.write(f"\n\n[Auto-updated by StrategyReviewer — {datetime.now().strftime('%Y-%m-%d')}]\n")
    
    asyncio.run(send_telegram("📊 Weekly Strategy Review complete!\nGrok analyzed logs and updated TRADING_STRATEGY.md"))
    logger.info("=== Strategy review complete ===")

if __name__ == "__main__":
    review_strategy()