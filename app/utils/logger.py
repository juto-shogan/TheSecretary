import logging
import os

# Create the log directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), '..', 'bot_logs')
os.makedirs(log_dir, exist_ok=True)

# Full path to the log file
log_file = os.path.join(log_dir, 'xbot.log')

# Configure logging to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file),       # Write logs to file
        logging.StreamHandler()              # Also print logs to terminal
    ]
)

# Export the logger
log = logging.getLogger("x-bot")