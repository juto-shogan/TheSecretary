import os
import requests
from dotenv import load_dotenv
from app.utils.logger import log

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    """Send a message to the configured Telegram chat."""
    if not BOT_TOKEN or not CHAT_ID:
        log.error("Telegram bot token or chat ID missing in .env")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            log.error(f"Telegram send failed: {resp.text}")
        else:
            log.info(f"Sent to Telegram: {message}")
    except Exception as e:
        log.error(f"Error sending Telegram message: {e}")
