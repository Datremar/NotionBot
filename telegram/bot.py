import logging as log

from aiogram import Bot, Dispatcher, types



log.basicConfig(level=log.INFO)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    log.info(message.text)
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dispatcher.message_handler()
async def echo(message: types.Message):
    log.info(message.text)
    await message.answer(message.text)
