from tg_bot.bot import Bot

if __name__ == '__main__':
    bot = Bot(token="5879916534:AAHJc5OXzZtJD7po4Miq5Jozf0w8kHHeQv4")
    bot.init_handlers()

    bot.run()
