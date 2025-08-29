from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Optional

# Константы для директорий/путей.

BASE_DIR = Path(__file__).resolve().parent.parent

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

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
    'ru.haddan': 'https://ru.haddan.ru/',
}

LICH_ROOM = 76

# Цена ресурсов поляны
FIELD_PRICES = {
    'Мухожор': 8,
    'Подсолнух': 15,
    'Капустница': 27,
    'Мандрагора': 60,
    'Зеленая массивка': 67,
    'Колючник Черный': 101,
    'Гертаниум': 190,
    }

# Список для парсинга 'http://ordenpegasa.ru/shop/'
RES_LIST = ['Мухожор', 'Подсолнух', 'Капустница', 'Мандрагора',
            'Зеленая массивка', 'Колючник черный', 'Гертаниум']

#  Константы для проведения боя
WINDOWS_PROFILE_DIR = 'hd_windows_profile'
LINUX_PROFILE_DIR = 'hd_linux_profile'


POETRY_SPIRIT_RIGHT_ANSWERS = {
    'давай дальше', ' / ', 'Начали!', 'Дальше!', 'пора обратно',
    'с наградой', 'Телепортироваться', 'Увечье нам не надо', 'Поехали!',
}

GAMBLE_SPIRIT_RIGHT_ANSWERS = {
    'Телепортироваться', 'делу давай!', ' / ', 'пошли',
}


#  Константы интерфейса Tkinter

SLOT_VALUES = ('1', '2', '3', '4', '5', '6', '7', 'p')


class SlotsPage(StrEnum):
    """Класс констант с номерами страниц слотов."""

    _0 = '1'
    _1 = '2'
    _2 = '3'
    _3 = '4'
    _4 = '5'
    _5 = '6'
    _6 = '7'
    _p = 'p'

    def __str__(self) -> str:
        return self.value


class Slot(StrEnum):
    """Класс констант с номерами быстрых слотов."""

    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _p = 'p'

    def __str__(self) -> str:
        return self.value


class Floor(StrEnum):
    """Класс констант с этажами лабиринта."""

    FIRST_FLOOR = '1'
    SECOND_FLOOR = '2'
    THIRD_FLOOR = '3'
    BABY_FIRST_FLOOR = '4'
    BABY_SECOND_FLOOR = '5'


class TkAlarmColors(StrEnum):
    """Класс констант с цветами приложения."""

    APP = '#FFF4DC'
    RED = '#FF0000'
    GREEN = 'green'
    BLACK = 'black'


@dataclass
class Room:
    """Класс комнаты лабиринта."""

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
    'фантазёрка': '2033-06-27 23:59:59',
    'выдра полевая': '2033-06-27 23:59:59',
    'sauron77': '2033-06-27 23:59:59',
    'Joker13': '2033-06-27 23:59:59',
    'Dark Messia': '2033-06-27 23:59:59',
    '-Смертник-': '2033-06-27 23:59:59',
}

DT_FORMAT = '%Y-%m-%d %H:%M:%S'


class NPCImgTags(StrEnum):
    """Класс констант с img тегами NPC."""

    gamble_spirit = 'img[id="roomnpc1850578"]'
    poetry_spirit = 'img[id="roomnpc1850579"]'
    mind_spirit = 'img[id="roomnpc1850577"]'
    distans_fairy = 'img[id="roomnpc231778"]'
    near_fairy = 'img[id="roomnpc17481"]'
    morning_dragon = 'img[id="roomnpc2460307"]'
    evening_dragon = 'img[id="roomnpc2337344"]'
    daily_dragon = 'img[id="roomnpc2460308"]'
    ancient_maze_city_portal_from_second_floor = 'img[id="roomnpc5038398"]'
    baby_maze_ciy_portal_from_first_floor = 'img[id="roomnpc5038442"]'
