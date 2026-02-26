import os
from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop
from google import genai

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠ GEMINI_API_KEY missing")
        return None
    return genai.Client(api_key=api_key)


async def conversational_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    client = get_client()

    if client is None:
        await update.message.reply_text("⚠ Gemini API key not configured.")
        raise ApplicationHandlerStop()

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_message,
        )

        await update.message.reply_text(response.text)

        raise ApplicationHandlerStop()

    except Exception as e:
        print("Gemini Error:", e)
        await update.message.reply_text("⚠ Gemini is not responding right now.")
        raise ApplicationHandlerStop()
