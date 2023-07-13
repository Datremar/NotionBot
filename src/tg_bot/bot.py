import logging

from telegram.ext import Application, CommandHandler

from src.tg_bot.commands.basic_commands import start, help_command
from src.tg_bot.conversations.delete_connection import DEL_CONN_CONVERSATION
from src.tg_bot.conversations.select_connection import SEL_CONN_CONVERSATION
from src.tg_bot.conversations.create_connection import CREATE_CONN_CONVERSATION
from src.tg_bot.conversations.create_task import TASK_CONVERSATION


logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, token):
        logger.info("Initializing the bot")
        self.bot = Application.builder().token(token).build()
        self.bot.builder().concurrent_updates(False)

    def init_handlers(self):
        logger.info("Setting up bot handlers")
        self.bot.add_handler(CommandHandler("start", start))
        self.bot.add_handler(CommandHandler("help", help_command))
        self.bot.add_handler(TASK_CONVERSATION)
        self.bot.add_handler(CREATE_CONN_CONVERSATION)
        self.bot.add_handler(SEL_CONN_CONVERSATION)
        self.bot.add_handler(DEL_CONN_CONVERSATION)

    def run(self):
        logger.info("Running the bot")
        self.bot.run_polling()
