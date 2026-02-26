from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TOKEN
from games import synonym, literature, psych, check_answer
from translation import auto_translate
from management import filter_bad_words, spam_control
from database import get_profile
from telegram import Update
from telegram.ext import ContextTypes

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_profile(update.message.from_user.id)
    if result:
        xp, level, correct, wrong = result
        await update.message.reply_text(
            f"Level: {level}\nXP: {xp}\nCorrect: {correct}\nWrong: {wrong}"
        )
    else:
        await update.message.reply_text("No data yet.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("synonym", synonym))
app.add_handler(CommandHandler("literature", literature))
app.add_handler(CommandHandler("psych", psych))
app.add_handler(CommandHandler("profile", profile))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_bad_words))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, spam_control))

app.run_polling()