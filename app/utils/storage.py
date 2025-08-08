# ./app/utils/storage.py
import json
import os

STORAGE_FILE = os.path.join(os.path.dirname(__file__), "..", "monitored_repos.json")

def load_monitored_repos():
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_monitored_repos(repos):
    with open(STORAGE_FILE, "w") as f:
        json.dump(repos, f, indent=4)

def add_repo(repo_name):
    repos = load_monitored_repos()
    if repo_name not in repos:
        repos.append(repo_name)
        save_monitored_repos(repos)
        return True
    return False

def remove_repo(repo_name):
    repos = load_monitored_repos()
    if repo_name in repos:
        repos.remove(repo_name)
        save_monitored_repos(repos)
        return True
    return False
