# app/telegram_bot.py
import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from app.utils.logger import log
from app.services import repo_manager  # expects add_subscription, remove, load_subscriptions
from app.services.github_service import add_github_webhook


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Optional: BOT can use CHAT_ID for direct alerts, but commands work without it
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # used by repo info fetch if present

if not BOT_TOKEN:
    log.error("TELEGRAM_BOT_TOKEN missing in .env. Bot cannot start.")
    raise SystemExit("Missing TELEGRAM_BOT_TOKEN in .env")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greet user and show help hint."""
    user = update.effective_user
    text = (
        f"Hey {user.first_name or 'there'}! I'm your GitHub monitor bot.\n\n"
        "Commands available:\n"
        "/monitor <owner/repo> — start monitoring a repo (automatically add webhook)\n"
        "/unmonitor <owner/repo> — stop monitoring\n"
        "/list — list monitored repos\n"
        "/repo <owner/repo> — fetch repo stats now\n"
        "/help — show this message\n"
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_command(update, context)


# Inside telegram_bot.py~

async def monitor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not context.args:
        await message.reply_text("❌ Please provide a repository. Example:\n`/monitor owner/repo`", parse_mode="Markdown")
        return

    repo = context.args[0].strip()

    # Validate repo format (owner/repo)
    if "/" not in repo:
        await message.reply_text("❌ Invalid repo format. Use: owner/repo")
        return

    await message.reply_text(f"🔍 Setting up monitoring for `{repo}`...", parse_mode="Markdown")

    # Try to add GitHub webhook
    if add_github_webhook(repo):
        await message.reply_text(f"✅ Monitoring started for `{repo}`", parse_mode="Markdown")
    else:
        await message.reply_text(f"❌ Failed to monitor `{repo}`. Check logs for details.", parse_mode="Markdown")


 
async def unmonitor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /unmonitor owner/repo")
        return

    repo_full = context.args[0].strip()
    try:
        removed = repo_manager.remove_subscription(repo_full)
        if removed:
            await update.message.reply_text(f"Stopped monitoring {repo_full}")
        else:
            await update.message.reply_text(f"{repo_full} was not being monitored.")
    except Exception as e:
        log.error(f"Error in /unmonitor: {e}")
        await update.message.reply_text(f"Failed to unmonitor {repo_full}: {e}")


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        subs = repo_manager.load_subscriptions()
        if not subs:
            await update.message.reply_text("No repos are currently being monitored.")
            return
        message = "Monitored repos:\n" + "\n".join(f"- {s}" for s in subs)
        await update.message.reply_text(message)
    except Exception as e:
        log.error(f"Error in /list: {e}")
        await update.message.reply_text("Failed to load subscriptions.")


def _fetch_repo_info(repo_full: str):
    """Helper: synchronously fetch repo info from GitHub REST API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    url = f"https://api.github.com/repos/{repo_full}"
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"GitHub API returned {resp.status_code}: {resp.text}")
    return resp.json()


async def repo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return repository stats on demand: stars, forks, open issues, latest commit date."""
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /repo owner/repo")
        return

    repo_full = context.args[0].strip()
    try:
        data = _fetch_repo_info(repo_full)

        name = data.get("full_name", repo_full)
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        watchers = data.get("subscribers_count", data.get("watchers_count", 0))
        open_issues = data.get("open_issues_count", 0)
        description = data.get("description") or "No description"
        html_url = data.get("html_url")
        pushed_at = data.get("pushed_at") or "Unknown"
        created_at = data.get("created_at") or "Unknown"

        reply = (
            f"*{name}*\n"
            f"{description}\n"
            f"⭐ Stars: {stars} | 🍴 Forks: {forks} | 👀 Watchers: {watchers}\n"
            f"🐞 Open issues: {open_issues}\n"
            f"Last push: {pushed_at}\n"
            f"Created: {created_at}\n"
            f"{html_url}"
        )
        # send as markdown
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception as e:
        log.error(f"/repo error for {repo_full}: {e}")
        await update.message.reply_text(f"Failed to fetch repo info: {e}")


def run_bot():
    """Start the Telegram bot (blocking)."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Basic commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Monitoring commands
    app.add_handler(CommandHandler("monitor", monitor_command))
    app.add_handler(CommandHandler("unmonitor", unmonitor_command))
    app.add_handler(CommandHandler("list", list_command))

    # Repo info
    app.add_handler(CommandHandler("repo", repo_command))

    # Start polling
    log.info("Starting Telegram bot (polling)...")
    app.run_polling()


if __name__ == "__main__":
    # Make logging from python-telegram-bot quieter; rely on your app logger
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    try:
        run_bot()
    except Exception as e:
        log.error(f"Telegram bot crashed: {e}")
        raise
