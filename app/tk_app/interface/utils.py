""""Методы интерфейса tkinter."""
import tkinter as tk


def label_packing(
        app: tk,
        elements_amount: int,
        row: int,
        column: int,
        sticky: str = 'c',
        horizon=False):
    """Метод размещения нескольких лейблов в окне приложения."""
    for element in range(elements_amount):
        widget = tk.Label(
            app,
            text=f'Р {element + 1} У {element + 1}',
            bg='#FFF4DC',
        )

        if not horizon:
            widget.grid(row=row + element, column=column)
        else:
            widget.grid(
                row=row,
                column=column + element,
                sticky=sticky,
            )
