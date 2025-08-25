"""Кд упраления игры с духами в лабиринте."""
import random

from constants import (
    GAMBLE_SPIRIT_RIGHT_ANSWERS,
    POETRY_SPIRIT_RIGHT_ANSWERS,
    NPCImgTags,
)
from loguru import logger
from selenium.common.exceptions import (
    InvalidSessionIdException,
)
from selenium.webdriver.common.by import By
from utils import (
    get_intimidation_and_next_room,
)

from .fight_driver import HaddanFightDriver


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

        self.try_to_switch_to_central_frame()

        gamble_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.gamble_spirit,
                    )

        if not gamble_spirit:
            return

        try:

            gamble_spirit[0].click()
            # sleep(1)

            logger.info('Играем с духом азарта.')
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
                    # sleep(0.5)
                    continue

                self.right_answers_choise(GAMBLE_SPIRIT_RIGHT_ANSWERS)

                spirit_answers = self.driver.find_elements(
                    By.CLASS_NAME,
                    'talksayTak',
                )
                # sleep(0.5)

        except Exception as e:
            logger.error(
                'При игре с духом азарта возникла ошибка: ',
                str(e),
            )

            self.play_with_gamble_spirit()

    def play_with_poetry_spirit(self) -> None:
        """Игра с духом поэзии."""
        if not self.driver:
            raise

        self.try_to_switch_to_central_frame()

        poetry_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.poetry_spirit)
        if not poetry_spirit:
            return

        try:
            poetry_spirit[0].click()
            # sleep(1)

            self.send_info_message(
                text='Пойманы духом поэзии',
            )
            logger.info('Играем с духом поэзии.')
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
                # sleep(0.5)
        except Exception as e:
            logger.error(
                'При игре с духом поэзии возникла ошибка: ',
                str(e),
            )

            self.play_with_poetry_spirit()

    def play_with_mind_spirit(self) -> None:
        """Игра с духом ума."""
        if not self.driver:
            raise InvalidSessionIdException

        self.try_to_switch_to_central_frame()

        mind_spirit = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        NPCImgTags.mind_spirit,
                    )

        if not mind_spirit:
            return

        try:
            mind_spirit[0].click()
            # sleep(0.5)

            logger.info('Играем с духом ума')
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
                # sleep(0.5)

        except Exception as e:
            logger.error(
                'При игре с духом ума возникла ошибка: ',
                str(e),
            )
            self.play_with_mind_spirit()
