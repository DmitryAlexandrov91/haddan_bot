import asyncio
import logging

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.utils import markdown
from constants import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

from aiogram.filters import CommandStart, Command

if TELEGRAM_BOT_TOKEN:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    if message.from_user:
        await message.answer(
            text=(
                f'Здравстуйте, {message.from_user.full_name}! '
                f'Ваш телеграм ID - {message.from_user.id}'
            )
        )


@dp.message(Command('help'))
async def handle_help(message: types.Message):
    await message.answer(
        text='Здесь будет инструкция'
    )


@dp.message()
async def echo_answer(message: types.Message):
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text='Start processing'
    # )
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text='Detected message',
    #     reply_to_message_id=message.message_id,
    # )
    # await message.answer(
    #     text='Wait a sec...',
    # )
    await message.answer(
        text=message.text,
        entities=message.entities  # entites содержит в себе список форматирования
    )
    # if message.text:
    #     await message.reply(text=message.text)
    # как отправить сообщение разным шрифтом
    # ручками
    # text = 'Пример сообщения с жирным словом'
    # entity_bold = types.MessageEntity(
    #     type='bold',
    #     offset=len('Пример сообщения с '),
    #     length=len('жирным')
    # )
    # entities = [entity_bold]
    # await message.answer(
    #     text=text, entities=entities
    # )
    # при помощи markdown


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # if TELEGRAM_BOT_TOKEN:
    #     aldbot = AioBotManager(
    #         token=TELEGRAM_BOT_TOKEN,
    #         admin_chat_id=TELEGRAM_CHAT_ID
    #     )
    asyncio.run(main())
    # # aldbot.sync_start()
