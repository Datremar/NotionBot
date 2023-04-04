from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

NAME, DESCRIPTION, WORKER, DEADLINE = range(4)


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yea, let's make a task :D")
    await update.message.reply_text(r"How shall we name it?")

    return NAME


async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    await update.message.reply_text(rf"Okay, let's call it {name}")
    await update.message.reply_text(r"Describe the task")

    return DESCRIPTION


async def task_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    description = update.message.from_user
    await update.message.reply_text(r"Sounds good!")
    await update.message.reply_text(r"Who will work on it?")

    return WORKER


async def task_worker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    worker = update.message.text
    await update.message.reply_text(rf"I'm sure {worker} will do a great job!")
    await update.message.reply_text(r"When's the deadline?")

    return DEADLINE


async def task_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    worker = update.message.from_user
    await update.message.reply_text(r"Let the deadlines be never crossed!")
    await update.message.reply_text(r"Aight, making the task!")

    return ConversationHandler.END


async def task_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(r"Oh, changed your mind? It's okay, I'm here for ya ;)")

    return ConversationHandler.END


TASK_CONVERSATION = ConversationHandler(
                        entry_points=[CommandHandler("task", task)],
                        states={
                            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],
                            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_description)],
                            WORKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_worker)],
                            DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_deadline)],
                        },
                        fallbacks=[CommandHandler("cancel", task_cancel)]
                    )
