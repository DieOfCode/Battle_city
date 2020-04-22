import random
import os
import math
import datetime
import pygame
import pygame.locals
import argparse
from settings import *
from constant import *
from Tank import *
from GameObject import *

LEVEL =1


def load_level():
    global LEVEL
    filename = 'levels/' + str(LEVEL)
    if not os.path.isfile(filename):
        raise AssertionError()
    game_map = []
    file = open(filename, 'r')
    data = file.read().split('\n')
    file.close()
    x, y = 0, 0
    for row in data:
        for char in row:
            if char == '#':
                game_map.append(Blocks(x, y, "BRICK", OBJ_SIZE))
            elif char == '@':
                game_map.append(Blocks(x, y, 'IRON', OBJ_SIZE))
            elif char == '%':
                game_map.append(Blocks(x, y, 'BUSH', OBJ_SIZE))
            elif char == '~':
                game_map.append(Blocks(x, y, 'WATER', OBJ_SIZE))
            elif char == '-':
                game_map.append(Blocks(x, y, 'IRON_FLOOR', OBJ_SIZE))
            elif char == 'C':
                game_map.append(Blocks(x, y, 'B', OBJ_SIZE))
            x += OBJ_SIZE
        x = 0
        y += OBJ_SIZE
    return game_map
