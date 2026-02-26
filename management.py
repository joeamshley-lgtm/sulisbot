from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
import time

BAD_WORDS = ["anjing", "babi"]

async def filter_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    for word in BAD_WORDS:
        if word in text:
            await update.message.delete()
            break

user_messages = {}

async def spam_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    now = time.time()

    if user not in user_messages:
        user_messages[user] = []

    user_messages[user].append(now)
    user_messages[user] = [t for t in user_messages[user] if now - t < 5]

    if len(user_messages[user]) > 5:
        await context.bot.restrict_chat_member(
            update.message.chat_id,
            user,
            ChatPermissions(can_send_messages=False),
            until_date=now + 30
        )