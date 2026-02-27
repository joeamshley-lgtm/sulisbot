from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler
)

from database import (
    get_group_settings,
    initialize_group_settings,
    update_group_setting
)


# =========================
# Helper: Build Panel UI
# =========================

def build_panel(chat_id: int):
    settings = get_group_settings(chat_id)

    ai_status = "ON 🤖" if settings["ai_enabled"] else "OFF ❌"
    games_status = "ON 🎮" if settings["games_enabled"] else "OFF ❌"
    translate_status = "ON 🌍" if settings["translate_enabled"] else "OFF ❌"
    mode = settings["mode"].capitalize()

    text = (
        "⚙ *Group Control Panel*\n\n"
        f"AI: {ai_status}\n"
        f"Games: {games_status}\n"
        f"Translate: {translate_status}\n"
        f"Mode: {mode}\n"
    )

    keyboard = [
        [InlineKeyboardButton("Toggle AI 🤖", callback_data=f"toggle_ai:{chat_id}")],
        [InlineKeyboardButton("Toggle Games 🎮", callback_data=f"toggle_games:{chat_id}")],
        [InlineKeyboardButton("Toggle Translate 🌍", callback_data=f"toggle_translate:{chat_id}")],
        [InlineKeyboardButton("Change Mode 🎓", callback_data=f"change_mode:{chat_id}")],
    ]

    return text, InlineKeyboardMarkup(keyboard)


# =========================
# /settings Command
# =========================

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works inside groups.")
        return

    member = await context.bot.get_chat_member(chat.id, user.id)

    await update.message.reply_text(
        f"Your Telegram status in this group is: {member.status}"
    )

    return
        

    initialize_group_settings(chat.id)

    text, markup = build_panel(chat.id)

    await update.message.reply_text(
        text,
        reply_markup=markup,
        parse_mode="Markdown"
    )


# =========================
# Callback Handler
# =========================

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    action, chat_id = data.split(":")
    chat_id = int(chat_id)

    if action == "toggle_ai":
        current = get_group_settings(chat_id)["ai_enabled"]
        update_group_setting(chat_id, "ai_enabled", not current)

    elif action == "toggle_games":
        current = get_group_settings(chat_id)["games_enabled"]
        update_group_setting(chat_id, "games_enabled", not current)

    elif action == "toggle_translate":
        current = get_group_settings(chat_id)["translate_enabled"]
        update_group_setting(chat_id, "translate_enabled", not current)

    elif action == "change_mode":
        current_mode = get_group_settings(chat_id)["mode"]

        modes = ["academic", "casual", "silent"]
        next_mode = modes[(modes.index(current_mode) + 1) % len(modes)]

        update_group_setting(chat_id, "mode", next_mode)

    text, markup = build_panel(chat_id)

    await query.edit_message_text(
        text,
        reply_markup=markup,
        parse_mode="Markdown"
    )


# =========================
# Register Function
# =========================

def register_admin_panel(app):
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CallbackQueryHandler(settings_callback))
