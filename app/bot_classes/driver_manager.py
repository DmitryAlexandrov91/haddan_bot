import logging
import platform
import random
import re
import threading
import tkinter as tk
from time import sleep
from typing import Optional

from configs import configure_logging
from constants import (CHROME_PATH, FIELD_PRICES,
                       GAMBLE_SPIRIT_RIGHT_ANSWERS,
                       POETRY_SPIRIT_RIGHT_ANSWERS, TELEGRAM_CHAT_ID,
                       Floor, Slot, SlotsPage)
from maze_utils import (find_path_via_boxes_with_directions,
                        find_path_with_directions, get_floor_map)
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # noqa
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telebot import TeleBot
from utils import (get_attr_from_string, get_dragon_time_wait,
                   get_intimidation_and_next_room, price_counter,
                   time_extractor)
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Класс управления объектом webdriver."""

    def __init__(self, bot=None):
        self.driver: webdriver.Chrome = None
        self.thread: threading = None
        self.options = self._get_default_options()
        self.bot: TeleBot = bot
        self.event: threading.Event = threading.Event()
        self.errors_count: int = 0
        self.wait_timeout: int = 30
        self.alarm_label: tk.Label = None
        self.info_label: tk.Label = None
        self.status_label: tk.Label = None
        self.start_button: tk.Button = None

    def _get_default_options(self):
        options = webdriver.ChromeOptions()

        #  Работа в полном окне
        options.add_argument('--start-maximized')

        # Анти-детект
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        # options.add_argument('--disable-gpu')

        #  экспериментально
        # options.add_argument('--single-process')
        # options.add_argument('--disable-features=V8ProxyResolver')

        #  Только DOM
        options.set_capability("pageLoadStrategy", "eager")

        #  Отключает расширения
        options.add_argument('--disable-extensions')
        #  Ускоряет загрузку
        options.add_argument('--disable-plugins-discovery')
        #  Блокируем уведомления(ломает бой)
        # options.add_argument('--disable-notifications')

        #  Разрешить старые плагины
        # options.add_argument('--allow-outdated-plugins')
        #  Автозагрузка плагинов
        # options.add_argument('--always-authorize-plugins')

        if platform.system() == 'Windows':
            options.binary_location = CHROME_PATH
        else:
            #  только для linux
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

        return options

    # Служебные методы взаимодействия. ******************************
    def start_driver(self):
        """Создаёт объект класса webdriver учитывая self.options."""
        self.close_driver()

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

    def get_active_driver(self) -> webdriver.Chrome:
        """Функция для проверки наличия активного драйвера."""
        return self.driver

    def print_element_content(self, element: WebElement):
        """Выводит в терминал html код элемента"""
        print(element.get_attribute('outerHTML'))

    def get_element_content(self, element: WebElement) -> str:
        """Возвращает сожержимое элемента."""
        return element.get_attribute('outerHTML')

    def save_url_content(self):
        """Сохраняет контент страницы.

        В файле page.html в корне проекта.
        """
        page_source = self.driver.page_source
        with open('page.html', 'w', encoding='utf-8') as file:
            file.write(page_source)

    def start_event(self):
        """Устанавливает флаг в положение True."""
        self.event.set()

    def stop_event(self):
        """Устанавливает флаг циклов в положение False."""
        self.event.clear()
    # ***************************************************************

    #  Методы взаимодействия с элементами.***************************
    def wait_while_element_will_be_clickable(self, element: WebElement):
        """Ждёт пока элемент станет кликабельным."""
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(element))

    def scroll_to_element(self, element: WebElement):
        """Прокручивает до нужного жлемента."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            element
        )

    def click_to_element_with_actionchains(self, element: WebElement):
        """Щёлкает по элементу методом click класса ActionChains.

        Максимальная эмуляция реального нажатия мышкой*
        """
        ActionChains(self.driver).move_to_element(
                element).click().perform()
    #  **************************************************************

    #  Методы взаимодействия с фреймами. **************************
    def try_to_switch_to_central_frame(self):
        """Переключается на центральный фрейм окна."""

        if self.driver.execute_script("return window.name;") != 'frmcentral':

            try:
                self.driver.switch_to.frame("frmcenterandchat")
                self.driver.switch_to.frame("frmcentral")

            except Exception:
                self.driver.switch_to.default_content()

    def try_to_switch_to_dialog(self):
        """Переключается на фрейм диалога."""

        if self.driver.execute_script("return window.name;") != 'thedialog':

            try:
                self.driver.switch_to.frame("thedialog")

            except Exception:
                self.driver.switch_to.default_content()

    def find_all_iframes(self):
        """Выводит в терминал список всех iframe егов на странице."""
        frames = self.driver.find_elements(By.TAG_NAME, 'iframe')
        if frames:
            print([frame.get_attribute('name') for frame in frames])
        else:
            print('iframe на странице не найдены')
    #  **************************************************************

    #  Методы ведения боя. ******************************************
    def get_active_spell(self) -> Optional[str]:
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
            spell_number: str,
            slot_number: str) -> Optional[str]:
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
            slots_page: SlotsPage,
            slot: Slot):
        """Открывает меню быстрых слотов и выбирает знужный закл."""
        if not self.check_come_back():
            active_spell = self.get_active_spell()
            # print(f'Активный закл - {active_spell}')
            spell_to_cast = self.get_spell_to_cast(
                spell_number=slot,
                slot_number=slots_page
            )
            # print(f'Нужно кастануть - {spell_to_cast}')
            if spell_to_cast != active_spell and not self.check_come_back():
                self.driver.execute_script(
                    f'slotsShow({int(slots_page) -1 })'
                )
                self.driver.execute_script(
                    f'return qs_onClickSlot(event,{int(slot) - 1})'
                )

    def get_hit_number(self) -> Optional[str]:
        """Возвращает номер удара в бою."""
        try:
            hit_number = self.driver.find_element(
                By.CSS_SELECTOR,
                'a[href="javascript:submitMove()"]'
            )
            return hit_number.text
        except Exception:
            return None

    def get_round_number(self) -> str:
        """Возвращает номер раунда.

        В формате "Раунд 1" и т.д.
        """
        rounds = self.driver.find_elements(
            By.CSS_SELECTOR, '#divlog p'
        )
        if rounds:
            amount = len(rounds)
            return f'Раунд {amount + 1}'
        else:
            return 'Раунд 1'
    # ***************************************************************

    def fight(
            self,
            spell_book: dict,
            default_slot: SlotsPage = SlotsPage._1,
            default_spell: Slot = Slot._1):
        """Проводит бой."""
        round = self.get_round_number()
        kick = self.get_hit_number()

        if not kick:
            self.try_to_come_back_from_fight()
            self.send_info_message(
                text='Бой завершён'
            )

        else:
            self.send_info_message(
                text='Проводим бой'
            )
            try:
                self.open_slot_and_choise_spell(
                    slots_page=spell_book[round][kick]['slot'],
                    slot=spell_book[round][kick]['spell'])
            except Exception:
                self.open_slot_and_choise_spell(
                    slots_page=default_slot,
                    slot=default_spell)

            self.try_to_switch_to_central_frame()
            # sleep(0.5)

            come_back = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Вернуться')
            if come_back:
                come_back[0].click()
                self.send_alarm_message(
                    text='Бой завершён'
                )

            else:

                try:
                    element = self.driver.execute_script(
                        '''
                        touchFight();
                        return document.activeElement;
                        '''
                    )
                    WebDriverWait(self.driver, 30).until_not(
                            EC.presence_of_element_located((
                                By.XPATH,
                                "//*[contains(text(),'Пожалуйста, подождите')]"
                                ))
                        )
                    try:
                        if element and EC.element_to_be_clickable(element):
                            element.click()
                            element.send_keys(Keys.TAB)
                    except Exception:
                        pass

                except Exception as e:
                    self.actions_after_exception(e)

                self.fight(
                    spell_book=spell_book,
                    default_slot=default_slot,
                    default_spell=default_spell)

    #  Методы игры с духами. ****************************************
    def play_with_gamble_spirit(self):
        """Игра с духом азарта."""
        try:
            self.try_to_switch_to_central_frame()

            gamble_spirit = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            'img[id="roomnpc1850578"]')

            if gamble_spirit:
                gamble_spirit[0].click()
                sleep(1)

                print('Играем с духом азарта.')
                self.send_info_message(
                    text='Пойманы духом азарта'
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
                        intimidation, next_room = get_intimidation_and_next_room(
                            spirit_text[0].text)

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

        except Exception as e:
            print(
                'При игре с духом азарта возникла ошибка: ',
                str(e)
            )
            self.try_to_switch_to_central_frame()

            gamble_spirit = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            'img[id="roomnpc1850578"]')

            if gamble_spirit:
                self.play_with_gamble_spirit()
            pass

    def play_with_poetry_spirit(self):
        """Игра с духом поэзии."""
        poetry_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850579"]')
        if poetry_spirit:
            try:
                poetry_spirit[0].click()
                sleep(1)

                self.send_info_message(
                    text='Пойманы духом поэзии'
                )
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
            except Exception as e:
                print(
                    'При игре с духом поэзии возникла ошибка: ',
                    str(e)
                )
                self.try_to_switch_to_central_frame()

                poetry_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850579"]')
                if poetry_spirit:
                    self.play_with_poetry_spirit()
                pass

    def play_with_mind_spirit(self):
        """Игра с духом ума."""
        mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850577"]')

        if mind_spirit:
            try:
                mind_spirit[0].click()
                sleep(0.5)

                print('Играем с духом ума')
                self.send_info_message(
                    text='Пойманы духом ума'
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
                print(
                    'При игре с духом ума возникла ошибка: ',
                    str(e)
                )
                self.try_to_switch_to_central_frame()

                mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850577"]'
                    )
                if mind_spirit:
                    self.play_with_mind_spirit()
                pass
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

    def check_kaptcha(
            self,
            message_to_tg: bool,
            telegram_id: int = None):
        """Проверяет наличие капчи на странице."""
        if not self.event.is_set():
            exit()
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
            self.sleep_while_event_is_true(time_to_sleep=30)
            # sleep(30)
            self.check_kaptcha(
                message_to_tg=message_to_tg,
                telegram_id=telegram_id)

    def check_health(
            self,
            min_hp: int,
            message_to_tg: bool,
            telegram_id: int):
        """"Проверка ХП.

        :min_hp: минимальное кол-во ХП.
        :message_to_tg: флаг отправки сообщений в ТГ.
        :telegram_id: телеграм id куда отправлять сообщение.
        """
        if not self.event.is_set():
            exit()

        self.driver.switch_to.default_content()
        health = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'span[id="m_hpc"]'
                )
        if health:
            hp = int(health[0].text)
            if hp < min_hp:
                if self.bot and message_to_tg and telegram_id:
                    self.bot.send_message(
                        chat_id=telegram_id,
                        text='Здоровье упало меньше минимума!'
                    )
                else:
                    print('Мало хп, спим 30 секунд!')
                self.sleep_while_event_is_true(time_to_sleep=30)
                # sleep(30)
                self.check_health(
                    min_hp=min_hp,
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id
                )

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
        """Переходит на север."""
        self.try_to_switch_to_central_frame()
        north = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На север"]')
        if not north:
            north = self.driver.find_elements(
                By.ID, 'roommarker0'
            )

        if north:
            north[0].click()
            return True
        return False

    def crossing_to_the_south(self) -> bool:
        """Переходит на юг.

        Если переход произошёл возвращает True
        """
        self.try_to_switch_to_central_frame()
        south = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На юг"]')
        if not south:
            south = self.driver.find_elements(
                By.ID, 'roommarker1'
            )
        if south:
            south[0].click()
            return True
        return False

    def crossing_to_the_west(self):
        """Переходит на запад."""
        self.try_to_switch_to_central_frame()
        west = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На запад"]')
        if west:
            west[0].click()
            return True
        return False

    def crossing_to_the_east(self):
        """Переходит на восток."""
        self.try_to_switch_to_central_frame()
        east = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На восток"]')
        if east:
            east[0].click()
            return True
        return False
    #  **************************************************************

    # Основные циклы приложения *************************************
    def glade_farm(
            self,
            price_dict: dict = FIELD_PRICES,
            slots: SlotsPage = SlotsPage._1,
            spell: Slot = Slot._1,
            message_to_tg: bool = False,
            telegram_id: int = None,
            spell_book: dict = None):
        """Фарм поляны."""
        while self.event.is_set() is True:

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

                            # print(f'Ждём {time_for_wait} секунд(ы).')

                            self.sleep_while_event_is_true(time_for_wait)
                            # sleep(time_for_wait)

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
                            message_for_log = (
                                f'{res_price[most_cheep_res]}')

                            self.scroll_to_element(
                                glade_fairy_answers[most_cheep_res]
                            )

                            glade_fairy_answers[most_cheep_res].click()

                            self.send_info_message(
                                text=f'Получено у феи: {message_for_log}'
                            )

                self.try_to_switch_to_central_frame()
                sleep(1)

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
                self.sleep_while_event_is_true(15)
                # sleep(15)
                print('Получено уведомление, ждём!')

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
            min_hp: int = None,
            telegram_id: int = None,
            spell_book: dict = None,
            cheerfulness: bool = False,
            cheerfulness_min: int = None,
            cheerfulness_slot: SlotsPage = SlotsPage._0,
            cheerfulness_spell: Slot = Slot._1
            ):
        """Фарм с проведением боя."""
        while self.event.is_set() is True:

            try:
                if cheerfulness:

                    self.check_cheerfulnes_level(
                        cheerfulnes_min=cheerfulness_min,
                        cheerfulnes_slot=cheerfulness_slot,
                        cheerfulnes_spell=cheerfulness_spell
                    )

                self.try_to_switch_to_central_frame()
                sleep(1)

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

                        if not self.crossing_to_the_south():
                            self.crossing_to_the_north()

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
                        self.sleep_while_event_is_true(30)
                        # sleep(30)

                self.check_health(
                    min_hp=min_hp,
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id
                )

            except UnexpectedAlertPresentException:
                print('Получено уведомление, ждём!')
                self.sleep_while_event_is_true(15)

            except Exception as e:
                self.actions_after_exception(exception=e)

    def dragon_farm(
            self,
            default_slot: SlotsPage = SlotsPage._1,
            default_spell: Slot = Slot._5,
            spell_book: dict = None,
            message_to_tg: bool = False,
            telegram_id: int = None):
        """"Фарм пыльных драконов."""

        while self.event.is_set() is True:

            try:

                self.try_to_switch_to_central_frame()
                sleep(1)

                self.check_kaptcha(
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id)
                self.check_error_on_page()

                self.try_to_come_back_from_fight()

                if self.check_for_fight():
                    self.fight(
                        spell_book=spell_book,
                        default_slot=default_slot,
                        default_spell=default_spell)

                dragon = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            'img[id="roomnpc2460308"]')
                if not dragon:
                    dragon = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            'img[id="roomnpc2337344"]')
                if not dragon:
                    dragon = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            'img[id="roomnpc2460307"]')
                if dragon:
                    self.click_to_element_with_actionchains(dragon[0])

                self.try_to_switch_to_dialog()
                sleep(1)

                dragon_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak'
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
                                'talksayBIG'
                            )
                            if dragon_text:
                                title = dragon_text[0].text
                                if 'Вам надо подождать до' in title:
                                    time_to_wait = get_dragon_time_wait(title)
                                    print(f'Ждём КД {time_to_wait} секунд(ы).')
                                    self.sleep_while_event_is_true(
                                        time_to_wait)

                                if 'Старт состоится' in title:
                                    time_to_wait = get_dragon_time_wait(title)
                                    print(
                                        'Ждём начала ивента '
                                        f'{time_to_wait} секунд(ы).'
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
                        default_spell=default_spell
                    )

                self.driver.switch_to.default_content()
                sleep(1)

            except UnexpectedAlertPresentException:
                print('Получено уведомление, ждём!')
                self.sleep_while_event_is_true(15)

            except Exception as e:
                self.actions_after_exception(e)

    def actions_after_exception(self, exception: Exception):
        """Общее действие обработки исключения."""
        configure_logging()
        logging.exception(
            f'\nВозникло исключение {str(exception)}\n',
            stack_info=False
        )
        try:

            self.driver.switch_to.default_content()
            self.errors_count += 1
            print(f'Текущее количество ошибок - {self.errors_count}')
            if self.errors_count >= 10:
                self.driver.refresh()
                self.errors_count = 0
                self.sleep_while_event_is_true(5)

        except AttributeError:
            self.clean_label_messages()
            self.send_alarm_message(
                'Сначала войдите в игру!'
            )
            self.stop_event()

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

    def check_cheerfulnes_level(
            self,
            cheerfulnes_min: int,
            cheerfulnes_slot: SlotsPage = SlotsPage._0,
            cheerfulnes_spell: Slot = Slot._1):
        """Проверяет уровень бодрости.

        Если меньше установленного уровня, пъёт элик.
        :cheerfulnes_min: минимальное кол-во бодрости.
        :cheerfulnes_slot: страница слотов с бодрой.
        :cheerfulnes_spell: номер слота с бодрой.
        """
        if self.check_for_fight() is False:
            cheerfulnes_level = self.driver.find_elements(
                By.CLASS_NAME, 'current-bf')
            if cheerfulnes_level:
                cheerfulnes = int(cheerfulnes_level[0].text)

                if cheerfulnes_min:

                    while cheerfulnes < cheerfulnes_min:

                        self.open_slot_and_choise_spell(
                            slots_page=cheerfulnes_slot,
                            slot=cheerfulnes_spell
                        )

                        sleep(1)

                        cheerfulnes_level = self.driver.find_elements(
                            By.CLASS_NAME, 'current-bf')
                        if cheerfulnes_level:
                            cheerfulnes = int(cheerfulnes_level[0].text)
                        else:
                            break

    def sleep_while_event_is_true(
            self, time_to_sleep: int):
        """Ждёт указанное количество секунд.

        Пока флаг event == True.
        :time_to_sleep: кол-во секунд для ожидания.
        """
        counter = time_to_sleep
        while self.event.is_set() is True and counter > 0:
            sleep(1)
            counter -= 1
            self.send_status_message(
                text=f'Ждём секунд: {counter}'
            )
        self.send_status_message()

    def maze_passing(
            self,
            via_drop: bool = True,
            to_the_room: int = None,
            message_to_tg: bool = False,
            telegram_id: int = None,
            slots: SlotsPage = SlotsPage._1,
            spell: Slot = Slot._1,
            mind_spirit_play: bool = True,
            min_hp: int = None,
            spell_book: dict = None,
            cheerfulness: bool = False,
            cheerfulness_min: int = None,
            cheerfulness_slot: SlotsPage = SlotsPage._0,
            cheerfulness_spell: Slot = Slot._1,
            first_floor: bool = False,
            second_floor: bool = False,
            third_floor: bool = False
            ):
        """Прохождение лабиринта."""

        temp_manager = DriverManager()
        self.send_status_message(
                text='Рисуем маршрут по наводке от Макса...',
            )

        if first_floor:
            labirint_map = get_floor_map(
                floor=Floor.FIRST_FLOOR,
                manager=temp_manager)
        if second_floor:
            labirint_map = get_floor_map(
                floor=Floor.SECOND_FLOOR,
                manager=temp_manager
                )
        if third_floor:
            labirint_map = get_floor_map(
                floor=Floor.THIRD_FLOOR,
                manager=temp_manager
                )

        if not first_floor and not second_floor and not third_floor:
            self.send_alarm_message(
                text='Выберите этаж на котором вы находитесь.',
            )
            self.stop_event()

        if not labirint_map:
            self.send_alarm_message(
                text='Не получилось нарисовать маршрут, '
                'нажмите стоп и попробуйте ещё раз.',
            )
            self.stop_event()

        while self.event.is_set() is True:

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
                    cheerfulness_spell=cheerfulness_spell
                )

                my_room = self.get_room_number()

                #  Если указана комната и не стоит выбор через весь дроп.
                if to_the_room is not None and not via_drop:

                    message = (
                        f'Двигаемся по прямой в комнату {to_the_room} '
                        f'из комнаты {my_room}'
                    )
                    print(message)
                    self.send_info_message(
                        text=message,
                    )

                    path = find_path_with_directions(
                        labirint_map=labirint_map,
                        start_room=my_room,
                        end_room=to_the_room
                    )

                #  Если указана комната и стоит выбор через весь дроп.
                if to_the_room is not None and via_drop:

                    message = (
                        f'Двигаемся через весь дроп в комнату {to_the_room} '
                        f'из комнаты {my_room}'
                    )
                    print(message)
                    self.send_info_message(
                        text=message
                    )

                    path = find_path_via_boxes_with_directions(
                        labirint_map=labirint_map,
                        start_room=my_room,
                        target_room=to_the_room
                    )

                if not path:
                    self.clean_label_messages()
                    self.send_alarm_message(
                        'Путь не найден, проверьте карту!'
                    )
                    self.stop_event()
                    self.start_button.configure(fg='black')
                    continue

                attempt = 0  # Счётчик попыток.

                while path:

                    try:
                        message = (f'Осталось комнат: {len(path)}')

                        self.send_status_message(
                            text=message,
                        )

                        self.try_to_switch_to_central_frame()
                        sleep(1)

                        WebDriverWait(self.driver, 30).until_not(
                                EC.presence_of_element_located((
                                    By.XPATH,
                                    "//*[contains(text(),'Вы можете попасть')]"
                                    ))
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
                            cheerfulness_spell=cheerfulness_spell
                        )

                        if path[0] == 'запад':
                            if self.crossing_to_the_west():
                                sleep(1)
                                last_turn = path.pop(0)
                                attempt = 0
                                continue
                            else:
                                attempt += 1
                                if attempt > 10:
                                    self.return_back_to_previous_room(
                                        last_turn=last_turn
                                    )

                        if path[0] == 'юг':
                            if self.crossing_to_the_south():
                                sleep(1)
                                last_turn = path.pop(0)
                                attempt = 0
                                continue
                            else:
                                attempt += 1
                                if attempt > 10:
                                    self.return_back_to_previous_room(
                                        last_turn=last_turn
                                    )
                        if path[0] == 'север':
                            if self.crossing_to_the_north():
                                sleep(1)
                                last_turn = path.pop(0)
                                attempt = 0
                                continue
                            else:
                                attempt += 1
                                if attempt > 10:
                                    self.return_back_to_previous_room(
                                        last_turn=last_turn
                                    )

                        if path[0] == 'восток':
                            if self.crossing_to_the_east():
                                sleep(1)
                                last_turn = path.pop(0)
                                attempt = 0
                                continue
                            else:
                                attempt += 1
                                if attempt > 10:
                                    self.return_back_to_previous_room(
                                        last_turn=last_turn
                                    )

                    except Exception as e:
                        print('По пути возникла ошибка: ', e)
                        self.driver._switch_to.default_content()
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
                            cheerfulness_spell=cheerfulness_spell
                        )

                        actual_room = self.get_room_number()
                        if actual_room and (
                            to_the_room is not None
                        ) and not via_drop:
                            path = find_path_with_directions(
                                labirint_map=labirint_map,
                                start_room=actual_room,
                                end_room=to_the_room
                            )
                        continue

                self.send_status_message(
                    text=f'Путь до комнаты {to_the_room} пройден.'
                )
                self.stop_event()
                self.start_button.configure(fg='black')

            except Exception as e:
                self.actions_after_exception(e)

    def get_room_number(self) -> Optional[int]:
        """Возвращает номер комнаты в лабе, в которой находится персонаж."""
        self.try_to_switch_to_central_frame()
        my_room = self.driver.find_elements(
                By.CLASS_NAME, 'LOCATION_NAME'
            )
        if my_room:
            return int(
                re.search(
                    r'№(\d+)',
                    my_room[0].text
                ).group(1)
            )

    def default_maze_actions(
            self,
            message_to_tg: bool = False,
            telegram_id: int = None,
            slots: SlotsPage = SlotsPage._1,
            spell: Slot = Slot._1,
            mind_spirit_play: bool = True,
            min_hp: int = None,
            spell_book: dict = None,
            cheerfulness: bool = False,
            cheerfulness_min: int = None,
            cheerfulness_slot: SlotsPage = SlotsPage._0,
            cheerfulness_spell: Slot = Slot._1):
        """Стандартный набор действий в лабиринте."""
        if cheerfulness:
            self.check_cheerfulnes_level(
                cheerfulnes_min=cheerfulness_min,
                cheerfulnes_slot=cheerfulness_slot,
                cheerfulnes_spell=cheerfulness_spell
            )

        self.try_to_switch_to_central_frame()
        # sleep(1)

        self.check_kaptcha(
            message_to_tg=message_to_tg,
            telegram_id=telegram_id)
        self.check_error_on_page()

        self.try_to_come_back_from_fight()

        if self.check_for_fight():
            self.fight(
                spell_book=spell_book,
                default_slot=slots,
                default_spell=spell)

        self.check_room_for_drop()

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
                self.send_info_message(
                    'Пойманы духом ума'
                )
                self.sleep_while_event_is_true(30)

        self.check_room_for_drop()

        self.check_health(
            min_hp=min_hp,
            message_to_tg=message_to_tg,
            telegram_id=telegram_id
        )

    def check_room_for_drop(self):
        """Проверяет наличие дропа к комнате лабиринта."""
        self.try_to_switch_to_central_frame()

        drop = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[alt="Гора Черепов"]'
        )
        message = 'Найдена гора черепов'
        if not drop:
            drop = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[alt="Сундук"]'
            )
            message = 'Найден сундук'
        if not drop:
            message = 'Найден окованный сундук'
            drop = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[alt="Окованный Cундук"]'
            )

        if drop:
            drop[0].click()
            self.send_info_message(message)

    def return_back_to_previous_room(
            self,
            last_turn):
        """"Действие возврата в предыдущую комнату."""

        if last_turn == 'запад':
            self.crossing_to_the_east()

        if last_turn == 'восток':
            self.crossing_to_the_west()

        if last_turn == 'север':
            self.crossing_to_the_south()

        if last_turn == 'юг':
            self.crossing_to_the_north()

    def send_alarm_message(
            self,
            text: str = ''):
        """Меняет текст alarm_label Tkinter."""
        self.alarm_label.configure(
            text=text
        )

    def send_info_message(
            self,
            text: str = ''):
        """Меняет текст info_label Tkinter."""
        self.info_label.configure(
            text=text
        )

    def send_status_message(
            self,
            text: str = ''):
        """Меняет текст status_label Tkinter."""
        self.status_label.configure(
            text=text
        )

    def clean_label_messages(self):
        """Очищает все уведомления."""
        self.send_alarm_message()
        self.send_info_message()
        self.send_status_message()
