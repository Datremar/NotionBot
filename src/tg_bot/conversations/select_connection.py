import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from src.tg_bot.conversations.utils.buttons import CANCEL, command_filter, SELECT_CONNECTION, SKIP
from src.tg_bot.conversations.utils.keyboards import StandardKeyboards
from src.tg_bot.utils.cache import cache
from src.tg_bot.utils.data_models import UserData

logger = logging.getLogger(__name__)

SEL_CONN = 1


async def select_conn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username

    logger.info("{} initialized select connection conversation".format(username))

    if username not in cache:
        user = UserData(
            username=username,
            connections={},
            current_connection=None
        )

        cache[username] = {
            "profile": user,
            "context": {
                "connection": {},
                "set_fields": {}
            }
        }

    connections = cache[username]["profile"].connections

    if not connections:
        await update.message.reply_text(
            text="Кажется, у тебя нет соединений. Стоит добавить хотя-бы одно ;)",
            reply_markup=StandardKeyboards.MAIN_MENU
        )

        return ConversationHandler.END

    current_connection = cache[username]["profile"].current_connection

    if current_connection is not None:
        await update.message.reply_text(text="Текущее соединение: {}".format(current_connection.name))

    await update.message.reply_text(
        text="Выбери соединение",
        reply_markup=StandardKeyboards.IN_PROGRESS(markup=[[conn] for conn in connections.keys()])
    )

    return SEL_CONN


async def select_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    response = update.message.text

    if response == SKIP.text:
        await update.message.reply_text(text="Этот момент нельзя пропустить")
        return

    connections = cache[username]["profile"].connections

    if response not in connections:
        await update.message.reply_text(text="У тебя нет такого соединения")
        return

    logger.info("{} selected connection".format(username))

    cache[username]["profile"].current_connection = connections[response]

    await update.message.reply_text(
        text="Переключил на соединение {}".format(response),
        reply_markup=StandardKeyboards.MAIN_MENU
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    cache.wipe_context(username=username)

    logger.info("{} cancelled select connection conversation".format(username))

    await update.message.reply_text(text="Отменяю :)", reply_markup=StandardKeyboards.MAIN_MENU)

    return ConversationHandler.END


SEL_CONN_CONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(f"^{SELECT_CONNECTION.text}$"), select_conn)],
    states={
        SEL_CONN: [
            MessageHandler(
                filters.TEXT & command_filter,
                select_db
            )
        ],
    },
    fallbacks=[MessageHandler(filters.Regex(f"^{CANCEL.text}$"), cancel)],
)
