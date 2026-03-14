import asyncio
import telegram
import os
from dotenv import load_dotenv

load_dotenv()

async def send_test():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    print(f"🔍 Debug: Using TOKEN (first 10 chars): {token[:10]}...")
    print(f"🔍 Debug: Using CHAT_ID: {chat_id}")
    
    if not token or not chat_id:
        print("❌ Missing token or chat_id in .env")
        return
    
    bot = telegram.Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text="✅ Telegram test SUCCESS — bot is now working!")
        print("🎉 Message sent successfully! Check Telegram now.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_test())