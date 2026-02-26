import os
from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop
from google import genai
from google.genai import types

# 1. Initialize the NEW async client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")).aio

# 2. Set up the AI model's academic persona using the new Config type
config = types.GenerateContentConfig(
    system_instruction=(
        "You are an elite academic assistant specializing in English literature, "
        "psychoanalytic theory, and Factual Reading. You help university students "
        "analyze texts, draft journal articles, and debate complex themes like "
        "structural fragmentation and Winnicott's True vs. False Self. Keep your answers "
        "insightful, well-structured, and academic, but conversational."
    )
)

async def conversational_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Send a "typing..." action to Telegram
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
      # 3. Generate the response using the new syntax
        response = await client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=config
        )
        
        # Telegram has a 4096 character limit per message.
        # We split the AI's long response into chunks of 4000 characters to be safe.
        ai_reply = response.text
        for i in range(0, len(ai_reply), 4000):
            await update.message.reply_text(ai_reply[i:i+4000])
        
        # Stop the message from hitting the auto-translator
        raise ApplicationHandlerStop()
        
    except Exception as e:
        await update.message.reply_text("I'm having a little trouble connecting to my academic database right now. Please try again in a moment!")
        print(f"Gemini Error: {e}")
        raise ApplicationHandlerStop()
