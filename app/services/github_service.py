# ./app/services/github_service.py
import os
import requests
from app.utils.logger import log

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub personal access token
WEBHOOK_URL = os.getenv("WEBHOOK_URL")    # FastAPI endpoint for GitHub events

def add_github_webhook(repo_full_name: str) -> bool:
    """
    Create a webhook for the given repository to send push, PR, and issue events.
    Returns True if successful, False otherwise.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "name": "web",
        "active": True,
        "events": ["push", "pull_request", "issues"],
        "config": {
            "url": WEBHOOK_URL,
            "content_type": "json",
            "insecure_ssl": "0"
        }
    }

    log.info(f"Attempting to create webhook for {repo_full_name}...")

    response = requests.post(
        f"{GITHUB_API_URL}/repos/{repo_full_name}/hooks",
        headers=headers,
        json=payload
    )

    if response.status_code in (201, 200):
        log.info(f"✅ Webhook successfully created for {repo_full_name}")
        return True
    else:
        log.error(f"❌ Failed to create webhook for {repo_full_name}: {response.text}")
        return False
