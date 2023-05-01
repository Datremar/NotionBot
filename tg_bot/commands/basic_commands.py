from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.conversations.utils.keyboards import StandardKeyboards


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username
    await update.message.reply_html(
        rf"Привет, {user}!",
        reply_markup=StandardKeyboards.MAIN_MENU,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here's what you can do:"
                                    "\n/help - to get commands descriptions,"
                                    "\n/task - to create a task in Notion.")
