import os

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

# Константы логгера
LOGS_DIR_PATH = os.path.join(BASE_DIR, 'logs')
LOG_FILE_NAME = 'haddan.log'
LOG_FILE_PATH = os.path.join(LOGS_DIR_PATH, LOG_FILE_NAME)
MAX_LOG_SIZE = 10 ** 6
MAX_LOGS_COUNT = 5
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

# константы адресов.
HADDAN_MAIN_URL = 'https://haddan.ru/'
HADDAN_RESERVE_URL = 'https://www.online-igra.ru/'
MEDITATION_URL = 'https://haddan.ru/room/func/temple.php'
KAPCHA_URL = 'https://haddan.ru/inner/img/gc.php'
SHOP_URL = 'http://ordenpegasa.ru/shop/'
LABIRINT_MAP_URL = 'https://haddan.novikovproject.ru/maze?level=1'

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
    'Подсолнух': 14,
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
