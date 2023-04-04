import logging

from telegram.ext import Application, CommandHandler

from redis_api.client import RedisClient
from tg_bot.commands.basic_commands import start, help_command
from tg_bot.conversations.task import TASK_CONVERSATION

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, token):
        self.redis_client = RedisClient()
        self.redis_client.init()

        self.bot = Application.builder().token(token).build()

    def init_handlers(self):
        self.bot.add_handler(CommandHandler("start", start))
        self.bot.add_handler(CommandHandler("help", help_command))
        self.bot.add_handler(TASK_CONVERSATION)

    def run(self):
        self.bot.run_polling()
