import os
from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop
from openai import AsyncOpenAI

# Initialize the OpenAI client using the token from Railway's variables
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def conversational_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # We send a "typing..." action so the user knows the bot is thinking
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        # Send the message to OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo", # You can change this to gpt-4o-mini if you prefer
            messages=[
                {"role": "system", "content": "You are an elite academic assistant specializing in literary analysis, psychoanalytic theory, and Factual Reading. You help university students analyze texts, draft journal articles, and debate complex themes like the True vs. False Self. Keep your answers insightful, well-structured, and academic, but conversational."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300 # Keeps responses from getting too long
        )
        
        # Extract the text from OpenAI's response
        ai_reply = response.choices[0].message.content
        
        # Send the reply back to Telegram
        await update.message.reply_text(ai_reply)
        
        # Stop the message from continuing to the auto-translator
        raise ApplicationHandlerStop()
        
    except Exception as e:
        await update.message.reply_text("I'm having a little trouble connecting to my academic database right now. Please try again in a moment!")
        print(f"OpenAI Error: {e}")
        raise ApplicationHandlerStop()
