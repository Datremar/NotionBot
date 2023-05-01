from telegram import Update

from notion.handlers.projects_handler import ProjectsHandler
from notion.handlers.worker_handler import WorkerHandler
from tg_bot.conversations.utils.keyboards import StandardKeyboards, DateKeyboards


NAME, PROJECT, WORKER, DEADLINE = range(4)


async def name_reply(update: Update):
    await update.message.reply_text(r"Как назовем?", reply_markup=StandardKeyboards.IN_PROGRESS())

    return NAME


async def project_reply(update: Update):
    await update.message.reply_text("Загружаю список проектов...")

    handler = ProjectsHandler()
    projects = handler.get_projects()

    await update.message.reply_text(
        "Выберите проект:",
        reply_markup=StandardKeyboards.IN_PROGRESS(markup=[[name] for name in projects])
    )

    return PROJECT


async def worker_reply(update: Update):
    await update.message.reply_text("Загружаю список исполнителей...")

    handler = WorkerHandler()
    workers = list(handler.get_workers().keys())

    await update.message.reply_text(
        "Выберите исполнителя:",
        reply_markup=StandardKeyboards.IN_PROGRESS(markup=[
            [workers[i], workers[i + 1] if i + 1 < len(workers) else ""] for i in range(0, len(workers), 2)
        ])
    )

    return WORKER


async def deadline_reply(update: Update):
    await update.message.reply_text("Теперь установим дедлайн")
    await update.message.reply_text("Введи год:", reply_markup=DateKeyboards.year)

    return DEADLINE