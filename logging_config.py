import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=f"logs/trading_{datetime.now().strftime('%Y-%m-%d')}.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("crypto_bot")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

def log_trade(action, symbol, reason, details=""):
    logger.info(f"{action} | {symbol} | Reason: {reason} | {details}")