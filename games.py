from telegram import Update
from telegram.ext import ContextTypes
from database import add_xp
from data import random_synonym, random_literature, random_psych

async def synonym(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, answer = random_synonym()
    context.user_data["answer"] = answer
    await update.message.reply_text(f"🎮 Give a synonym for the word: '{word}'")

async def literature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    definition, answer = random_literature()
    context.user_data["answer"] = answer
    await update.message.reply_text(f"📚 What is the literary term for:\n'{definition}'?")

async def psych(update: Update, context: ContextTypes.DEFAULT_TYPE):
    definition, answer = random_psych()
    context.user_data["answer"] = answer
    await update.message.reply_text(f"🧠 What is the psychological term for:\n'{definition}'?")

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "answer" not in context.user_data:
        return

    # Check if the user's text matches the answer (ignoring capitalization)
    if update.message.text.lower().strip() == context.user_data["answer"].lower():
        add_xp(update.message.from_user)
        # Clear the answer so they can't just type it again
        del context.user_data["answer"]
        await update.message.reply_text("✅ Correct! XP added to your profile. Type the command again for another question!")
    else:
        await update.message.reply_text("❌ Not quite! Try again, or type another command to change the subject.")
