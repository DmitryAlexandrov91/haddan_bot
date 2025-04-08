"""Цены ресурсов поляны."""
import gc
import threading
import tkinter as tk
import logging


from bot_classes import DriverManager
from constants import FIELD_PRICES
from tk_app.core import app
from utils import get_glade_price_list
from configs import configure_logging

GLADE_PRICES = FIELD_PRICES.copy()


res_price_label = tk.Label(
    app,
    text='Цена ресурсов:', bg='#FFF4DC'
)
res_price_label.grid(
    row=3,
    column=1)

price_dict_content = '\n'.join(
    f'{key}: {value}' for key, value in GLADE_PRICES.items())
price_label = tk.Label(app, text=price_dict_content, bg='#FFF4DC')
price_label.grid(row=4, column=1, columnspan=1, rowspan=5)


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


def update_price_from_search():
    try:
        global price_label
        global GLADE_PRICES
        manager = DriverManager()
        GLADE_PRICES = get_glade_price_list(manager)
        price_dict_content = '\n'.join(
            f'{key}: {value}' for key, value in GLADE_PRICES.items()
        )
        price_label.config(text=price_dict_content)
        manager.close_driver()
        sync_button.configure(foreground='black')
        gc.collect()
    except Exception as e:
        configure_logging()
        logging.exception(
            f'\nВозникло исключение {str(e)}\n',
            stack_info=True
        )


def start_price_update():
    sync_button.configure(foreground='green')
    new_thread = threading.Thread(target=update_price_from_search)
    new_thread.start()


sync_button = tk.Button(
    app,
    text='синхра цен с поисковиком',
    width=22,
    bg='#FFF4DC',
    command=lambda: start_price_update()
)
sync_button.grid(
    row=3, column=0
)

# Мухожор
muhozhor_label = tk.Label(
    text='Мухожор',
    bg='#FFF4DC'
)
muhozhor_label.grid(row=4, column=0, sticky='w')

muhozhor_field = tk.Entry(
    app, width=5
)
muhozhor_field.grid(row=4, column=0, sticky='e')

muhozhor_button = tk.Button(
    app,
    text='изменить',
    width=7,
    bg='#FFF4DC',
    command=lambda: price_change(muhozhor_label, muhozhor_field)
    )
muhozhor_button.grid(row=4, column=2)

# Подсолнух
podsolnuh_label = tk.Label(
    text='Подсолнух',
    bg='#FFF4DC'
)
podsolnuh_label.grid(row=5, column=0, sticky='w')

podsolnuh_field = tk.Entry(
    app, width=5
)
podsolnuh_field.grid(row=5, column=0, sticky='e')

podsolnuh_button = tk.Button(
    app,
    text='изменить',
    width=7,
    bg='#FFF4DC',
    command=lambda: price_change(podsolnuh_label, podsolnuh_field)
    )
podsolnuh_button.grid(row=5, column=2)

# Капустница
kapusta_label = tk.Label(
    text='Капустница',
    bg='#FFF4DC'
)
kapusta_label.grid(row=6, column=0, sticky='w')

kapusta_field = tk.Entry(
    app, width=5
)
kapusta_field.grid(row=6, column=0, sticky='e')

kapusta_button = tk.Button(
    app,
    text='изменить',
    width=7,
    bg='#FFF4DC',
    command=lambda: price_change(kapusta_label, kapusta_field)
    )
kapusta_button.grid(row=6, column=2)


# Мандрагора
mandragora_label = tk.Label(
    text='Мандрагора',
    bg='#FFF4DC'
)
mandragora_label.grid(row=8, column=0, sticky='w')

mandragora_field = tk.Entry(
    app, width=5
)
mandragora_field.grid(row=8, column=0, sticky='e')

mandragora_button = tk.Button(
    app,
    text='изменить',
    width=7,
    bg='#FFF4DC',
    command=lambda: price_change(mandragora_label, mandragora_field)
    )
mandragora_button.grid(row=8, column=2)

# Зеленая Массивка
green_mass_label = tk.Label(
    text='Зеленая массивка',
    bg='#FFF4DC'
)
green_mass_label.grid(row=9, column=0, sticky='w')

green_mass_field = tk.Entry(
    app, width=5
)
green_mass_field.grid(row=9, column=0, sticky='e')

green_mass_button = tk.Button(
    app,
    text='изменить',
    width=7,
    bg='#FFF4DC',
    command=lambda: price_change(green_mass_label, green_mass_field)
    )
green_mass_button.grid(row=9, column=2)

# Колючник Черный
koluchka_label = tk.Label(
    text='Колючник Черный',
    bg='#FFF4DC'
)
koluchka_label.grid(row=10, column=0, sticky='w')

koluchka_field = tk.Entry(
    app, width=5
)
koluchka_field.grid(row=10, column=0, sticky='e')

koluchka_button = tk.Button(
    app,
    text='изменить',
    width=7,
    bg='#FFF4DC',
    command=lambda: price_change(koluchka_label, koluchka_field)
    )
koluchka_button.grid(row=10, column=2)

# Гертаниум
gertanium_label = tk.Label(
    text='Гертаниум',
    bg='#FFF4DC'
)
gertanium_label.grid(row=11, column=0, sticky='w')

gertanium_field = tk.Entry(
    app, width=5
)
gertanium_field.grid(row=11, column=0, sticky='e')

gertanium_button = tk.Button(
    app,
    text='изменить',
    width=7,
    bg='#FFF4DC',
    command=lambda: price_change(gertanium_label, gertanium_field)
    )
gertanium_button.grid(row=11, column=2)
