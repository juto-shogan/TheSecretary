from fastapi import APIRouter, Request, Header
from app.utils.logger import log
from app.services.github_handler import (
    handle_push_event,
    handle_issue_event,
    handle_pr_event
)
from app.services.telegram_notifier import send_telegram_message

router = APIRouter()

@router.post("/github-webhook")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None)
):
    payload = await request.json()
    log.info(f"📩 Received GitHub event: {x_github_event}")

    if x_github_event == "push":
        message = handle_push_event(payload)

    elif x_github_event == "issues":
        message = handle_issue_event(payload)

    elif x_github_event == "pull_request":
        message = handle_pr_event(payload)

    else:
        message = f"Unhandled event type: {x_github_event}"
        log.info(message)

    # Send update to Telegram
    send_telegram_message(message)

    return {"status": "ok", "message": message}
