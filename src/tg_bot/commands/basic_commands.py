from telegram import Update
from telegram.ext import ContextTypes

from src.tg_bot.conversations.utils.keyboards import StandardKeyboards
from src.tg_bot.utils.cache import cache


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username

    if user not in cache:
        cache.new_profile(username=user)

    await update.message.reply_html(
        rf"Привет, {user}!",
        reply_markup=StandardKeyboards.MAIN_MENU,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here's what you can do:"
                                    "\n/start - to start chatting with the bot,"
                                    "\n/help - to see available commands.")
