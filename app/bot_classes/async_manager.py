import asyncio
import threading


class AsyncManager:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self._start_loop_thread()
        self.event = asyncio.Event()
        self.farm_task = None

    def _start_loop_thread(self):
        """Запускает event loop в отдельном потоке"""
        def run_loop():
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        threading.Thread(target=run_loop, daemon=True).start()

    @property
    def event_is_running(self):
        """Цикл запущен."""
        return self.event.is_set()
