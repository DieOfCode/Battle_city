import configparser
import pygame
from constant import PLAYER_SPRITE


pygame.init()

OBJ_SIZE = 16
CONST_SPEED = 1

ENEMY_TYPES = ['regular', 'heavy', 'fast']

DISPLAY_WIDTH = 520
DISPLAY_HEIGHT = 416
FPS = 60

TIMER = pygame.time.Clock()

GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                       pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption('Battle city')
pygame.display.set_icon(PLAYER_SPRITE)

