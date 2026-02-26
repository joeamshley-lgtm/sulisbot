import os
from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop
import google.generativeai as genai

# Connect to Gemini using your Railway variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the AI model with an elite academic persona
system_instruction = (
    "You are an elite academic assistant specializing in literary analysis, "
    "psychoanalytic theory, and Factual Reading. You help university students "
    "analyze texts, draft journal articles, and debate complex themes like "
    "Winnicott's True vs. False Self. Keep your answers insightful, well-structured, "
    "and academic, but conversational."
)

# Initialize the specific Gemini model
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction
)

async def conversational_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Send a "typing..." action to Telegram
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        # Ask Gemini to generate a response asynchronously
        response = await model.generate_content_async(user_message)
        
        # Send the text back to the user
        await update.message.reply_text(response.text)
        
        # Stop the message from hitting the auto-translator
        raise ApplicationHandlerStop()
        
    except Exception as e:
        await update.message.reply_text("I'm having a little trouble connecting to my academic database right now. Please try again in a moment!")
        print(f"Gemini Error: {e}")
        raise ApplicationHandlerStop()
