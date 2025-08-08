from dotenv import load_dotenv
import os

load_dotenv()

botName = os.getenv('BOT_NAME')

bot_description = os.getenv('BOT_DESCRIPTION')

print(botName)
print(bot_description)