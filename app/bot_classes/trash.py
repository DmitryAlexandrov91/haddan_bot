# Мусорка. Недоделки говноделки, которые жалко удалять полностью.

def fight_with_multicast(
        self,
        main_fight_slot=2, main_fight_spell=1,
        treatment_slot=4, treatment_spell=1,
        fight_slot_2=2, fight_spell_2=2,
        fight_slot_3=2, fight_spell_3=3,
        fight_slot_4=2, fight_spell_4=4,
        fight_slot_5=2, fight_spell_5=6,
        additional_spells=False):
    user_casts = [
        main_fight_spell, fight_spell_2,
        fight_spell_3, fight_spell_4, fight_spell_5
    ]

    if self.choises.get('treatment', False) is False:
        self.open_slot_and_choise_spell(
            slots_number=treatment_slot,
            spell_number=treatment_spell
        )
        self.choises['treatment'] = True

    if additional_spells:
        self.open_slot_and_choise_spell(
            slots_number=main_fight_slot,
            spell_number=random.choice(user_casts)
        )

    choise = self.choises.get('choised', False)
    if not choise:
        self.open_slot_and_choise_spell(
            slots_number=main_fight_slot,
            spell_number=main_fight_spell
        )
        self.choises['choised'] = True

    sleep(0.5)
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
            # self.wait_while_element_will_be_clickable(
            #     hits[0]
            # )
            hits[0].click()
            sleep(0.5)
            self.fight_with_multicast(
                main_fight_slot=main_fight_slot,
                main_fight_spell=main_fight_spell,
                treatment_slot=treatment_slot,
                treatment_spell=treatment_spell,
                fight_slot_2=fight_slot_2, fight_spell_2=fight_spell_2,
                fight_slot_3=fight_slot_3, fight_spell_3=fight_spell_3,
                fight_slot_4=fight_slot_4, fight_spell_4=fight_spell_4,
                fight_slot_5=fight_slot_5, fight_spell_5=fight_spell_5
            )

def heavy_farm(
        self,
        main_fight_slot=2, main_fight_spell=1,
        treatment_slot=4, treatment_spell=1,
        fight_slot_2=2, fight_spell_2=2,
        fight_slot_3=2, fight_spell_3=3,
        fight_slot_4=2, fight_spell_4=4,
        fight_slot_5=2, fight_spell_5=6,
        up_down_move=False, left_right_move=False,
        mind_spirit_play=True, additional_spells=False,
        min_hp=10000):
    """Фарм с отхилом и доп ударами."""
    while self.event.is_set() is True:
        try:
            self.check_error_on_page()
            self.try_to_switch_to_central_frame()
            hits = self.driver.find_elements(
                By.CSS_SELECTOR,
                'img[onclick="touchFight();"]')
            if hits:
                self.fight_with_multicast(
                    main_fight_slot=main_fight_slot,
                    main_fight_spell=main_fight_spell,
                    treatment_slot=treatment_slot,
                    treatment_spell=treatment_spell,
                    fight_slot_2=fight_slot_2, fight_spell_2=fight_spell_2,
                    fight_slot_3=fight_slot_3, fight_spell_3=fight_spell_3,
                    fight_slot_4=fight_slot_4, fight_spell_4=fight_spell_4,
                    fight_slot_5=fight_slot_5, fight_spell_5=fight_spell_5,
                    additional_spells=additional_spells)
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
                    self.bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text='Обнаружен дух ума!'
                    )
                    sleep(30)

            self.choises.clear()
            hp = self.check_health()
            if hp is not None and hp < min_hp:
                print(f'Здоровье меньше {min_hp}, спим 10 секунд.')
                sleep(10)

            sleep(0.5)

        except Exception as e:
            configure_logging()
            logging.exception(
                f'\nВозникло исключение {str(e)}\n',
                stack_info=True
            )
            sleep(2)
            self.driver.switch_to.default_content()