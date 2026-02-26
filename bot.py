import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- Custom Modules ---
from config import TOKEN
from games import synonym, literature, psych, check_answer
from translation import auto_translate
from management import filter_bad_words, spam_control
from database import get_profile
from chat import conversational_chat


# =========================
# Commands
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to RigenSulisbot!\nType /help to see commands."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Commands:\n"
        "/synonym\n"
        "/literature\n"
        "/psych\n"
        "/profile\n"
    )


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_profile(update.message.from_user.id)
    if result:
        xp, level, correct, wrong = result
        await update.message.reply_text(
            f"Level: {level}\nXP: {xp}\nCorrect: {correct}\nWrong: {wrong}"
        )
    else:
        await update.message.reply_text("No data yet.")


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Welcome {member.first_name}! Type /help to start learning!"
        )


# =========================
# Railway Health Server
# =========================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")


def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


threading.Thread(target=run_health_server, daemon=True).start()


# =========================
# Initialize App
# =========================

print("=== BOT INITIALIZING ===")

app = ApplicationBuilder().token(TOKEN).build()

# Command Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("synonym", synonym))
app.add_handler(CommandHandler("literature", literature))
app.add_handler(CommandHandler("psych", psych))
app.add_handler(CommandHandler("profile", profile))

# Welcome new members
app.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
)

# Security layer
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, filter_bad_words),
    group=1
)
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, spam_control),
    group=2
)

# Game answer checking
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer),
    group=3
)

# Auto translation
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, auto_translate),
    group=4
)

# ChatGPT (last so it doesn’t block others)
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, conversational_chat),
    group=5
)

print("=== STARTING POLLING ===")
app.run_polling(drop_pending_updates=True)
