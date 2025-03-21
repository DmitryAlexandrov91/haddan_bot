from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telebot import TeleBot, types
from webdriver_manager.chrome import ChromeDriverManager

from constants import (FIRST_CHAR, SECOND_CHAR,
                       TELEGRAM_BOT_TOKEN, PASSWORD)
from utils import (
    HaddanBot, save_url_content, send_photo, try_to_switch_to_central_frame)


from haddan_bot import glade_farm, kaptcha_find


bot = TeleBot(token=TELEGRAM_BOT_TOKEN)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_html = types.KeyboardButton('/html')
button_location = types.KeyboardButton('/screen')
button_field_farm = types.KeyboardButton('/field_farm')
keyboard.add(button_html)
keyboard.add(button_location)
keyboard.add(button_field_farm)

SwordS = HaddanBot(char=FIRST_CHAR, bot=bot, driver=driver)
Nordman = HaddanBot(char=SECOND_CHAR, bot=bot, driver=driver)


@bot.message_handler(commands=['1'])
def first_char_login_game(message):
    chat = message.chat
    chat_id = chat.id

    bot.send_message(
        chat_id=chat_id,
        text='Заходим в игру под главным персонажем.',
        reply_markup=keyboard,
    )
    SwordS.login_to_game(PASSWORD)
    kaptcha_find(driver, bot)



@bot.message_handler(commands=['2'])
def second_char_login_game(message):
    chat = message.chat
    chat_id = chat.id

    bot.send_message(
        chat_id=chat_id,
        text='Заходим в игру под инкой.',
        reply_markup=keyboard,
    )
    Nordman.login_to_game()
    kaptcha_find(driver, bot)


@bot.message_handler(commands=['html'])
def get_page_html(message):
    chat = message.chat
    chat_id = chat.id
    save_url_content(driver)
    bot.send_message(
            chat_id=chat_id,
            text='html код страницы сохранён',
            reply_markup=keyboard,
        )


@bot.message_handler(commands=['screen'])
def get_page_screenshot(message):
    chat = message.chat
    chat_id = chat.id
    driver.get_screenshot_as_file('screenshot.png')
    bot.send_message(
            chat_id=chat_id,
            text='Отправляю скрин экрана.',
            reply_markup=keyboard,
        )
    send_photo(bot, 'screenshot.png')


@bot.message_handler(commands=['field_farm'])
def field_farm(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(
            chat_id=chat_id,
            text='Начинаю фарм поляны.',
            reply_markup=keyboard,
        )
    glade_farm(driver, bot)


@bot.message_handler(content_types=['text'])
def kaptcha_handler(message):
    chat = message.chat
    chat_id = chat.id
    text = message.text
    try:
        try_to_switch_to_central_frame(driver)
        kaptcha_runes = driver.find_elements(
            By.CLASS_NAME,
            'captcha_rune'
        )

        for number in text:
            kaptcha_runes[int(number)].click()
            sleep(0.5)
        try_to_switch_to_central_frame(driver)
        buttons = driver.find_elements(
                        By.TAG_NAME, 'button')
        if buttons:
            buttons[1].click()

    except Exception:
        bot.send_message(
            chat_id=chat_id,
            text='Ошибка при вводе капчи, попробуйте ещё раз.',
            reply_markup=keyboard,
        )


def main():
    try:
        bot.polling()
    except Exception as e:
        print(f'Возникла ошибка {str(e)}')
        sleep(30)


if __name__ == '__main__':
    main()
