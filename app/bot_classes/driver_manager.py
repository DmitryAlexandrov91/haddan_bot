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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telebot import TeleBot
from utils import price_counter, time_extractor, get_intimidation_and_next_room
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Класс управления объектом webdriver."""

    def __init__(self, bot=None):
        self.driver: webdriver.Chrome = None
        self.thread: threading = None
        self.options: webdriver.ChromeOptions = webdriver.ChromeOptions()
        if bot is not None:
            self.bot: TeleBot = bot
        self.choises: dict = {}
        self.event: threading.Event = threading.Event()

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

    def save_url_content(self):
        """Сохраняет контент страницы.

        В файле page.html в корне проекта.
        """
        page_source = self.driver.page_source
        with open('page.html', "w", encoding="utf-8") as file:
            file.write(page_source)

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

    def try_to_switch_to_central_frame(self):
        """Переключается на центральный фрейм окна."""
        frames = self.driver.find_elements(By.TAG_NAME, 'iframe')
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

    def quick_slots_open(self):
        """Открывает меню быстрых слотов."""
        # slot_buttons = self.driver.find_elements(
        #     By.ID, 'lSlot1')
        # if not slot_buttons:
        slots = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'lSlotsBtn')))
        self.wait_while_element_will_be_clickable(
            slots
        )
        slots.click()

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
            if spirit_answers:
                spirit_text = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayBIG')
                if 'Параметры' in spirit_text[0].text:
                    intimidation, next_room = get_intimidation_and_next_room(spirit_text[0].text)
                    if next_room >= intimidation:
                        right_choise = self.driver.find_elements(
                            By.PARTIAL_LINK_TEXT, 'Довольно')
                        right_choise[0].click()
                    else:
                        right_choise = self.driver.find_elements(
                            By.PARTIAL_LINK_TEXT, 'Дальше!')
                        right_choise[0].click()

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
            if spirit_answers:
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

    def play_with_mind_spirit(self):
        mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'img[id="roomnpc1850577"]')

        if mind_spirit:
            self.wait_while_element_will_be_clickable(
                 mind_spirit[0]
            )
            mind_spirit[0].click()
            sleep(1)
            self.try_to_switch_to_dialog()

            spirit_answers = self.driver.find_elements(
                By.CLASS_NAME,
                'talksayTak0')
            if spirit_answers:
                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Легко')
                if right_choise:
                    right_choise[0].click()

                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Сходить')

                if right_choise:
                    right_choise[random.choice([0, 1])].click()

                right_choise = self.driver.find_elements(
                        By.PARTIAL_LINK_TEXT, 'Телепортироваться')
                
                if right_choise:
                    right_choise[0].click()

    def one_spell_fight(self, slots=2, spell=1):
        """Проводит бой одним заклом."""
        choise = self.choises.get('choised', False)
        if not choise:
            self.driver.switch_to.default_content()
            self.quick_slots_open()
            self.quick_slot_choise(slots)
            self.spell_choise(spell)
            self.choises['choised'] = True
            self.quick_slots_open()
            self.try_to_switch_to_central_frame()
        come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Вернуться')
        if come_back:
            self.wait_while_element_will_be_clickable(
                come_back[0]
            )
            come_back[0].click()
            sleep(1)
        else:
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
            hits = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[onclick="touchFight();"]')
            if hits:
                self.wait_while_element_will_be_clickable(
                    hits[0]
                )
                hits[0].click()
                sleep(0.5)
                self.one_spell_fight(slots=2, spell=1)

    def send_photo(self, photo):
        """Отправляет фотку в телеграм."""
        self.bot.send_photo(TELEGRAM_CHAT_ID, open(photo, 'rb'))

    def check_kaptcha(self):
        """Проверяет наличие капчи на странице."""
        self.try_to_switch_to_central_frame()
        kaptcha = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'img[src="/inner/img/bc.php"]'
                )
        if kaptcha:
            if self.bot is None:
                print('Обнаружена капча!')
            else:
                self.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text='Обнаружена капча!'
                )
            sleep(30)
        # self.driver.refresh()
        # self.driver.execute_script("window.location.reload();")
        self.driver.switch_to.default_content()

    def glade_farm(
            self,
            price_dict: dict = FIELD_PRICES,
            slots=2,
            spell=1):
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
                            print(res_price)
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
                self.check_kaptcha()
            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=True
                )
                # sleep(2)
                # self.driver.refresh()
                # self.driver.execute_script("window.location.reload();")
                self.driver.switch_to.default_content()

    def one_spell_farm(self, slots=2, spell=1, with_move=False):
        """Фарм с проведением боя одним заклом."""
        self.start_event()
        while self.event.is_set() is True:
            # sleep(1)
            try:
                self.try_to_switch_to_central_frame()
                hits = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'img[onclick="touchFight();"]')
                if hits:
                    self.one_spell_fight(
                        slots=slots, spell=spell)
                else:
                    if with_move:
                        move = random.choice([Keys.DOWN, Keys.UP])
                        ActionChains(self.driver).send_keys(move).perform()
                self.play_with_poetry_spirit()
                self.play_with_gamble_spirit()
                self.play_with_mind_spirit()

                self.choises.clear()
                self.check_kaptcha()
                self.chech_health()
                sleep(0.5)

            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=True
                )
                # sleep(2)
                self.driver.switch_to.default_content()

    def start_event(self):
        """Ставит флаг запуска циклов в положение True."""
        self.event.set()

    def stop_event(self):
        """Ставит флаг запуска циклов в положение False."""
        self.event.clear()

    def chech_health(self):
        self.driver.switch_to.default_content()
        health = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'span[id="m_hpc"]'
                )
        if health:
            hp = int(health[0].text)
            if hp < 10000:
                sleep(10)

        else:
            print('Здоровье не найдено.')