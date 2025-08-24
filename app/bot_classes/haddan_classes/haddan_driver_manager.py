"""Основные циклы приложения, завязаные на интерфейсе окна tkinter."""
import asyncio
import os
import threading
import time
from datetime import datetime
from time import sleep

import requests
from PIL import Image
from aiogram import Bot, Dispatcher, F, Router, types
from constants import (
    BASE_DIR,
    FIELD_PRICES,
    LICH_ROOM,
    NPCImgTags,
    Room,
    Slot,
    SlotsPage,
)
from dao.crud import event_crud
from dao.database import sync_session_maker
from loguru import logger
from maze_utils import (
    find_path_via_boxes_with_directions,
    find_path_with_directions,
    get_sity_portal_room_number,
    get_upper_portal_room_number,
)
from selenium.common.exceptions import (
    InvalidSessionIdException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from utils import (
    get_dragon_time_wait,
    price_counter,
    time_extractor,
)

from bot_classes.services import make_transition

from .spirit_play import HaddanSpiritPlay
from .user import HaddanUser


class HaddanDriverManager(HaddanSpiritPlay):
    """Главный класс создания необходимых объектов и циклов событий.

    Для внедрения aiogram внутри синхронного tkinter
    И работоспособности основных циклов бота
    Для игры haddan.ru.
    """

    def __init__(
            self,
            user: HaddanUser | None = None,
            bot: Bot | None = None,
    ) -> None:
        """Инициализация класса HaddanDriverManager."""
        super().__init__(bot=bot)
        self.user = user
        self.loop = asyncio.new_event_loop()
        self.polling_started = asyncio.Event()

        if self.bot:
            self.router = Router()
            self._register_handlers()
            self.dp = Dispatcher()
            self.dp.include_router(self.router)

        threading.Thread(
            target=self.start_loop,
            daemon=True,
        ).start()
        self.passed_forest_rooms: set = set()
        self.passed_maze_rooms: set = set()
        self.maze_first_floor_map: list[list[Room]] | None = None
        self.maze_second_floor_map: list[list[Room]] | None = None
        self.maze_third_floor_map: list[list[Room]] | None = None
        self.baby_maze_first_floor_map: list[list[Room]] | None = None
        self.baby_maze_second_floor_map: list[list[Room]] | None = None
        self.fight_counter: int = 0
        self.domen: str | None = None
        self.kapthca_sent = False

    def _register_handlers(self) -> None:
        """Регистрация обработчиков сообщений."""
        @self.router.message(F.text)
        async def kaptcha_handler(message: types.Message) -> None:
            """Обработчик ответа на капчу."""
            if not self.driver:
                raise InvalidSessionIdException
            text = message.text
            if text:
                if len(text) <= 3 and text.isdigit():
                    self.try_to_switch_to_central_frame()
                    kaptcha_runes = self.driver.find_elements(
                        By.CLASS_NAME,
                        'captcha_rune',
                    )
                    if kaptcha_runes:
                        for number in text:
                            kaptcha_runes[int(number)].click()
                            await asyncio.sleep(0.5)
                    self.try_to_switch_to_central_frame()
                    buttons = self.driver.find_elements(
                                    By.TAG_NAME, 'button')
                    if buttons:
                        buttons[1].click()
                        self.sync_send_message(
                            telegram_id=message.chat.id,
                            text='Ответ принят.',
                        )
                        logger.info('Получен ответ на капчу через telegram')
                        self.kapthca_sent = False

                        try:
                            source_file = os.path.join(BASE_DIR, "kaptcha.png")
                            save_dir = "app/ai_kaptcha/kaptcha"

                            timestamp = datetime.now().strftime("%H%M%S")

                            new_filename = f"{text}_{timestamp}.png"
                            dest_file = os.path.join(save_dir, new_filename)

                            os.makedirs(save_dir, exist_ok=True)
                            if os.path.exists(source_file):
                                os.rename(source_file, dest_file)
                            else:
                                logger.warning(
                                    f"⚠️ Файл не найден: {source_file}",
                                )
                        except Exception as e:
                            logger.error(
                                f"⛔ Ошибка при обработке файла: {e}",
                            )

    def start_loop(self) -> None:
        """Запускает поток с aiogram ботом."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def send_msg(self, text: str, telegram_id: int) -> None:
        """Аминхронная отправка сообщения."""
        await self.bot.send_message(
            chat_id=telegram_id,
            text=text,
        ) if self.bot else None

    async def send_kaptcha(self, telegram_id: int) -> None:
        """Асинхронная отправка капчи."""
        if not self.bot:
            return
        try:

            img = Image.open('kaptcha.png')
            resized_img = img.resize((1280, 500))
            resized_img.save('kaptcha.png')

            await self.bot.send_photo(
                chat_id=telegram_id,
                photo=types.FSInputFile('kaptcha.png'),
                )
            await self.bot.send_photo(
                chat_id=telegram_id,
                photo=types.FSInputFile('runes.png'))

        except Exception:
            self.sync_send_message(
                telegram_id=telegram_id,
                text='С отправкой капчи какой-то косяк!',
            )

    async def start_polling(self) -> None:
        """Асинхронный старт поллинга бота."""
        if not self.bot:
            return

        if not self.polling_started.is_set():
            self.polling_started.set()

            try:

                await self.dp.start_polling(
                    self.bot,
                    handle_signals=False,
                )

                logger.info(
                    f'Запущен поллинг бота c id {self.bot.id}',
                )

            except Exception as e:
                logger.error(f"Ошибка при старте поллинга {str(e)}.")

    async def stop_polling(self) -> None:
        """Асинхронная остановка поллинга бота."""
        if not self.bot:
            return

        if self.polling_started.is_set():
            try:
                self.polling_started.clear()
                await self.dp.stop_polling()
                logger.info(
                    f'Остановлен поллинг бота с id {self.bot.id} ',
                )
            except Exception as e:
                logger.error(f"Ошибка при остановке поллинга {str(e)}")

    def sync_send_message(self, text: str, telegram_id: int) -> None:
        """Синхронная отправка сообщения."""
        asyncio.run_coroutine_threadsafe(
            self.send_msg(
                text=text,
                telegram_id=telegram_id,
            ),
            self.loop,
        )

    def sync_send_kaptcha(self, telegram_id: int) -> None:
        """Синхронна отправка капчи."""
        asyncio.run_coroutine_threadsafe(
            self.send_kaptcha(telegram_id=telegram_id),
            self.loop,
        )

    def sync_start_polling(self) -> None:
        """Синхронный старт поллинга бота."""
        asyncio.run_coroutine_threadsafe(
            self.start_polling(),
            self.loop,
        )

    def sync_stop_polling(self) -> None:
        """Синхроная остановка поллинга бота."""
        asyncio.run_coroutine_threadsafe(
            self.stop_polling(),
            self.loop,
        )

    def check_kaptcha(
            self,
            message_to_tg: bool,
            telegram_id: int | None = None) -> None:
        """Проверяет наличие капчи на странице."""
        if not self.driver:
            raise InvalidSessionIdException

        if not self.cycle_is_running:
            return
        kaptcha = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'img[src="/inner/img/bc.php"]',
                )

        if kaptcha:
            self.send_info_message(
                    'Обнаружена капча',
                )

            if self.bot and message_to_tg and telegram_id:

                cookies = {
                    cookie['name']: cookie[
                        'value'] for cookie in self.driver.get_cookies()}

                src = kaptcha[0].get_attribute('src')

                if not src:
                    return

                response = requests.get(src, cookies=cookies)
                with open('kaptcha.png', 'wb') as f:
                    f.write(response.content)

                self.sync_send_message(
                    text='Обнаружена капча!',
                    telegram_id=telegram_id)
                logger.info('Обнаружена капча')

                if not self.kapthca_sent:
                    self.sync_send_kaptcha(telegram_id=telegram_id)
                    self.kapthca_sent = True

                self.sync_start_polling()

                self.wait_until_kaptcha_after_tg_message(30)

            else:
                self.driver.execute_script(
                    'window.alert("Обнаружена капча!");')
                self.wait_until_alert_present(30)
                self.wait_until_kaptcha_on_page(5)

            self.check_kaptcha(
                message_to_tg=message_to_tg,
                telegram_id=telegram_id)

        else:
            self.sync_stop_polling()

    def check_health(
            self,
            min_hp: int | None,
            message_to_tg: bool,
            telegram_id: int | None) -> None:
        """"Проверка ХП.

        :min_hp: минимальное кол-во ХП.
        :message_to_tg: флаг отправки сообщений в ТГ.
        :telegram_id: телеграм id куда отправлять сообщение.
        """
        if not self.driver:
            raise InvalidSessionIdException

        if not self.cycle_is_running:
            return

        if min_hp:

            self.driver.switch_to.default_content()
            health = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'span[id="m_hpc"]',
                    )
            if health:
                hp = int(health[0].text)
                if hp < min_hp:
                    logger.info('Мало хп, спим 30 секунд!')
                    if self.bot and message_to_tg and telegram_id:
                        self.sync_send_message(
                            telegram_id=telegram_id,
                            text='Здоровье упало меньше минимума!',
                        )

                    self.sleep_while_event_is_true(time_to_sleep=30)
                    self.check_health(
                        min_hp=min_hp,
                        message_to_tg=message_to_tg,
                        telegram_id=telegram_id,
                    )

    def glade_farm(
            self,
            price_dict: dict = FIELD_PRICES,
            slots: SlotsPage = SlotsPage._1,
            spell: Slot = Slot._1,
            message_to_tg: bool = False,
            telegram_id: int | None = None,
            spell_book: dict | None = None) -> None:
        """Фарм поляны."""
        if not self.driver:
            raise InvalidSessionIdException

        while self.cycle_is_running:

            try:

                self.try_to_switch_to_central_frame()
                sleep(1)

                self.try_to_click_to_glade_fairy()

                self.try_to_switch_to_dialog()
                sleep(1)

                glade_fairy_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak')
                if glade_fairy_answers:
                    if len(glade_fairy_answers) == 1:

                        wait_tag = self.driver.find_elements(
                            By.CLASS_NAME,
                            'talksayBIG')

                        if wait_tag and 'где-то через' in wait_tag[0].text:
                            time_for_wait = time_extractor(wait_tag[0].text)

                            self.sleep_while_event_is_true(time_for_wait)

                        try:
                            glade_fairy_answers[0].click()
                            continue
                        except Exception:
                            continue

                    if len(glade_fairy_answers) == 3:
                        glade_fairy_answers[1].click()

                    if len(glade_fairy_answers) > 3:
                        sleep(1)
                        resurses = self.driver.find_elements(By.TAG_NAME, 'li')

                        if resurses:
                            res_price = [res.text for res in resurses]
                            most_cheep_res = price_counter(
                                res_price,
                                price_diсt=price_dict)
                            message_for_log = (
                                f'{res_price[most_cheep_res]}')

                            self.scroll_to_element(
                                glade_fairy_answers[most_cheep_res],
                            )

                            glade_fairy_answers[most_cheep_res].click()

                            self.send_info_message(
                                text=f'Получено у феи: {message_for_log}',
                            )

                if self.check_for_fight():
                    self.fight(
                        spell_book=spell_book,
                        default_slot=slots,
                        default_spell=spell)
                self.check_kaptcha(
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id)

                self.driver.switch_to.default_content()

            except UnexpectedAlertPresentException:
                self.send_status_message('Получено уведомление, ждём.')
                self.wait_until_kaptcha_on_page(30)

            except Exception as e:
                self.actions_after_exception(exception=e)

    def actions_with_fight_counter(
            self,
            fights: int,
            ) -> None:
        """"Действия с счётчиком боёв."""
        if not self.driver:
            raise InvalidSessionIdException

        self.fight_counter += 1
        if self.user and self.fight_counter >= fights:
            self.try_to_switch_to_upper()
            self.user.exit_from_game()
            self.user.login_to_game(
                domen=self.domen,
            )

            logger.info(
                f"Перелогин персонажа {self.user.char}",
            )

            self.wait_until_browser_test(time=10)

            self.fight_counter = 0

    def farm(
            self,
            slots: SlotsPage = SlotsPage._1,
            spell: Slot = Slot._1,
            up_down_move: bool = False,
            left_right_move: bool = False,
            mind_spirit_play: bool = True,
            message_to_tg: bool = True,
            min_hp: int | None = None,
            telegram_id: int | None = None,
            spell_book: dict | None = None,
            cheerfulness: bool = False,
            cheerfulness_min: int | None = None,
            cheerfulness_slot: SlotsPage = SlotsPage._0,
            fight_counter: int = 20,
            cheerfulness_spell: Slot = Slot._1) -> None:
        """Фарм с проведением боя."""
        if not self.driver:
            return

        self.time_stamp = time.time()
        refresh_ttl = float(os.getenv("MIN_TO_REFRESH", 5))

        while self.cycle_is_running:

            try:

                if cheerfulness:
                    self.check_cheerfulnes_level(
                        cheerfulnes_min=cheerfulness_min,
                        cheerfulnes_slot=cheerfulness_slot,
                        cheerfulnes_spell=cheerfulness_spell,
                    )

                self.try_to_switch_to_central_frame()
                # sleep(1)

                self.check_kaptcha(message_to_tg=message_to_tg,
                                   telegram_id=telegram_id)

                self.try_to_come_back_from_fight()

                if self.check_for_fight():
                    self.fight(
                        spell_book=spell_book,
                        default_slot=slots,
                        default_spell=spell)

                    self.actions_with_fight_counter(
                        fights=fight_counter,
                    )

                else:
                    self.wait_until_transition_timeout(5)

                    if up_down_move:
                        if not self.crossing_to_the_north():
                            self.crossing_to_the_south()

                        if self.check_for_fight():
                            self.fight(
                                spell_book=spell_book,
                                default_slot=slots,
                                default_spell=spell)

                            self.actions_with_fight_counter(
                                fights=fight_counter,
                            )

                    if left_right_move:
                        if not self.crossing_to_the_west():
                            self.crossing_to_the_east()

                        if self.check_for_fight():
                            self.fight(
                                spell_book=spell_book,
                                default_slot=slots,
                                default_spell=spell)

                            self.actions_with_fight_counter(
                                fights=fight_counter,
                            )

                # self.check_for_slot_clear_alarm_message()

                self.play_with_poetry_spirit()
                self.play_with_gamble_spirit()

                if mind_spirit_play:
                    self.play_with_mind_spirit()

                else:
                    self.actions_with_mind_spirit(
                        message_to_tg=message_to_tg,
                        telegram_id=telegram_id,
                    )

                self.check_health(
                    min_hp=min_hp,
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id,
                )

                if time.time() - self.time_stamp > refresh_ttl * 60:
                    self.time_stamp = time.time()
                    self.full_refresh()

            except Exception as e:
                self.actions_after_exception(exception=e)

    def dragon_farm(
            self,
            default_slot: SlotsPage = SlotsPage._1,
            default_spell: Slot = Slot._5,
            spell_book: dict | None = None,
            message_to_tg: bool = False,
            telegram_id: int | None = None) -> None:
        """"Фарм пыльных драконов."""
        if not self.driver:
            raise InvalidSessionIdException

        while self.cycle_is_running:

            try:

                self.try_to_switch_to_central_frame()
                sleep(1)

                self.check_kaptcha(
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id)

                self.try_to_come_back_from_fight()

                if self.check_for_fight():
                    self.fight(
                        spell_book=spell_book,
                        default_slot=default_slot,
                        default_spell=default_spell)

                dragon = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            NPCImgTags.daily_dragon,
                        )
                if not dragon:
                    dragon = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            NPCImgTags.evening_dragon,
                        )
                if not dragon:
                    dragon = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            NPCImgTags.morning_dragon,
                        )
                if dragon:
                    self.click_to_element_with_actionchains(dragon[0])

                self.try_to_switch_to_dialog()
                sleep(1)

                dragon_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak',
                )
                if dragon_answers:
                    for answer in dragon_answers:
                        sleep(1)

                        if 'Напасть' in answer.text or (
                           'Продолжить' in answer.text):
                            self.click_to_element_with_actionchains(answer)
                            continue
                        if 'Уйти' in answer.text or 'Убежать' in answer.text:
                            dragon_text = self.driver.find_elements(
                                By.CLASS_NAME,
                                'talksayBIG',
                            )
                            if dragon_text:
                                title = dragon_text[0].text
                                if 'Вам надо подождать до' in title:
                                    time_to_wait = get_dragon_time_wait(title)
                                    self.send_info_message(
                                        'Дракон отдыхает',
                                    )
                                    self.sleep_while_event_is_true(
                                        time_to_wait)

                                if 'Старт состоится' in title:
                                    time_to_wait = get_dragon_time_wait(title)
                                    self.send_info_message(
                                        'Ждём начала ивента '
                                        f'{time_to_wait} секунд(ы).',
                                    )
                                    self.sleep_while_event_is_true(
                                        time_to_wait)

                            try:
                                self.click_to_element_with_actionchains(answer)
                            except Exception:
                                continue

                self.try_to_switch_to_central_frame()
                sleep(1)

                if self.check_for_fight():
                    self.fight(
                        spell_book=spell_book,
                        default_slot=default_slot,
                        default_spell=default_spell,
                    )

                self.driver.switch_to.default_content()
                sleep(1)

            except Exception as e:
                self.actions_after_exception(e)

    def check_cheerfulnes_level(
            self,
            cheerfulnes_min: int | None,
            cheerfulnes_slot: SlotsPage = SlotsPage._0,
            cheerfulnes_spell: Slot = Slot._1) -> None:
        """Проверяет уровень бодрости.

        Если меньше установленного уровня, пъёт элик.
        :cheerfulnes_min: минимальное кол-во бодрости.
        :cheerfulnes_slot: страница слотов с бодрой.
        :cheerfulnes_spell: номер слота с бодрой.
        """
        if not self.driver:
            raise InvalidSessionIdException

        if self.check_for_fight() is True:
            return

        self.driver.switch_to.default_content()
        cheerfulnes_level = self.driver.find_elements(
            By.CLASS_NAME, 'current-bf')
        if cheerfulnes_level:
            cheerfulnes = int(cheerfulnes_level[0].text)

            if cheerfulnes_min:

                while cheerfulnes < cheerfulnes_min and (
                    self.check_for_fight() is False
                ):

                    self.open_slot_and_choise_spell(
                        slots_page=cheerfulnes_slot,
                        slot=cheerfulnes_spell,
                    )

                    sleep(1)

                    cheerfulnes_level = self.driver.find_elements(
                        By.CLASS_NAME, 'current-bf')
                    if cheerfulnes_level:
                        cheerfulnes = int(cheerfulnes_level[0].text)
                    else:
                        break

    def maze_passing(
        self,
        labirint_map: list[list[Room]],
        via_drop: bool = True,
        to_the_room: int | None = None,
        message_to_tg: bool = False,
        telegram_id: int | None = None,
        slots: SlotsPage = SlotsPage._1,
        spell: Slot = Slot._1,
        mind_spirit_play: bool = True,
        min_hp: int | None = None,
        spell_book: dict | None = None,
        cheerfulness: bool = False,
        cheerfulness_min: int | None = None,
        cheerfulness_slot: SlotsPage = SlotsPage._0,
        cheerfulness_spell: Slot = Slot._1,
        first_floor: bool = False,
        second_floor: bool = False,
        third_floor: bool = False,
        baby_maze: bool = False,
    ) -> None:
        """Прохождение лабиринта."""
        if not self.driver:
            raise InvalidSessionIdException

        while self.cycle_is_running:

            try:

                self.default_maze_actions(
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id,
                    slots=slots,
                    spell=spell,
                    mind_spirit_play=mind_spirit_play,
                    min_hp=min_hp,
                    spell_book=spell_book,
                    cheerfulness=cheerfulness,
                    cheerfulness_min=cheerfulness_min,
                    cheerfulness_slot=cheerfulness_slot,
                    cheerfulness_spell=cheerfulness_spell,
                )

                self.try_to_switch_to_central_frame()

                my_room = self.get_room_number()

                if my_room is None:
                    continue

                #  Если указана комната и не стоит выбор через весь дроп.
                if to_the_room is not None and not via_drop:

                    message = (
                        f'Двигаемся по прямой в комнату {to_the_room} '
                    )
                    logger.info(message)
                    self.send_info_message(
                        text=message,
                    )

                    path = find_path_with_directions(
                        labirint_map=labirint_map,
                        start_room=my_room,
                        end_room=to_the_room,
                    )

                #  Если указана комната и стоит выбор через весь дроп.
                if to_the_room is not None and via_drop:

                    message = (
                        f'Двигаемся через весь дроп в комнату {to_the_room} '
                    )
                    logger.info(message)
                    self.send_info_message(
                        text=message,
                    )

                    path = find_path_via_boxes_with_directions(
                        labirint_map=labirint_map,
                        start_room=my_room,
                        target_room=to_the_room,
                        passed_rooms=self.passed_maze_rooms,
                    )

                # Если не указана комната и стоит выбор через весь дроп.
                if to_the_room is None and via_drop:

                    if first_floor:
                        if not baby_maze:
                            to_the_room = get_upper_portal_room_number(
                                labirint_map=labirint_map,
                            )
                            message = (
                                'Двигаемся через весь дроп к '
                                'порталу на второй этаж '
                                f'в комнату {to_the_room} '
                            )
                        else:
                            to_the_room = get_sity_portal_room_number(
                                labirint_map=labirint_map,
                            )
                            message = (
                                'Двигаемся через весь дроп к '
                                'порталу в город '
                                f'в комнату {to_the_room} '
                            )

                    if second_floor:
                        to_the_room = get_sity_portal_room_number(
                            labirint_map=labirint_map,
                        )
                        message = (
                            'Двигаемся через весь дроп к порталу в город '
                            f'в комнату {to_the_room} '
                        )

                    if third_floor:
                        to_the_room = LICH_ROOM
                        message = (
                            'Двигаемся напрямую к '
                            'личу '
                            f'в комнату {to_the_room} '
                        )

                    self.send_info_message(
                        text=message,
                    )

                    if to_the_room is not None:
                        path = find_path_via_boxes_with_directions(
                            labirint_map=labirint_map,
                            start_room=my_room,
                            target_room=to_the_room,
                            passed_rooms=self.passed_maze_rooms,
                        )

                #  Если не указана комната и не стоит выбор через весь дроп.
                if to_the_room is None and not via_drop:

                    if first_floor:
                        to_the_room = get_upper_portal_room_number(
                            labirint_map=labirint_map,
                        )
                        message = (
                            'Двигаемся напрямую к '
                            'порталу на второй этаж '
                            f'в комнату {to_the_room} '
                        )
                    if second_floor:
                        to_the_room = get_upper_portal_room_number(
                            labirint_map=labirint_map,
                        )
                        message = (
                            'Двигаемся напрямую к '
                            'порталу на третий этаж '
                            f'в комнату {to_the_room} '
                        )

                    if third_floor:
                        to_the_room = LICH_ROOM
                        message = (
                            'Двигаемся напрямую к '
                            'личу '
                            f'в комнату {to_the_room} '
                        )

                    self.send_info_message(
                        text=message,
                    )

                    if to_the_room is not None:
                        path = find_path_with_directions(
                            labirint_map=labirint_map,
                            start_room=my_room,
                            end_room=to_the_room,
                        )

                if not path:
                    self.clean_label_messages()
                    self.send_alarm_message(
                        'Путь не найден, проверьте карту!',
                    )
                    self.stop_event()
                    if self.start_button:
                        self.start_button.configure(fg='black')
                    continue

                while path and self.cycle_is_running:

                    try:
                        self.wait_until_transition_timeout(5)

                        message = (f'Осталось комнат: {len(path)}')

                        self.send_status_message(
                            text=message,
                        )

                        self.default_maze_actions(
                            message_to_tg=message_to_tg,
                            telegram_id=telegram_id,
                            slots=slots,
                            spell=spell,
                            mind_spirit_play=mind_spirit_play,
                            min_hp=min_hp,
                            spell_book=spell_book,
                            cheerfulness=cheerfulness,
                            cheerfulness_min=cheerfulness_min,
                            cheerfulness_slot=cheerfulness_slot,
                            cheerfulness_spell=cheerfulness_spell,
                        )

                        passed_room = self.get_room_number()
                        if passed_room is None:
                            continue
                        self.passed_maze_rooms.add(passed_room)

                        if path[0] == 'запад':
                            if self.crossing_to_the_west():
                                last_turn = path.pop(0)
                                continue
                            self.return_back_to_previous_room(
                                last_turn=last_turn,
                            )

                        elif path[0] == 'юг':
                            if self.crossing_to_the_south():
                                last_turn = path.pop(0)
                                continue
                            self.return_back_to_previous_room(
                                last_turn=last_turn,
                            )

                        elif path[0] == 'север':
                            if self.crossing_to_the_north():
                                last_turn = path.pop(0)
                                continue
                            self.return_back_to_previous_room(
                                last_turn=last_turn,
                            )

                        elif path[0] == 'восток':
                            if self.crossing_to_the_east():
                                last_turn = path.pop(0)
                                continue
                            self.return_back_to_previous_room(
                                last_turn=last_turn,
                            )

                    except Exception:
                        self.driver._switch_to.default_content()
                        self.default_maze_actions(
                            message_to_tg=message_to_tg,
                            telegram_id=telegram_id,
                            slots=slots,
                            spell=spell,
                            mind_spirit_play=mind_spirit_play,
                            min_hp=min_hp,
                            spell_book=spell_book,
                            cheerfulness=cheerfulness,
                            cheerfulness_min=cheerfulness_min,
                            cheerfulness_slot=cheerfulness_slot,
                            cheerfulness_spell=cheerfulness_spell,
                        )

                        actual_room = self.get_room_number()
                        if actual_room and (
                            to_the_room is not None
                        ) and not via_drop:
                            path = find_path_with_directions(
                                labirint_map=labirint_map,
                                start_room=actual_room,
                                end_room=to_the_room,
                            )
                        continue

                sleep(1)

                self.default_maze_actions(
                            message_to_tg=message_to_tg,
                            telegram_id=telegram_id,
                            slots=slots,
                            spell=spell,
                            mind_spirit_play=mind_spirit_play,
                            min_hp=min_hp,
                            spell_book=spell_book,
                            cheerfulness=cheerfulness,
                            cheerfulness_min=cheerfulness_min,
                            cheerfulness_slot=cheerfulness_slot,
                            cheerfulness_spell=cheerfulness_spell,
                        )
                message = f'Путь до комнаты {to_the_room} пройден!'

                self.try_to_switch_to_central_frame()
                sleep(1)
                city_portal = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[alt="Портал в город"]',
                    )
                if city_portal:
                    city_portal[0].click()
                    self.try_to_switch_to_dialog()
                    come_back = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Телепортироваться.',
                        )
                    if come_back:
                        come_back[0].click()

                self.send_status_message(
                    text=message,
                )
                self.stop_event()

                if self.start_button:
                    self.start_button.configure(fg='black')

            except Exception as e:
                self.actions_after_exception(e)

    def default_maze_actions(
        self,
        message_to_tg: bool = False,
        telegram_id: int | None = None,
        slots: SlotsPage = SlotsPage._1,
        spell: Slot = Slot._1,
        mind_spirit_play: bool = True,
        min_hp: int | None = None,
        spell_book: dict | None = None,
        cheerfulness: bool = False,
        cheerfulness_min: int | None = None,
        cheerfulness_slot: SlotsPage = SlotsPage._0,
        cheerfulness_spell: Slot = Slot._1,
    ) -> None:
        """Стандартный набор действий в лабиринте."""
        if not self.driver:
            raise InvalidSessionIdException

        self.check_kaptcha(
            message_to_tg=message_to_tg,
            telegram_id=telegram_id)

        if self.check_for_fight():
            self.fight(
                spell_book=spell_book,
                default_slot=slots,
                default_spell=spell)

        self.try_to_come_back_from_fight()

        self.try_to_switch_to_central_frame()
        # sleep(0.5)

        self.play_with_poetry_spirit()
        self.play_with_gamble_spirit()

        if mind_spirit_play:
            self.play_with_mind_spirit()

        else:
            self.actions_with_mind_spirit(
                message_to_tg=message_to_tg,
                telegram_id=telegram_id,
            )

        self.check_room_for_drop()

        fountain = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[alt="Бодрящий фонтан"]',
            )
        if fountain:
            fountain[0].click()
            self.try_to_switch_to_dialog()
            drink = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Выпить',
                        )
            if drink:
                drink[0].click()

            come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Отойти',
                    )
            if come_back:
                come_back[0].click()

        if cheerfulness and self.check_for_fight() is False:
            self.check_cheerfulnes_level(
                cheerfulnes_min=cheerfulness_min,
                cheerfulnes_slot=cheerfulness_slot,
                cheerfulnes_spell=cheerfulness_spell,
            )

        self.check_health(
            min_hp=min_hp,
            message_to_tg=message_to_tg,
            telegram_id=telegram_id,
        )

    def forest_passing(
        self,
        message_to_tg: bool = False,
        telegram_id: int | None = None,
        slots: SlotsPage = SlotsPage._1,
        spell: Slot = Slot._1,
        spell_book: dict | None = None,
        cheerfulness: bool = False,
        cheerfulness_min: int | None = None,
        cheerfulness_slot: SlotsPage = SlotsPage._0,
        cheerfulness_spell: Slot = Slot._1,
    ) -> None:
        """Логика прохождения леса."""
        if not self.driver:
            raise InvalidSessionIdException

        while self.cycle_is_running:

            try:

                if cheerfulness:

                    self.check_cheerfulnes_level(
                        cheerfulnes_min=cheerfulness_min,
                        cheerfulnes_slot=cheerfulness_slot,
                        cheerfulnes_spell=cheerfulness_spell,
                    )

                self.check_room_for_stash_and_herd()

                self.check_kaptcha(
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id,
                )

                self.try_to_come_back_from_fight()

                if self.check_for_fight():
                    self.fight(
                        spell_book=spell_book,
                        default_slot=slots,
                        default_spell=spell)

                self.check_room_for_stash_and_herd()

                self.wait_until_transition_timeout(5)

                self.check_room_for_stash_and_herd()

                room_number = self.get_room_number()

                if room_number is None:
                    continue

                if room_number == 89:

                    back_from_forest = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'a[href="/room/room.php?id=19529728"]',
                    )
                    if back_from_forest:
                        self.click_to_element_with_actionchains(
                            back_from_forest[0],
                        )
                    Alert(self.driver).accept()
                    self.stop_event()

                    if self.forest_button:
                        self.forest_button.configure(fg='black')

                    self.send_info_message('Лес пройден')
                    logger.info(
                        'Лес пройден',
                    )

                    with sync_session_maker() as session:

                        event_crud.create(
                            session=session,
                            event_name='Пройден лес',
                        )

                make_transition(
                    room_number=room_number,
                    right=self.crossing_to_the_east,
                    left=self.crossing_to_the_west,
                    up=self.crossing_to_the_north,
                    down=self.crossing_to_the_south,
                    passed_rooms=self.passed_forest_rooms,
                )
                self.check_room_for_stash_and_herd()

            except Exception as e:
                self.actions_after_exception(e)

    def actions_with_mind_spirit(
        self,
        message_to_tg: bool,
        telegram_id: int | None,
    ) -> None:
        """Действия для ручной игре с духом ума."""
        if not self.driver:
            raise InvalidSessionIdException

        mind_spirit = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    NPCImgTags.mind_spirit,
                )

        if not mind_spirit:
            return

        logger.info(
            'Пойманы духом ума',
        )

        if self.bot and message_to_tg and telegram_id:
            self.sync_send_message(
                telegram_id=telegram_id,
                text='Обнаружен дух ума!',
            )
            self.wait_until_mind_spirit_on_page(5)

        else:
            self.driver.execute_script(
                'window.alert("Обнаружен дух ума!");',
            )
            self.wait_until_alert_present(30)
            self.wait_until_mind_spirit_on_page(5)

    def full_refresh(self) -> None:
        """Метод перезагрузки игры (в случае ошибок сервера и интернета)."""
        if not self.driver:
            raise InvalidSessionIdException

        self.driver.refresh()
        # self.driver.get(self.domen + 'main.php')

        self.user.login_to_game(
            domen=self.domen,
        )

        logger.info('Плановая перезагрузка игры')
