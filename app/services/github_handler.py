from app.utils.logger import log

def handle_push_event(payload: dict) -> str:
    """Handle GitHub push events and return a short summary."""
    repo_name = payload.get("repository", {}).get("full_name", "Unknown repo")
    pusher = payload.get("pusher", {}).get("name", "Unknown user")
    commit_count = len(payload.get("commits", []))

    message = f"📌 {pusher} pushed {commit_count} commit(s) to {repo_name}."
    log.info(message)
    return message


def handle_issue_event(payload: dict) -> str:
    """Handle GitHub issues events and return a short summary."""
    action = payload.get("action", "performed an action on")
    issue_title = payload.get("issue", {}).get("title", "Untitled issue")
    user = payload.get("issue", {}).get("user", {}).get("login", "Unknown user")
    repo_name = payload.get("repository", {}).get("full_name", "Unknown repo")

    message = f"🐛 Issue '{issue_title}' {action} by {user} in {repo_name}."
    log.info(message)
    return message


def handle_pr_event(payload: dict) -> str:
    """Handle GitHub pull request events and return a short summary."""
    action = payload.get("action", "performed an action on")
    pr_title = payload.get("pull_request", {}).get("title", "Untitled PR")
    user = payload.get("pull_request", {}).get("user", {}).get("login", "Unknown user")
    repo_name = payload.get("repository", {}).get("full_name", "Unknown repo")

    message = f"🔀 Pull Request '{pr_title}' {action} by {user} in {repo_name}."
    log.info(message)
    return message
