import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from notion.client import NotionClient
from notion.handlers.fields_handler import FieldsHandler
from notion.handlers.notion_db_handler import NotionDBHandler
from tg_bot.conversations.utils.buttons import SKIP, ADD_CONNECTION, CANCEL, command_filter, BACK
from tg_bot.conversations.utils.conversation_points.conn_points import CONN_NAME, TOKEN_QUERY, DB_ID, \
    DB_FIELDS, UDB_ID, PROJECTS_DB
from tg_bot.conversations.utils.replies.conn_replies import ConnectionReplier
from tg_bot.conversations.utils.keyboards import StandardKeyboards
from tg_bot.utils.cache import cache

logger = logging.getLogger(__name__)


def token_valid(token: str):
    if not token.startswith("secret_"):
        return False
    if len(token) != 50:
        return False

    return True


async def conn_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username

    logger.info('{} started conversation "create connection"'.format(username))

    if username not in cache:
        cache.new_profile(username=username)

    replier = ConnectionReplier(
        options={
            "has_user_db": True,
            "has_projects_db": True
        }
    )

    cache[username]["replier"] = replier

    return await replier.current_reply(update=update, username=username)


async def connection_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    response = update.message.text
    replier = cache[username]["replier"]

    logger.info("{} selected connection name".format(username))

    if response == SKIP.text:
        await update.message.reply_text(text="Этот момент нельзя пропустить")
        return
    if response == BACK.text:
        await update.message.reply_text("Вернуться нельзя. Ты уже в начале")
        return

    if response in cache[username]["profile"].connections:
        await update.message.reply_text(text="Соединение с таким названием уже есть. Давай другое ;)")
        return

    cache[username]["context"]["connection"]["name"] = response

    return await replier.next_reply(update=update, username=username)


async def token_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    response = update.message.text
    replier = cache[username]["replier"]

    if response == SKIP.text:
        await update.message.reply_text(text="Этот момент нельзя пропустить")
        return
    if response == BACK.text:
        await update.message.reply_text("Возвращаемся...")
        return await replier.previous_reply(update=update, username=username)

    logger.info("{} entered token".format(username))

    if not token_valid(response):
        await update.message.reply_text(text="Кажется, токен был введен неверно. Попробуй еще раз")
        return

    cache[username]["context"]["connection"]["token"] = response
    cache[username]["context"]["databases"] = NotionDBHandler(client=NotionClient(token=response)).databases

    return await replier.next_reply(update=update, username=username)


async def db_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    response = update.message.text
    replier = cache[username]["replier"]

    logger.info("{} added database id".format(username))

    if response == SKIP.text:
        await update.message.reply_text(text="Этот момент нельзя пропустить")
        return
    if response == BACK.text:
        await update.message.reply_text("Возвращаемся...")
        return await replier.previous_reply(update=update, username=username)

    selected_db = cache[username]["context"]["databases"][response]

    cache[username]["context"]["connection"]["database_id"] = selected_db

    token = cache[username]["context"]["connection"]["token"]
    cache[username]["context"]["fields"] = FieldsHandler(
        client=NotionClient(token=token),
        database_id=selected_db
    ).fields

    return await replier.next_reply(update=update, username=username)


async def db_fields(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    response = update.message.text
    replier = cache[username]["replier"]

    if response == BACK.text:
        cache[username]["context"]["set_fields"] = {}
        await update.message.reply_text("Возвращаемся...")
        return await replier.previous_reply(update=update, username=username)

    chosen_field = None

    if "task_name_field" not in cache[username]["context"]["set_fields"]:
        if response == SKIP.text:
            await update.message.reply_text(text="Этот момент нельзя пропустить")
            return

        logger.info("{} is setting up task field".format(username))

        chosen_field = cache[username]["context"]["fields"][response]
        cache[username]["context"]["set_fields"]["task_name_field"] = chosen_field
        await update.message.reply_text(text="Выбери поле ответственного задачи:",
                                        reply_markup=StandardKeyboards.IN_PROGRESS(
                                            markup=[[button] for button in cache[username]["context"]["fields"].keys()]
                                        ))

        return
    elif "worker_field_name" not in cache[username]["context"]["set_fields"]:
        if response != SKIP.text:
            chosen_field = cache[username]["context"]["fields"][response]

        logger.info("{} is setting up worker field".format(username))

        cache[username]["context"]["set_fields"]["worker_field_name"] = chosen_field
        await update.message.reply_text(text="Выбери поле проекта задачи:", reply_markup=StandardKeyboards.IN_PROGRESS(
            markup=[[button] for button in cache[username]["context"]["fields"].keys()]
        ))

        return
    elif "project_field_name" not in cache[username]["context"]["set_fields"]:
        if response != SKIP.text:
            chosen_field = cache[username]["context"]["fields"][response]

        logger.info("{} is setting up project field".format(username))

        cache[username]["context"]["set_fields"]["project_field_name"] = chosen_field
        await update.message.reply_text(text="Выбери поле дедлайна задачи:", reply_markup=StandardKeyboards.IN_PROGRESS(
            markup=[[button] for button in cache[username]["context"]["fields"].keys()]
        ))

        return
    elif "deadline_field_name" not in cache[username]["context"]["set_fields"]:
        if response != SKIP.text:
            chosen_field = cache[username]["context"]["fields"][response]

        logger.info("{} is setting up deadline field".format(username))

        cache[username]["context"]["set_fields"]["deadline_field_name"] = chosen_field

    current_step = replier.stepper.step

    replier.reinit(
        options={
            "has_user_db": cache[username]["context"]["set_fields"]["worker_field_name"],
            "has_projects_db": cache[username]["context"]["set_fields"]["project_field_name"]
        },
        step=current_step
    )

    return await replier.next_reply(update=update, username=username)


async def user_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    response = update.message.text
    replier = cache[username]["replier"]

    if response == SKIP.text:
        await update.message.reply_text(text="Пропускаем...")
        return
    if response == BACK.text:
        await update.message.reply_text("Возвращаемся...")
        return await replier.previous_reply(update=update, username=username)

    logger.info("{} is setting up worker database connection".format(username))

    selected_db = cache[username]["context"]["databases"][response]

    cache[username]["context"]["connection"]["user_db_id"] = selected_db

    return await replier.next_reply(update=update, username=username)


async def projects_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    response = update.message.text
    replier = cache[username]["replier"]

    if response == SKIP.text:
        await update.message.reply_text(text="Пропускаем...")
        return
    if response == BACK.text:
        await update.message.reply_text("Возвращаемся...")
        return await replier.previous_reply(update=update, username=username)

    logger.info("{} is setting up project database connection".format(username))

    selected_db = cache[username]["context"]["databases"][response]

    cache[username]["context"]["connection"]["projects_db_id"] = selected_db

    return await replier.next_reply(update=update, username=username)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    cache.wipe_context(username=username)

    logger.info("{} cancelled connection setup".format(username))

    await update.message.reply_text(text="Стираю записи :)", reply_markup=StandardKeyboards.MAIN_MENU)

    return ConversationHandler.END


CREATE_CONN_CONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(f"^{ADD_CONNECTION.text}$"), conn_name)],
    states={
        CONN_NAME: [
            MessageHandler(
                filters.TEXT & command_filter,
                connection_name
            )
        ],
        TOKEN_QUERY: [
            MessageHandler(
                filters.TEXT & command_filter,
                token_query
            )
        ],
        DB_ID: [
            MessageHandler(
                filters.TEXT & command_filter,
                db_id
            )
        ],
        DB_FIELDS: [
            MessageHandler(
                filters.TEXT & command_filter,
                db_fields
            )
        ],
        UDB_ID: [
            MessageHandler(
                filters.TEXT & command_filter,
                user_db
            )
        ],
        PROJECTS_DB: [
            MessageHandler(
                filters.TEXT & command_filter,
                projects_db
            )
        ],
    },
    fallbacks=[MessageHandler(filters.Regex(f"^{CANCEL.text}$"), cancel)],
)
