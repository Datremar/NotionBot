from aiogram.utils import executor

from telegram.bot import dispatcher

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
