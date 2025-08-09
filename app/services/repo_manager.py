import os
import requests
import json
from dotenv import load_dotenv
from app.utils.logger import log

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your FastAPI webhook endpoint
SUBSCRIPTIONS_FILE = "subscriptions.json"

def load_subscriptions():
    if not os.path.exists(SUBSCRIPTIONS_FILE):
        return []
    with open(SUBSCRIPTIONS_FILE, "r") as f:
        return json.load(f)

def save_subscriptions(subscriptions):
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(subscriptions, f, indent=2)

def add_subscription(repo_full_name):
    subs = load_subscriptions()
    if repo_full_name in subs:
        return f"Already monitoring {repo_full_name}."
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": "web",
        "active": True,
        "events": ["push", "issues", "pull_request"],
        "config": {
            "url": WEBHOOK_URL,
            "content_type": "json"
        }
    }

    resp = requests.post(
        f"https://api.github.com/repos/{repo_full_name}/hooks",
        headers=headers,
        json=payload
    )

    if resp.status_code in [201, 200]:
        subs.append(repo_full_name)
        save_subscriptions(subs)
        log.info(f"Now monitoring {repo_full_name}")
        return f"✅ Now monitoring {repo_full_name}"
    else:
        log.error(f"Failed to add webhook: {resp.text}")
        return f"❌ Failed to monitor {repo_full_name}: {resp.text}"
