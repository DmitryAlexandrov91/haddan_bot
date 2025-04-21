"""Основные функции прохождения лабиринта."""
import re
import tempfile
from collections import deque
from time import sleep
from typing import List, Optional, Tuple

from constants import LABIRINT_MAP_URL, Floor, Room
from selenium.webdriver.common.by import By


def text_delimetr(text: str) -> Optional[tuple[int, str]]:
    expr = r'^(\d+)([\s\S]+)'
    match = re.match(expr, text)

    if match:
        number_part = int(match.group(1))
        rest_part = match.group(2)

        return number_part, rest_part


def get_labirint_map(
        url: str,
        floor: Floor,
        manager) -> list[Room]:
    lab_url = url + floor

    manager.driver.set_page_load_timeout(30)
    manager.driver.set_script_timeout(30)

    manager.driver.get(lab_url)

    sleep(1)

    map_table = manager.driver.find_elements(
        By.CLASS_NAME, 'maze-map__content')

    sleep(1)

    if map_table:
        rows = map_table[0].find_elements(By.TAG_NAME, 'tr')

        labirint_map = []

        for row in rows:
            rooms_in_row = row.find_elements(By.TAG_NAME, 'td')
            line = []

            for room in rooms_in_row:
                # Получаем текст и атрибуты комнаты
                text = room.text.strip()
                gif_path = room.get_attribute('background')
                gif_name = gif_path.split('/')[-1][:4]
                north, south, west, east = gif_name

                if len(text) <= 3:
                    line.append(
                        Room(
                            number=int(text),
                            north=bool(int(north)),
                            south=bool(int(south)),
                            west=bool(int(west)),
                            east=bool(int(east))
                        )
                    )
                else:
                    room_number, rest_part = text_delimetr(text)
                    line.append(
                        Room(
                            number=room_number,
                            box_outer='портал' not in rest_part,
                            box_item=rest_part,
                            north=bool(int(north)),
                            south=bool(int(south)),
                            west=bool(int(west)),
                            east=bool(int(east))
                        )
                    )
            labirint_map.append(line)

    return labirint_map


def find_room_position(
        labirint_map: List[List[Room]],
        room_number: int) -> Optional[Tuple[int, int]]:
    """Находит координаты комнаты по номеру"""
    for i, row in enumerate(labirint_map):
        for j, room in enumerate(row):
            if room.number == room_number:
                return (i, j)
    return None


def get_neighbors(
        labirint_map: List[List[Room]],
        pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Возвращает соседние комнаты, в которые можно перейти"""
    i, j = pos
    room = labirint_map[i][j]
    neighbors = []

    if room.north and i > 0 and labirint_map[i-1][j].south:
        neighbors.append((i-1, j))
    if room.south and i < len(labirint_map)-1 and labirint_map[i+1][j].north:
        neighbors.append((i+1, j))
    if room.west and j > 0 and labirint_map[i][j-1].east:
        neighbors.append((i, j-1))
    if room.east and j < len(labirint_map[0])-1 and labirint_map[i][j+1].west:
        neighbors.append((i, j+1))

    return neighbors


def find_shortest_path(
        labirint_map: List[List[Room]],
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """BFS: поиск кратчайшего пути между двумя точками.

    (возвращает координаты)
    """
    queue = deque([start_pos])
    visited = {start_pos: None}

    while queue:
        current = queue.popleft()
        if current == end_pos:
            break

        for neighbor in get_neighbors(labirint_map, current):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)
    else:
        return None

    path = []
    current = end_pos
    while current != start_pos:
        path.append(current)
        current = visited[current]
    path.append(start_pos)
    path.reverse()

    return path


def get_direction(
        current_pos: Tuple[int, int],
        next_pos: Tuple[int, int]) -> str:
    """Определяет направление движения между двумя точками"""
    ci, cj = current_pos
    ni, nj = next_pos

    if ni == ci - 1 and nj == cj:
        return "север"
    elif ni == ci + 1 and nj == cj:
        return "юг"
    elif ni == ci and nj == cj - 1:
        return "запад"
    elif ni == ci and nj == cj + 1:
        return "восток"
    else:
        raise ValueError("Невозможно определить направление")


def convert_path_to_directions(
        labirint_map: List[List[Room]],
        path_coords: List[Tuple[int, int]]) -> List[str]:
    """Преобразует путь в координатах в список направлений"""
    directions = []
    for i in range(len(path_coords) - 1):
        current = path_coords[i]
        next_pos = path_coords[i + 1]
        direction = get_direction(current, next_pos)
        directions.append(direction)
    return directions


def find_path_with_directions(
    labirint_map: List[List[Room]],
    start_room: int,
    end_room: int
) -> Optional[List[str]]:
    """Находит путь и возвращает направления (например, ['юг', 'восток'])"""
    start_pos = find_room_position(labirint_map, start_room)
    end_pos = find_room_position(labirint_map, end_room)

    if not start_pos or not end_pos:
        return None

    path_coords = find_shortest_path(labirint_map, start_pos, end_pos)
    if not path_coords:
        return None

    return convert_path_to_directions(labirint_map, path_coords)


def find_path_via_boxes_with_directions(
    labirint_map: List[List[Room]],
    start_room: int,
    target_room: int
) -> Optional[List[str]]:
    """
    Возвращает направления для пути:
    1) Через все комнаты с box_outer=True,
    2) С завершением в target_room.
    """
    boxes = [
        (i, j)
        for i, row in enumerate(labirint_map)
        for j, room in enumerate(row)
        if room.box_outer
    ]

    start_pos = find_room_position(labirint_map, start_room)
    target_pos = find_room_position(labirint_map, target_room)

    if not start_pos or not target_pos:
        return None

    full_path_coords = []
    current_pos = start_pos

    # Проходим через все коробки
    remaining_boxes = set(boxes)
    while remaining_boxes:
        nearest_box = None
        shortest_path = None

        for box in remaining_boxes:
            path = find_shortest_path(labirint_map, current_pos, box)
            if path and (
                shortest_path is None or len(path) < len(shortest_path)
            ):
                shortest_path = path
                nearest_box = box

        if not nearest_box:
            return None

        full_path_coords.extend(shortest_path[1:])  # Исключаем текущую позицию
        current_pos = nearest_box
        remaining_boxes.remove(nearest_box)

    # Идём в целевую комнату
    if current_pos != target_pos:
        path_to_target = find_shortest_path(
            labirint_map,
            current_pos,
            target_pos
        )
        if not path_to_target:
            return None
        full_path_coords.extend(path_to_target[1:])

    # Преобразуем координаты в направления
    full_path_coords = [start_pos] + full_path_coords
    return convert_path_to_directions(labirint_map, full_path_coords)


def get_floor_map(
        floor: Floor,
        manager) -> list[list[Room]]:
    manager.options.add_argument('--headless')
    temp_directory = tempfile.mkdtemp()
    manager.options.add_argument(f'--user-data-dir={temp_directory}')
    manager.start_driver()

    labirint_map = get_labirint_map(
        url=LABIRINT_MAP_URL,
        floor=floor,
        manager=manager)

    return labirint_map
