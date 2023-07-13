import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from src.database.handlers.connection_handler import ConnectionHandler
from src.tg_bot.conversations.utils.buttons import CANCEL, command_filter, SKIP, DELETE_CONNECTION
from src.tg_bot.conversations.utils.keyboards import StandardKeyboards
from src.tg_bot.utils.cache import cache


logger = logging.getLogger(__name__)


DEL_CONN = 1


async def delete_conn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username

    logger.info("{} initialized delete connection conversation".format(username))

    if username not in cache or not cache[username]["profile"].connections:
        await update.message.reply_text(
            text="Кажется, у тебя нет соединений. Стоит добавить хотя-бы одно ;)",
            reply_markup=StandardKeyboards.MAIN_MENU
        )

        return ConversationHandler.END

    connections = cache[username]["profile"].connections
    current_connection = cache[username]["profile"].current_connection

    if current_connection is not None:
        await update.message.reply_text(text="Текущее соединение: {}".format(current_connection.name))

    await update.message.reply_text(
        text="Выбери соединение",
        reply_markup=StandardKeyboards.IN_PROGRESS(markup=[[conn] for conn in connections.keys()])
    )

    return DEL_CONN


async def delete_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    response = update.message.text

    if response == SKIP.text:
        await update.message.reply_text(text="Этот момент нельзя пропустить")
        return

    connections = cache[username]["profile"].connections

    if response not in connections:
        await update.message.reply_text(text="У тебя нет такого соединения")
        return

    ConnectionHandler.delete_connection(username=username, name=response)

    cache[username]["profile"].connections.pop(response)

    current_connection = cache[username]["profile"].current_connection
    if current_connection is not None and response == current_connection.name:
        cache[username]["profile"].current_connection = None

    await update.message.reply_text(
        text="Соединение {} было удалено".format(response),
        reply_markup=StandardKeyboards.MAIN_MENU
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    cache.wipe_context(username=username)

    logger.info("{} cancelled delete connection conversation".format(username))

    await update.message.reply_text(text="Отменяю :)", reply_markup=StandardKeyboards.MAIN_MENU)

    return ConversationHandler.END


DEL_CONN_CONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(f"^{DELETE_CONNECTION.text}$"), delete_conn)],
    states={
        DEL_CONN: [
            MessageHandler(
                filters.TEXT & command_filter,
                delete_db
            )
        ],
    },
    fallbacks=[MessageHandler(filters.Regex(f"^{CANCEL.text}$"), cancel)],
)
