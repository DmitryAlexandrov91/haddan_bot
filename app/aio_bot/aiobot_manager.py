"""Класс управления aiogram ботом."""
import asyncio
import logging

from aiogram import Bot, Dispatcher, types, Router, F

from aiogram.filters import CommandStart


class AioBotManager:
    """Класс создания бота со встроенным обработчиком событий."""
    dp = Dispatcher()
    router = Router()

    def __init__(
            self,
            token: str,
            admin_chat_id: types.ChatIdUnion | None = None
    ):
        self.bot = Bot(token=token)
        if admin_chat_id:
            self.admin_id = admin_chat_id

        @self.router.message(CommandStart())
        async def handle_start(message: types.Message):
            if message.from_user:
                await message.answer(
                    text=f'Привет, {message.from_user.full_name}'
                )

        @self.router.message(F.text)
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
            try:
                await message.send_copy(
                    chat_id=message.chat.id
                )
            except TypeError:
                await message.reply(
                    text='Что-то новое'
                )

        self.dp.include_router(self.router)

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
    pass
    # if TELEGRAM_BOT_TOKEN:
    #     aldbot = AioBotManager(
    #         token=TELEGRAM_BOT_TOKEN,
    #         admin_chat_id=TELEGRAM_CHAT_ID
    #     )
    # asyncio.run(aldbot.start_bot())
    # # aldbot.sync_start()
