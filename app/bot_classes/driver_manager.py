import logging
import platform
import random
import threading
from datetime import datetime
from time import sleep
from typing import Optional

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
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telebot import TeleBot
from utils import (get_attr_from_string, get_dragon_time_wait,
                   get_intimidation_and_next_room, price_counter,
                   time_extractor)
from webdriver_manager.chrome import ChromeDriverManager

from constants import SlotsPage, Spell


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
        options.add_argument('--single-process')
        options.add_argument('--disable-features=V8ProxyResolver')

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
            slots_number: str,
            spell_number: str):
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
            default_spell: Spell = Spell._1):
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
            # sleep(0.5)

            come_back = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Вернуться')
            if come_back:
                come_back[0].click()

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
        north = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На север"]')
        if not north:
            north = self.driver.find_elements(
                By.ID, 'roommarker0'
            )

        if north:
            north[0].click()

    def crossing_to_the_south(self):
        south = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На юг"]')
        if not south:
            south = self.driver.find_elements(
                By.ID, 'roommarker1'
            )
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
            slots: SlotsPage = SlotsPage._1,
            spell: Spell = Spell._1,
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
                            print(f'Ждём {time_for_wait} секунд(ы).')

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
                            now = datetime.now().strftime(TIME_FORMAT)
                            message_for_log = (
                                f'{res_price[most_cheep_res]} {now}')

                            self.scroll_to_element(
                                glade_fairy_answers[most_cheep_res]
                            )

                            glade_fairy_answers[most_cheep_res].click()

                            print(message_for_log)

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
            spell: Spell = Spell._1,
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
            cheerfulness_spell: Spell = Spell._1
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
                        self.crossing_to_the_south()
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
            default_spell: Spell = Spell._5,
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

        self.driver.switch_to.default_content()
        self.errors_count += 1
        print(f'Текущее количество ошибок - {self.errors_count}')
        if self.errors_count >= 10:
            self.driver.refresh()
            self.errors_count = 0
            sleep(5)

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
            cheerfulnes_spell: Spell = Spell._1):
        """Проверяет уровень бодрости.

        Если меньше установленного уровня, пъёт элик.
        :cheerfulnes_min: минимальное кол-во бодрости.
        :cheerfulnes_slot: страница слотов с бодрой.
        :cheerfulnes_spell: номер слота с бодрой.
        """
        cheerfulnes_level = self.driver.find_elements(
            By.CLASS_NAME, 'current-bf')
        if cheerfulnes_level:
            cheerfulnes = int(cheerfulnes_level[0].text)

            if cheerfulnes_min:

                while cheerfulnes < cheerfulnes_min:

                    self.open_slot_and_choise_spell(
                        slots_number=cheerfulnes_slot,
                        spell_number=cheerfulnes_spell
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
