import logging
import platform
import random
import threading
from datetime import datetime
from time import sleep

from configs import configure_logging
from constants import (CHROME_PATH, FIELD_PRICES, GAMBLE_SPIRIT_RIGHT_ANSWERS,
                       POETRY_SPIRIT_RIGHT_ANSWERS, TELEGRAM_CHAT_ID,
                       TIME_FORMAT)
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # noqa
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telebot import TeleBot
from utils import (get_attr_from_string, get_intimidation_and_next_room,
                   price_counter, time_extractor)
from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.firefox.service import Service
# from webdriver_manager.firefox import GeckoDriverManager


class DriverManager:
    """Класс управления объектом webdriver."""

    def __init__(self, bot=None):
        self.driver: webdriver.Chrome = None
        self.thread: threading = None
        self.options = self._get_default_options()
        self.bot: TeleBot = bot
        self.event: threading.Event = threading.Event()
        self.errors_count = 0
        self.wait_timeout = 30

    def _get_default_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])

        if platform.system() == 'Windows':
            options.add_argument('--start-maximized')
            options.binary_location = CHROME_PATH

        return options

    # Служебные методы взаимодействия. ******************************
    def start_driver(self):
        """Создаёт объект класса webdriver учитывая self.options."""
        if self.driver is None:

            try:
                service = Service(
                    executable_path=ChromeDriverManager().install(),
                    service_args=['--verbose'],
                )

                self.driver = webdriver.Chrome(
                    service=service,
                    options=self.options
                )
                self.thread = threading.current_thread()
                self.driver.set_page_load_timeout(self.wait_timeout)
                self.driver.set_script_timeout(self.wait_timeout)
                # self.driver.implicitly_wait(0.5)

            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=False
                )

    def close_driver(self):
        """Закрывает активный driver если таковой имеется."""
        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=False
                )
            finally:
                self.driver = None
                self.thread = None

    def get_active_driver(self):
        """Функция для проверки наличия активного драйвера."""
        return self.driver

    def print_element_content(self, element):
        """Выводит в терминал html код элемента"""
        print(element.get_attribute('outerHTML'))

    def get_element_content(self, element):
        """Возвращает сожержимое элемента."""
        return element.get_attribute('outerHTML')

    def save_url_content(self):
        """Сохраняет контент страницы.

        В файле page.html в корне проекта.
        """
        page_source = self.driver.page_source
        with open('page.html', "w", encoding="utf-8") as file:
            file.write(page_source)

    def start_event(self):
        """Ставит флаг запуска циклов в положение True."""
        self.event.set()

    def stop_event(self):
        """Ставит флаг запуска циклов в положение False."""
        self.event.clear()
    # ***************************************************************

    #  Методы взаимодействия с элементами.***************************
    def wait_while_element_will_be_clickable(self, element):
        """Ждёт пока элемент станет кликабельным."""
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(element))

    def scroll_to_element(self, element):
        """Прокручивает до нужного жлемента."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            element
        )

    def click_to_element_with_actionchains(self, element):
        """Щёлкает по элементу методом click класса ActionChains.

        Максимальная эмуляция реального нажатия мышкой*
        """
        ActionChains(self.driver).move_to_element(
                element).click().perform()
    #  **************************************************************

    #  Методы переключения между фреймами. **************************
    def try_to_switch_to_central_frame(self):
        """Переключается на центральный фрейм окна."""

        try:
            self.driver.switch_to.default_content()

            sleep(0.5)

            self.driver.switch_to.frame("frmcenterandchat")
            self.driver.switch_to.frame("frmcentral")

        except Exception:
            pass

    def try_to_switch_to_dialog(self):
        """Переключается на фрейм диалога."""

        try:
            sleep(0.5)
            self.driver.switch_to.frame("thedialog")

        except Exception:
            pass

    def find_all_iframes(self):
        """Выводит в терминал список всех iframe егов на странице."""
        frames = self.driver.find_elements(By.TAG_NAME, 'iframe')
        if frames:
            print([frame.get_attribute('name') for frame in frames])
        else:
            print('iframe на странице не найдены')
    #  **************************************************************

    #  Методы ведения боя. ******************************************
    def get_active_spell(self):
        """Возвращает название заклинания, которое используется в бою."""
        self.try_to_switch_to_central_frame()
        spell = self.driver.find_elements(
            By.CSS_SELECTOR,
            'a[href="javascript:fight_goAndShowSlots(true)"]'
        )

        if spell:
            return get_attr_from_string(
                self.get_element_content(spell[0]),
                'title'
            )

    def get_spell_to_cast(
            self,
            spell_number,
            slot_number):
        """Возвращает название заклинания, которое нужно использовать."""
        self.driver.switch_to.default_content()
        self.driver.execute_script(
                f'slotsShow({int(slot_number) - 1})'
            )
        spell_to_cast = self.driver.find_elements(
            By.ID, f'lSlot{spell_number}'
        )
        if spell_to_cast:
            return get_attr_from_string(
                self.get_element_content(spell_to_cast[0]),
                'title'
            )

    def open_slot_and_choise_spell(
            self,
            slots_number,
            spell_number):
        """Открывает меню быстрых слотов и выбирает знужный закл."""
        if not self.check_come_back():
            active_spell = self.get_active_spell()
            # print(f'Активный закл - {active_spell}')
            spell_to_cast = self.get_spell_to_cast(
                spell_number=spell_number,
                slot_number=slots_number
            )
            # print(f'Нужно кастануть - {spell_to_cast}')
            if spell_to_cast != active_spell and not self.check_come_back():
                self.driver.execute_script(
                    f'slotsShow({int(slots_number) -1 })'
                )
                self.driver.execute_script(
                    f'return qs_onClickSlot(event,{int(spell_number) - 1})'
                )

    def get_hit_number(self) -> str:
        """Возвращает номер удара в бою."""
        try:
            hit_number = self.driver.find_element(
                By.CSS_SELECTOR,
                'a[href="javascript:submitMove()"]'
            )
            return hit_number.text
        except Exception:
            print('Номер удара не найден.')

    def get_round_number(self) -> str:
        """Возвращает номер раунда"""
        for i in range(1, 7):
            round_name = self.driver.find_elements(
                    By.NAME,
                    f'roundr{i}')
            if not round_name:
                return 'Раунд 1'
            else:
                return f'Раунд {i + 1}'
    # ***************************************************************

    def fight(self, spell_book, default_slot, default_spell):
        """Проводит бой."""
        round = self.get_round_number()
        kick = self.get_hit_number()

        if not kick:
            self.try_to_come_back_from_fight()

        else:
            try:
                self.open_slot_and_choise_spell(
                    slots_number=spell_book[round][kick]['slot'],
                    spell_number=spell_book[round][kick]['spell'])
            except Exception:
                self.open_slot_and_choise_spell(
                    slots_number=default_slot,
                    spell_number=default_spell)

            self.try_to_switch_to_central_frame()
            come_back = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Вернуться')
            if come_back:
                come_back[0].click()

            else:

                try:
                    WebDriverWait(self.driver, 30).until_not(
                            EC.presence_of_element_located((
                                By.XPATH,
                                "//*[contains(text(),'Пожалуйста, подождите')]"
                                ))
                        )
                    element = self.driver.execute_script(
                        '''
                        touchFight();
                        return document.activeElement;
                        '''
                    )
                    if element:
                        element.click()
                        ActionChains(self.driver).send_keys(Keys.TAB).perform()

                except Exception as e:
                    self.actions_after_exception(e)

                self.fight(
                    spell_book=spell_book,
                    default_slot=default_slot,
                    default_spell=default_spell)

    #  Методы игры с духами. ****************************************
    def play_with_gamble_spirit(self):
        """Игра с духом азарта."""
        gamble_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850578"]')

        if gamble_spirit:
            gamble_spirit[0].click()
            sleep(1)
            self.try_to_switch_to_dialog()
            spirit_answers = self.driver.find_elements(
                By.CLASS_NAME,
                'talksayTak')

            while spirit_answers:
                spirit_text = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayBIG')

                if spirit_text and 'Параметры' in spirit_text[0].text:
                    intimidation, next_room = get_intimidation_and_next_room(
                        spirit_text[0].text)

                    if not intimidation or not next_room:  # exp
                        continue

                    if next_room >= intimidation:
                        right_choise = self.driver.find_elements(
                            By.PARTIAL_LINK_TEXT, 'Довольно')
                        right_choise[0].click()
                    else:
                        right_choise = self.driver.find_elements(
                            By.PARTIAL_LINK_TEXT, 'Дальше!')
                        right_choise[0].click()

                    spirit_answers = self.driver.find_elements(
                        By.CLASS_NAME,
                        'talksayTak'
                    )
                    sleep(0.5)
                    continue

                self.right_answers_choise(GAMBLE_SPIRIT_RIGHT_ANSWERS)

                spirit_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak'
                )
                sleep(0.5)

    def play_with_poetry_spirit(self):
        """Игра с духом поэзии."""
        poetry_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850579"]')
        if poetry_spirit:
            poetry_spirit[0].click()
            sleep(1)

            print('Играем с духом поэзии.')
            self.try_to_switch_to_dialog()
            spirit_answers = self.driver.find_elements(
                By.CLASS_NAME,
                'talksayTak0')
            while spirit_answers:
                self.right_answers_choise(POETRY_SPIRIT_RIGHT_ANSWERS)
                spirit_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak0'
                )
                sleep(0.5)

    def play_with_mind_spirit(self):
        """Игра с духом ума."""
        mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850577"]')

        if mind_spirit:
            mind_spirit[0].click()
            sleep(0.5)
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
    #  **************************************************************

    # Фарм поляны. **************************************************
    def try_to_click_to_glade_fairy(self):
        """Ищет фею поляны и щёлкает на неё."""
        glade_fairy = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc231778"]')
        if not glade_fairy:
            glade_fairy = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc17481"]')

        if glade_fairy:
            self.click_to_element_with_actionchains(glade_fairy[0])
    # ***************************************************************

    def send_photo(self, photo):
        """Отправляет фотку в телеграм."""
        self.bot.send_photo(TELEGRAM_CHAT_ID, open(photo, 'rb'))

    def check_kaptcha(self, message_to_tg, telegram_id=None):
        """Проверяет наличие капчи на странице."""
        kaptcha = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'img[src="/inner/img/bc.php"]'
                )
        if kaptcha:
            if self.bot and message_to_tg and telegram_id:
                self.bot.send_message(
                    chat_id=telegram_id,
                    text='Обнаружена капча!'
                )
            else:
                self.driver.execute_script(
                    'window.alert("Обнаружена капча!");')
            sleep(30)
            self.check_kaptcha(
                message_to_tg=message_to_tg,
                telegram_id=telegram_id)

    def check_health(self) -> int:
        """"Возвращает кол-во  ХП персонажа."""
        self.driver.switch_to.default_content()
        health = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'span[id="m_hpc"]'
                )
        if health:
            hp = int(health[0].text)
            return hp

    def check_error_on_page(self):
        error = self.driver.find_elements(
            By.PARTIAL_LINK_TEXT, 'Ошибка')
        if error:
            print('Обнаружена ошибка на странице, перезагружаем окно.')
            self.driver.refresh()
        come_back = self.driver.find_elements(
            By.CSS_SELECTOR, 'a[href="javascript:history.back()"]')
        if come_back:
            self.click_to_element_with_actionchains(come_back[0])

    # Переходы ******************************************************
    def crossing_to_the_north(self):
        north = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На север"]')
        if north:
            north[0].click()

    def crossing_to_the_south(self):
        south = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На юг"]')
        if south:
            south[0].click()

    def crossing_to_the_west(self):
        west = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На запад"]')
        if west:
            west[0].click()

    def crossing_to_the_east(self):
        east = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На восток"]')
        if east:
            east[0].click()
    #  **************************************************************

    # Основные циклы приложения *************************************
    def glade_farm(
            self,
            price_dict: dict = FIELD_PRICES,
            slots=2,
            spell=1,
            message_to_tg=False,
            telegram_id=None,
            spell_book: dict = None):
        """Фарм поляны."""
        while self.event.is_set() is True:
            # self.driver.implicitly_wait(0.5)

            sleep(1)
            try:

                self.try_to_switch_to_central_frame()
                self.try_to_click_to_glade_fairy()
                self.try_to_switch_to_dialog()

                glade_fairy_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak')
                if glade_fairy_answers:
                    sleep(1)
                    if len(glade_fairy_answers) == 1:

                        sleep(1)
                        wait_tag = self.driver.find_elements(
                            By.CLASS_NAME,
                            'talksayBIG')
                        if wait_tag and 'где-то через' in wait_tag[0].text:
                            sleep(1)
                            sleep(time_extractor(wait_tag[0].text))
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
                            print(res_price)
                            most_cheep_res = price_counter(
                                res_price,
                                price_diсt=price_dict)
                            now = datetime.now().strftime(TIME_FORMAT)
                            message_for_log = (
                                f'{res_price[most_cheep_res]} {now}')

                            self.scroll_to_element(
                                glade_fairy_answers[most_cheep_res]
                            )

                            glade_fairy_answers[most_cheep_res].click()
                            with open(
                                'glade_farm.txt',
                                "r+",
                                encoding="utf-8"
                            ) as file:
                                content = file.read()
                                file.seek(0)
                                file.write(f'{message_for_log}\n')
                                file.write(content)
                            print(message_for_log)

                self.try_to_switch_to_central_frame()

                if self.check_for_fight():
                    self.fight(
                        spell_book=spell_book,
                        default_slot=slots,
                        default_spell=spell)
                self.check_kaptcha(
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id)
                self.check_error_on_page()
                self.driver.switch_to.default_content()

            except UnexpectedAlertPresentException:
                sleep(15)
                print('Получено уведомление, ждём!')

            except Exception as e:
                self.actions_after_exception(exception=e)

    def farm(
            self,
            slots=2,
            spell=1,
            up_down_move=False,
            left_right_move=False,
            mind_spirit_play=True,
            message_to_tg=False,
            min_hp: int = None,
            telegram_id=None,
            spell_book: dict = None):
        """Фарм с проведением боя одним заклом."""
        while self.event.is_set() is True:

            try:
                self.try_to_switch_to_central_frame()
                self.check_kaptcha(message_to_tg=message_to_tg,
                                   telegram_id=telegram_id)
                self.check_error_on_page()

                self.try_to_come_back_from_fight()

                if self.check_for_fight():
                    self.fight(
                        spell_book=spell_book,
                        default_slot=slots,
                        default_spell=spell)

                else:
                    WebDriverWait(self.driver, 30).until_not(
                            EC.presence_of_element_located((
                                By.XPATH,
                                "//*[contains(text(),'Вы можете попасть')]"
                                ))
                        )

                    if up_down_move:
                        self.crossing_to_the_north()
                        self.crossing_to_the_south()

                        if self.check_for_fight():
                            self.fight(
                                spell_book=spell_book,
                                default_slot=slots,
                                default_spell=spell)

                    if left_right_move:
                        self.crossing_to_the_west()
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
                    mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850577"]')

                    if mind_spirit:
                        if self.bot and message_to_tg and telegram_id:
                            self.bot.send_message(
                                chat_id=telegram_id,
                                text='Обнаружен дух ума!'
                            )
                        else:
                            self.driver.execute_script(
                                'window.alert("Обнаружен дух ума!");'
                            )
                        sleep(30)

                hp = self.check_health()
                if hp is not None and hp < min_hp:
                    if self.bot and message_to_tg and telegram_id:
                        self.bot.send_message(
                            chat_id=telegram_id,
                            text='Здоровье упало меньше минимума!'
                        )
                    else:
                        print('Мало хп, спим 30 секунд!')
                    sleep(30)

            except UnexpectedAlertPresentException:
                sleep(15)
                print('Получено уведомление, ждём!')

            except Exception as e:
                self.actions_after_exception(exception=e)

    def actions_after_exception(self, exception: Exception):
        """Общее действие обработки исключения."""
        configure_logging()
        logging.exception(
            f'\nВозникло исключение {str(exception)}\n',
            stack_info=False
        )

        self.driver.switch_to.default_content()
        self.errors_count += 1
        print(f'Текущее количество ошибок - {self.errors_count}')
        if self.errors_count >= 30:
            self.driver.refresh()
            self.errors_count = 0
            sleep(10)

    def right_answers_choise(self, right_answers):
        """Проходит циклом по правильным ответам.

        Если такой ответ есть, нажимает на него.
        """
        for answer in right_answers:
            right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, answer)
            if right_choise:
                right_choise[0].click()

    def check_for_fight(self) -> bool:
        """Если идёт бой, возвращает True."""
        hits = self.driver.find_elements(
            By.CSS_SELECTOR,
            'a[href="javascript:submitMove()"]'
        )
        return bool(hits)

    def check_come_back(self) -> bool:
        """Если бой закончен, возвращает True."""
        come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Вернуться')
        return bool(come_back)

    def try_to_come_back_from_fight(self):
        """"Если бой закончен, нажимает 'вернуться' """
        come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Вернуться')
        if come_back:
            come_back[0].click()
