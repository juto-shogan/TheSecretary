# ./app/utils/telegram.py
import requests
import os
from app.utils.logger import log

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Your personal chat ID

def send_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        log.error("Telegram bot token or chat ID not set")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            log.info(f"Sent Telegram message: {text}")
            return True
        else:
            log.error(f"Failed to send message: {res.text}")
            return False
    except Exception as e:
        log.error(f"Error sending message to Telegram: {e}")
        return False
