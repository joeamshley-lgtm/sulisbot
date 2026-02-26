import os
from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop
from openai import AsyncOpenAI


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠ OPENAI_API_KEY is missing")
        return None
    return AsyncOpenAI(api_key=api_key)


async def conversational_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    client = get_client()

    if client is None:
        await update.message.reply_text(
            "⚠ OpenAI API key is not configured properly."
        )
        raise ApplicationHandlerStop()

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # better & cheaper than 3.5
            messages=[
                {
                    "role": "system",
                    "content": "You are an elite academic assistant specializing in literary analysis, psychoanalytic theory, and Factual Reading."
                },
                {"role": "user", "content": user_message}
            ],
            max_tokens=300
        )

        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)

        raise ApplicationHandlerStop()

    except Exception as e:
        print("OpenAI Error:", e)
        await update.message.reply_text(
            "⚠ I'm having trouble connecting to OpenAI right now."
        )
        raise ApplicationHandlerStop()
