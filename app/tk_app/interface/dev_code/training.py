"""Наработки по реализации функционала прохождения лабиринта."""
import re
from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup
from requests_html import HTMLSession


@dataclass
class Room:
    number: int
    box_outer: bool = False
    box_item: Optional[str] = None
    north: bool = False
    south: bool = False
    west: bool = False
    east: bool = False


def text_delimetr(text: str) -> Optional[tuple[int, str]]:
    expr = r'^(\d+)([\s\S]+)'
    match = re.match(expr, text)

    if match:
        number_part = int(match.group(1))
        rest_part = match.group(2)

        return number_part, rest_part


LAB_URL = 'https://haddan.novikovproject.ru/maze?level='


def get_labirint_map(
        session: HTMLSession,
        url: str,
        floor: str) -> list[Room]:
    parsed_url = url + floor
    response = session.get(parsed_url)
    response.html.render(sleep=3)
    soup = BeautifulSoup(response.html.html, 'lxml')
    map = soup.find(class_='maze-map__content')
    rows = map.find_all('tr')
    labirint_map = []

    for row in rows:
        rooms_in_row = row.find_all('td')

        line = []
        for room in rooms_in_row:
            text = room.text.strip()
            gif_path = room['background']
            gif_name = gif_path.split('/')[-1][:4]
            north, south, west, east = gif_name

            if len(text) <= 3:
                line.append(
                    Room(
                        number=int(text),
                        north=bool(int(north)),
                        south=bool(int(south)),
                        west=bool(int(west)),
                        east=bool(int(east)),
                    ),
                )
            else:
                room_number, rest_part = text_delimetr(text)
                line.append(
                    Room(
                        number=room_number,
                        box_outer=True if 'портал' not in rest_part else False,
                        box_item=rest_part,
                        north=bool(int(north)),
                        south=bool(int(south)),
                        west=bool(int(west)),
                        east=bool(int(east)),
                    ),
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
    """BFS: поиск кратчайшего пути между двумя точками

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


def get_outer_boxes(labirint_map: List[List[Room]]) -> List[Tuple[int, int]]:
    """Список координат всех комнат с box_outer=True"""
    return [
        (i, j)
        for i, row in enumerate(labirint_map)
        for j, room in enumerate(row)
        if room.box_outer
    ]


def find_path_via_boxes_to_target(
    labirint_map: List[List[Room]],
    start_room: int,
    target_room: int,
) -> Optional[List[int]]:
    """Находит путь, который:
    1) Начинается в start_room,
    2) Проходит через ВСЕ комнаты с box_outer=True,
    3) Заканчивается в target_room.
    """
    start_pos = find_room_position(labirint_map, start_room)
    target_pos = find_room_position(labirint_map, target_room)
    if not start_pos or not target_pos:
        return None

    boxes = get_outer_boxes(labirint_map)
    if not boxes:
        # Если нет коробок, просто ищем путь до target_room
        path_coords = find_shortest_path(labirint_map, start_pos, target_pos)
        return [
            labirint_map[i][j].number for (i, j) in path_coords
            ] if path_coords else None

    current_pos = start_pos
    remaining_boxes = set(boxes)
    full_path = [start_room]

    # Проходим через все коробки
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
            return None  # Не удалось найти путь

        # Добавляем путь к коробке
        for (i, j) in shortest_path[1:]:
            full_path.append(labirint_map[i][j].number)

        current_pos = nearest_box
        remaining_boxes.remove(nearest_box)

    # Идём из последней коробки в target_room
    if current_pos != target_pos:
        path_to_target = find_shortest_path(
            labirint_map,
            current_pos,
            target_pos,
        )
        if not path_to_target:
            return None
        for (i, j) in path_to_target[1:]:
            full_path.append(labirint_map[i][j].number)

    return full_path


if __name__ == "__main__":
    session = HTMLSession()
    url = LAB_URL
    floor = '1'
    # 1. Получаем карту
    labirint_map = get_labirint_map(
        session, url, floor)

    # 2. Ищем путь через все коробки с завершением в комнате 48
    start_room = 0
    target_room = 0
    path = find_path_via_boxes_to_target(labirint_map, start_room, target_room)

    if path:
        print(
            "Путь через все коробки до комнаты",
            target_room, ":", " → ".join(map(str, path)))
    else:
        print("Путь не найден")
