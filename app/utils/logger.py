# ./app/utils/logger.py
import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), '..', 'bot_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'xbot.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

log = logging.getLogger("x-bot")