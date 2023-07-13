from telegram import KeyboardButton
from telegram.ext import filters

ADD_CONNECTION = KeyboardButton("Добавить БД")
SELECT_CONNECTION = KeyboardButton("Выбрать БД")
DELETE_CONNECTION = KeyboardButton("Удалить БД")
MAKE_TASK = KeyboardButton("Поставить Задачу✍️")
CANCEL = KeyboardButton("Отмена❌")
SKIP = KeyboardButton("Пропустить💁")
BACK = KeyboardButton("Назад↩️")

command_filter = ~filters.COMMAND & \
                 ~filters.Regex(f"^{CANCEL.text}$") & \
                 ~filters.Regex(f"^{MAKE_TASK.text}$")

