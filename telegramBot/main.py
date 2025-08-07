from dotenv import load_dotenv
import os

load_dotenv()

botName = os.getenv('BOT_NAME')
print(botName)