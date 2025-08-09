from app.utils.logger import log

def handle_push_event(payload: dict) -> str:
    """Return a short summary for GitHub push events."""
    repo = payload.get("repository", {}).get("full_name", "Unknown repo")
    pusher = payload.get("pusher", {}).get("name", "Unknown user")
    commits = payload.get("commits", [])
    commit_count = len(commits)

    # Compact one-line message
    message = f"[Push] {pusher} pushed {commit_count} commit(s) to {repo}."
    log.info(message)
    return message


def handle_issue_event(payload: dict) -> str:
    """Return a short summary for GitHub issue events."""
    action = payload.get("action", "updated")
    title = payload.get("issue", {}).get("title", "Untitled issue")
    user = payload.get("issue", {}).get("user", {}).get("login", "Unknown user")
    repo = payload.get("repository", {}).get("full_name", "Unknown repo")

    message = f"[Issue] '{title}' {action} by {user} in {repo}."
    log.info(message)
    return message


def handle_pr_event(payload: dict) -> str:
    """Return a short summary for GitHub pull request events."""
    action = payload.get("action", "updated")
    title = payload.get("pull_request", {}).get("title", "Untitled PR")
    user = payload.get("pull_request", {}).get("user", {}).get("login", "Unknown user")
    repo = payload.get("repository", {}).get("full_name", "Unknown repo")

    message = f"[PR] '{title}' {action} by {user} in {repo}."
    log.info(message)
    return message
