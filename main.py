import logging
import os

from tg_bot.bot import Bot
from tg_bot.utils.cache import cache

from config import config

logging.basicConfig(
    filename="logs.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO if config["logger"]["debug"] == False else logging.DEBUG,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Starting the service")
    cache.load()
    bot = Bot(token=os.getenv("NOTIONBOT_TOKEN"))
    bot.init_handlers()

    bot.run()
