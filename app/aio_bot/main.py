import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from constants import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

if TELEGRAM_BOT_TOKEN:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    if message.from_user:
        await message.answer(
            text=(
                f'Здравствуйте, {message.from_user.full_name}! '
                f'Ваш телеграм ID - {message.from_user.id}'
            )
        )


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # if TELEGRAM_BOT_TOKEN:
    #     bot = Bot(
    #         token=TELEGRAM_BOT_TOKEN
    #     )
    asyncio.run(main())
