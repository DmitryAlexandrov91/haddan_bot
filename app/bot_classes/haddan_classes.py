import asyncio
import logging
import os
import random
import re
import threading
from datetime import datetime
from time import sleep
from typing import Optional

import requests
from PIL import Image
from aiogram import Bot, Dispatcher, F, Router, types
from config import configure_logging
from constants import (
    BASE_DIR,
    FIELD_PRICES,
    GAMBLE_SPIRIT_RIGHT_ANSWERS,
    HADDAN_URL,
    LICH_ROOM,
    POETRY_SPIRIT_RIGHT_ANSWERS,
    NPCImgTags,
    Room,
    Slot,
    SlotsPage,
)
from dao.crud import event_crud
from dao.database import sync_session_maker
from maze_utils import (
    find_path_via_boxes_with_directions,
    find_path_with_directions,
    get_sity_portal_room_number,
    get_upper_portal_room_number,
)
from selenium import webdriver
from selenium.common.exceptions import (
    InvalidSessionIdException,
    StaleElementReferenceException,
    TimeoutException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from utils import (
    get_dragon_time_wait,
    get_intimidation_and_next_room,
    price_counter,
    time_extractor,
)

from .driver_manager import DriverManager
from .services import make_transition

configure_logging()


class HaddanUser:

    """Бот класс управления действиями персонажа.

    Принимает два обязательных аргумента при инициализации:
    :char: никнейм персонажа,
    :driver: объект класса webdriver.Chrome.

    """

    def __init__(
            self,
            char: str,
            driver: webdriver.Chrome,
            password: str,
    ) -> None:
        """Инициализация класса HaddanUser."""
        self.driver = driver
        self.char = char
        self.password = password
        self.login_url: str = HADDAN_URL

    def login_to_game(self, domen: str) -> None:
        """Заходит в игру под заданным именем char."""
        self.driver.get(domen)
        username_field = self.driver.find_element(
            By.NAME, 'username')
        username_field.send_keys(self.char)
        password_field = self.driver.find_element(
            By.NAME, 'passwd')
        password_field.send_keys(self.password)
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR,
            '[href="javascript:void(enterHaddan())"]')
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(
                submit_button),
            )
        submit_button.click()


class HaddanCommonDriver(DriverManager):
    """Класс управления фреймами и общие методы."""

    def try_to_switch_to_central_frame(self) -> None:
        """Переключается на центральный фрейм окна."""
        if not self.driver:
            raise InvalidSessionIdException

        if self.driver.execute_script("return window.name;") != 'frmcentral':

            try:
                self.driver.switch_to.frame("frmcentral")

            except Exception:
                self.driver.switch_to.default_content()

    def try_to_switch_to_dialog(self) -> None:
        """Переключается на фрейм диалога."""
        if not self.driver:
            raise InvalidSessionIdException

        if self.driver.execute_script("return window.name;") != 'thedialog':

            try:
                self.driver.switch_to.frame("thedialog")

            except Exception:
                self.driver.switch_to.default_content()

    def find_all_iframes(self) -> None:
        """Выводит в терминал список всех iframe егов на странице."""
        if not self.driver:
            raise InvalidSessionIdException

        frames = self.driver.find_elements(By.TAG_NAME, 'iframe')
        if frames:
            logging.info([frame.get_attribute('name') for frame in frames])
        else:
            logging.info('iframe на странице не найдены')

    def get_room_number(self) -> int | None:
        """Возвращает номер комнаты в лабе, в которой находится персонаж."""
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()

        my_room = self.driver.find_elements(
                By.CLASS_NAME, 'LOCATION_NAME',
            )
        if my_room:
            text = my_room[0].text
            pattern = r'№(\d+)'

            result = re.search(pattern, text)

            if result:
                return int(result.group(1))

        return None

    def wait_until_kaptcha_on_page(self, time: int) -> None:
        """Ждёт до time секунд пор пока каптча на странице."""
        if not self.driver:
            raise InvalidSessionIdException

        if not self.cycle_is_running:
            exit()

        try:

            WebDriverWait(self.driver, time).until_not(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'img[src="/inner/img/bc.php"]',
                    )),
            )

        except TimeoutException:
            self.wait_until_kaptcha_on_page(time=time)

    def wait_until_kaptcha_after_tg_message(self, time: int) -> None:
        """Ждёт пока каптча на странице после отправки фото капчи в тг."""
        if not self.driver:
            raise InvalidSessionIdException

        try:

            WebDriverWait(self.driver, time).until_not(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'img[src="/inner/img/bc.php"]',
                    )),
            )

        except TimeoutException:
            pass

    def wait_until_mind_spirit_on_page(self, time: int) -> None:
        """Ждёт до time секунд пока дух ума на странице."""
        if not self.driver:
            raise InvalidSessionIdException

        if not self.cycle_is_running:
            exit()

        try:

            WebDriverWait(self.driver, time).until_not(
                    ec.presence_of_element_located((
                        By.CSS_SELECTOR,
                        NPCImgTags.mind_spirit,
                        ),
                    ),
                )

        except TimeoutException:
            self.wait_until_mind_spirit_on_page(time=time)

    def wait_until_transition_timeout(self, time: int) -> None:
        """Ждёт до time секунд перехода в другую локацию."""
        if not self.driver:
            raise InvalidSessionIdException

        if not self.cycle_is_running:
            exit()

        try:

            WebDriverWait(self.driver, time).until_not(
                ec.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(text(),'Вы можете попасть')]",
                    )),
            )

        except TimeoutException:
            self.wait_until_transition_timeout(time=time)

    def wait_until_alert_present(self, time: int) -> None:
        """Ждёт по time секунд пока на странице есть уведомление."""
        if not self.driver:
            raise InvalidSessionIdException

        if not self.cycle_is_running:
            exit()

        try:

            WebDriverWait(self.driver, time).until(
                lambda driver: not self.is_alert_present(),
            )

        except TimeoutException:
            self.wait_until_alert_present(time=time)

    def try_to_click_to_glade_fairy(self) -> None:
        """Ищет фею поляны и щёлкает на неё."""
        if not self.driver:
            raise InvalidSessionIdException

        glade_fairy = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.distans_fairy,
                    )
        if not glade_fairy:
            glade_fairy = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.distans_fairy,
                    )

        if glade_fairy:
            self.click_to_element_with_actionchains(glade_fairy[0])

    def actions_after_exception(self, exception: Exception) -> None:
        """Общее действие обработки исключения."""
        logging.error(
            f'\nВозникло исключение {str(exception)}\n',
            stack_info=False,
        )

        if not self.driver:
            raise InvalidSessionIdException

        self.check_for_slot_clear_alarm_message()

        try:

            self.driver.switch_to.default_content()
            self.errors_count += 1
            logging.info(f'Текущее количество ошибок - {self.errors_count}')
            if self.errors_count >= 10:
                self.driver.refresh()
                self.errors_count = 0
                self.sleep_while_event_is_true(5)

        except AttributeError:
            self.clean_label_messages()
            self.send_alarm_message(
                'Сначала войдите в игру!',
            )
            self.stop_event()

    def check_for_slot_clear_alarm_message(self) -> None:
        """Проверяет на наличие окна, спрашивающего об очистке слота."""
        if not self.driver:
            raise InvalidSessionIdException

        self.driver.switch_to.default_content()
        alarm_window = self.driver.find_elements(
                By.CSS_SELECTOR,
                'input[id="talkModalButtonID_CANCEL"]')
        if alarm_window:
            alarm_window[0].click()
        self.try_to_switch_to_central_frame()


class HaddanFightDriver(HaddanCommonDriver):
    """Всё что связано с логикой проведения боя."""

    def check_for_fight(self) -> bool:
        """Если идёт бой, возвращает True."""
        self.try_to_switch_to_central_frame()

        if not self.driver:
            raise InvalidSessionIdException

        hits = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[onclick="touchFight();"]',
        )
        return bool(hits)

    def try_to_come_back_from_fight(self) -> None:
        """"Если бой закончен, нажимает 'вернуться'."""
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()
        come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Вернуться')
        if come_back:
            self.click_to_element_with_actionchains(come_back[0])

    def check_come_back(self) -> bool:
        """Если бой закончен, возвращает True."""
        if not self.driver:
            raise InvalidSessionIdException

        come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Вернуться')
        return bool(come_back)

    def get_active_spell(self) -> Optional[str]:
        """Возвращает название заклинания, которое используется в бою."""
        self.try_to_switch_to_central_frame()

        if not self.driver:
            raise InvalidSessionIdException

        spell = self.driver.find_elements(
            By.CSS_SELECTOR,
            'a[href="javascript:fight_goAndShowSlots(true)"]',
        )

        if spell:
            return self.get_attr_from_element(
                spell[0],
                'title',
            )
        return None

    def get_spell_to_cast(
            self,
            spell_number: str,
            slot_number: str) -> Optional[str]:
        """Возвращает название заклинания, которое нужно использовать."""
        if not self.driver:
            raise InvalidSessionIdException

        self.driver.switch_to.default_content()
        self.driver.execute_script(
                f'slotsShow({int(slot_number) - 1})',
            )
        spell_to_cast = self.driver.find_elements(
            By.ID, f'lSlot{spell_number}',
        )
        if spell_to_cast:
            return self.get_attr_from_element(
                spell_to_cast[0],
                'title',
            )
        return None

    def open_slot_and_choise_spell(
            self,
            slots_page: SlotsPage,
            slot: Slot) -> None:
        """Открывает меню быстрых слотов и выбирает знужный закл."""
        if not self.driver:
            raise InvalidSessionIdException

        self.check_for_slot_clear_alarm_message()

        if not self.check_come_back():

            if slots_page == 'p' == slot:
                self.try_to_switch_to_central_frame()
                kick = self.driver.find_elements(
                    By.CSS_SELECTOR, 'img[src="/@!images/fight/knife.gif"]',
                )
                if kick:
                    kick[0].click()

            else:
                active_spell = self.get_active_spell()
                spell_to_cast = self.get_spell_to_cast(
                    spell_number=slot,
                    slot_number=slots_page,
                )
                if spell_to_cast != active_spell and (
                    not self.check_come_back()
                ):
                    self.driver.execute_script(
                        f'slotsShow({int(slots_page) - 1})',
                    )
                    self.driver.execute_script(
                        f'return qs_onClickSlot(event,{int(slot) - 1})',
                    )

    def get_hit_number(self) -> Optional[str]:
        """Возвращает номер удара в бою."""
        if not self.driver:
            raise InvalidSessionIdException

        try:
            hit_number = self.driver.find_element(
                By.CSS_SELECTOR,
                'a[href="javascript:void(submitMove())"]',
            )
            return hit_number.text
        except Exception:
            return None

    def get_round_number(self) -> str | None:
        """Возвращает номер раунда.

        В формате 'Раунд 1', 'Раунд 2' и т.д.
        """
        if not self.driver:
            raise InvalidSessionIdException

        rounds = self.driver.find_elements(
            By.CSS_SELECTOR, '#divlog p',
        )
        if rounds:
            last_round = rounds[0].find_elements(
                By.CLASS_NAME, 'sys_time',
            )
            if last_round:
                current_round = last_round[0].text.rstrip().split()
                current_round[-1] = str(int(current_round[-1]) + 1)
                return f'{current_round[0]} {current_round[1]}'

        return 'Раунд 1'

    def fight(
            self,
            spell_book: dict | None,
            default_slot: SlotsPage = SlotsPage._1,
            default_spell: Slot = Slot._1) -> None:
        """Проводит бой."""
        if not self.driver:
            raise InvalidSessionIdException

        if not self.cycle_is_running:
            exit()

        # self.check_for_slot_clear_alarm_message()

        current_round = self.get_round_number()
        kick = self.get_hit_number()

        if not kick:
            self.try_to_come_back_from_fight()
            self.send_info_message(
                text='Бой завершён',
            )

        else:
            self.send_info_message(
                text='Проводим бой',
            )
            try:
                if spell_book:
                    self.open_slot_and_choise_spell(
                        slots_page=spell_book[current_round][kick]['slot'],
                        slot=spell_book[current_round][kick]['spell'])

                else:
                    self.open_slot_and_choise_spell(
                        slots_page=default_slot,
                        slot=default_spell)

            except Exception:
                # self.check_for_slot_clear_alarm_message()
                self.open_slot_and_choise_spell(
                    slots_page=default_slot,
                    slot=default_spell)

            self.try_to_switch_to_central_frame()

            come_back = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Вернуться')
            if come_back:
                come_back[0].click()
                self.send_alarm_message(
                    text='Бой завершён',
                )

            else:

                try:
                    element = self.driver.execute_script(
                        '''
                        touchFight();
                        return document.activeElement;
                        ''',
                    )
                    sleep(float(os.getenv('BEETS_DELAY', 0.2)))
                    # WebDriverWait(self.driver, 30).until_not(
                    #         ec.presence_of_element_located((
                    #             By.XPATH,
                    #             "//*[contains(text(),"
                    #             "'Пожалуйста, подождите')]",
                    #             )),
                    #     )
                    try:
                        if element:
                            element.send_keys(Keys.TAB)
                    except Exception:
                        pass

                except Exception as e:
                    self.actions_after_exception(e)

                self.fight(
                    spell_book=spell_book,
                    default_slot=default_slot,
                    default_spell=default_spell)


class HaddanSpiritPlay(HaddanFightDriver):
    """Класс игры с духами."""

    def right_answers_choise(self, right_answers: set) -> None:
        """Проходит циклом по правильным ответам.

        Если такой ответ есть, нажимает на него.
        """
        if not self.driver:
            raise InvalidSessionIdException

        for answer in right_answers:
            right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, answer)
            if right_choise:
                self.click_to_element_with_actionchains(
                    right_choise[0],
                )

    def play_with_gamble_spirit(self) -> None:
        """Игра с духом азарта."""
        if not self.driver:
            return

        try:
            self.try_to_switch_to_central_frame()

            gamble_spirit = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            NPCImgTags.gamble_spirit,
                        )

            if gamble_spirit:
                gamble_spirit[0].click()
                sleep(1)

                logging.info('Играем с духом азарта.')
                self.send_info_message(
                    text='Пойманы духом азарта',
                )
                self.try_to_switch_to_dialog()
                spirit_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak')

                while spirit_answers:

                    spirit_text = self.driver.find_elements(
                        By.CLASS_NAME,
                        'talksayBIG')

                    if spirit_text and 'Параметры' in spirit_text[0].text:
                        intimidation, next_room = (
                            get_intimidation_and_next_room(
                                spirit_text[0].text)
                        )

                        if next_room >= intimidation:
                            right_choise = self.driver.find_elements(
                                By.PARTIAL_LINK_TEXT, 'Довольно')
                            self.click_to_element_with_actionchains(
                                right_choise[0],
                            )
                        else:
                            right_choise = self.driver.find_elements(
                                By.PARTIAL_LINK_TEXT, 'Дальше!')
                            if not right_choise:
                                right_choise = self.driver.find_elements(
                                    By.PARTIAL_LINK_TEXT,
                                    'Пробуем снова')
                            if not right_choise:
                                right_choise = self.driver.find_elements(
                                    By.PARTIAL_LINK_TEXT,
                                    'Телепортироваться')
                            if right_choise:
                                self.click_to_element_with_actionchains(
                                    right_choise[0],
                                )

                        spirit_answers = self.driver.find_elements(
                            By.CLASS_NAME,
                            'talksayTak',
                        )
                        sleep(0.5)
                        continue

                    self.right_answers_choise(GAMBLE_SPIRIT_RIGHT_ANSWERS)

                    spirit_answers = self.driver.find_elements(
                        By.CLASS_NAME,
                        'talksayTak',
                    )
                    sleep(0.5)

        except Exception as e:
            logging.error(
                'При игре с духом азарта возникла ошибка: ',
                str(e),
            )
            self.try_to_switch_to_central_frame()

            gamble_spirit = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            NPCImgTags.gamble_spirit,
                        )

            if gamble_spirit:
                self.play_with_gamble_spirit()
            pass

    def play_with_poetry_spirit(self) -> None:
        """Игра с духом поэзии."""
        if not self.driver:
            raise

        poetry_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.poetry_spirit)
        if poetry_spirit:
            try:
                poetry_spirit[0].click()
                sleep(1)

                self.send_info_message(
                    text='Пойманы духом поэзии',
                )
                logging.info('Играем с духом поэзии.')
                self.try_to_switch_to_dialog()
                spirit_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak0')
                while spirit_answers:
                    self.right_answers_choise(POETRY_SPIRIT_RIGHT_ANSWERS)
                    spirit_answers = self.driver.find_elements(
                        By.CLASS_NAME,
                        'talksayTak0',
                    )
                    sleep(0.5)
            except Exception as e:
                logging.error(
                    'При игре с духом поэзии возникла ошибка: ',
                    str(e),
                )
                self.try_to_switch_to_central_frame()

                poetry_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.poetry_spirit,
                    )
                if poetry_spirit:
                    self.play_with_poetry_spirit()
                pass

    def play_with_mind_spirit(self) -> None:
        """Игра с духом ума."""
        if not self.driver:
            raise InvalidSessionIdException

        mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.mind_spirit,
                    )

        if mind_spirit:
            try:
                mind_spirit[0].click()
                sleep(0.5)

                logging.info('Играем с духом ума')
                self.send_info_message(
                    text='Пойманы духом ума',
                )
                self.try_to_switch_to_dialog()

                spirit_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak0')
                while spirit_answers:
                    right_choise = self.driver.find_elements(
                            By.PARTIAL_LINK_TEXT, 'Легко')
                    if right_choise:
                        right_choise[0].click()

                    random_play = self.driver.find_elements(
                            By.PARTIAL_LINK_TEXT, 'Сходить')

                    if random_play:
                        random_play[random.choice([0, 1])].click()

                    right_choise = self.driver.find_elements(
                            By.PARTIAL_LINK_TEXT, 'Телепортироваться')
                    if right_choise:
                        right_choise[0].click()

                    spirit_answers = self.driver.find_elements(
                        By.CLASS_NAME,
                        'talksayTak0')
                    sleep(0.5)

            except Exception as e:
                logging.error(
                    'При игре с духом ума возникла ошибка: ',
                    str(e),
                )
                self.try_to_switch_to_central_frame()

                mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.mind_spirit,
                    )
                if mind_spirit:
                    self.play_with_mind_spirit()
                pass


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
                                logging.warning(
                                    f"⚠️ Файл не найден: {source_file}",
                                )
                        except Exception as e:
                            logging.error(
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

            except Exception as e:
                logging.error(f"Ошибка при старте поллинга {str(e)}.")

    async def stop_polling(self) -> None:
        """Асинхронная остановка поллинга бота."""
        if self.polling_started.is_set():
            try:
                self.polling_started.clear()
                await self.dp.stop_polling()
            except Exception as e:
                logging.error(f"Ошибка при остановке поллинга {str(e)}")

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
            exit()
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
                logging.info('Обнаружена капча!')

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
            exit()

        if min_hp:

            self.driver.switch_to.default_content()
            health = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'span[id="m_hpc"]',
                    )
            if health:
                hp = int(health[0].text)
                if hp < min_hp:
                    logging.info('Мало хп, спим 30 секунд!')
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

    def crossing_to_the_north(self) -> bool:
        """Переходит на север."""
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()
        north = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На север"]')
        if not north:
            north = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[title="К берегу"]')

        if not north:
            north = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[title="К спуску"]')

        if not north:
            north = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[title="К Спуску"]')

        if north:
            self.click_to_element_with_actionchains(north[0])
            # north[0].click()
            return True
        return False

    def crossing_to_the_south(self) -> bool | None:
        """Переходит на юг.

        Если переход произошёл, возвращает True
        """
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()
        south = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На юг"]')
        if not south:
            south = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[title="К побережью"]')

        if not south:
            south = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[title="К спуску"]')

        if not south:
            south = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[title="К Берегу"]')

        if not south:
            south = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[title="К Мостику"]')

        if south:

            self.click_to_element_with_actionchains(south[0])

            return True
        return False

    def crossing_to_the_west(self) -> bool:
        """Переходит на запад."""
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()
        west = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На запад"]')
        if west:
            self.click_to_element_with_actionchains(west[0])
            # west[0].click()
            return True
        return False

    def crossing_to_the_east(self) -> bool:
        """Переходит на восток."""
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()
        east = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На восток"]')
        if east:
            self.click_to_element_with_actionchains(east[0])
            # east[0].click()
            return True
        return False

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
            cheerfulness_spell: Slot = Slot._1) -> None:
        """Фарм с проведением боя."""
        if not self.driver:
            return

        while self.cycle_is_running:

            try:

                # self.check_for_slot_clear_alarm_message()

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

                    if left_right_move:
                        if not self.crossing_to_the_west():
                            self.crossing_to_the_east()

                        if self.check_for_fight():
                            self.fight(
                                spell_book=spell_book,
                                default_slot=slots,
                                default_spell=spell)

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

        if self.check_for_fight() is False:
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
                    logging.info(message)
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
                    logging.info(message)
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

        if cheerfulness and self.check_for_fight() is False:
            self.check_cheerfulnes_level(
                cheerfulnes_min=cheerfulness_min,
                cheerfulnes_slot=cheerfulness_slot,
                cheerfulnes_spell=cheerfulness_spell,
            )

        self.try_to_switch_to_central_frame()
        sleep(0.5)

        self.check_kaptcha(
            message_to_tg=message_to_tg,
            telegram_id=telegram_id)

        self.try_to_come_back_from_fight()

        if self.check_for_fight():
            self.fight(
                spell_book=spell_book,
                default_slot=slots,
                default_spell=spell)

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

        self.check_health(
            min_hp=min_hp,
            message_to_tg=message_to_tg,
            telegram_id=telegram_id,
        )

    def check_room_for_drop(self) -> None:
        """Проверяет наличие дропа к комнате лабиринта."""
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()
        sleep(0.5)

        try:

            drop = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[alt="Гора Черепов"]',
            )
            message = 'Найдена гора черепов'
            if not drop:
                drop = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'img[alt="Сундук"]',
                )
                message = 'Найден сундук'
            if not drop:
                message = 'Найден окованный сундук'
                drop = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'img[alt="Окованный Cундук"]',
                )

            if drop:
                drop[0].click()
                sleep(1)
                self.send_info_message(message)
                self.check_room_for_drop()

        except StaleElementReferenceException:
            self.check_room_for_drop()

    def check_room_for_stash_and_herd(self) -> None:
        """Проверяет комнату в лесу на наличие тайника."""
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()
        sleep(0.5)

        drop = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[alt="Тайник"]',
        )
        if not drop:
            drop = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[alt="Табун"]',
            )
        if drop:
            self.click_to_element_with_actionchains(drop[0])
            # drop[0].click()
            sleep(0.5)

    def return_back_to_previous_room(
            self,
            last_turn: str,
    ) -> None:
        """"Действие возврата в предыдущую комнату."""
        match last_turn:
            case 'запад': self.crossing_to_the_east()
            case 'восток': self.crossing_to_the_west()
            case 'север': self.crossing_to_the_south()
            case 'юг': self.crossing_to_the_north()
            case _: pass

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

                else:
                    self.check_room_for_stash_and_herd()

                    self.wait_until_transition_timeout(15)

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

                        with sync_session_maker() as session:

                            event_crud.create(
                                session=session,
                                event_name="Пройден лес",
                            )

                        break

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

        if mind_spirit:
            self.send_info_message(
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
