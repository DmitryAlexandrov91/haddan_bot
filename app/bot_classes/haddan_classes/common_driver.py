"""Общие методы, независимые от интерфейса tkinter."""
import re
from time import sleep

from constants import (
    NPCImgTags,
)
from loguru import logger
from selenium.common.exceptions import (
    InvalidSessionIdException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bot_classes.driver_manager import DriverManager


class HaddanCommonDriver(DriverManager):
    """Класс управления фреймами и общие независимые от HaddanDriver методы."""

    def try_to_switch_to_central_frame(self) -> None:
        """Переключается на центральный фрейм окна."""
        if not self.driver:
            raise InvalidSessionIdException

        if self.driver.execute_script('return window.name;') != 'frmcentral':

            try:
                self.driver.switch_to.frame('frmcentral')

            except Exception:
                self.driver.switch_to.default_content()

    def try_to_switch_to_dialog(self) -> None:
        """Переключается на фрейм диалога."""
        if not self.driver:
            raise InvalidSessionIdException

        if self.driver.execute_script('return window.name;') != 'thedialog':

            try:
                self.driver.switch_to.frame('thedialog')

            except Exception:
                self.driver.switch_to.default_content()

    def try_to_switch_to_upper(self) -> None:
        """Переключается на фрейм upper с кнопкой выхода из игры."""
        if not self.driver:
            raise InvalidSessionIdException

        if self.driver.execute_script('return window.name;') != 'frmupper':

            try:
                self.driver.switch_to.frame("frmupper")

            except Exception:
                self.driver.switch_to.default_content()

    def find_all_iframes(self) -> None:
        """Выводит в терминал список всех iframe егов на странице."""
        if not self.driver:
            raise InvalidSessionIdException

        frames = self.driver.find_elements(By.TAG_NAME, 'iframe')
        if frames:
            logger.info([frame.get_attribute('name') for frame in frames])
        else:
            logger.info('iframe на странице не найдены')

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

    def wait_until_browser_test(self, time: int) -> None:
        """Ждёт time секунд пока идёт проверка браузера.

        По истечению времени ожидания перезагружает окно.
        """
        if not self.driver:
            raise InvalidSessionIdException

        if not self.cycle_is_running:
            exit()

        try:
            WebDriverWait(
                self.driver, timeout=time,
            ).until_not(
                ec.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(text(),"
                    "'Проверка браузера')]",
                    )),
            )
        except TimeoutException:
            logger.warning(
                'Игра зависла на проверке браузера при перелогине',
            )
            self.driver.refresh()

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
        if not self.driver:
            raise InvalidSessionIdException

        if isinstance(
            exception,
            (TimeoutException, StaleElementReferenceException),
        ):
            logger.error(
                f'Возникла ошибка - {exception.__class__.__name__}',
            )
        else:
            logger.exception(
                f'Возникла ошибка - {exception.__class__.__name__}',
                )

        self.check_for_slot_clear_alarm_message()

        try:

            self.driver.switch_to.default_content()
            self.errors_count += 1
            # logger.info(f'Текущее количество ошибок - {self.errors_count}')
            if self.errors_count >= 10:
                self.driver.refresh()
                logger.info('Перезагрузка страницы')
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
            logger.warning(
                'Обнаружено окно c вопросом очистить слот',
            )
            alarm_window[0].click()

        information_window = self.driver.find_elements(
            By.PARTIAL_LINK_TEXT, 'Выбрано недостаточно зон удара',
        )
        if information_window:
            logger.warning(
                    'Обнаружено окно с сообщением, что не выбрана зона удара',
                )
            window = self.driver.find_elements(
                By.CSS_SELECTOR,
                'input[id="talkModalButtonID_OK"]')
            if window:
                logger.debug(
                    'Найден тег input[id="talkModalButtonID_OK"]',
                )
                window[0].click()

        self.try_to_switch_to_central_frame()

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
                sleep(0.5)
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
