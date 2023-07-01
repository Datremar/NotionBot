import asyncio
import logging

from telegram import Update
from telegram.ext import ConversationHandler

from database.handlers.connection_handler import ConnectionHandler
from notion.client import NotionClient
from notion.connection import Connection
from notion.handlers.notion_db_handler import NotionDBHandler
from notion.handlers.utils.field_names import FieldNames
from tg_bot.conversations.utils.conversation_points.conn_points import CONN_NAME, TOKEN_QUERY, DB_ID, DB_FIELDS, UDB_ID, \
    PROJECTS_DB
from tg_bot.conversations.utils.keyboards import StandardKeyboards
from tg_bot.conversations.utils.replies.replier import Replier
from tg_bot.utils.cache import cache


logger = logging.getLogger(__name__)


class ConnectionReplier(Replier):
    def __init__(self, options: dict):
        self.steps = [
            CONN_NAME,
            TOKEN_QUERY,
            DB_ID,
            DB_FIELDS,
            UDB_ID if options["has_user_db"] is not None else None,
            PROJECTS_DB if options["has_projects_db"] is not None else None,
            ConversationHandler.END
        ]

        self.replies = {
            CONN_NAME: conn_name_reply,
            TOKEN_QUERY: token_reply,
            DB_ID: db_id_reply,
            DB_FIELDS: fields_reply,
            UDB_ID: udb_reply,
            PROJECTS_DB: projects_reply,
            ConversationHandler.END: end_reply
        }

        super().__init__(self.replies, self.steps)

    def reinit(self, options: dict, step: int):
        self.steps = [
            CONN_NAME,
            TOKEN_QUERY,
            DB_ID,
            DB_FIELDS,
            UDB_ID if options["has_user_db"] is not None else None,
            PROJECTS_DB if options["has_projects_db"] is not None else None,
            ConversationHandler.END
        ]
        super().restart(self.steps, step=step)


async def conn_name_reply(update: Update, username: str, **kwargs):
    await update.message.reply_text(text="Как назовем соединение с БД?", reply_markup=StandardKeyboards.IN_PROGRESS())

    return CONN_NAME


async def token_reply(update: Update, username: str, **kwargs):
    await update.message.reply_text(text="Установим соединение с твоей базой данных Notion :D")
    await update.message.reply_text(text="Убедись, что у тебя создан токен авторизации в Notion. Он нам скоро "
                                         "понадобится")
    await update.message.reply_text(text="Если ты не знаешь о каком токене идет речь, вот ссылка на то, как его "
                                         "создать")
    await update.message.reply_text(text="https://developers.notion.com/docs/authorization")

    await asyncio.sleep(2)

    await update.message.reply_text(text="Введи токен авторизации :)")

    return TOKEN_QUERY


async def db_id_reply(update: Update, username: str, **kwargs):
    await update.message.reply_text(
        text="Выбери базу данных, где лежат записи о задачах",
        reply_markup=StandardKeyboards.IN_PROGRESS(
            markup=[
                [dbid] for dbid in cache[username]["context"]["databases"].keys()
            ]
        )
    )

    return DB_ID


async def fields_reply(update: Update, username: str, **kwargs):
    await update.message.reply_text(text="Теперь назначим поля...")
    await update.message.reply_text(text="Выбери поле названия задачи:", reply_markup=StandardKeyboards.IN_PROGRESS(
        markup=[[button] for button in cache[username]["context"]["fields"].keys()]
    ))

    return DB_FIELDS


async def udb_reply(update: Update, username: str, **kwargs):
    token = cache[username]["context"]["connection"]["token"]
    await update.message.reply_text(text="Загружаю список...")
    await update.message.reply_text(
        text="Выбери базу данных, где лежат записи о работниках",
        reply_markup=StandardKeyboards.IN_PROGRESS(
            markup=[
                [dbid] for dbid in NotionDBHandler(
                    client=NotionClient(token=token)
                ).databases.keys()
            ]
        )
    )

    return UDB_ID


async def projects_reply(update: Update, username: str, **kwargs):
    token = cache[username]["context"]["connection"]["token"]
    await update.message.reply_text(text="Загружаю список...")
    await update.message.reply_text(
        text="Выбери базу данных, где лежат записи о проектах",
        reply_markup=StandardKeyboards.IN_PROGRESS(
            markup=[
                [dbid] for dbid in NotionDBHandler(
                    client=NotionClient(token=token)
                ).databases.keys()
            ]
        )
    )

    return PROJECTS_DB


async def end_reply(update: Update, username: str):
    logger.info("{} is establishing connection to the database".format(username))
    await update.message.reply_text(text="Устанавливаю соединение...")

    conn = cache[username]["context"]["connection"]
    set_fields = cache[username]["context"]["set_fields"]

    con_name = conn["name"]
    token = conn["token"]
    name_field = set_fields["task_name_field"]["name"]
    database_id = conn["database_id"]

    worker_field = set_fields["worker_field_name"]
    project_field = set_fields["project_field_name"]
    deadline_field = set_fields["deadline_field_name"]

    worker_field_name = worker_field["name"] if worker_field is not None else None
    project_field_name = project_field["name"] if project_field is not None else None
    deadline_field_name = deadline_field["name"] if deadline_field is not None else None

    user_db_id = conn["user_db_id"] if worker_field is not None else None
    projects_db_id = conn["projects_db_id"] if project_field is not None else None

    connection = cache[username]["profile"].connections[con_name] = Connection(
        username=username,
        name=con_name,
        token=token,
        database_id=database_id,
        user_db_id=user_db_id,
        projects_db_id=projects_db_id,
        field_names=FieldNames(
            task_name_field=name_field,
            worker_field_name=worker_field_name,
            project_field_name=project_field_name,
            deadline_field_name=deadline_field_name
        )
    )

    if all(connection.check_connection()) and connection.make_test_task():
        ConnectionHandler.save_connection(
            username=connection.username,
            name=connection.name,
            token=connection.token,
            database_id=connection.database_id,
            user_db_id=connection.user_db_id,
            projects_db_id=connection.projects_db_id,
            fields=connection.field_names.dict()
        )

        await update.message.reply_text(text="Соединение успешно установлено!")
        await update.message.reply_text(text="Приятного пользования :)", reply_markup=StandardKeyboards.MAIN_MENU)

        cache[username]["profile"].current_connection = connection
    else:
        await update.message.reply_text(text="Что-то пошло не так... Не получилось установить соединение с вашей БД :/",
                                        reply_markup=StandardKeyboards.MAIN_MENU
                                        )

    cache.wipe_context(username)

    return ConversationHandler.END
