import configparser
import pygame

pygame.init()




WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (122, 0, 0)
RED_DARK = (255, 0, 0)
GREEN = (0, 135, 0)
LIGHT_GREEN = (0, 255, 0)
YELLOW = (200, 200, 0)
LIGHT_YELLOW = (100, 100, 0)
GREY = (220, 220, 220)

OBJ_SIZE = 16
CONST_SPEED = 1

ENEMY_TYPES = ['regular', 'heavy', 'fast']

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 416
FPS = 60

BEST_MUSIC = pygame.mixer.Sound('sounds/DOOM.ogg')
FIRE_SOUND = pygame.mixer.Sound('sounds/fire.ogg')

sprites = pygame.transform.scale(pygame.image.load("images/sprites.gif"), [192, 224])
PLAYER_SPRITE = sprites.subsurface(0, 0, 26, 13 * 2)
MISSILE = pygame.image.load('images/missile.png')

# HUD = pygame.image.load('images/hud.png')
# TOP_HUD = pygame.image.load('images/top_hud.png')
BRICK = sprites.subsurface(48 * 2, 64 * 2, 8 * 2, 8 * 2)
BUSH = sprites.subsurface(56 * 2, 72 * 2, 8 * 2, 8 * 2)
IRON_BRICK = sprites.subsurface(48 * 2, 72 * 2, 8 * 2, 8 * 2)
IRON_FLOOR = sprites.subsurface(64 * 2, 72 * 2, 8 * 2, 8 * 2)
WATER = sprites.subsurface(64 * 2, 64 * 2, 8 * 2, 8 * 2)
CASTLE_IMG = sprites.subsurface(0, 15 * 2, 16 * 2, 16 * 2)
DESTR_CASTLE = sprites.subsurface(16 * 2, 15 * 2, 16 * 2, 16 * 2)

TIMER = pygame.time.Clock()
RECT_MAP = []

SMALL_FONT = pygame.font.Font("fonts/prstart.ttf", 15)
FONT = pygame.font.Font("fonts/prstart.ttf", 50)
BUTTON_FONT = pygame.font.Font("fonts/prstart.ttf", 20)

GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                       pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption('Battle city')
pygame.display.set_icon(PLAYER_SPRITE)
