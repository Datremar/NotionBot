import datetime

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler

from notion.handlers.projects_handler import ProjectsHandler
from notion.handlers.task_handler import TaskHandler
from notion.handlers.worker_handler import WorkerHandler

from tg_bot.conversations.utils.buttons import CANCEL, SKIP, MAKE_TASK, BACK
from tg_bot.conversations.utils.keyboards import StandardKeyboards, DateKeyboards
from tg_bot.conversations.utils.replies import name_reply, project_reply, worker_reply, deadline_reply
from tg_bot.utils.cache import cache
from tg_bot.utils.data_models import UserData

NAME, PROJECT, WORKER, DEADLINE = range(4)


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username

    if username not in cache:
        cache[username] = UserData(
            username=username,
            task={},
            deadline={}
        )

    await update.message.reply_text("Давай сделаем задачу :)")

    return await name_reply(update)


async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    reply = update.message.text

    if reply == SKIP.text:
        await update.message.reply_text("Имя нельзя пропустить :)")
        return await name_reply(update)

    if reply == BACK.text:
        return await name_reply(update)

    cache[username].task["name"] = reply

    await update.message.reply_text(rf"Хорошо. Назовем ее {reply}")

    return await project_reply(update)


async def task_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    reply = update.message.text

    if reply == BACK.text:
        return await name_reply(update)

    if reply != SKIP.text:
        handler = ProjectsHandler()

        cache[username].task["project_id"] = handler.get_id(reply)

        await update.message.reply_text(rf"Вы выбрали: {reply}")
    else:
        await update.message.reply_text("Пропускаем проект...")

    return await worker_reply(update)


async def task_worker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    reply = update.message.text

    if reply == BACK.text:
        await update.message.reply_text("Возвращаемся...")
        return await project_reply(update)

    if reply == SKIP.text:
        await update.message.reply_text(rf"Пропускаем ответственного...")
        await update.message.reply_text("Теперь установим дедлайн")
        await update.message.reply_text("Введи год:", reply_markup=DateKeyboards.year)

        return DEADLINE

    handler = WorkerHandler()

    cache[username].task["worker_id"] = handler.get_id(reply)

    await update.message.reply_text(rf"Вы выбрали: {reply}")

    return await deadline_reply(update)


async def task_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    reply = update.message.text

    if reply == SKIP.text:
        await update.message.reply_text("Дедлайн нельзя пропустить :)")
        return DEADLINE

    if reply == BACK.text:
        await update.message.reply_text("Возвращаемся...")
        return await worker_reply(update)

    if "year" not in cache[username].deadline:
        cache[username].deadline["year"] = int(reply)

        await update.message.reply_text("Теперь месяц:", reply_markup=DateKeyboards.month)

        return DEADLINE
    elif "month" not in cache[username].deadline:
        month_names = {
            "Январь": 1,
            "Февраль": 2,
            "Март": 3,
            "Апрель": 4,
            "Май": 5,
            "Июнь": 6,
            "Июль": 7,
            "Август": 8,
            "Сентябрь": 9,
            "Октябрь": 10,
            "Ноябрь": 11,
            "Декабрь": 12,
        }

        cache[username].deadline["month"] = month_names[reply]

        await update.message.reply_text("И наконец день:", reply_markup=DateKeyboards.day(
            month=cache[username].deadline["month"],
            year=cache[username].deadline["year"]
        ))

        return DEADLINE
    elif "day" not in cache[username].deadline:
        cache[username].deadline["day"] = int(reply)

    date = datetime.date(**cache[username].deadline)

    cache[username].task["deadline"] = date.isoformat()

    await update.message.reply_text(r"Пусть дедлайны никогда не будут пересечены!")
    await update.message.reply_text(r"Все готово, создаю задачу!", reply_markup=StandardKeyboards.MAIN_MENU)

    handler = TaskHandler()
    handler.create_task(**cache[username].task)

    await update.message.reply_text(r"Задача создана! Можешь проверять ;)")

    cache[username].wipe()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    await update.message.reply_text(r"Передумал? Все в порядке, я здесь, если понадоблюсь ;)",
                                    reply_markup=StandardKeyboards.MAIN_MENU)

    cache[username].wipe()

    return ConversationHandler.END


command_filter = ~filters.COMMAND &\
                 ~filters.Regex(f"^{CANCEL.text}$") &\
                 ~filters.Regex(f"^{MAKE_TASK.text}$") &\
                 ~filters.Regex(f"^{BACK.text}$")

TASK_CONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(f"^{MAKE_TASK.text}$"), task)],
    states={
        NAME: [MessageHandler(
            filters.TEXT & command_filter,
            task_name
        )],
        PROJECT: [MessageHandler(
            filters.TEXT & command_filter,
            task_project
        )],
        WORKER: [MessageHandler(
            filters.TEXT & command_filter,
            task_worker
        )],
        DEADLINE: [MessageHandler(
            filters.TEXT & command_filter,
            task_deadline
        )],
    },
    fallbacks=[
        MessageHandler(filters.Regex(f"^{CANCEL.text}$"), cancel)
    ]
)
