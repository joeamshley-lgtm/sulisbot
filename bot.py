import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Your custom module imports
from config import TOKEN
from games import synonym, literature, psych, check_answer
from translation import auto_translate
from management import filter_bad_words, spam_control
from database import get_profile

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_profile(update.message.fromuser.id)
    if result:
        xp, level, correct, wrong = result
        await update.message.reply_text(
            f"Level: {level}\nXP: {xp}\nCorrect: {correct}\nWrong: {wrong}"
        )
    else:
        await update.message.reply_text("No data yet.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is alive and ready for research!")

# --- Railway Health Server ---
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

print("=== BOT INITIALIZING ===")

# Initialize the app ONLY ONCE
app = ApplicationBuilder().token(TOKEN).build()

# 1. Command Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("synonym", synonym))
app.add_handler(CommandHandler("literature", literature))
app.add_handler(CommandHandler("psych", psych))
app.add_handler(CommandHandler("profile", profile))

# 2. Message Handlers (Grouped so they don't block each other)
# Group 1: Security/Management checks run first
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_bad_words), group=1)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, spam_control), group=2)

# Group 2: Features/Games run after security checks
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer), group=3)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_translate), group=4)

print("=== STARTING POLLING ===")
app.run_polling(drop_pending_updates=True)
print("=== THIS SHOULD NEVER PRINT ===")
