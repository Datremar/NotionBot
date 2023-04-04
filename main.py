from tg_bot.bot import Bot

if __name__ == '__main__':
    bot = Bot(token="")
    bot.init_handlers()

    bot.run()
