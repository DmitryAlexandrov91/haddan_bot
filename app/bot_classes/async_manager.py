import asyncio
import logging
import threading

from aiogram import Bot, Dispatcher

from constants import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN


class AsyncBotManager:
    def __init__(
            self,
            token=TELEGRAM_BOT_TOKEN,
            chat_id=TELEGRAM_CHAT_ID
    ):
        self.loop = asyncio.new_event_loop()
        self._start_loop_thread()
        self.event = asyncio.Event()
        self.farm_task = None
        self.bot = Bot(
            token=token
        )
        self.chat_id = chat_id
        self.dp = Dispatcher()

    def _start_loop_thread(self):
        """Запускает event loop в отдельном потоке"""
        def run_loop():
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        threading.Thread(target=run_loop, daemon=True).start()

    async def send_msg(self, text):
        await self.bot.send_message(TELEGRAM_CHAT_ID, text)

    def sync_send(self, text):
        asyncio.run_coroutine_threadsafe(
            self.send_msg(text),
            self.loop
        )

    async def async_polling(self):
        logging.basicConfig(level=logging.DEBUG)
        await self.dp.start_polling(self.bot)

    def sync_polling(self):
        asyncio.run_coroutine_threadsafe(
            self.async_polling,
            self.loop
        )

    @property
    def event_is_running(self):
        """Цикл запущен."""
        return self.event.is_set()


if __name__ == '__main__':
    manager = AsyncBotManager()
    manager.sync_send(
        text='Тестируем Aiogram через собственный менеджер.'
    )
