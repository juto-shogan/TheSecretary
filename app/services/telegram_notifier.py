import os
import requests
from app.utils.logger import log
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text: str):
    """Send a message to the Telegram chat."""
    if not BOT_TOKEN or not CHAT_ID:
        log.error("Telegram BOT_TOKEN or CHAT_ID is not set in .env")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            log.info("📤 Sent message to Telegram successfully.")
        else:
            log.error(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        log.error(f"Error sending Telegram message: {e}")

