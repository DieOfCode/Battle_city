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

BEST_MUSIC = pygame.mixer.Sound('sounds/DOOM.ogg')
FIRE_SOUND = pygame.mixer.Sound('sounds/fire.ogg')
BUTTON_MUSIC = pygame.mixer.Sound('sounds/background.ogg')
START_SCREEN = pygame.mixer.Sound('sounds/ANewMorning.ogg')

sprites = pygame.transform.scale(pygame.image.load("images/sprites.gif"), [192, 224])
PLAYER_SPRITE = sprites.subsurface(0, 0, 26, 13 * 2)
MISSILE = pygame.image.load('images/missile.png')
CASUAL_ENEMY = sprites.subsurface(64, 0, 26, 13 * 2)
FAST_ENEMY = sprites.subsurface(96, 0, 26, 13 * 2)
POPA_BOL_ENEMY = sprites.subsurface(128, 0, 26, 13 * 2)

EXPLODE = pygame.image.load('images/exp_1.png')
BRICK = sprites.subsurface(48 * 2, 64 * 2, 8 * 2, 8 * 2)
BUSH = sprites.subsurface(56 * 2, 72 * 2, 8 * 2, 8 * 2)
IRON_BRICK = sprites.subsurface(48 * 2, 72 * 2, 8 * 2, 8 * 2)
IRON_FLOOR = sprites.subsurface(64 * 2, 72 * 2, 8 * 2, 8 * 2)
WATER = sprites.subsurface(64 * 2, 64 * 2, 8 * 2, 8 * 2)
CASTLE_IMG = sprites.subsurface(0, 15 * 2, 16 * 2, 16 * 2)
DESTR_CASTLE = sprites.subsurface(16 * 2, 15 * 2, 16 * 2, 16 * 2)

SMALL_FONT = pygame.font.Font("fonts/prstart.ttf", 15)
FONT = pygame.font.Font("fonts/prstart.ttf", 45)
BUTTON_FONT = pygame.font.Font("fonts/prstart.ttf", 20)


