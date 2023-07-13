import logging

from telegram import Update
from telegram.ext import ConversationHandler

from src.tg_bot.conversations.utils.conversation_points.task_points import NAME, PROJECT, WORKER, DEADLINE
from src.tg_bot.conversations.utils.keyboards import StandardKeyboards, DateKeyboards
from src.tg_bot.conversations.utils.replies.replier import Replier
from src.tg_bot.utils.cache import cache


logger = logging.getLogger(__name__)


class TaskReplier(Replier):
    def __init__(self, options: dict):
        self.steps = [
            NAME,
            PROJECT if options["has_project"] else None,
            WORKER if options["has_worker"] else None,
            DEADLINE if options["has_deadline"] else None,
            ConversationHandler.END
        ]

        self.replies = {
            NAME: name_reply,
            PROJECT: project_reply,
            WORKER: worker_reply,
            DEADLINE: deadline_reply,
            ConversationHandler.END: end_reply
        }

        super().__init__(self.replies, self.steps)

    def reinit(self, options: dict):
        self.steps = [
            NAME,
            PROJECT if options["has_project"] else None,
            WORKER if options["has_worker"] else None,
            DEADLINE if options["has_deadline"] else None,
            ConversationHandler.END
        ]
        super().restart(self.steps)


async def name_reply(update: Update, username: str):
    await update.message.reply_text(r"Как назовем?", reply_markup=StandardKeyboards.IN_PROGRESS())

    return NAME


async def project_reply(update: Update, username: str):
    await update.message.reply_text("Загружаю список проектов...")

    handler = cache[username]["profile"].current_connection.projects_handler
    projects = handler.get_projects()

    await update.message.reply_text(
        "Выберите проект:",
        reply_markup=StandardKeyboards.IN_PROGRESS(markup=[[name] for name in projects])
    )

    return PROJECT


async def worker_reply(update: Update, username: str):
    await update.message.reply_text("Загружаю список исполнителей...")

    handler = cache[username]["profile"].current_connection.worker_handler
    workers = list(handler.get_workers().keys())

    await update.message.reply_text(
        "Выберите исполнителя:",
        reply_markup=StandardKeyboards.IN_PROGRESS(markup=[
            [workers[i], workers[i + 1] if i + 1 < len(workers) else ""] for i in range(0, len(workers), 2)
        ])
    )

    return WORKER


async def deadline_reply(update: Update, username: str):
    await update.message.reply_text("Теперь установим дедлайн")
    await update.message.reply_text("Введи год:", reply_markup=DateKeyboards.year)

    return DEADLINE


async def end_reply(update: Update, username: str):
    await update.message.reply_text(r"Все готово, создаю задачу!", reply_markup=StandardKeyboards.MAIN_MENU)

    logger.info("{} finished making a task".format(username))

    handler = cache[username]["profile"].current_connection.task_handler
    handler.create_task(**cache[username]["context"]["task"])

    await update.message.reply_text(r"Задача создана! Можешь проверять ;)")

    cache.wipe_context(username)

    return ConversationHandler.END
