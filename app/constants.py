import os
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def get_bool_param_from_env(variable: str | bool) -> bool:
    if isinstance(variable, bool):
        return variable
    else:
        if variable.lower() == 'false':
            return False
        return True


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
HADDAN_URL = 'https://haddan.ru/'
HADDAN_RESERVE_URL = 'https://www.online-igra.ru/'
MEDITATION_URL = 'https://haddan.ru/room/func/temple.php'
KAPCHA_URL = 'https://haddan.ru/inner/img/gc.php'
SHOP_URL = 'http://ordenpegasa.ru/shop/'
LABIRINT_MAP_URL = 'https://haddan.novikovproject.ru/maze?level='
DOMENS = {
    'haddan': 'https://haddan.ru/',
    'online-igra': 'https://www.online-igra.ru/',
    'new.haddan': 'https://new.haddan.ru/',
    'ru.haddan': 'https://ru.haddan.ru/'
}


# Переменные окружения.
FIRST_CHAR = os.getenv('FIRST_CHAR', None)
SECOND_CHAR = os.getenv('SECOND_CHAR', None)
THIRD_CHAR = os.getenv('THIRD_CHAR', None)
PASSWORD = os.getenv('HADDAN_PASSWORD', None)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', None)
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', None)

CHARS = [
    FIRST_CHAR,
    SECOND_CHAR,
    THIRD_CHAR
]


# Заказные данные
USER_CHAR = 'фантазёрка'
USER_PASSWORD = 'пароль игрока'
USER_CHAR_ID = 'тг id игрока'

# Настройки программы.
PAUSE_DURATION_SECONDS = 50
TIME_FORMAT = '%d.%m.%Y %H:%M:%S'
MIN_HP_VALUE = os.getenv('MIN_HP_VALUE', 0)
LICH_ROOM = 76
MIND_SPIRIT_PLAY = get_bool_param_from_env(
    os.getenv('MIND_SPIRIT_PLAY', True))
CHEERFULNESS = get_bool_param_from_env(
    os.getenv('CHEERFULNESS', False))
DEFAULT_SLOTS_PAGE = os.getenv('DEFAULT_SLOTS_PAGE', '2')
DEFAULT_SLOT = os.getenv('DEFAULT_SLOT', '1')
DEFAULT_CHEERFULNESS_SLOTS_PAGE = os.getenv(
    'DEFAULT_CHEERFULNESS_SLOTS_PAGE', '1'
)
DEFAULT_CHEERFULNESS_SLOT = os.getenv('DEFAULT_CHEERFULNESS_SLOT', '1')

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


POETRY_SPIRIT_RIGHT_ANSWERS = {
    'давай дальше', ' / ', 'Начали!', 'Дальше!', 'пора обратно',
    'с наградой', 'Телепортироваться', 'Увечье нам не надо', 'Поехали!'
}

GAMBLE_SPIRIT_RIGHT_ANSWERS = {
    'Телепортироваться', 'делу давай!', ' / ', 'пошли'
}


#  Константы интерфейса Tkinter

SLOT_VALUES = ('1', '2', '3', '4', '5', '6', '7', 'p')


class SlotsPage(StrEnum):
    _0 = '1'
    _1 = '2'
    _2 = '3'
    _3 = '4'
    _4 = '5'
    _5 = '6'
    _6 = '7'
    _p = 'p'

    def __str__(self):
        return self.value


class Slot(StrEnum):
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _p = 'p'

    def __str__(self):
        return self.value


class Floor(StrEnum):
    FIRST_FLOOR = '1'
    SECOND_FLOOR = '2'
    THIRD_FLOOR = '3'
    BABY_FIRST_FLOOR = '4'
    BABY_SECOND_FLOOR = '5'


class TkAlarmColors(StrEnum):
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


DEFAULT_TK_STATUS = 'Бот готов к работе'


CHARS_ACCESS = {
    'SwordS': '2033-06-28 23:59:59',
    'Nordman': '2033-06-27 23:59:59',
    'фантазёрка': '2033-06-27 23:59:59'
}

DT_FORMAT = '%Y-%m-%d %H:%M:%S'


#  Константы для парсинга Selenium


class Iframes(StrEnum):
    """Класс констант с именами фреймов."""
