import datetime
import logging
from calendar import monthrange

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler

from tg_bot.conversations.utils.buttons import CANCEL, SKIP, MAKE_TASK, BACK, command_filter
from tg_bot.conversations.utils.conversation_points.task_points import NAME, PROJECT, WORKER, DEADLINE
from tg_bot.conversations.utils.keyboards import StandardKeyboards, DateKeyboards
from tg_bot.conversations.utils.replies.task_replies import TaskReplier
from tg_bot.utils.cache import cache

logger = logging.getLogger(__name__)


def day_valid(day: str, month: str, year: str) -> bool:
    days = monthrange(year=int(year), month=int(month))[1]

    return day in [str(d) for d in range(1, days + 1)]


async def create_task(username: str, update: Update):
    await update.message.reply_text(r"Все готово, создаю задачу!", reply_markup=StandardKeyboards.MAIN_MENU)

    logger.info("{} creating a task".format(username))

    handler = cache[username]["profile"].current_connection.task_handler
    handler.create_task(**cache[username]["context"]["task"])

    await update.message.reply_text(r"Задача создана! Можешь проверять ;)")

    cache[username].wipe_context()


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username

    logger.info("{} initialized task creation conversation".format(username))

    if username not in cache or not cache[username]["profile"].connections:
        await update.message.reply_text(r"У тебя нет ни одного соединения с БД Notion. Невозможно создать задачу")
        return ConversationHandler.END

    if cache[username]["profile"].current_connection is None:
        await update.message.reply_text(r"Не выбрано соединение с БД. Невозможно создать задачу")
        return ConversationHandler.END

    replier = TaskReplier(
        options=cache[username]["profile"].current_connection.has_optional_fields()
    )
    cache[username]["replier"] = replier

    cache[username]["context"]["task"] = {}

    return await replier.current_reply(update=update, username=username)


async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    replier = cache[username]["replier"]
    response = update.message.text

    if response == SKIP.text:
        await update.message.reply_text("Имя нельзя пропустить :)")
        return
    if response == BACK.text:
        await update.message.reply_text("Вернуться нельзя. Ты уже в начале")
        return

    logger.info("{} selected task name".format(username))

    cache[username]["context"]["task"]["name"] = response
    await update.message.reply_text(rf"Хорошо. Назовем ее {response}")

    return await replier.next_reply(update=update, username=username)


async def task_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    replier = cache[username]["replier"]
    response = update.message.text

    if response == BACK.text:
        return await replier.previous_reply(update=update, username=username)
    if response == SKIP.text:
        await update.message.reply_text("Пропускаем проект...")

        return await replier.next_reply(update=update, username=username)

    logger.info("{} selected a project for the task".format(username))

    handler = cache[username]["profile"].current_connection.projects_handler

    project = handler.get_id(response)
    if not project:
        await update.message.reply_text(rf"Такого проекта нет. Попробуй снова :)")
        return

    cache[username]["context"]["task"]["project_id"] = project
    await update.message.reply_text(rf"Вы выбрали: {response}")

    return await replier.next_reply(update=update, username=username)


async def task_worker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    replier = cache[username]["replier"]
    response = update.message.text

    if response == BACK.text:
        await update.message.reply_text("Возвращаемся...")
        return await replier.previous_reply(update=update, username=username)
    if response == SKIP.text:
        await update.message.reply_text(rf"Пропускаем ответственного...")
        return await replier.next_reply(update=update, username=username)

    logger.info("{} selected a worker for the task".format(username))

    handler = cache[username]["profile"].current_connection.worker_handler

    worker = handler.get_id(response)
    if not worker:
        await update.message.reply_text(rf"Такого работника нет. Попробуй снова :)")
        return

    cache[username]["context"]["task"]["worker_id"] = worker

    await update.message.reply_text(rf"Вы выбрали: {response}")

    return await replier.next_reply(update=update, username=username)


async def task_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    replier = cache[username]["replier"]
    response = update.message.text

    if response == SKIP.text:
        await update.message.reply_text("Пропускаем...")
        return await replier.next_reply(update=update, username=username)
    if response == BACK.text:
        await update.message.reply_text("Возвращаемся...")
        cache[username]["context"]["deadline"] = dict()
        return await replier.previous_reply(update=update, username=username)

    if "deadline" not in cache[username]["context"]:
        cache[username]["context"]["deadline"] = dict()

    if "year" not in cache[username]["context"]["deadline"]:
        year = response
        if [year] not in DateKeyboards.years:
            await update.message.reply_text("Такой опции нет... Выбери год из списка ;)")
            return

        cache[username]["context"]["deadline"]["year"] = int(year)

        await update.message.reply_text("Теперь месяц:", reply_markup=DateKeyboards.month)
        return
    elif "month" not in cache[username]["context"]["deadline"]:
        month = response
        if [month] not in DateKeyboards.months:
            await update.message.reply_text("Такой опции нет... Выбери месяц из списка ;)")
            return

        cache[username]["context"]["deadline"]["month"] = DateKeyboards.months.index([month]) + 1

        await update.message.reply_text("И наконец день:", reply_markup=DateKeyboards.day(
            month=cache[username]["context"]["deadline"]["month"],
            year=cache[username]["context"]["deadline"]["year"]
        ))
        return
    elif "day" not in cache[username]["context"]["deadline"]:
        day = response
        if not day_valid(
            day=day,
            month=cache[username]["context"]["deadline"]["month"],
            year=cache[username]["context"]["deadline"]["year"]
        ):
            await update.message.reply_text("Такой опции нет... Выбери день из списка ;)")
            return

    cache[username]["context"]["deadline"]["day"] = int(response)

    logger.info("{} selected a deadline for the task".format(username))

    date = datetime.date(**cache[username]["context"]["deadline"])

    cache[username]["context"]["task"]["deadline"] = date.isoformat()

    await update.message.reply_text(r"Пусть дедлайны никогда не будут пересечены!")

    return await replier.next_reply(update=update, username=username)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username

    logger.info("{} cancelled task creation".format(username))

    await update.message.reply_text(r"Передумал? Все в порядке. Я здесь, если понадоблюсь ;)",
                                    reply_markup=StandardKeyboards.MAIN_MENU)

    cache.wipe_context(username=username)

    return ConversationHandler.END


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
