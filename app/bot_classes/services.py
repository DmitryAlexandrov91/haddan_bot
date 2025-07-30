"""Вспомогательные функции для классов."""
from typing import Callable


def make_transition(
        room_number: int,
        right: Callable[[], None],
        left: Callable[[], None],
        up: Callable[[], None],
        down: Callable[[], None],
        passed_rooms: set,
) -> None:
    """Делает переход в лесу, в зависимости от местоположения.

    Сумасшедствие с паттерном match case.
    """
    passed_rooms.add(room_number)

    match room_number:
        case 1 | 2 | 3 | 5 | 80 | 96 | 186 | 187 | 188 | 219 | 220 | 55 | (
            112 | 66 | 52 | 53 | 68 | 99 | 182 | 46 | 62 | 9 | 44 | 71 | 73 | (
                56 | 101 | 102 | 146 | 130 | 144 | 176 | 173 | 23 | 19 | 20 | (
                    21)
            )
        ): right()
        case 39 | 38 | 37 | 51 | 83 | 115 | 129 | 143 | 172 | 203: left()
        case 22 | 113 | 98 | 82 | 233 | 218 | 216 | 241: up()
        case 4 | 8 | 24 | 36 | 50 | 65 | 81 | 97 | 54 | 84 | 100 | (
            114 | 128 | 142 | 157 | 189 | 204 | 221 | 236 | 171 | 202 | 217 | (
                232 | 184 | 213
            )
        ): down()
        case 7: left() if 6 not in passed_rooms else right()
        case 6: left() if 5 not in passed_rooms else right()
        case 67: left() if 66 not in passed_rooms else up()
        case 69: left() if 68 not in passed_rooms else down()
        case 251: left() if 250 not in passed_rooms else right()
        case 250: up() if 235 not in passed_rooms else right()
        case 235: left() if 234 not in passed_rooms else down()
        case 234: down() if 249 not in passed_rooms else right()
        case 249: left() if 248 not in passed_rooms else up()
        case 248: up() if 233 not in passed_rooms else right()
        case 247: left() if 246 not in passed_rooms else right()
        case 246: up() if 231 not in passed_rooms else right()
        case 231: left() if 230 not in passed_rooms else down()
        case 230: up() if 215 not in passed_rooms else right()
        case 215: up() if 200 not in passed_rooms else down()
        case 200:
            if 201 not in passed_rooms:
                right()
            elif 185 in passed_rooms and 201 in passed_rooms:
                down()
            else:
                up()
        case 201: down() if 216 not in passed_rooms else left()
        case 185: up() if 170 not in passed_rooms else down()
        case 169: left() if 168 not in passed_rooms else right()
        case 170: left() if 169 not in passed_rooms else down()
        case 168: down() if 183 not in passed_rooms else right()
        case 183: left() if 182 not in passed_rooms else right()
        case 199: down() if 214 not in passed_rooms else left()
        case 214: down() if 229 not in passed_rooms else up()
        case 229: left() if 228 not in passed_rooms else up()
        case 228:
            if 213 not in passed_rooms and 243 not in passed_rooms:
                up()
            elif 243 not in passed_rooms and 213 in passed_rooms:
                down()
            else:
                right()
        case 243:
            if 244 not in passed_rooms and 242 not in passed_rooms:
                right()
            elif 244 in passed_rooms and 242 not in passed_rooms:
                left()
            else:
                up()
        case 242: up() if 227 not in passed_rooms else right()
        case 227: left() if 226 not in passed_rooms else down()
        case 226: down() if 241 not in passed_rooms else right()
        case 198: left()
        case 197: down()
        case 212: left()
        case 211 | 196 | 181: up()
        case 166: (
            up() if 181 in passed_rooms and 151 not in passed_rooms
            else right()
        )
        case 151: up() if 136 not in passed_rooms else down()
        case 136: up() if 121 not in passed_rooms else down()
        case 121: right() if 122 not in passed_rooms else down()
        case 122: (
            down() if 123 not in passed_rooms and 137 not in passed_rooms
            else left()
        )
        case 137 | 138: right()
        case 139 | 124: up()
        case 109: left()
        case 108: (
            left() if 107 not in passed_rooms and 93 not in passed_rooms
            else down()
        )
        case 107: left()
        case 106 | 91: up()
        case 76: right() if 77 not in passed_rooms else up()
        case 77: down() if 92 not in passed_rooms else left()
        case 92: up()
        case 61: up()
        case 47: down()
        case 63 | 48: up()
        case 33: left() if 32 not in passed_rooms else right()
        case 32: left()
        case 31: up()
        case 16 | 17: right()
        case 18: down()
        case 34: right() if 35 not in passed_rooms else down()
        case 49 | 64: down()
        case 79: left()
        case 78: down()
        case 93: right() if 94 not in passed_rooms else down()
        case 94: right() if 95 not in passed_rooms else left()
        case 95: down() if 110 not in passed_rooms else left()
        case 110: right() if 111 not in passed_rooms else up()
        case 111: down() if 126 not in passed_rooms else left()
        case 126:
            if 127 not in passed_rooms and 125 not in passed_rooms:
                right()
            elif 125 not in passed_rooms and 127 in passed_rooms:
                left()
            else:
                up()
        case 127: left()
        case 125: down() if 140 not in passed_rooms else right()
        case 140: down() if 155 not in passed_rooms else up()
        case 155:
            if 154 not in passed_rooms and 156 not in passed_rooms:
                right()
            elif 154 not in passed_rooms and 156 in passed_rooms:
                left()
            else:
                up()
        case 156: up() if 141 not in passed_rooms else left()
        case 141: down()
        case 154: left() if 153 not in passed_rooms else right()
        case 153: left() if 152 not in passed_rooms else right()
        case 152: right()
        case 123: left()
        case 167: right()
        case 252 | 253: right()
        case 254: up()
        case 239 | 238: left()
        case 237: up()
        case 222: right() if 223 not in passed_rooms else up()
        case 223: left()
        case 207: right()
        case 208 | 193: up()
        case 178: right()
        case 179: down()
        case 194: right()
        case 195: down() if 210 not in passed_rooms else up()
        case 210: left() if 209 not in passed_rooms else up()
        case 209: down() if 224 not in passed_rooms else right()
        case 224: right() if 225 not in passed_rooms else up()
        case 225: down() if 240 not in passed_rooms else left()
        case 240: down() if 255 not in passed_rooms else up()
        case 255: up()
        case 180 | 165 | 150 | 135 | 120: up()
        case 105: left()
        case 104: down()
        case 119: left()
        case 118: down()
        case 133: right()
        case 134 | 149: down()
        case 164: left()
        case 163: up() if 148 not in passed_rooms else left()
        case 162 | 161 | 160: left()
        case 159: left() if 158 not in passed_rooms else up()
        case 158: down()
        case 174: right() if 175 not in passed_rooms else up()
        case 175: right() if 176 not in passed_rooms else left()
        case 177: down()
        case 192: left()
        case 191: left()
        case 190: down() if 205 not in passed_rooms else up()
        case 205: right() if 206 not in passed_rooms else up()
        case 206: left()
        case 145: up()
        case 131: down()
        case 147 | 132: up()
        case 117: left()
        case 116: up()
        case 103: up()
        case 88 | 87 | 86: left()
        case 85 | 70: up()
        case 57: down()
        case 72: left() if 71 not in passed_rooms else right()
        case 74: up()
        case 59: left()
        case 58 | 43: up()
        case 28 | 27: left()
        case 26: down()
        case 41: right() if 42 not in passed_rooms else left()
        case 42: left()
        case 40 | 25: up()
        case 10: left() if 9 not in passed_rooms else right()
        case 11 | 12 | 13 | 14: right()
        case 15: down()
        case 30: left()
        case 29: down()
        case 45 | 60 | 75: down()
        case 90: left()
        case 244: right() if 245 not in passed_rooms else left()
        case 245: left()
        case 35: left()
        case 148: down()
