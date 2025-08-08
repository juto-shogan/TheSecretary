from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from app.utils.storage import add_repo, remove_repo, load_monitored_repos
from app.utils.logger import log
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def monitor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /monitor username/repo")
        return

    repo_name = context.args[0]
    if add_repo(repo_name):
        await update.message.reply_text(f"✅ Now monitoring `{repo_name}`")
        log.info(f"Started monitoring {repo_name}")
    else:
        await update.message.reply_text(f"⚠️ Already monitoring `{repo_name}`")

async def unmonitor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /unmonitor username/repo")
        return

    repo_name = context.args[0]
    if remove_repo(repo_name):
        await update.message.reply_text(f"❌ Stopped monitoring `{repo_name}`")
        log.info(f"Stopped monitoring {repo_name}")
    else:
        await update.message.reply_text(f"⚠️ `{repo_name}` was not being monitored")

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repos = load_monitored_repos()
    if repos:
        await update.message.reply_text("📋 Monitored repos:\n" + "\n".join(f"- {r}" for r in repos))
    else:
        await update.message.reply_text("📋 No repos are currently being monitored.")

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("monitor", monitor_command))
    app.add_handler(CommandHandler("unmonitor", unmonitor_command))
    app.add_handler(CommandHandler("list", list_command))

    log.info("Telegram bot started")
    app.run_polling()
