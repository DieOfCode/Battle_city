import os
from constant import constant
from settings import DISPLAY_WIDTH, GAME_DISP_WIDTH
from game_object.game_object import Blocks


class LoadLevel:
    def __init__(self):
        self.enemy_respawn_position = []
        self.bonus_respawn_position = []
        self.artillery_position = []

    def load_level(self, level):
        filename = 'levels/' + str(level)
        if not os.path.isfile(filename):
            raise AssertionError()
        game_map = []
        file = open(filename, 'r')
        data = file.read().split('\n')
        file.close()
        previous_elem = ""
        resp_position = []
        x, y = 0, 0
        for row in data:
            for char in row:
                if char == '#':
                    game_map.append(Blocks(x, y, "BRICK", constant.OBJ_SIZE))
                    self.add_bonus_position(x, y)
                    previous_elem = "#"
                elif char == '@':
                    game_map.append(Blocks(x, y, 'IRON', constant.OBJ_SIZE))
                    self.add_bonus_position(x, y)
                    previous_elem = "@"
                elif char == '%':
                    game_map.append(Blocks(x, y, 'BUSH', constant.OBJ_SIZE))
                    self.add_bonus_position(x, y)
                    previous_elem = "%"
                elif char == '~':
                    game_map.append(Blocks(x, y, 'WATER', constant.OBJ_SIZE))
                    previous_elem = "~"
                elif char == '-':
                    game_map.append(Blocks(x, y, 'IRON_FLOOR', constant.OBJ_SIZE))
                    previous_elem = "-"
                elif char == 'C':
                    game_map.append(Blocks(x, y, 'B', 2 * constant.OBJ_SIZE))
                elif char == 'A':
                    self.artillery_position.append((x, y))
                elif char == '.' and previous_elem and x != y:
                    previous_elem = None
                    resp_position.append((x, y))
                x += constant.OBJ_SIZE
            x = 0
            y += constant.OBJ_SIZE
        self.enemy_respawn_position = list(resp_position[:len(resp_position) // 2])
        return game_map

    def add_bonus_position(self, x, y):
        if 0 < x < DISPLAY_WIDTH - 26 and 0 < y < GAME_DISP_WIDTH:
            self.bonus_respawn_position.append((x, y))
