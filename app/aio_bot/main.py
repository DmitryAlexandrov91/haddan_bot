import asyncio
import logging

from aiogram import Bot, Dispatcher, types, Router, F
from constants import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

from aiogram.filters import CommandStart

# if TELEGRAM_BOT_TOKEN:
#     bot = Bot(token=TELEGRAM_BOT_TOKEN)

# dp = Dispatcher()


# @dp.message()
# async def echo_answer(message: types.Message):
#     await bot.send_message(
#         chat_id=message.chat.id,
#         text='Start processing'
#     )
#     await bot.send_message(
#         chat_id=message.chat.id,
#         text='Detected message',
#         reply_to_message_id=message.message_id,
#     )
#     await message.answer(
#         text='Wait a sec...',
#     )
#     if message.text:
#         await message.reply(text=message.text)


# async def main():
#     logging.basicConfig(level=logging.DEBUG)
#     await dp.start_polling(bot)


# router = Router()


# @router.message()
# async def echo_answer(message: types.Message):
#     await message.answer("Wait a sec...")
#     if message.text:
#         await message.reply(text=message.text)


class AioBotManager:
    def __init__(
            self,
            token: str,
            admin_chat_id: types.ChatIdUnion | None = None
    ):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        router = Router()

        @router.message(CommandStart())
        async def handle_start(message: types.Message):
            await message.answer(
                text=f'Привет, {message.from_user.full_name}'
            )

        @router.message(F.text)
        async def echo_answer(message: types.Message):
            await self.bot.send_message(
                chat_id=message.chat.id,
                text='Start processing'
            )
            await self.bot.send_message(
                chat_id=message.chat.id,
                text='Detected message',
                reply_to_message_id=message.message_id,
            )
            await message.answer(
                text='Wait a sec...',
            )
            # отправляем копию сообщения
            try:
                await message.send_copy(
                    chat_id=message.chat.id
                )
            # if message.text:
            #     await message.reply(text=message.text)
            # elif message.sticker:
            #     await message.reply_sticker(
            #         sticker=message.sticker.file_id
            #     )
            except TypeError:
                await message.reply(
                    text='Что-то новое'
                )

        self.dp.include_router(router)

    async def start_bot(self):
        logging.basicConfig(level=logging.DEBUG)
        await self.dp.start_polling(self.bot)

    def sync_start(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        asyncio.run_coroutine_threadsafe(
            self.start_bot(),
            self.loop
        )
        self.loop.run_forever()


if __name__ == '__main__':
    if TELEGRAM_BOT_TOKEN:
        aldbot = AioBotManager(
            token=TELEGRAM_BOT_TOKEN,
            admin_chat_id=TELEGRAM_CHAT_ID
        )
    # asyncio.run(aldbot.start_bot())
    aldbot.sync_start()
