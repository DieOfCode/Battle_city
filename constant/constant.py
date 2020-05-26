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
TANK_SIZE = 26
CONST_SPEED = 1

BEST_MUSIC = pygame.mixer.Sound('media/sounds/DOOM.ogg')
FIRE_SOUND = pygame.mixer.Sound('media/sounds/fire.ogg')
BUTTON_MUSIC = pygame.mixer.Sound('media/sounds/background.ogg')
START_SCREEN = pygame.mixer.Sound('media/sounds/ANewMorning.ogg')

sprites = pygame.transform.scale(pygame.image.load("media/images/sprites.gif"), [192, 224])
bomb_sprites = pygame.transform.scale(pygame.image.load("media/images/bomb.png"), [156, 26])

PLAYER_SPRITE = sprites.subsurface(0, 0, 26, 13 * 2)
CASUAL_ENEMY = sprites.subsurface(64, 0, 26, 13 * 2)
FAST_ENEMY = sprites.subsurface(96, 0, 26, 13 * 2)
POPA_BOL_ENEMY = sprites.subsurface(128, 0, 26, 13 * 2)
ART_ENEMY = sprites.subsurface(160, 32, 26, 13 * 2)

MISSILE = pygame.image.load('media/images/missile.png')
BOMB = bomb_sprites.subsurface(0, 0, 26, 26)
AIM = pygame.transform.scale(pygame.image.load("media/images/target.png"), [26, 26])

EXPLODE = pygame.image.load('media/images/exp_1.png')
BIG_EXPLODE = sprites.subsurface(64 * 2, 80 * 2, 26, 26)
BRICK = sprites.subsurface(48 * 2, 64 * 2, 8 * 2, 8 * 2)
BUSH = sprites.subsurface(56 * 2, 72 * 2, 8 * 2, 8 * 2)
IRON_BRICK = sprites.subsurface(48 * 2, 72 * 2, 8 * 2, 8 * 2)
IRON_FLOOR = sprites.subsurface(64 * 2, 72 * 2, 8 * 2, 8 * 2)
WATER = sprites.subsurface(64 * 2, 64 * 2, 8 * 2, 8 * 2)
CASTLE_IMG = sprites.subsurface(0, 15 * 2, 16 * 2, 16 * 2)
DESTR_CASTLE = sprites.subsurface(16 * 2, 15 * 2, 16 * 2, 16 * 2)

ENEMY_LIFE = sprites.subsurface(81 * 2, 57 * 2, 7 * 2, 7 * 2)
PLAYER_LIFE = sprites.subsurface(89 * 2, 56 * 2, 7 * 2, 8 * 2)
FLAG = sprites.subsurface(64 * 2, 49 * 2, 16 * 2, 15 * 2)

BONUS_LIFE = sprites.subsurface(32, 64, 32, 30)
BONUS_SPEED = sprites.subsurface(128, 64, 32, 30)
BONUS_DAMAGE = sprites.subsurface(96, 64, 32, 30)

SMALL_FONT = pygame.font.Font("media/fonts/prstart.ttf", 15)
FONT = pygame.font.Font("media/fonts/prstart.ttf", 45)
BUTTON_FONT = pygame.font.Font("media/fonts/prstart.ttf", 20)
