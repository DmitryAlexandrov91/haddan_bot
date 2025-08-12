from time import sleep
from typing import Optional

from config import configure_logging
from constants import (
    BEETS_TIMEOUT,
    Slot,
    SlotsPage,
)
from selenium.common.exceptions import (
    InvalidSessionIdException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .common_driver import HaddanCommonDriver

configure_logging()


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
            if spell_to_cast != active_spell:
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

        if self.check_for_fight() is False:
            return

        current_round = self.get_round_number()
        kick = self.get_hit_number()

        if not kick:
            self.try_to_come_back_from_fight()
            self.send_info_message(
                text='Бой завершён',
            )
            return

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
            if self.check_for_fight() is False:
                return

            self.open_slot_and_choise_spell(
                slots_page=default_slot,
                slot=default_spell)

        self.try_to_switch_to_central_frame()

        come_back = self.driver.find_elements(
                    By.PARTIAL_LINK_TEXT, 'Вернуться')
        if come_back:
            come_back[0].click()

        if self.check_for_fight() is False:
            return

        try:

            element = self.driver.execute_script(
                '''
                touchFight();
                return document.activeElement;
                ''',
            )
            sleep(BEETS_TIMEOUT)
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

            if not self.check_for_fight:
                return

            self.fight(
                spell_book=spell_book,
                default_slot=default_slot,
                default_spell=default_spell)

        except Exception as e:
            self.actions_after_exception(e)
