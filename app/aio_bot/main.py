import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from constants import TELEGRAM_BOT_TOKEN

if TELEGRAM_BOT_TOKEN:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
