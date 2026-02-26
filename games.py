from telegram import Update
from telegram.ext import ContextTypes
from database import add_xp
from data import random_synonym, random_literature, random_psych

async def synonym(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, answer = random_synonym()
    context.user_data["answer"] = answer
    await update.message.reply_text(f"Give a synonym of '{word}'")

async def literature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, answer = random_literature()
    context.user_data["answer"] = answer
    await update.message.reply_text(f"Define literary term '{word}'")

async def psych(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, answer = random_psych()
    context.user_data["answer"] = answer
    await update.message.reply_text(f"Define psychological term '{word}'")

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "answer" not in context.user_data:
        return

    if update.message.text.lower() == context.user_data["answer"].lower():
        add_xp(update.message.from_user)
        await update.message.reply_text("✅ Correct! XP added.")
    else:
        await update.message.reply_text("❌ Wrong.")