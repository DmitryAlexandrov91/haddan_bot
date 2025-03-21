"""Приложение haddan."""
import ctypes
import os
import threading
import tkinter as tk
from PIL import Image, ImageTk

from bot_classes import DriverManager, HaddanBot
from constants import FIELD_PRICES
from utils import get_glade_price_list

manager = DriverManager()
manager.options.add_argument('--start-maximized')
profile_dir = os.path.join(os.getcwd(), 'haddan_tk_profile')
os.makedirs(profile_dir, exist_ok=True)
manager.options.add_argument(f"user-data-dir={profile_dir}")
manager.options.add_experimental_option(
    "excludeSwitches", ["enable-automation"]
)
manager.options.add_experimental_option('useAutomationExtension', False)

GLADE_PRICES = FIELD_PRICES.copy()


def is_ru_lang_keyboard():
    """Функция для буфера обмена на англ. языке."""
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    return hex(pf(0)) == '0x4190419'


def keys(event):
    """Функция для буфера обмена на англ. языке."""
    if is_ru_lang_keyboard():
        if event.keycode == 86:
            event.widget.event_generate("<<Paste>>")
        elif event.keycode == 67:
            event.widget.event_generate("<<Copy>>")
        elif event.keycode == 88:
            event.widget.event_generate("<<Cut>>")
        elif event.keycode == 65535:
            event.widget.event_generate("<<Clear>>")
        elif event.keycode == 65:
            event.widget.event_generate("<<SelectAll>>")


app = tk.Tk()
app.title("Собиратель трав v1.0")
app.bind("<Control-KeyPress>", keys)
app.configure(bg='#FFF4DC')
img = Image.open('icon.ico')
photo = ImageTk.PhotoImage(img)

app.iconphoto(True, photo)


def tk_glade_farm():

    char = username_field.get().strip()
    password = password_field.get().strip()

    if char and password:
        manager.start_driver()
        User = HaddanBot(
            char=char,
            password=password,
            driver=manager.driver)
        User.login_to_game()

        manager.glade_farm(
            price_dict=GLADE_PRICES)


def start_thread():
    manager.thread = threading.Thread(target=tk_glade_farm)
    manager.thread.start()


def stop_farm():
    manager.close_driver()


# Панель запуска фарма поляны
glade__farm_lable = tk.Label(
    app,
    text='Фарм поляны.',
    bg='#FFF4DC')
glade__farm_lable.grid(row=0, column=0)

glade__farm_lable_2 = tk.Label(
    app,
    text='Введите имя и пароль от персонажа и нажмите ->',
    bg='#FFF4DC')
glade__farm_lable_2.grid(row=0, column=1)

username_label = tk.Label(app, text='имя', bg='#FFF4DC')
username_label.grid(row=1, column=0)

username_field = tk.Entry(app, width=30)
username_field.grid(row=1, column=1)


password_label = tk.Label(app, text='пароль', bg='#FFF4DC')
password_label.grid(row=2, column=0)

password_field = tk.Entry(app, width=30)
password_field.grid(row=2, column=1)

# Блок Цены ресурсов

res_price_label = tk.Label(
    app,
    text='Цена ресурсов:', bg='#FFF4DC'
)
res_price_label.grid(row=3, column=1)

price_dict_content = '\n'.join(
    f'{key}: {value}' for key, value in GLADE_PRICES.items())
price_label = tk.Label(app, text=price_dict_content, bg='#FFF4DC')
price_label.grid(row=4, column=1)


# Блок изменения цены ресурсов.
def label_update():
    price_dict_content = '\n'.join(
        f'{key}: {value}' for key, value in GLADE_PRICES.items())
    price_label['label'] = price_dict_content


def price_change(label, field):
    new_price = field.get().strip()
    if new_price:
        GLADE_PRICES[label['text']] = int(new_price)
        update_price_label()  # Обновляем лейбл с ценами


def update_price_label():
    global price_label
    price_dict_content = '\n'.join(
        f'{key}: {value}' for key, value in GLADE_PRICES.items()
    )
    price_label.config(text=price_dict_content)


# Мухожор
muhozhor_label = tk.Label(
    text='Мухожор',
    bg='#FFF4DC'
)
muhozhor_label.grid(row=5, column=0)

muhozhor_field = tk.Entry(
    app, width=5
)
muhozhor_field.grid(row=5, column=1)

muhozhor_button = tk.Button(
    app,
    text='изменить',
    width=9,
    bg='#FFF4DC',
    command=lambda: price_change(muhozhor_label, muhozhor_field)
    )
muhozhor_button.grid(row=5, column=2)

# Подсолнух
podsolnuh_label = tk.Label(
    text='Подсолнух',
    bg='#FFF4DC'
)
podsolnuh_label.grid(row=6, column=0)

podsolnuh_field = tk.Entry(
    app, width=5
)
podsolnuh_field.grid(row=6, column=1)

podsolnuh_button = tk.Button(
    app,
    text='изменить',
    width=9,
    bg='#FFF4DC',
    command=lambda: price_change(podsolnuh_label, podsolnuh_field)
    )
podsolnuh_button.grid(row=6, column=2)

# Капустница
kapusta_label = tk.Label(
    text='Капустница',
    bg='#FFF4DC'
)
kapusta_label.grid(row=7, column=0)

kapusta_field = tk.Entry(
    app, width=5
)
kapusta_field.grid(row=7, column=1)

kapusta_button = tk.Button(
    app,
    text='изменить',
    width=9,
    bg='#FFF4DC',
    command=lambda: price_change(kapusta_label, kapusta_field)
    )
kapusta_button.grid(row=7, column=2)


# Мандрагора
mandragora_label = tk.Label(
    text='Мандрагора',
    bg='#FFF4DC'
)
mandragora_label.grid(row=8, column=0)

mandragora_field = tk.Entry(
    app, width=5
)
mandragora_field.grid(row=8, column=1)

mandragora_button = tk.Button(
    app,
    text='изменить',
    width=9,
    bg='#FFF4DC',
    command=lambda: price_change(mandragora_label, mandragora_field)
    )
mandragora_button.grid(row=8, column=2)

# Зеленая Массивка
green_mass_label = tk.Label(
    text='Зеленая массивка',
    bg='#FFF4DC'
)
green_mass_label.grid(row=9, column=0)

green_mass_field = tk.Entry(
    app, width=5
)
green_mass_field.grid(row=9, column=1)

green_mass_button = tk.Button(
    app,
    text='изменить',
    width=9,
    bg='#FFF4DC',
    command=lambda: price_change(green_mass_label, green_mass_field)
    )
green_mass_button.grid(row=9, column=2)

# Колючник Черный
koluchka_label = tk.Label(
    text='Колючник Черный',
    bg='#FFF4DC'
)
koluchka_label.grid(row=10, column=0)

koluchka_field = tk.Entry(
    app, width=5
)
koluchka_field.grid(row=10, column=1)

koluchka_button = tk.Button(
    app,
    text='изменить',
    width=9,
    bg='#FFF4DC',
    command=lambda: price_change(koluchka_label, koluchka_field)
    )
koluchka_button.grid(row=10, column=2)

# Гертаниум
gertanium_label = tk.Label(
    text='Гертаниум',
    bg='#FFF4DC'
)
gertanium_label.grid(row=11, column=0)

gertanium_field = tk.Entry(
    app, width=5
)
gertanium_field.grid(row=11, column=1)

gertanium_button = tk.Button(
    app,
    text='изменить',
    width=9,
    bg='#FFF4DC',
    command=lambda: price_change(gertanium_label, gertanium_field)
    )
gertanium_button.grid(row=11, column=2)


# Кнопки управления фармом поляны.

glade_farm_start_buttton = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_thread
    )
glade_farm_start_buttton.grid(
    row=0, column=2
)

glade_farm_stop_buttton = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_farm
    )
glade_farm_stop_buttton.grid(
    row=2, column=2
)


# Информационный блок


def glade_farm_txt_open():
    os.startfile('glade_farm.txt')


statistic_button = tk.Button(
    app,
    text='лог подбора трав',
    width=15,
    bg='#FFF4DC',
    command=glade_farm_txt_open
)
statistic_button.grid(
    row=12, column=1
)


def update_price_from_search():
    global price_label
    global GLADE_PRICES
    manager = DriverManager()
    GLADE_PRICES = get_glade_price_list(manager)
    price_dict_content = '\n'.join(
        f'{key}: {value}' for key, value in GLADE_PRICES.items()
    )
    price_label.config(text=price_dict_content)
    manager.close_driver()


def start_price_update(manager):
    manager.thread = threading.Thread(target=update_price_from_search)
    manager.thread.start()


sync_button = tk.Button(
    app,
    text='синхра цен с поисковиком',
    width=20,
    bg='#FFF4DC',
    command=lambda: start_price_update(manager)
)
sync_button.grid(
    row=3, column=0
)


if __name__ == '__main__':
    app.mainloop()
