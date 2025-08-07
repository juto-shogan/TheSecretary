from dotenv import load_dotenv
import os
import tweepy
from app.utils.logger import log

log.info("bot started")

# Load environment variables from .env file
load_dotenv()
log.info("Loading environment variables from .env file")

log.info("Loading Twitter API credentials from environment variables")   
# Retrieve Twitter API credentials from environment variables
try:
    consumer_key = os.getenv('API_KEY')
    consumer_secret = os.getenv('API_KEY_SECRET')
    bearer_token = os.getenv('BEARER_TOKEN')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
    
    # Check if all required environment variables are set
    if not all([consumer_key, consumer_secret, bearer_token, access_token, access_token_secret]):
        raise ValueError("One or more environment variables are missing.")
    
    else:
        # variable confirmation
        print("All required environment variables are set.")
    
    # load confirmation
    print("Environment variables loaded successfully.")
    
    # exception handling for missing variables
except ValueError as ve:
    log.error(f"Error: {ve}")
    print(f"Error: {ve}")
    exit(1)
except Exception as e:
    log.error(f"Error loading environment variables: {e}")
    print(f"Error loading environment variables: {e}")
    exit(1)



# Authentication variable for Twitter using Tweepy
auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)  

# Authenticate to Twitter
api = tweepy.API(auth)

# success confirmation
print("Successfully loaded Twitter API object: ", api)
# Check if the authentication was successful
try:
    api.verify_credentials()
    log.info("Authentication OK")
    print("Authentication OK")
except Exception as e:
    log.error(f"Error during authentication: {e}")
    print("Error during authentication:", e)
    exit(1)