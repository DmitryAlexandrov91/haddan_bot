import logging
import random
import threading
from datetime import datetime
from time import sleep

from configs import configure_logging
from constants import FIELD_PRICES, TELEGRAM_CHAT_ID, TIME_FORMAT
from selenium import webdriver
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


class DriverManager:
    """Класс управления объектом webdriver."""

    def __init__(self, bot=None):
        self.driver: webdriver.Chrome = None
        self.thread: threading = None
        self.options: webdriver.ChromeOptions = webdriver.ChromeOptions()
        self.bot: TeleBot = bot
        self.choises: dict = {}
        self.event: threading.Event = threading.Event()
        self.errors_count = 0

    # Служебные методы взаимодействия. ******************************
    def start_driver(self):
        """Создаёт объект класса webdriver учитывая self.options."""
        if self.driver is None or self.driver.session_id is None:
            service = Service(executable_path=ChromeDriverManager().install())
            self.driver = webdriver.Chrome(
                service=service,
                options=self.options)
            self.thread = threading.current_thread()

    def close_driver(self):
        """Закрывает активный driver если таковой имеется."""
        if self.driver is not None:
            self.driver.quit()
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
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(element))

    def scroll_to_element(self, element):
        """Прокручивает до нужного жлемента."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            element
        )

    def click_to_element_with_actionchains(self, element):
        """Щёлкает по элементу методом click класса ActionChains"""
        ActionChains(self.driver).move_to_element(
                element).click().perform()
    #  **************************************************************

    #  Методы переключения между фреймами. **************************
    def try_to_switch_to_central_frame(self):
        """Переключается на центральный фрейм окна."""
        frames = self.driver.find_elements(By.TAG_NAME, 'iframe')
        sleep(0.5)
        if frames:
            for frame in frames:
                if frame.get_attribute('name') == 'frmcenterandchat':
                    self.driver.switch_to.frame("frmcenterandchat")
                    self.driver.switch_to.frame("frmcentral")
                    break

    def try_to_switch_to_dialog(self):
        """Переключается на фрейм диалога."""
        frames = self.driver.find_elements(By.TAG_NAME, 'iframe')
        if frames:
            for frame in frames:
                if frame.get_attribute('id') == 'thedialog':
                    self.driver.switch_to.frame("thedialog")
                    break

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

    def get_spell_to_cast(self, spell_number):
        """Возвращает название заклинания, которое нужно использовать."""
        self.driver.switch_to.default_content()
        spell_to_cast = self.driver.find_elements(
            By.ID, f'lSlot{spell_number}'
        )
        if spell_to_cast:
            return get_attr_from_string(
                self.get_element_content(spell_to_cast[0]),
                'title'
            )

    def quick_slots_open(self):
        """Открывает меню быстрых слотов."""
        quick_slots = self.driver.find_elements(
            By.CSS_SELECTOR,
            'a[href="javascript:qs_toggleSlots()"]'
        )
        if quick_slots:
            quick_slots[0].click()

    def quick_slots_close(self):
        """Закрывает меню быстрых слотов."""
        quick_slots = self.driver.find_elements(
            By.CSS_SELECTOR,
            'a[href="javascript:Slot.showSlots()"]'
        )
        if quick_slots:
            try:
                quick_slots[0].click()
            except Exception:
                print('Слоты уже закрыты!')
                pass

    def quick_slot_choise(self, slots_number):
        """Открывает нужную страницу быстрых слотов.

        1 - страница с напитками
        2 - страница с заклами №1
        3 - страница с заклами №2 и тд
        """
        slots = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, f'slotsBtn{slots_number}')
                )
            )
        self.wait_while_element_will_be_clickable(
            slots
        )
        slots.click()

    def spell_choise(self, spell_number):
        """Щёлкает по нужному заклинанию на странице слотов 1-7"""
        spell = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, f'lSlot{spell_number}')
                )
            )
        self.wait_while_element_will_be_clickable(
            spell
        )
        spell.click()

    def open_slot_and_choise_spell(
            self,
            slots_number: int,
            spell_number: int):
        """Открывает меню быстрых слотов и выбирает знужный закл."""
        active_spell = self.get_active_spell()
        spell_to_cast = self.get_spell_to_cast(
            spell_number=spell_number
        )
        if spell_to_cast != active_spell:
            self.driver.switch_to.default_content()
            self.quick_slots_open()
            self.quick_slot_choise(slots_number=slots_number)
            self.spell_choise(spell_number=spell_number)
            self.quick_slots_close()
            self.try_to_switch_to_central_frame()

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

    def one_spell_fight(self, slots=2, spell=1):
        """Проводит бой одним заклом."""
        choise = self.choises.get('choised', False)
        if not choise:
            self.open_slot_and_choise_spell(
                slots_number=slots, spell_number=spell)
            self.choises['choised'] = True
        self.try_to_switch_to_central_frame()
        come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Вернуться')
        if come_back:
            self.click_to_element_with_actionchains(come_back[0])

        else:
            hits = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[onclick="touchFight();"]')
            if hits:
                self.click_to_element_with_actionchains(hits[0])
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                self.one_spell_fight(slots=slots, spell=spell)
    # ***************************************************************

    #  Методы игры с духами. ****************************************
    def play_with_gamble_spirit(self):
        """Ищет фею поляны и щёлкает на неё."""
        gamble_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850578"]')

        if gamble_spirit:
            self.wait_while_element_will_be_clickable(
                 gamble_spirit[0]
            )
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
                if 'Параметры' in spirit_text[0].text:
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

                right_choise = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Телепортироваться')
                if right_choise:
                    right_choise[0].click()

                right_choise = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'делу давай!')
                if right_choise:
                    right_choise[0].click()

                right_choise = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, ' / ')
                if right_choise:
                    right_choise[0].click()

                right_choise = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'пошли')
                if right_choise:
                    right_choise[0].click()
                spirit_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak'
                )
                sleep(0.5)

    def play_with_poetry_spirit(self):
        poetry_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850579"]')
        if poetry_spirit:
            self.wait_while_element_will_be_clickable(
                 poetry_spirit[0]
            )
            poetry_spirit[0].click()
            sleep(1)

            print('Играем с духом поэзии.')
            self.try_to_switch_to_dialog()
            spirit_answers = self.driver.find_elements(
                By.CLASS_NAME,
                'talksayTak0')
            while spirit_answers:
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'давай дальше')
                if right_choise:
                    right_choise[0].click()
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, ' / ')
                if right_choise:
                    right_choise[0].click()
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Начали!')
                if right_choise:
                    right_choise[0].click()
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Дальше!')
                if right_choise:
                    right_choise[0].click()
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'пора обратно')
                if right_choise:
                    right_choise[0].click()
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'с наградой')
                if right_choise:
                    right_choise[0].click()
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Телепортироваться')
                if right_choise:
                    right_choise[0].click()
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Увечье нам не надо')
                if right_choise:
                    right_choise[0].click()
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Поехали!')
                if right_choise:
                    right_choise[0].click()
                spirit_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak0'
                )
                sleep(0.5)

    def play_with_mind_spirit(self):
        mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850577"]')

        if mind_spirit:
            self.wait_while_element_will_be_clickable(
                 mind_spirit[0]
            )
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

        if len(glade_fairy) > 0:
            self.wait_while_element_will_be_clickable(
                 glade_fairy[0]
            )
            glade_fairy[0].click()
            sleep(1)
    # ***************************************************************

    def send_photo(self, photo):
        """Отправляет фотку в телеграм."""
        self.bot.send_photo(TELEGRAM_CHAT_ID, open(photo, 'rb'))

    def check_kaptcha(self, message_to_tg, telegram_id=None):
        """Проверяет наличие капчи на странице."""
        self.try_to_switch_to_central_frame()
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
        # self.driver.execute_script("window.location.reload();")
        self.driver.switch_to.default_content()

    def check_health(self):
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
        self.try_to_switch_to_central_frame()
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
            self.wait_while_element_will_be_clickable(
                north[0]
            )
            north[0].click()

    def crossing_to_the_south(self):
        south = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На юг"]')
        if south:
            self.wait_while_element_will_be_clickable(
                south[0]
            )
            south[0].click()

    def crossing_to_the_west(self):
        west = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На запад"]')
        if west:
            self.wait_while_element_will_be_clickable(
                west[0]
            )
            west[0].click()

    def crossing_to_the_east(self):
        east = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[title="На восток"]')
        if east:
            self.wait_while_element_will_be_clickable(
                east[0]
            )
            east[0].click()
    #  **************************************************************

    # Основные циклы приложения *************************************
    def glade_farm(
            self,
            price_dict: dict = FIELD_PRICES,
            slots=2,
            spell=1,
            message_to_tg=False,
            telegram_id=None):
        """Фарм поляны(пока без распознования капчи)"""
        self.start_event()
        while self.event.is_set() is True:
            # sleep(1)
            try:
                self.try_to_switch_to_central_frame()
                self.try_to_click_to_glade_fairy()
                self.try_to_switch_to_dialog()
                glade_fairy_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak')
                if glade_fairy_answers:
                    if len(glade_fairy_answers) == 1:
                        wait_tag = self.driver.find_elements(
                            By.CLASS_NAME,
                            'talksayBIG')
                        if wait_tag:
                            self.wait_while_element_will_be_clickable(
                                wait_tag[0]
                            )
                            sleep(time_extractor(wait_tag[0].text))
                            glade_fairy_answers[0].click()
                    if len(glade_fairy_answers) == 3:
                        self.wait_while_element_will_be_clickable(
                            glade_fairy_answers[1]
                        )
                        glade_fairy_answers[1].click()
                    if len(glade_fairy_answers) > 3:
                        resurses = self.driver.find_elements(By.TAG_NAME, 'li')
                        if resurses:
                            res_price = [res.text for res in resurses]
                            most_cheep_res = price_counter(
                                res_price,
                                price_diсt=price_dict)
                            now = datetime.now().strftime(TIME_FORMAT)
                            message_for_log = (
                                f'{res_price[most_cheep_res]} {now}')
                            self.wait_while_element_will_be_clickable(
                                glade_fairy_answers[most_cheep_res]
                            )
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
                hits = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'img[onclick="touchFight();"]')
                if hits:
                    sleep(2)
                    self.one_spell_fight(slots=slots, spell=spell)
                self.choises.clear()
                self.check_kaptcha(
                    message_to_tg=message_to_tg,
                    telegram_id=telegram_id)
                self.check_error_on_page()
            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=True
                )
                sleep(2)
                self.driver.switch_to.default_content()
                self.errors_count += 1
                print(f'Текущее количество ошибок - {self.errors_count}')
                if self.errors_count > 30:
                    self.driver.refresh()
                    self.errors_count = 0

    def one_spell_farm(
            self,
            slots=2,
            spell=1,
            up_down_move=False,
            left_right_move=False,
            mind_spirit_play=True,
            message_to_tg=False,
            min_hp=10000,
            telegram_id=None):
        """Фарм с проведением боя одним заклом."""
        while self.event.is_set() is True:
            sleep(1)
            try:
                self.check_kaptcha(message_to_tg=message_to_tg)
                self.check_error_on_page()
                self.try_to_switch_to_central_frame()
                come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Вернуться')
                if come_back:
                    self.click_to_element_with_actionchains(come_back[0])
                hits = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'img[onclick="touchFight();"]')
                if hits:
                    self.one_spell_fight(
                        slots=slots, spell=spell)
                else:
                    if up_down_move:
                        self.crossing_to_the_north()
                        self.crossing_to_the_south()

                    if left_right_move:
                        self.crossing_to_the_west()
                        self.crossing_to_the_east()

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

                self.choises.clear()
                hp = self.check_health()
                if hp is not None and hp < min_hp:
                    if self.bot and message_to_tg and telegram_id:
                        self.bot.send_message(
                            chat_id=telegram_id,
                            text='Здоровье упало меньше минимума!'
                        )
                    else:
                        self.driver.execute_script(
                            'window.alert("Мало здоровья, спим 30 секунд!");'
                        )
                    sleep(30)

            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=True
                )
                sleep(2)
                self.driver.switch_to.default_content()
                self.errors_count += 1
                print(f'Текущее количество ошибок - {self.errors_count}')
                if self.errors_count > 30:
                    self.driver.refresh()
                    self.errors_count = 0
