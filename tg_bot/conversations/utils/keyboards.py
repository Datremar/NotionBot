from datetime import date
from calendar import monthrange
from telegram import ReplyKeyboardMarkup

from tg_bot.conversations.utils.buttons import MAKE_TASK, CANCEL, BACK, SKIP


class StandardKeyboards:
    MAIN_MENU = ReplyKeyboardMarkup([
        [MAKE_TASK],
    ], resize_keyboard=True)

    @staticmethod
    def IN_PROGRESS(markup=None):
        keyboard = [
            [SKIP, CANCEL, BACK],
        ]
        if markup is not None:
            for button in markup:
                keyboard.append(button)

        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


class DateKeyboards:
    year = StandardKeyboards.IN_PROGRESS(markup=([str(date.today().year + i)] for i in range(11)))
    month = StandardKeyboards.IN_PROGRESS(
        markup=[
            ["Январь"],
            ["Февраль"],
            ["Март"],
            ["Апрель"],
            ["Май"],
            ["Июнь"],
            ["Июль"],
            ["Август"],
            ["Сентябрь"],
            ["Октябрь"],
            ["Ноябрь"],
            ["Декабрь"]
        ]
    )

    @staticmethod
    def day(month: str, year: str):
        days = monthrange(year=int(year), month=int(month))[1]
        days = [str(day) for day in range(1, days + 1)]

        days = [
            *(days[i:i + 7] for i in range(0, 28, 7)),
            days[28:] if len(days) > 28 else [""]
        ]

        return StandardKeyboards.IN_PROGRESS(markup=days)
