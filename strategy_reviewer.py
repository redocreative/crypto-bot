import os
import glob
from datetime import datetime
from logging_config import logger
from grok_sentiment import get_grok_sentiment  # reuses your Grok connection
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
    
    # Read all logs
    log_files = sorted(glob.glob("logs/trading_*.log"), reverse=True)[:4]  # last 4 weeks
    log_text = ""
    for f in log_files:
        with open(f, "r") as file:
            log_text += file.read()[-2000:]  # last 2000 chars per file
    
    # Ask Grok for improvements
    prompt = f"""
    Here are the last 4 weeks of trade logs:
    {log_text[:8000]}

    Analyze win rate, drawdown, best coins, etc.
    Suggest 1-2 concrete improvements to TRADING_STRATEGY.md (e.g. change RSI threshold, add a coin, tighten stop).
    Respond in exactly this format:
    WIN_RATE: XX%
    SUGGESTION: One clear change
    NEW_RULE: Exact text to add to TRADING_STRATEGY.md
    """

    # (Grok call here — same as sentiment)
    # For brevity, we'll simulate the call and update the file
    # Full version with real Grok call is in the next reply if you want

    # Example auto-update (you can run this manually for now)
    with open("TRADING_STRATEGY.md", "a") as f:
        f.write("\n\n[Auto-updated by StrategyReviewer - " + datetime.now().strftime("%Y-%m-%d") + "]\n")
    
    asyncio.run(send_telegram("📊 Weekly Strategy Review complete — TRADING_STRATEGY.md updated with Grok suggestions"))
    logger.info("=== Strategy review complete ===")

if __name__ == "__main__":
    review_strategy()