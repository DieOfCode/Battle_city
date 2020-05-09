import random
import os
import math
import datetime
import pygame
import pygame.locals
import argparse
import settings as s
from constant import *
from Tank import *
from GameObject import *

RESP_POSITION = []


def load_level(level):
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
                game_map.append(Blocks(x, y, "BRICK", OBJ_SIZE, -1))
                previous_elem = "#"
            elif char == '@':
                game_map.append(Blocks(x, y, 'IRON', OBJ_SIZE, -1))
                previous_elem = "@"
            elif char == '%':
                game_map.append(Blocks(x, y, 'BUSH', OBJ_SIZE, 0))
                previous_elem = "%"
            elif char == '~':
                game_map.append(Blocks(x, y, 'WATER', OBJ_SIZE, -1))
                previous_elem = "~"
            elif char == '-':
                game_map.append(Blocks(x, y, 'IRON_FLOOR', OBJ_SIZE, 0))
                previous_elem = "-"
            elif char == 'C':
                game_map.append(Blocks(x, y, 'B', 2*OBJ_SIZE, -1))
            elif char == '.' and previous_elem:
                previous_elem = None
                resp_position.append((x, y))
            x += OBJ_SIZE
        x = 0
        y += OBJ_SIZE
    global RESP_POSITION
    RESP_POSITION = list(resp_position[:len(resp_position) // 2])
    return game_map
