import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


# Константы для директорий/путей.
BASE_DIR = os.getcwd()
DOWNLOADS_DIR_NAME = os.path.join(BASE_DIR, 'temp')
KAPCHA_NAME = 'kapcha.png'
SCREENSHOT_NAME = 'screenshot.png'
PAGE_SOURCE_NAME = 'page_source.html'
GLADE_FARM_LOG = 'glade_farm.txt'
KAPCHA_PATH = os.path.join(DOWNLOADS_DIR_NAME, KAPCHA_NAME)
PAGE_SOURCE_PATH = os.path.join(DOWNLOADS_DIR_NAME, PAGE_SOURCE_NAME)
SCREENSHOT_PATH = os.path.join(DOWNLOADS_DIR_NAME, SCREENSHOT_NAME)
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# Константы логгера
LOGS_DIR_PATH = os.path.join(BASE_DIR, 'logs')
LOG_FILE_NAME = 'haddan.log'
LOG_FILE_PATH = os.path.join(LOGS_DIR_PATH, LOG_FILE_NAME)
MAX_LOG_SIZE = 10 ** 6
MAX_LOGS_COUNT = 3
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

# константы адресов.
HADDAN_MAIN_URL = 'https://haddan.ru/'
HADDAN_RESERVE_URL = 'https://www.online-igra.ru/'
MEDITATION_URL = 'https://haddan.ru/room/func/temple.php'
KAPCHA_URL = 'https://haddan.ru/inner/img/gc.php'
SHOP_URL = 'http://ordenpegasa.ru/shop/'
LABIRINT_MAP_URL = 'https://haddan.novikovproject.ru/maze?level='


# Переменные окружения.
FIRST_CHAR = os.getenv('FIRST_CHAR', None)
SECOND_CHAR = os.getenv('SECOND_CHAR', None)
PASSWORD = os.getenv('HADDAN_PASSWORD', None)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Заказные данные
USER_CHAR = 'фантазёрка'
USER_PASSWORD = 'пароль игрока'
USER_CHAR_ID = 'тг id игрока'

# Остальное.
PAUSE_DURATION_SECONDS = 50
TIME_FORMAT = '%d.%m.%Y %H:%M:%S'
MIN_HP_VALUE = 10000

# Цена ресурсов поляны
FIELD_PRICES = {
    'Мухожор': 8,
    'Подсолнух': 15,
    'Капустница': 27,
    'Мандрагора': 60,
    'Зеленая массивка': 67,
    'Колючник Черный': 101,
    'Гертаниум': 190
    }

# Список для парсинга 'http://ordenpegasa.ru/shop/'
RES_LIST = ['Мухожор', 'Подсолнух', 'Капустница', 'Мандрагора',
            'Зеленая массивка', 'Колючник черный', 'Гертаниум']

#  Константы для проведения боя
WINDOWS_PROFILE_DIR = 'hd_windows_profile'
LINUX_PROFILE_DIR = 'hd_linux_profile'


POETRY_SPIRIT_RIGHT_ANSWERS = (
    'давай дальше', ' / ', 'Начали!', 'Дальше!', 'пора обратно',
    'с наградой', 'Телепортироваться', 'Увечье нам не надо', 'Поехали!'
)

GAMBLE_SPIRIT_RIGHT_ANSWERS = (
    'Телепортироваться', 'делу давай!', ' / ', 'пошли'
)


#  Константы интерфейса Tkinter

SLOT_VALUES = ('1', '2', '3', '4', '5', '6', '7')


class SlotsPage(Enum):
    _0 = '1'
    _1 = '2'
    _2 = '3'
    _3 = '4'
    _4 = '5'
    _5 = '6'
    _6 = '7'

    def __str__(self):
        return self.value


class Slot(Enum):
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'

    def __str__(self):
        return self.value


class Floor(Enum):
    FIRST_FLOOR = '1'
    SECOND_FLOOR = '2'
    THIRD_FLOOR = '3'


class TkAlarmColors(Enum):
    APP = '#FFF4DC'
    RED = '#FF0000'
    GREEN = 'green'
    BLACK = 'black'


@dataclass
class Room:
    number: int
    box_outer: bool = False
    box_item: Optional[str] = None
    north: bool = False
    south: bool = False
    west: bool = False
    east: bool = False


DEFAULT_TK_ALARM = 'Бот готов к работе'
