from telegram import Update
from telegram.ext import ContextTypes
from deep_translator import GoogleTranslator
from langdetect import detect

async def auto_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    detected = detect(text)
    target = "en" if detected != "en" else "id"
    translated = GoogleTranslator(source=detected, target=target).translate(text)

    await update.message.reply_text(
        f"Detected: {detected}\nTranslation:\n{translated}"
    )